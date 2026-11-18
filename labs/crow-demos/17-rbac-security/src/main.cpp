// Лекція 17. Авторизація (RBAC) і захист вебзастосунку.
//
//  Ролі:            user < editor < admin
//  Політика:        таблиця «метод + шлях -> мінімальна роль», усе інше — за замовчуванням потребує входу
//  Захист:          CSRF-токен, нова сесія при вході (fixation), обмеження спроб входу,
//                   перевірка власника ресурсу (IDOR), заголовки безпеки, таймаути сесії

#include <chrono>
#include <cstdlib>
#include <iostream>
#include <map>
#include <mutex>
#include <optional>
#include <regex>
#include <string>
#include <vector>

#include <nlohmann/json.hpp>

#include "auth/cookies.hpp"
#include "auth/login_throttle.hpp"
#include "auth/password.hpp"
#include "auth/session_store.hpp"
#include "crow.h"

using json = nlohmann::json;
using auth::Role;

struct StoredUser {
    int id;
    std::string password_hash;
    Role role;
};

struct Note {
    int id;
    std::string owner;
    std::string text;
};

static std::mutex g_mutex;
static std::map<std::string, StoredUser> g_users;
static std::vector<Note> g_notes;
static std::vector<std::string> g_articles;
static int g_next_user_id = 1, g_next_note_id = 1;

static auth::SessionStore g_sessions(std::chrono::minutes(30), std::chrono::hours(8));
static auth::LoginThrottle g_throttle(5, std::chrono::seconds(60));
static bool g_cookie_secure = false;

static crow::response json_response(int code, const json& j) {
    crow::response res(code, j.dump());
    res.set_header("Content-Type", "application/json");
    return res;
}

// Порівняння рядків за сталий час: тривалість не залежить від того, скільки символів збіглося.
static bool constant_time_equals(const std::string& a, const std::string& b) {
    unsigned char diff = static_cast<unsigned char>(a.size() ^ b.size());
    for (size_t i = 0; i < a.size() && i < b.size(); ++i) diff |= static_cast<unsigned char>(a[i] ^ b[i]);
    return diff == 0;
}

// ---------------------------------------------------------------------------
// Middleware 1: завантаження сесії з cookie
// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Middleware 2: заголовки безпеки на кожній відповіді (ставляться в after_handle)
// ---------------------------------------------------------------------------
struct SecurityHeaders {
    struct context {};
    void before_handle(crow::request&, crow::response&, context&) {}
    void after_handle(crow::request&, crow::response& res, context&) {
        res.set_header("X-Content-Type-Options", "nosniff");
        res.set_header("X-Frame-Options", "DENY");
        res.set_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'");
        res.set_header("Referrer-Policy", "no-referrer");
        res.set_header("Cache-Control", "no-store");
    }
};

// ---------------------------------------------------------------------------
// Middleware 3: авторизація за таблицею політики + перевірка CSRF
// ---------------------------------------------------------------------------
struct Rule {
    crow::HTTPMethod method;
    std::string prefix;          // шлях збігається, якщо починається з prefix
    std::optional<Role> min_role;  // порожнє значення = публічний ресурс
};

static const std::vector<Rule> kPolicy = {
    {crow::HTTPMethod::GET, "/public", std::nullopt},
    {crow::HTTPMethod::POST, "/login", std::nullopt},
    {crow::HTTPMethod::POST, "/register", std::nullopt},
    {crow::HTTPMethod::POST, "/articles", Role::Editor},
    {crow::HTTPMethod::DELETE, "/articles", Role::Editor},
    {crow::HTTPMethod::GET, "/admin", Role::Admin},
    {crow::HTTPMethod::DELETE, "/admin", Role::Admin},
    // Усе інше (див. нижче): потрібен вхід у систему
};

struct Authorizer {
    struct context {};

    template <typename AllContext>
    void before_handle(crow::request& req, crow::response& res, context&, AllContext& all_ctx) {
        auto& session = all_ctx.template get<SessionLoader>();

        // 1. Яке правило діє для цього запиту
        std::optional<Role> required = Role::User;  // deny by default: за замовчуванням потрібен вхід
        for (const auto& rule : kPolicy) {
            if (rule.method == req.method && req.url.rfind(rule.prefix, 0) == 0) {
                required = rule.min_role;
                break;
            }
        }
        if (!required) return;  // публічний ресурс

        // 2. Автентифікація: чи відомо, хто це
        if (!session.user) return deny(req, res, 401, "Потрібен вхід", "-");

        // 3. Авторизація: чи вистачає ролі
        if (static_cast<int>(session.user->role) < static_cast<int>(*required))
            return deny(req, res, 403, "Недостатньо прав", session.user->username);

        // 4. CSRF: змінювальні методи мають передати токен сесії
        const bool mutating = req.method == crow::HTTPMethod::POST || req.method == crow::HTTPMethod::PUT ||
                              req.method == crow::HTTPMethod::PATCH || req.method == crow::HTTPMethod::DELETE;
        if (mutating && !constant_time_equals(req.get_header_value("X-CSRF-Token"), session.user->csrf_token))
            return deny(req, res, 403, "Невірний або відсутній CSRF-токен", session.user->username);

        std::cout << "[AUTHZ] " << crow::method_name(req.method) << " " << req.url
                  << " user=" << session.user->username << " role=" << auth::role_name(session.user->role)
                  << " -> allow\n";
    }

