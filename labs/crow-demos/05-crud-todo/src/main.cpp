// Лекція 05. HTTP-методи і CRUD: TODO API у пам'яті.
// POST створює, GET читає, PUT замінює, PATCH змінює частину, DELETE видаляє.

#include <cstdlib>
#include <map>
#include <mutex>
#include <string>

#include "crow.h"

struct Todo {
    int id = 0;
    std::string title;
    std::string description;
    bool completed = false;
};

class TodoStore {
public:
    Todo create(std::string title, std::string description) {
        std::lock_guard<std::mutex> lock(mutex_);
        Todo t{next_id_++, std::move(title), std::move(description), false};
        items_[t.id] = t;
        return t;
    }
    bool find(int id, Todo& out) {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = items_.find(id);
        if (it == items_.end()) return false;
        out = it->second;
        return true;
    }
    std::vector<Todo> all() {
        std::lock_guard<std::mutex> lock(mutex_);
        std::vector<Todo> v;
        for (const auto& [id, t] : items_) v.push_back(t);
        return v;
    }
    bool replace(const Todo& t) {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = items_.find(t.id);
        if (it == items_.end()) return false;
        it->second = t;
        return true;
    }
    bool remove(int id) {
        std::lock_guard<std::mutex> lock(mutex_);
        return items_.erase(id) > 0;
    }

private:
    std::mutex mutex_;
    std::map<int, Todo> items_;
    int next_id_ = 1;
};

static crow::json::wvalue to_json(const Todo& t) {
    crow::json::wvalue j;
    j["id"] = t.id;
    j["title"] = t.title;
    j["description"] = t.description;
    j["completed"] = t.completed;
    return j;
}

static crow::response error(int code, const std::string& message) {
    crow::json::wvalue j;
    j["error"] = message;
    return crow::response(code, j);
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    crow::SimpleApp app;
    TodoStore store;

    // CREATE: POST /todos -> 201 Created + Location
    CROW_ROUTE(app, "/todos").methods(crow::HTTPMethod::POST)([&store](const crow::request& req) {
        auto body = crow::json::load(req.body);
        if (!body) return error(400, "Тіло запиту не є коректним JSON");
        if (!body.has("title") || body["title"].t() != crow::json::type::String)
            return error(400, "Поле title (рядок) обов'язкове");

        std::string description = body.has("description") ? std::string(body["description"].s()) : "";
        Todo t = store.create(body["title"].s(), description);

        crow::response res(201, to_json(t));
        res.set_header("Location", "/todos/" + std::to_string(t.id));
        return res;
    });

    // READ (колекція) із фільтром ?completed=true|false
    CROW_ROUTE(app, "/todos").methods(crow::HTTPMethod::GET)([&store](const crow::request& req) {
        const char* filter = req.url_params.get("completed");
        crow::json::wvalue::list items;
        for (const auto& t : store.all()) {
            if (filter && (std::string(filter) == "true") != t.completed) continue;
            items.push_back(to_json(t));
        }
        crow::json::wvalue j;
        j["count"] = items.size();
        j["data"] = std::move(items);
        return crow::response(200, j);
    });

    // READ (один елемент)
    CROW_ROUTE(app, "/todos/<int>").methods(crow::HTTPMethod::GET)([&store](int id) {
        Todo t;
        if (!store.find(id, t)) return error(404, "Задачу не знайдено");
        return crow::response(200, to_json(t));
    });

    // UPDATE (повна заміна): PUT вимагає всі поля
    CROW_ROUTE(app, "/todos/<int>").methods(crow::HTTPMethod::PUT)([&store](const crow::request& req, int id) {
        auto body = crow::json::load(req.body);
        if (!body) return error(400, "Тіло запиту не є коректним JSON");
        if (!body.has("title") || !body.has("description") || !body.has("completed"))
            return error(400, "PUT вимагає всі поля: title, description, completed");

        Todo t{id, body["title"].s(), body["description"].s(), body["completed"].b()};
        if (!store.replace(t)) return error(404, "Задачу не знайдено");
        return crow::response(200, to_json(t));
    });

    // UPDATE (часткове): PATCH змінює лише передані поля
    CROW_ROUTE(app, "/todos/<int>").methods(crow::HTTPMethod::PATCH)([&store](const crow::request& req, int id) {
        auto body = crow::json::load(req.body);
        if (!body) return error(400, "Тіло запиту не є коректним JSON");

        Todo t;
        if (!store.find(id, t)) return error(404, "Задачу не знайдено");
        if (body.has("title")) t.title = body["title"].s();
        if (body.has("description")) t.description = body["description"].s();
        if (body.has("completed")) t.completed = body["completed"].b();
        store.replace(t);
        return crow::response(200, to_json(t));
    });

    // DELETE: 204 без тіла, повторне видалення дає 404
    CROW_ROUTE(app, "/todos/<int>").methods(crow::HTTPMethod::DELETE)([&store](int id) {
        if (!store.remove(id)) return error(404, "Задачу не знайдено");
        return crow::response(204);
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
