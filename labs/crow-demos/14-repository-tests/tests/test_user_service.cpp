// Тести бізнес-логіки. Сервіс отримує підроблений репозиторій і не потребує
// ні файлів, ні мережі, ні сервера.

#include <doctest/doctest.h>

#include "domain/user_service.hpp"
#include "infra/in_memory_user_repository.hpp"

// Шпигун: обгортає реальну реалізацію й рахує виклики add.
class SpyRepository : public InMemoryUserRepository {
public:
    User add(const NewUser& u) override {
        ++add_calls;
        return InMemoryUserRepository::add(u);
    }
    int add_calls = 0;
};

TEST_CASE("створення користувача") {
    SpyRepository repo;
    UserService service(repo);

    SUBCASE("коректні дані зберігаються й отримують id") {
        auto r = service.create({"Іван", "ivan@example.com", 25});
        CHECK(r.status == Status::Created);
        REQUIRE(r.user.has_value());
        CHECK(r.user->id == 1);
        CHECK(repo.add_calls == 1);
    }

    SUBCASE("некоректні дані не доходять до сховища") {
        auto r = service.create({"І", "bad", 200});
        CHECK(r.status == Status::Invalid);
        CHECK(r.message.find("name") != std::string::npos);
        CHECK(r.message.find("email") != std::string::npos);
        CHECK(r.message.find("age") != std::string::npos);
        CHECK(repo.add_calls == 0);
    }

    SUBCASE("дубль email дає конфлікт") {
        service.create({"Іван", "ivan@example.com", 25});
        auto r = service.create({"Інший Іван", "ivan@example.com", 30});
        CHECK(r.status == Status::Conflict);
        CHECK(repo.add_calls == 1);
    }
}

TEST_CASE("читання й видалення") {
    InMemoryUserRepository repo;
    UserService service(repo);
    auto created = service.create({"Марія", "maria@example.com", 31});

    CHECK(service.get(created.user->id).status == Status::Ok);
    CHECK(service.get(99).status == Status::NotFound);
    CHECK(service.remove(created.user->id).status == Status::Ok);
    CHECK(service.remove(created.user->id).status == Status::NotFound);
    CHECK(service.list().empty());
}

TEST_CASE("зміна email") {
    InMemoryUserRepository repo;
    UserService service(repo);
    auto a = service.create({"Анна", "anna@example.com", 20});
    auto b = service.create({"Борис", "boris@example.com", 22});

    CHECK(service.change_email(a.user->id, "new@example.com").status == Status::Ok);
    CHECK(service.change_email(a.user->id, "boris@example.com").status == Status::Conflict);
    CHECK(service.change_email(a.user->id, "bad").status == Status::Invalid);
    CHECK(service.change_email(99, "x@example.com").status == Status::NotFound);
    // Повторне встановлення власного email не є конфліктом
    CHECK(service.change_email(b.user->id, "boris@example.com").status == Status::Ok);
}
