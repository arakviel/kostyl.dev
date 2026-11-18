// Лекція 03. Маршрути: статичні шляхи, path-параметри, query-параметри.

#include <cstdlib>
#include <map>
#include <sstream>
#include <string>

#include "crow.h"

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;

    crow::SimpleApp app;

    const std::map<int, std::string> users = {
        {1, "Іван Петренко"}, {2, "Марія Коваленко"}, {3, "Петро Сидоренко"}};

    // Статичні маршрути, вкладені шляхи
    CROW_ROUTE(app, "/")([] { return "Головна"; });
    CROW_ROUTE(app, "/api/v1/status")([] { return "API v1 працює"; });

    // <int>, <double>, <string> — path-параметри, тип визначає, що буде прийнято
    CROW_ROUTE(app, "/users/<int>")([&users](int id) {
        auto it = users.find(id);
        if (it == users.end()) return crow::response(404, "Користувача не знайдено");
        return crow::response(200, "Користувач: " + it->second);
    });

    CROW_ROUTE(app, "/square/<double>")([](double x) {
        return crow::response(std::to_string(x * x));
    });

    CROW_ROUTE(app, "/hello/<string>")([](const std::string& name) {
        return "Привіт, " + name + "!";
    });

    // Кілька параметрів у шляху
    CROW_ROUTE(app, "/calc/add/<int>/<int>")([](int a, int b) {
        return std::to_string(a + b);
    });

    // <path> захоплює решту шляху разом зі слешами
    CROW_ROUTE(app, "/files/<path>")([](const std::string& p) {
        return "Запитано файл: " + p;
    });

    // Query-параметри: /search?q=Марія&limit=5
    CROW_ROUTE(app, "/search")([&users](const crow::request& req) {
        const char* q = req.url_params.get("q");
        if (!q) return crow::response(400, "Параметр q обов'язковий");

        int limit = 10;
        if (const char* l = req.url_params.get("limit")) limit = std::atoi(l);

        std::ostringstream out;
        int found = 0;
        for (const auto& [id, name] : users) {
            if (found >= limit) break;
            if (name.find(q) != std::string::npos) {
                out << id << ". " << name << "\n";
                ++found;
            }
        }
        if (found == 0) return crow::response(404, "Нічого не знайдено");
        return crow::response(200, out.str());
    });

    // Список значень: Crow читає ключ із дужками, /tags?t[]=cpp&t[]=web
    CROW_ROUTE(app, "/tags")([](const crow::request& req) {
        std::ostringstream out;
        for (const auto& t : req.url_params.get_list("t")) out << t << "\n";
        return out.str();
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
