// Лекція 08. nlohmann/json: DTO, to_json/from_json, валідація, помилки.

#include <algorithm>
#include <cstdlib>
#include <map>
#include <mutex>
#include <optional>
#include <string>
#include <vector>

#include <nlohmann/json.hpp>

#include "crow.h"

using json = nlohmann::json;

// Автоматична (де)серіалізація: макрос генерує to_json/from_json для всіх полів.
struct Address {
    std::string city;
    std::string zip;
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(Address, city, zip)

struct User {
    int id = 0;
    std::string name;
    std::string email;
    int age = 0;
    std::vector<std::string> roles;
    Address address;
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(User, id, name, email, age, roles, address)

// DTO для створення: id немає, role має значення за замовчуванням.
struct CreateUserDto {
    std::string name;
    std::string email;
    int age = 0;
    std::string role = "user";
};

// Ручна реалізація from_json дає контроль над обов'язковістю й значеннями за замовчуванням.
void from_json(const json& j, CreateUserDto& d) {
    j.at("name").get_to(d.name);   // at() кидає виняток, якщо ключа немає
    j.at("email").get_to(d.email);
    j.at("age").get_to(d.age);
    d.role = j.value("role", "user");  // value() підставляє значення за замовчуванням
}

static crow::response json_response(int code, const json& j) {
    crow::response res(code, j.dump());
    res.set_header("Content-Type", "application/json");
    return res;
}

static crow::response error(int code, const std::string& message) {
    return json_response(code, json{{"error", message}});
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    crow::SimpleApp app;

    std::mutex mutex;
    std::map<int, User> users;
    int next_id = 1;

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::POST)([&](const crow::request& req) {
        try {
            json j = json::parse(req.body);          // parse_error при некоректному JSON
            CreateUserDto dto = j.get<CreateUserDto>();  // out_of_range / type_error при невідповідності

            if (dto.age < 0 || dto.age > 150) return error(400, "age: значення від 0 до 150");

            std::lock_guard<std::mutex> lock(mutex);
            User u;
            u.id = next_id++;
            u.name = dto.name;
            u.email = dto.email;
            u.age = dto.age;
            u.roles = {dto.role};
            users[u.id] = u;
            return json_response(201, u);  // User перетворюється на JSON неявно
        } catch (const json::parse_error& e) {
            return error(400, std::string("Некоректний JSON: ") + e.what());
        } catch (const json::out_of_range& e) {
            return error(400, std::string("Відсутнє поле: ") + e.what());
        } catch (const json::type_error& e) {
            return error(400, std::string("Невірний тип поля: ") + e.what());
        }
    });

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::GET)([&](const crow::request& req) {
        std::lock_guard<std::mutex> lock(mutex);
        json arr = json::array();
        const char* role = req.url_params.get("role");
        for (const auto& [id, u] : users) {
            if (role && std::find(u.roles.begin(), u.roles.end(), role) == u.roles.end()) continue;
            arr.push_back(u);
        }
        return json_response(200, json{{"count", arr.size()}, {"data", arr}});
    });

    CROW_ROUTE(app, "/users/<int>").methods(crow::HTTPMethod::GET)([&](int id) {
        std::lock_guard<std::mutex> lock(mutex);
        auto it = users.find(id);
        if (it == users.end()) return error(404, "Користувача не знайдено");
        return json_response(200, it->second);
    });

    // Форматований вивід: dump(2) для читання людиною
    CROW_ROUTE(app, "/users/<int>/pretty")([&](int id) {
        std::lock_guard<std::mutex> lock(mutex);
        auto it = users.find(id);
        if (it == users.end()) return error(404, "Користувача не знайдено");
        crow::response res(200, json(it->second).dump(2));
        res.set_header("Content-Type", "application/json");
        return res;
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
