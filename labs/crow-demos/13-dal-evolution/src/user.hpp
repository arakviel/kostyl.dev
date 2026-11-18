#pragma once
// Спільна модель для всіх етапів: структура користувача і її JSON-вигляд.

#include <string>

#include <nlohmann/json.hpp>

struct User {
    int id = 0;
    std::string name;
    std::string email;
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(User, id, name, email)
