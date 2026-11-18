// Етап 4. Active Record: об'єкт сам вміє зберігати себе (user.save()) і знаходити
// (User::find). Модель і доступ до даних злиті в одному класі.
// Зручно для невеликих застосунків; недоліки: клас знає про файл, тестувати без
// файлу важко, замінити сховище означає змінити модель.

#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <mutex>
#include <optional>
#include <vector>

#include "crow.h"
#include "user.hpp"

class UserRecord {
public:
    int id = 0;
    std::string name;
    std::string email;

    static void use_file(std::string path) { file() = std::move(path); load(); }

    static std::vector<UserRecord> all() {
        std::lock_guard<std::mutex> lock(mutex());
        return rows();
    }

    static std::optional<UserRecord> find(int id) {
        std::lock_guard<std::mutex> lock(mutex());
        for (const auto& r : rows())
            if (r.id == id) return r;
        return std::nullopt;
    }

    // Запис самого себе: присвоює id, якщо запис новий
    void save() {
        std::lock_guard<std::mutex> lock(mutex());
        if (id == 0) {
            for (const auto& r : rows()) id = std::max(id, r.id);
            ++id;
            rows().push_back(*this);
        } else {
            for (auto& r : rows())
                if (r.id == id) r = *this;
        }
        flush();
    }

    nlohmann::json to_json() const { return nlohmann::json{{"id", id}, {"name", name}, {"email", email}}; }

private:
    static std::string& file() { static std::string f; return f; }
    static std::mutex& mutex() { static std::mutex m; return m; }
    static std::vector<UserRecord>& rows() { static std::vector<UserRecord> r; return r; }

    static void load() {
        std::ifstream in(file());
        if (!in) return;
        auto j = nlohmann::json::parse(in, nullptr, false);
        if (j.is_discarded()) return;
        for (const auto& item : j) {
            UserRecord r;
            r.id = item["id"];
            r.name = item["name"];
            r.email = item["email"];
            rows().push_back(r);
        }
    }
    static void flush() {
        nlohmann::json arr = nlohmann::json::array();
        for (const auto& r : rows()) arr.push_back(r.to_json());
        std::ofstream out(file());
        out << arr.dump(2);
    }
};

static crow::response json_response(int code, const nlohmann::json& j) {
    crow::response res(code, j.dump());
    res.set_header("Content-Type", "application/json");
    return res;
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    UserRecord::use_file(argc > 2 ? argv[2] : "users_stage4.json");
    crow::SimpleApp app;

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::GET)([] {
        nlohmann::json arr = nlohmann::json::array();
        for (const auto& r : UserRecord::all()) arr.push_back(r.to_json());
        return json_response(200, arr);
    });

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        auto body = nlohmann::json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.contains("name") || !body.contains("email"))
            return crow::response(400, "name та email обов'язкові");
        UserRecord r;
        r.name = body["name"];
        r.email = body["email"];
        r.save();
        return json_response(201, r.to_json());
    });

    CROW_ROUTE(app, "/users/<int>")([](int id) {
        auto r = UserRecord::find(id);
        if (!r) return crow::response(404, "Користувача не знайдено");
        return json_response(200, r->to_json());
    });

    app.port(static_cast<uint16_t>(port)).run();
}
