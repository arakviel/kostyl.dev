#pragma once
#include <string>

#include <nlohmann/json.hpp>

// Доменна модель. Нічого не знає ні про HTTP, ні про сховище.
struct User {
    int id = 0;
    std::string name;
    std::string email;
    int age = 0;
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(User, id, name, email, age)

// Дані для створення: id присвоює репозиторій.
struct NewUser {
    std::string name;
    std::string email;
    int age = 0;
};
