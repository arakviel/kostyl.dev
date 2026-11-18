// Перевірки, специфічні для SQL-реалізації: обмеження, транзакції, ін'єкції, файл бази.

#include <doctest/doctest.h>

#include <filesystem>

#include "domain/user_service.hpp"
#include "infra/sqlite_user_repository.hpp"

namespace fs = std::filesystem;

TEST_CASE("обмеження бази даних") {
    SqliteUserRepository repo(":memory:");
    repo.add({"Анна", "anna@example.com", 20});

    SUBCASE("UNIQUE на email: другий запис із тим самим email кидає виняток") {
        CHECK_THROWS_AS(repo.add({"Інша Анна", "anna@example.com", 30}), std::runtime_error);
        CHECK(repo.find_all().size() == 1);
    }

    SUBCASE("CHECK на age: значення поза діапазоном відхиляється самою базою") {
        CHECK_THROWS_AS(repo.add({"Дід", "old@example.com", 200}), std::runtime_error);
    }
}

TEST_CASE("транзакція: або все, або нічого") {
    SqliteUserRepository repo(":memory:");

    SUBCASE("успішна пачка зберігається цілком") {
        auto created = repo.add_many({{"Анна", "a@example.com", 20}, {"Борис", "b@example.com", 22}});
        CHECK(created.size() == 2);
        CHECK(repo.find_all().size() == 2);
    }

    SUBCASE("помилка в другому записі скасовує й перший") {
        CHECK_THROWS(repo.add_many({{"Анна", "dup@example.com", 20}, {"Борис", "dup@example.com", 22}}));
        CHECK(repo.find_all().empty());
    }
}

// Небезпечна функція, яку НЕ можна писати: значення вставлено в текст запиту.
static int count_by_email_unsafe(const sqlite::Database& db, const std::string& email) {
    sqlite::Statement st(db, "SELECT COUNT(*) FROM users WHERE email = '" + email + "'");
    st.step();
    return st.column_int(0);
}

TEST_CASE("SQL-ін'єкція: конкатенація проти підготовленого запиту") {
    SqliteUserRepository repo(":memory:");
    repo.add({"Анна", "anna@example.com", 20});
    repo.add({"Борис", "boris@example.com", 22});

    const std::string attack = "x' OR '1'='1";

    // Конкатенація: умова стала завжди істинною, повернулись ВСІ рядки
    CHECK(count_by_email_unsafe(repo.database(), attack) == 2);

    // Підготовлений запит: той самий рядок шукається як звичайне значення
    CHECK_FALSE(repo.find_by_email(attack).has_value());
}

TEST_CASE("дані в файлі переживають перезапуск") {
    fs::path path = fs::temp_directory_path() / "crow_demo15_persist.db";
    fs::remove(path);
    {
        SqliteUserRepository repo(path.string());
        repo.add({"Анна", "anna@example.com", 20});
    }
    SqliteUserRepository reopened(path.string());  // migrate() повторно не ламає схему
    REQUIRE(reopened.find_all().size() == 1);
    CHECK(reopened.find_all()[0].name == "Анна");
    CHECK(reopened.add({"Борис", "boris@example.com", 22}).id == 2);
    fs::remove(path);
}

TEST_CASE("UserService не помічає, що сховище змінилося") {
    SqliteUserRepository repo(":memory:");
    UserService service(repo);

    CHECK(service.create({"Іван", "ivan@example.com", 25}).status == Status::Created);
    CHECK(service.create({"Іван", "ivan@example.com", 30}).status == Status::Conflict);
    CHECK(service.create({"І", "bad", 200}).status == Status::Invalid);
    CHECK(service.get(1).user->name == "Іван");
}
