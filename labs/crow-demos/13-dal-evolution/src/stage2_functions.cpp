// Етап 2. Утилітарні функції: читання й запис винесено в load_users / save_users.
// Дублювання зникло, але обробники й далі знають, що дані живуть у JSON-файлі
// (передають шлях), а функції — вільні й не мають спільного стану.

#include <cstdlib>
#include <fstream>
#include <vector>

#include "crow.h"
#include "user.hpp"

std::vector<User> load_users(const std::string& file) {
    std::ifstream in(file);
    if (!in) return {};
    auto j = nlohmann::json::parse(in, nullptr, false);
    if (j.is_discarded()) return {};
    return j.get<std::vector<User>>();
}

void save_users(const std::string& file, const std::vector<User>& users) {
    std::ofstream out(file);
    out << nlohmann::json(users).dump(2);
}

static crow::response json_response(int code, const nlohmann::json& j) {
    crow::response res(code, j.dump());
    res.set_header("Content-Type", "application/json");
    return res;
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    const std::string file = argc > 2 ? argv[2] : "users_stage2.json";
    crow::SimpleApp app;

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::GET)([&file] {
        return json_response(200, load_users(file));
    });

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::POST)([&file](const crow::request& req) {
        auto body = nlohmann::json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.contains("name") || !body.contains("email"))
            return crow::response(400, "name та email обов'язкові");

        auto users = load_users(file);
        int next_id = 1;
        for (const auto& u : users) next_id = std::max(next_id, u.id + 1);
        User u{next_id, body["name"], body["email"]};
        users.push_back(u);
        save_users(file, users);
        return json_response(201, u);
    });

    CROW_ROUTE(app, "/users/<int>")([&file](int id) {
        for (const auto& u : load_users(file))
            if (u.id == id) return json_response(200, u);
        return crow::response(404, "Користувача не знайдено");
    });

    app.port(static_cast<uint16_t>(port)).run();
}
