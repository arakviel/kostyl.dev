// Етап 3. DAO (Data Access Object): клас інкапсулює сховище.
// Обробники викликають find_all/find_by_id/insert і не знають про файл.
// Мютекс і формат зберігання сховані всередині.

#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <mutex>
#include <optional>
#include <vector>

#include "crow.h"
#include "user.hpp"

class UserDao {
public:
    explicit UserDao(std::string file) : file_(std::move(file)) { load(); }

    std::vector<User> find_all() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return users_;
    }

    std::optional<User> find_by_id(int id) const {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = std::find_if(users_.begin(), users_.end(), [id](const User& u) { return u.id == id; });
        if (it == users_.end()) return std::nullopt;
        return *it;
    }

    User insert(User u) {
        std::lock_guard<std::mutex> lock(mutex_);
        int next_id = 1;
        for (const auto& existing : users_) next_id = std::max(next_id, existing.id + 1);
        u.id = next_id;
        users_.push_back(u);
        save();
        return u;
    }

private:
    void load() {
        std::ifstream in(file_);
        if (!in) return;
        auto j = nlohmann::json::parse(in, nullptr, false);
        if (!j.is_discarded()) users_ = j.get<std::vector<User>>();
    }
    void save() const {
        std::ofstream out(file_);
        out << nlohmann::json(users_).dump(2);
    }

    std::string file_;
    mutable std::mutex mutex_;
    std::vector<User> users_;
};

static crow::response json_response(int code, const nlohmann::json& j) {
    crow::response res(code, j.dump());
    res.set_header("Content-Type", "application/json");
    return res;
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    const std::string file = argc > 2 ? argv[2] : "users_stage3.json";
    crow::SimpleApp app;
    UserDao dao(file);

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::GET)([&dao] {
        return json_response(200, dao.find_all());
    });

    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::POST)([&dao](const crow::request& req) {
        auto body = nlohmann::json::parse(req.body, nullptr, false);
        if (body.is_discarded() || !body.contains("name") || !body.contains("email"))
            return crow::response(400, "name та email обов'язкові");
        return json_response(201, dao.insert(User{0, body["name"], body["email"]}));
    });

    CROW_ROUTE(app, "/users/<int>")([&dao](int id) {
        auto u = dao.find_by_id(id);
        if (!u) return crow::response(404, "Користувача не знайдено");
        return json_response(200, *u);
    });

    app.port(static_cast<uint16_t>(port)).run();
}
