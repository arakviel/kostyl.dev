// Етап 1. Прямий доступ: кожен обробник сам відкриває файл, розбирає JSON і пише назад.
// Проблеми: дублювання коду, формат файлу відомий скрізь, жодного блокування,
// бізнес-правила змішані з вводом-виводом.

#include <cstdlib>
#include <fstream>

#include "crow.h"
#include "user.hpp"

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    const std::string file = argc > 2 ? argv[2] : "users_stage1.json";
    crow::SimpleApp app;

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::GET)([&file] {
        std::ifstream in(file);
        nlohmann::json j = in ? nlohmann::json::parse(in, nullptr, false) : nlohmann::json::array();
        if (j.is_discarded()) j = nlohmann::json::array();
        crow::response res(200, j.dump());
        res.set_header("Content-Type", "application/json");
        return res;
    });

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::POST)([&file](const crow::request& req) {
        auto body = nlohmann::json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.contains("name") || !body.contains("email"))
            return crow::response(400, "name та email обов'язкові");

        // Те саме читання файлу, що й вище — скопійоване
        std::ifstream in(file);
        nlohmann::json all = in ? nlohmann::json::parse(in, nullptr, false) : nlohmann::json::array();
        if (all.is_discarded()) all = nlohmann::json::array();

        int next_id = 1;
        for (const auto& u : all) next_id = std::max<int>(next_id, u["id"].get<int>() + 1);
        nlohmann::json created = {{"id", next_id}, {"name", body["name"]}, {"email", body["email"]}};
        all.push_back(created);

        std::ofstream out(file);
        out << all.dump(2);

        crow::response res(201, created.dump());
        res.set_header("Content-Type", "application/json");
        return res;
    });

    CROW_ROUTE(app, "/users/<int>")([&file](int id) {
        // І ще раз те саме читання файлу
        std::ifstream in(file);
        nlohmann::json all = in ? nlohmann::json::parse(in, nullptr, false) : nlohmann::json::array();
        if (all.is_discarded()) all = nlohmann::json::array();
        for (const auto& u : all) {
            if (u["id"].get<int>() == id) {
                crow::response res(200, u.dump());
                res.set_header("Content-Type", "application/json");
                return res;
            }
        }
        return crow::response(404, "Користувача не знайдено");
    });

    app.port(static_cast<uint16_t>(port)).run();
}