    template <typename AllContext>
    void after_handle(crow::request&, crow::response&, context&, AllContext&) {}

private:
    static void deny(crow::request& req, crow::response& res, int code, const std::string& message,
                     const std::string& who) {
        std::cout << "[AUTHZ] " << crow::method_name(req.method) << " " << req.url << " user=" << who
                  << " -> deny " << code << "\n";
        res.code = code;
        res.set_header("Content-Type", "application/json");
        res.write(json{{"error", message}}.dump());
        res.end();
    }
};

static std::string current_user(crow::App<SessionLoader, SecurityHeaders, Authorizer>& app, const crow::request& req) {
    return app.get_context<SessionLoader>(req).user->username;
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    g_cookie_secure = std::getenv("COOKIE_SECURE") != nullptr;

    crow::App<SessionLoader, SecurityHeaders, Authorizer> app;
    static const std::string dummy_hash = auth::hash_password("dummy-password-for-timing");

    // Демонстраційні облікові записи
    g_users["alice"] = {g_next_user_id++, auth::hash_password("alice-password"), Role::Admin};
    g_users["bob"] = {g_next_user_id++, auth::hash_password("bob-password"), Role::Editor};
    g_users["carol"] = {g_next_user_id++, auth::hash_password("carol-password"), Role::User};

    CROW_ROUTE(app, "/public")([] { return json_response(200, {{"status", "ok"}}); });

    CROW_ROUTE(app, "/register").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        auto body = json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.value("username", json()).is_string() || !body.value("password", json()).is_string())
            return json_response(400, {{"error", "Потрібні рядкові поля username і password"}});
        const std::string username = body["username"], password = body["password"];
        static const std::regex name_re("^[A-Za-z0-9_]{3,32}$");
        if (!std::regex_match(username, name_re) || password.size() < 8)
            return json_response(400, {{"error", "username: 3-32 символи [A-Za-z0-9_], password: від 8"}});
        std::string hash = auth::hash_password(password);
        std::lock_guard<std::mutex> lock(g_mutex);
        if (g_users.count(username)) return json_response(409, {{"error", "Користувач уже існує"}});
        // Роль завжди user: клієнт не може сам обрати роль (масове присвоєння)
        g_users[username] = {g_next_user_id++, hash, Role::User};
        return json_response(201, {{"username", username}, {"role", "user"}});
    });

    CROW_ROUTE(app, "/login").methods(crow::HTTPMethod::POST)([&app](const crow::request& req) {
        auto body = json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.value("username", json()).is_string() || !body.value("password", json()).is_string())
            return json_response(400, {{"error", "Потрібні рядкові поля username і password"}});
        const std::string username = body["username"], password = body["password"];

        // Обмеження спроб: перевіряємо ДО дорогого хешування
        const std::string throttle_key = username + "|" + req.remote_ip_address;
        if (int wait = g_throttle.seconds_locked(throttle_key)) {
            crow::response res = json_response(429, {{"error", "Забагато невдалих спроб"}});
            res.set_header("Retry-After", std::to_string(wait));
            return res;
        }

        std::optional<StoredUser> user;
        {
            std::lock_guard<std::mutex> lock(g_mutex);
            if (auto it = g_users.find(username); it != g_users.end()) user = it->second;
        }
        const bool ok = auth::verify_password(user ? user->password_hash : dummy_hash, password) && user;
        if (!ok) {
            g_throttle.record_failure(throttle_key);
            return json_response(401, {{"error", "Невірний логін або пароль"}});
        }
        g_throttle.record_success(throttle_key);

        // Захист від session fixation: стару сесію з цього запиту знищуємо, видаємо НОВИЙ ідентифікатор
        auto& ctx = app.get_context<SessionLoader>(req);
        if (!ctx.token.empty()) g_sessions.destroy(ctx.token);
        std::string token = g_sessions.create({user->id, username, user->role, ""});

        crow::response res = json_response(200, {{"username", username}, {"role", auth::role_name(user->role)}});
        auth::CookieOptions opt;
        opt.max_age = 3600;
        opt.secure = g_cookie_secure;
        res.add_header("Set-Cookie", auth::make_set_cookie("sid", token, opt));
        return res;
    });

    CROW_ROUTE(app, "/logout").methods(crow::HTTPMethod::POST)([&app](const crow::request& req) {
        g_sessions.destroy(app.get_context<SessionLoader>(req).token);
        crow::response res = json_response(200, {{"status", "logged out"}});
        auth::CookieOptions opt;
        opt.max_age = 0;
        opt.secure = g_cookie_secure;
        res.add_header("Set-Cookie", auth::make_set_cookie("sid", "", opt));
        return res;
    });

    CROW_ROUTE(app, "/me")([&app](const crow::request& req) {
        auto& u = *app.get_context<SessionLoader>(req).user;
        return json_response(200, {{"username", u.username}, {"role", auth::role_name(u.role)}});
    });

    // Клієнт отримує CSRF-токен і додає його в заголовок X-CSRF-Token до змінювальних запитів
    CROW_ROUTE(app, "/csrf")([&app](const crow::request& req) {
        return json_response(200, {{"csrf_token", app.get_context<SessionLoader>(req).user->csrf_token}});
    });

    // ---- Статті: читати може кожен автентифікований, створювати лише editor і вище ----
    CROW_ROUTE(app, "/articles").methods(crow::HTTPMethod::GET)([] {
        std::lock_guard<std::mutex> lock(g_mutex);
        return json_response(200, g_articles);
    });
    CROW_ROUTE(app, "/articles").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        auto body = json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.value("title", json()).is_string())
            return json_response(400, {{"error", "Потрібне рядкове поле title"}});
        std::lock_guard<std::mutex> lock(g_mutex);
        g_articles.push_back(body["title"]);
        return json_response(201, {{"title", body["title"]}});
    });

    // ---- Нотатки: належать власнику (захист від IDOR) ----
    CROW_ROUTE(app, "/notes").methods(crow::HTTPMethod::POST)([&app](const crow::request& req) {
        auto body = json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.value("text", json()).is_string())
            return json_response(400, {{"error", "Потрібне рядкове поле text"}});
        std::lock_guard<std::mutex> lock(g_mutex);
        Note n{g_next_note_id++, current_user(app, req), body["text"]};
        g_notes.push_back(n);
        return json_response(201, {{"id", n.id}, {"owner", n.owner}, {"text", n.text}});
    });

    // НЕБЕЗПЕЧНО: перевіряє лише вхід, але не власника (IDOR)
    CROW_ROUTE(app, "/notes-insecure/<int>")([](int id) {
        std::lock_guard<std::mutex> lock(g_mutex);
        for (const auto& n : g_notes)
            if (n.id == id) return json_response(200, {{"id", n.id}, {"owner", n.owner}, {"text", n.text}});
        return json_response(404, {{"error", "Нотатку не знайдено"}});
    });

    // ПРАВИЛЬНО: власник або admin; чужу нотатку не відрізняємо від неіснуючої (404, не 403)
    CROW_ROUTE(app, "/notes/<int>")([&app](const crow::request& req, int id) {
        auto& u = *app.get_context<SessionLoader>(req).user;
        std::lock_guard<std::mutex> lock(g_mutex);
        for (const auto& n : g_notes) {
            if (n.id != id) continue;
            if (n.owner != u.username && u.role != Role::Admin)
                return json_response(404, {{"error", "Нотатку не знайдено"}});
            return json_response(200, {{"id", n.id}, {"owner", n.owner}, {"text", n.text}});
        }
        return json_response(404, {{"error", "Нотатку не знайдено"}});
    });

    // ---- Адміністрування ----
    CROW_ROUTE(app, "/admin/users")([] {
        std::lock_guard<std::mutex> lock(g_mutex);
        json arr = json::array();
        for (const auto& [name, u] : g_users) arr.push_back({{"username", name}, {"role", auth::role_name(u.role)}});
        return json_response(200, arr);
    });
    CROW_ROUTE(app, "/admin/users/<string>").methods(crow::HTTPMethod::DELETE)([](const std::string& name) {
        {
            std::lock_guard<std::mutex> lock(g_mutex);
            if (!g_users.erase(name)) return json_response(404, {{"error", "Користувача не знайдено"}});
        }
        g_sessions.destroy_all_for(name);  // видалений користувач одразу втрачає всі сесії
        return json_response(200, {{"deleted", name}});
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
