// Лекція 06. REST-дизайн і валідація даних.
// Ресурс /users з перевіркою вхідних даних, перерахуванням усіх помилок
// у відповіді, унікальністю email (409) і перевіркою Content-Type (415).

#include <algorithm>
#include <cstdlib>
#include <map>
#include <mutex>
#include <string>
#include <vector>

#include "crow.h"

struct User {
    int id;
    std::string name;
    std::string email;
    int age;
};

static std::mutex g_mutex;
static std::map<int, User> g_users;
static int g_next_id = 1;

// Довжина в символах UTF-8: байти-продовження (10xxxxxx) не рахуються.
static size_t utf8_length(const std::string& s) {
    size_t n = 0;
    for (unsigned char c : s)
        if ((c & 0xC0) != 0x80) ++n;
    return n;
}

// Валідація повертає перелік усіх помилок, а не лише першу: клієнт виправляє все за один раз.
static std::vector<std::string> validate_user(const crow::json::rvalue& body) {
    std::vector<std::string> errors;

    if (!body.has("name") || body["name"].t() != crow::json::type::String) {
        errors.push_back("name: обов'язкове рядкове поле");
    } else {
        size_t len = utf8_length(body["name"].s());
        if (len < 2 || len > 50) errors.push_back("name: довжина від 2 до 50 символів");
    }

    if (!body.has("email") || body["email"].t() != crow::json::type::String) {
        errors.push_back("email: обов'язкове рядкове поле");
    } else {
        std::string email = body["email"].s();
        auto at = email.find('@');
        bool ok = at != std::string::npos && at > 0 && email.find('.', at) != std::string::npos &&
                  email.find('@', at + 1) == std::string::npos;
        if (!ok) errors.push_back("email: некоректний формат");
    }

    if (!body.has("age") || body["age"].t() != crow::json::type::Number) {
        errors.push_back("age: обов'язкове числове поле");
    } else {
        int age = static_cast<int>(body["age"].i());
        if (age < 0 || age > 150) errors.push_back("age: значення від 0 до 150");
    }
    return errors;
}

static crow::json::wvalue to_json(const User& u) {
    crow::json::wvalue j;
    j["id"] = u.id;
    j["name"] = u.name;
    j["email"] = u.email;
    j["age"] = u.age;
    return j;
}

static crow::response error(int code, const std::string& message) {
    crow::json::wvalue j;
    j["error"] = message;
    return crow::response(code, j);
}

static crow::response validation_error(const std::vector<std::string>& errors) {
    crow::json::wvalue j;
    j["error"] = "Помилка валідації";
    crow::json::wvalue::list list;
    for (const auto& e : errors) list.push_back(e);
    j["details"] = std::move(list);
    return crow::response(400, j);
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    crow::SimpleApp app;

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        // 1. Формат: чи вказано JSON
        const std::string ct = req.get_header_value("Content-Type");
        if (ct.find("application/json") == std::string::npos)
            return error(415, "Content-Type має бути application/json");

        // 2. Синтаксис: чи це коректний JSON
        auto body = crow::json::load(req.body);
        if (!body) return error(400, "Тіло запиту не є коректним JSON");

        // 3. Дані: типи, обов'язковість, діапазони
        auto errors = validate_user(body);
        if (!errors.empty()) return validation_error(errors);

        std::lock_guard<std::mutex> lock(g_mutex);
        // 4. Бізнес-правило: email унікальний
        std::string email = body["email"].s();
        for (const auto& [id, u] : g_users)
            if (u.email == email) return error(409, "Користувач із таким email уже існує");

        User u{g_next_id++, body["name"].s(), email, static_cast<int>(body["age"].i())};
        g_users[u.id] = u;
        crow::response res(201, to_json(u));
        res.set_header("Location", "/users/" + std::to_string(u.id));
        return res;
    });

    // Колекція: пагінація, сортування, фільтр
    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::GET)([](const crow::request& req) {
        int page = 1, limit = 10;
        if (const char* p = req.url_params.get("page")) page = std::atoi(p);
        if (const char* l = req.url_params.get("limit")) limit = std::atoi(l);
        if (page < 1 || limit < 1 || limit > 100)
            return error(400, "page >= 1, 1 <= limit <= 100");

        const char* min_age = req.url_params.get("min_age");
        const char* sort = req.url_params.get("sort");

        std::lock_guard<std::mutex> lock(g_mutex);
        std::vector<User> list;
        for (const auto& [id, u] : g_users)
            if (!min_age || u.age >= std::atoi(min_age)) list.push_back(u);

        if (sort && std::string(sort) == "-age")
            std::sort(list.begin(), list.end(), [](const User& a, const User& b) { return a.age > b.age; });

        const size_t total = list.size();
        const size_t from = static_cast<size_t>(page - 1) * static_cast<size_t>(limit);
        crow::json::wvalue::list items;
        for (size_t i = from; i < total && i < from + static_cast<size_t>(limit); ++i)
            items.push_back(to_json(list[i]));

        crow::json::wvalue j;
        j["total"] = total;
        j["page"] = page;
        j["limit"] = limit;
        j["data"] = std::move(items);
        return crow::response(200, j);
    });

    CROW_ROUTE(app, "/users/<int>").methods(crow::HTTPMethod::GET)([](int id) {
        std::lock_guard<std::mutex> lock(g_mutex);
        auto it = g_users.find(id);
        if (it == g_users.end()) return error(404, "Користувача не знайдено");
        return crow::response(200, to_json(it->second));
    });

    CROW_ROUTE(app, "/users/<int>").methods(crow::HTTPMethod::DELETE)([](int id) {
        std::lock_guard<std::mutex> lock(g_mutex);
        if (!g_users.erase(id)) return error(404, "Користувача не знайдено");
        return crow::response(204);
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
