#pragma once
#include <sqlite3.h>

#include <memory>
#include <mutex>
#include <stdexcept>
#include <string>

#include "domain/user_repository.hpp"

namespace sqlite {

// RAII-обгортка над sqlite3*: з'єднання закривається у деструкторі.
class Database {
public:
    explicit Database(const std::string& path) {
        sqlite3* raw = nullptr;
        if (sqlite3_open(path.c_str(), &raw) != SQLITE_OK) {
            std::string message = raw ? sqlite3_errmsg(raw) : "не вдалося відкрити базу";
            sqlite3_close(raw);
            throw std::runtime_error("SQLite: " + message);
        }
        db_.reset(raw);
    }

    sqlite3* get() const { return db_.get(); }

    void exec(const std::string& sql) const {
        char* error = nullptr;
        if (sqlite3_exec(db_.get(), sql.c_str(), nullptr, nullptr, &error) != SQLITE_OK) {
            std::string message = error ? error : "невідома помилка";
            sqlite3_free(error);
            throw std::runtime_error("SQLite: " + message);
        }
    }

private:
    struct Closer {
        void operator()(sqlite3* db) const { sqlite3_close(db); }
    };
    std::unique_ptr<sqlite3, Closer> db_;
};

// RAII-обгортка над підготовленим запитом (prepared statement).
class Statement {
public:
    Statement(const Database& db, const std::string& sql) : db_(db.get()) {
        sqlite3_stmt* raw = nullptr;
        if (sqlite3_prepare_v2(db_, sql.c_str(), -1, &raw, nullptr) != SQLITE_OK)
            throw std::runtime_error(std::string("SQLite prepare: ") + sqlite3_errmsg(db_));
        stmt_.reset(raw);
    }

    // Параметри нумеруються з 1. Значення НЕ вставляються в текст запиту.
    Statement& bind(int index, const std::string& value) {
        check(sqlite3_bind_text(stmt_.get(), index, value.c_str(), -1, SQLITE_TRANSIENT));
        return *this;
    }
    Statement& bind(int index, int value) {
        check(sqlite3_bind_int(stmt_.get(), index, value));
        return *this;
    }

    // true, якщо є наступний рядок результату
    bool step() {
        int rc = sqlite3_step(stmt_.get());
        if (rc == SQLITE_ROW) return true;
        if (rc == SQLITE_DONE) return false;
        throw std::runtime_error(std::string("SQLite: ") + sqlite3_errmsg(db_));
    }

    int column_int(int index) const { return sqlite3_column_int(stmt_.get(), index); }
    std::string column_text(int index) const {
        const unsigned char* text = sqlite3_column_text(stmt_.get(), index);
        return text ? reinterpret_cast<const char*>(text) : "";
    }

private:
    void check(int rc) const {
        if (rc != SQLITE_OK) throw std::runtime_error(std::string("SQLite bind: ") + sqlite3_errmsg(db_));
    }
    struct Finalizer {
        void operator()(sqlite3_stmt* s) const { sqlite3_finalize(s); }
    };
    sqlite3* db_;
    std::unique_ptr<sqlite3_stmt, Finalizer> stmt_;
};

}  // namespace sqlite

// Реалізація IUserRepository поверх SQLite. Бізнес-логіка (UserService) цього не помічає.
class SqliteUserRepository : public IUserRepository {
public:
    // Шлях ":memory:" створює базу в оперативній пам'яті (для тестів).
    explicit SqliteUserRepository(const std::string& path) : db_(path) { migrate(); }

    std::vector<User> find_all() const override {
        std::lock_guard<std::mutex> lock(mutex_);
        sqlite::Statement st(db_, "SELECT id, name, email, age FROM users ORDER BY id");
        std::vector<User> result;
        while (st.step()) result.push_back(read_user(st));
        return result;
    }

    std::optional<User> find_by_id(int id) const override {
        std::lock_guard<std::mutex> lock(mutex_);
        sqlite::Statement st(db_, "SELECT id, name, email, age FROM users WHERE id = ?");
        st.bind(1, id);
        if (!st.step()) return std::nullopt;
        return read_user(st);
    }

    std::optional<User> find_by_email(const std::string& email) const override {
        std::lock_guard<std::mutex> lock(mutex_);
        sqlite::Statement st(db_, "SELECT id, name, email, age FROM users WHERE email = ?");
        st.bind(1, email);
        if (!st.step()) return std::nullopt;
        return read_user(st);
    }

    User add(const NewUser& input) override {
        std::lock_guard<std::mutex> lock(mutex_);
        return insert(input);
    }

    // Атомарне додавання кількох: або всі, або жодного.
    std::vector<User> add_many(const std::vector<NewUser>& inputs) {
        std::lock_guard<std::mutex> lock(mutex_);
        db_.exec("BEGIN IMMEDIATE");
        try {
            std::vector<User> created;
            for (const auto& input : inputs) created.push_back(insert(input));
            db_.exec("COMMIT");
            return created;
        } catch (...) {
            db_.exec("ROLLBACK");
            throw;
        }
    }

    bool update(const User& user) override {
        std::lock_guard<std::mutex> lock(mutex_);
        sqlite::Statement st(db_, "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?");
        st.bind(1, user.name).bind(2, user.email).bind(3, user.age).bind(4, user.id);
        st.step();
        return sqlite3_changes(db_.get()) > 0;
    }

    bool remove(int id) override {
        std::lock_guard<std::mutex> lock(mutex_);
        sqlite::Statement st(db_, "DELETE FROM users WHERE id = ?");
        st.bind(1, id);
        st.step();
        return sqlite3_changes(db_.get()) > 0;
    }

    // Доступ до з'єднання потрібен лише тестам (демонстрація SQL-ін'єкції).
    const sqlite::Database& database() const { return db_; }

private:
    // Схема створюється при старті; повторний запуск її не ламає (IF NOT EXISTS).
    void migrate() {
        db_.exec(
            "CREATE TABLE IF NOT EXISTS users ("
            "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "  name TEXT NOT NULL,"
            "  email TEXT NOT NULL UNIQUE,"
            "  age INTEGER NOT NULL CHECK (age BETWEEN 0 AND 150)"
            ")");
    }

    User insert(const NewUser& input) {
        sqlite::Statement st(db_, "INSERT INTO users (name, email, age) VALUES (?, ?, ?)");
        st.bind(1, input.name).bind(2, input.email).bind(3, input.age);
        st.step();
        return User{static_cast<int>(sqlite3_last_insert_rowid(db_.get())), input.name, input.email, input.age};
    }

    static User read_user(const sqlite::Statement& st) {
        return User{st.column_int(0), st.column_text(1), st.column_text(2), st.column_int(3)};
    }

    sqlite::Database db_;
    mutable std::mutex mutex_;
};
