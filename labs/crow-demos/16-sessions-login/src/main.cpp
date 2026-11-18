// Лекція 16. Cookies, сесії, реєстрація й вхід.
//
//  - cookie «visits» показує, що значення cookie контролює клієнт;
//  - сесія зберігає дані на сервері, а в cookie лежить лише випадковий ідентифікатор;
//  - паролі зберігаються як argon2id-хеші.

#include <chrono>
#include <cstdlib>
#include <iostream>
#include <map>
#include <mutex>
#include <optional>
#include <regex>
#include <string>

#include <nlohmann/json.hpp>

#include "auth/cookies.hpp"
#include "auth/password.hpp"
#include "auth/session_store.hpp"
#include "crow.h"

using json = nlohmann::json;

struct StoredUser {
    int id;
    std::string password_hash;
};

static std::mutex g_users_mutex;
static std::map<std::string, StoredUser> g_users;  // username -> дані
static int g_next_user_id = 1;
static auth::SessionStore g_sessions(std::chrono::minutes(30));

static constexpr int kSessionSeconds = 3600;

static crow::response json_response(int code, const json& j) {
    crow::response res(code, j.dump());
    res.set_header("Content-Type", "application/json");
    return res;
}

// Middleware: для кожного запиту читає cookie sid і підставляє користувача з сесії.
struct SessionLoader {
    struct context {
        std::optional<auth::SessionData> user;
        std::string token;
    };
    void before_handle(crow::request& req, crow::response&, context& ctx) {
        auto cookies = auth::parse_cookies(req.get_header_value("Cookie"));
        auto it = cookies.find("sid");
        if (it == cookies.end()) return;
        ctx.token = it->second;
        ctx.user = g_sessions.get(it->second);
    }
    void after_handle(crow::request&, crow::response&, context&) {}
};

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    crow::App<SessionLoader> app;

    // Хеш для неіснуючого користувача: щоб час відповіді не видавав, чи є такий логін
    static const std::string dummy_hash = auth::hash_password("dummy-password-for-timing");

    // ---- Cookies без сесії: значення належить клієнту ----
    CROW_ROUTE(app, "/cookie-demo/visit")([](const crow::request& req) {
        auto cookies = auth::parse_cookies(req.get_header_value("Cookie"));
        int visits = 0;
        if (auto it = cookies.find("visits"); it != cookies.end()) visits = std::atoi(it->second.c_str());
        ++visits;

        crow::response res(200, "Візитів: " + std::to_string(visits) + "\n");
        auth::CookieOptions opt;
        opt.max_age = 3600;
        res.add_header("Set-Cookie", auth::make_set_cookie("visits", std::to_string(visits), opt));
        return res;
    });

    // ---- Реєстрація ----
    CROW_ROUTE(app, "/register").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        auto body = json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.contains("username") || !body.contains("password") ||
            !body["username"].is_string() || !body["password"].is_string())
            return json_response(400, {{"error", "Потрібні рядкові поля username і password"}});

        const std::string username = body["username"];
        const std::string password = body["password"];
        static const std::regex name_re("^[A-Za-z0-9_]{3,32}$");
        if (!std::regex_match(username, name_re))
            return json_response(400, {{"error", "username: 3-32 символи, літери латиниці, цифри, _"}});
        if (password.size() < 8) return json_response(400, {{"error", "password: щонайменше 8 символів"}});

        std::string hash = auth::hash_password(password);  // повільно навмисно
        std::lock_guard<std::mutex> lock(g_users_mutex);
        if (g_users.count(username)) return json_response(409, {{"error", "Користувач уже існує"}});
        g_users[username] = StoredUser{g_next_user_id++, hash};
        return json_response(201, {{"username", username}});
    });

    // ---- Вхід: створює сесію й ставить cookie ----
    CROW_ROUTE(app, "/login").methods(crow::HTTPMethod::POST)([&](const crow::request& req) {
        auto body = json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.contains("username") || !body.contains("password") ||
            !body["username"].is_string() || !body["password"].is_string())
            return json_response(400, {{"error", "Потрібні рядкові поля username і password"}});

        const std::string username = body["username"];
        const std::string password = body["password"];

        std::optional<StoredUser> user;
        {
            std::lock_guard<std::mutex> lock(g_users_mutex);
            if (auto it = g_users.find(username); it != g_users.end()) user = it->second;
        }

        // Перевірка виконується завжди; для невідомого логіна — проти фіктивного хешу.
        const bool ok = auth::verify_password(user ? user->password_hash : dummy_hash, password) && user;
        if (!ok) return json_response(401, {{"error", "Невірний логін або пароль"}});

        std::string token = g_sessions.create({user->id, username});

        crow::response res = json_response(200, {{"username", username}});
        auth::CookieOptions opt;
        opt.max_age = kSessionSeconds;  // HttpOnly і SameSite=Lax — за замовчуванням
        res.add_header("Set-Cookie", auth::make_set_cookie("sid", token, opt));
        return res;
    });

    // ---- Захищений ресурс ----
    CROW_ROUTE(app, "/me")([&app](const crow::request& req) {
        auto& ctx = app.get_context<SessionLoader>(req);
        if (!ctx.user) return json_response(401, {{"error", "Потрібен вхід"}});
        return json_response(200, {{"id", ctx.user->user_id}, {"username", ctx.user->username}});
    });

    // ---- Вихід: знищує сесію на сервері й видаляє cookie ----
    CROW_ROUTE(app, "/logout").methods(crow::HTTPMethod::POST)([&app](const crow::request& req) {
        auto& ctx = app.get_context<SessionLoader>(req);
        if (!ctx.token.empty()) g_sessions.destroy(ctx.token);

        crow::response res = json_response(200, {{"status", "logged out"}});
        auth::CookieOptions opt;
        opt.max_age = 0;  // Max-Age=0 наказує браузеру видалити cookie
        res.add_header("Set-Cookie", auth::make_set_cookie("sid", "", opt));
        return res;
    });

    // Кількість активних сесій (для демонстрації знищення)
    CROW_ROUTE(app, "/debug/sessions")([] {
        return json_response(200, {{"active", g_sessions.size()}});
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
