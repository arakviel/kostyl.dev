#pragma once
#include "crow.h"
#include "domain/user_service.hpp"

// HTTP-шар: перетворює запити на виклики сервісу, а Status на коди відповіді.
// Тут немає ні бізнес-правил, ні доступу до сховища.
namespace api {

inline crow::response json_response(int code, const nlohmann::json& j) {
    crow::response res(code, j.dump());
    res.set_header("Content-Type", "application/json");
    return res;
}

inline int http_code(Status s) {
    switch (s) {
        case Status::Ok: return 200;
        case Status::Created: return 201;
        case Status::NotFound: return 404;
        case Status::Conflict: return 409;
        case Status::Invalid: return 400;
    }
    return 500;
}

inline crow::response to_response(const Result& r) {
    if (r.status == Status::Ok && !r.user) return crow::response(204);
    if (r.user) return json_response(http_code(r.status), *r.user);
    return json_response(http_code(r.status), nlohmann::json{{"error", r.message}});
}

template <typename App>
void register_user_routes(App& app, UserService& service) {
    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::GET)([&service] {
        return json_response(200, service.list());
    });

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::POST)([&service](const crow::request& req) {
        auto body = nlohmann::json::parse(req.body, nullptr, false);
        if (body.is_discarded()) return json_response(400, {{"error", "Тіло запиту не є коректним JSON"}});
        try {
            NewUser input{body.at("name").get<std::string>(), body.at("email").get<std::string>(),
                          body.at("age").get<int>()};
            return to_response(service.create(input));
        } catch (const nlohmann::json::exception& e) {
            return json_response(400, {{"error", "Потрібні поля name, email, age з коректними типами"}});
        }
    });

    CROW_ROUTE(app, "/users/<int>").methods(crow::HTTPMethod::GET)([&service](int id) {
        return to_response(service.get(id));
    });

    CROW_ROUTE(app, "/users/<int>").methods(crow::HTTPMethod::DELETE)([&service](int id) {
        return to_response(service.remove(id));
    });

    CROW_ROUTE(app, "/users/<int>/email").methods(crow::HTTPMethod::PUT)([&service](const crow::request& req, int id) {
        auto body = nlohmann::json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.contains("email") || !body["email"].is_string())
            return json_response(400, {{"error", "Потрібне рядкове поле email"}});
        return to_response(service.change_email(id, body["email"].get<std::string>()));
    });
}

}  // namespace api
