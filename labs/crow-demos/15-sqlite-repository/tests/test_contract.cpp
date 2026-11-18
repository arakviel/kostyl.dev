// Той самий контракт, що й у демо 14, тепер для трьох реалізацій.

#include <doctest/doctest.h>

#include <atomic>
#include <filesystem>
#include <memory>

#include "infra/in_memory_user_repository.hpp"
#include "infra/json_file_user_repository.hpp"
#include "infra/sqlite_user_repository.hpp"

namespace fs = std::filesystem;

template <typename Repo>
struct Factory;

template <>
struct Factory<InMemoryUserRepository> {
    static std::unique_ptr<IUserRepository> make() { return std::make_unique<InMemoryUserRepository>(); }
};

template <>
struct Factory<JsonFileUserRepository> {
    static std::unique_ptr<IUserRepository> make() {
        static std::atomic<int> counter{0};
        fs::path path = fs::temp_directory_path() / ("crow_demo15_users_" + std::to_string(++counter) + ".json");
        fs::remove(path);
        return std::make_unique<JsonFileUserRepository>(path.string());
    }
};

template <>
struct Factory<SqliteUserRepository> {
    static std::unique_ptr<IUserRepository> make() { return std::make_unique<SqliteUserRepository>(":memory:"); }
};

TEST_CASE_TEMPLATE("контракт IUserRepository", Repo, InMemoryUserRepository, JsonFileUserRepository,
                   SqliteUserRepository) {
    auto repo = Factory<Repo>::make();

    SUBCASE("порожнє сховище") {
        CHECK(repo->find_all().empty());
        CHECK_FALSE(repo->find_by_id(1).has_value());
    }

    SUBCASE("add присвоює зростаючі id") {
        auto a = repo->add({"Анна", "anna@example.com", 20});
        auto b = repo->add({"Борис", "boris@example.com", 22});
        CHECK(a.id == 1);
        CHECK(b.id == 2);
        CHECK(repo->find_all().size() == 2);
    }

    SUBCASE("пошук за id та email") {
        auto a = repo->add({"Анна", "anna@example.com", 20});
        REQUIRE(repo->find_by_id(a.id).has_value());
        CHECK(repo->find_by_id(a.id)->name == "Анна");
        REQUIRE(repo->find_by_email("anna@example.com").has_value());
        CHECK(repo->find_by_email("anna@example.com")->id == a.id);
        CHECK_FALSE(repo->find_by_email("none@example.com").has_value());
    }

    SUBCASE("update змінює запис, а для відсутнього повертає false") {
        auto a = repo->add({"Анна", "anna@example.com", 20});
        a.age = 21;
        CHECK(repo->update(a));
        CHECK(repo->find_by_id(a.id)->age == 21);
        User ghost{99, "X", "x@example.com", 1};
        CHECK_FALSE(repo->update(ghost));
    }

    SUBCASE("remove видаляє запис і не повторює id") {
        auto a = repo->add({"Анна", "anna@example.com", 20});
        CHECK(repo->remove(a.id));
        CHECK_FALSE(repo->remove(a.id));
        auto b = repo->add({"Борис", "boris@example.com", 22});
        CHECK(b.id != a.id);
    }
}
