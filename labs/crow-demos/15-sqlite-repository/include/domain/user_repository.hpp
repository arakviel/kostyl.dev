#pragma once
#include <optional>
#include <string>
#include <vector>

#include "domain/user.hpp"

// Інтерфейс репозиторію: колекція користувачів, з якою працює бізнес-логіка.
// Реалізацій може бути скільки завгодно: пам'ять, JSON-файл, SQLite.
class IUserRepository {
public:
    virtual ~IUserRepository() = default;

    virtual std::vector<User> find_all() const = 0;
    virtual std::optional<User> find_by_id(int id) const = 0;
    virtual std::optional<User> find_by_email(const std::string& email) const = 0;

    // Зберігає нового користувача і повертає його з присвоєним id.
    virtual User add(const NewUser& user) = 0;
    // Повертає false, якщо користувача з таким id немає.
    virtual bool update(const User& user) = 0;
    virtual bool remove(int id) = 0;
};
