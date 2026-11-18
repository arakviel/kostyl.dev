// Лекція 07. JSON у Crow: читання (rvalue) і створення (wvalue).

#include <cstdlib>
#include <sstream>
#include <string>

#include "crow.h"

static const char* type_name(crow::json::type t) {
    switch (t) {
        case crow::json::type::Null: return "null";
        case crow::json::type::False:
        case crow::json::type::True: return "boolean";
        case crow::json::type::Number: return "number";
        case crow::json::type::String: return "string";
        case crow::json::type::List: return "array";
        case crow::json::type::Object: return "object";
        case crow::json::type::Function: return "function";
    }
    return "unknown";
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    crow::SimpleApp app;

    // Читання: розбір довільного JSON і звіт про його структуру
    CROW_ROUTE(app, "/inspect").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        auto body = crow::json::load(req.body);
        if (!body) return crow::response(400, "Некоректний JSON");

        std::ostringstream out;
        out << "тип кореня: " << type_name(body.t()) << "\n";
        if (body.t() == crow::json::type::Object) {
            for (const auto& key : body.keys())
                out << "  " << key << ": " << type_name(body[key].t()) << "\n";
        }
        return crow::response(200, out.str());
    });

    // Читання вкладених полів і масивів
    CROW_ROUTE(app, "/order").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        auto body = crow::json::load(req.body);
        if (!body) return crow::response(400, "Некоректний JSON");
        if (!body.has("customer") || !body.has("items"))
            return crow::response(400, "Потрібні поля customer та items");

        std::string name = body["customer"]["name"].s();
        double total = 0;
        int count = 0;
        for (const auto& item : body["items"]) {
            total += item["price"].d() * static_cast<double>(item["qty"].i());
            count += static_cast<int>(item["qty"].i());
        }

        crow::json::wvalue res;
        res["customer"] = name;
        res["positions"] = body["items"].size();
        res["units"] = count;
        res["total"] = total;
        return crow::response(200, res);
    });

    // Безпечний варіант: доступ до відсутнього ключа чи невірного типу кидає виняток,
    // який без перехоплення перетворюється на 500. Тут він стає 400.
    CROW_ROUTE(app, "/order-safe").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        auto body = crow::json::load(req.body);
        if (!body) return crow::response(400, "Некоректний JSON");
        try {
            double total = 0;
            for (const auto& item : body["items"])
                total += item["price"].d() * static_cast<double>(item["qty"].i());
            crow::json::wvalue res;
            res["total"] = total;
            return crow::response(200, res);
        } catch (const std::runtime_error& e) {
            crow::json::wvalue err;
            err["error"] = std::string("Невірна структура JSON: ") + e.what();
            return crow::response(400, err);
        }
    });

    // Створення: вкладені об'єкти й масиви
    CROW_ROUTE(app, "/profile")([] {
        crow::json::wvalue j;
        j["name"] = "Іван Петренко";
        j["age"] = 25;
        j["active"] = true;
        j["score"] = 4.75;
        j["address"]["city"] = "Київ";
        j["address"]["zip"] = "01001";
        j["note"] = nullptr;

        crow::json::wvalue::list skills;
        skills.push_back("C++");
        skills.push_back("CMake");
        j["skills"] = std::move(skills);

        crow::json::wvalue::list projects;
        for (int i = 1; i <= 2; ++i) {
            crow::json::wvalue p;
            p["id"] = i;
            p["title"] = "Проєкт " + std::to_string(i);
            projects.push_back(std::move(p));
        }
        j["projects"] = std::move(projects);
        return j;
    });

    // Що буде, якщо звернутися до неіснуючого ключа або не того типу
    CROW_ROUTE(app, "/probe").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        auto body = crow::json::load(req.body);
        if (!body) return crow::response(400, "Некоректний JSON");
        crow::json::wvalue res;
        res["has_missing"] = body.has("missing");
        res["name_type"] = body.has("name") ? type_name(body["name"].t()) : "відсутнє";
        res["age_as_int"] = body.has("age") && body["age"].t() == crow::json::type::Number
                                ? body["age"].i()
                                : -1;
        return crow::response(200, res);
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
