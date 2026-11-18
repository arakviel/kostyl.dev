// Лекція 04. Request і Response: заголовки, статус-коди, типи відповідей.

#include <cstdlib>
#include <sstream>
#include <set>
#include <string>

#include "crow.h"

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;

    crow::SimpleApp app;

    // Що містить request: метод, URL, заголовки, тіло, IP клієнта
    CROW_ROUTE(app, "/inspect").methods(crow::HTTPMethod::GET, crow::HTTPMethod::POST)(
        [](const crow::request& req) {
            std::ostringstream out;
            out << "method: " << crow::method_name(req.method) << "\n"
                << "url: " << req.url << "\n"
                << "raw_url: " << req.raw_url << "\n"
                << "remote_ip: " << req.remote_ip_address << "\n"
                << "User-Agent: " << req.get_header_value("User-Agent") << "\n"
                << "Content-Length: " << req.body.size() << "\n"
                << "body: " << req.body << "\n";
            return crow::response(200, out.str());
        });

    // Довільний статус-код: /status/404.
    // Crow знає лише коди зі своєї таблиці; для решти (наприклад, 418, 422)
    // відповідь перетворюється на 500, тому такі коди відсікаються заздалегідь.
    CROW_ROUTE(app, "/status/<int>")([](int code) {
        static const std::set<int> known = {200, 201, 202, 204, 301, 302, 304, 400, 401, 403,
                                            404, 405, 409, 413, 429, 500, 501, 502, 503, 504};
        if (!known.count(code)) return crow::response(400, "Код " + std::to_string(code) + " не підтримується");
        return crow::response(code, "Статус " + std::to_string(code));
    });

    // Типи відповідей
    CROW_ROUTE(app, "/text")([] {
        crow::response res(200, "Звичайний текст");
        res.set_header("Content-Type", "text/plain; charset=utf-8");
        return res;
    });

    CROW_ROUTE(app, "/html")([] {
        crow::response res(200, "<html><body><h1>HTML</h1></body></html>");
        res.set_header("Content-Type", "text/html; charset=utf-8");
        return res;
    });

    CROW_ROUTE(app, "/json")([] {
        crow::json::wvalue body;
        body["id"] = 1;
        body["name"] = "Іван";
        body["tags"] = std::vector<std::string>{"cpp", "web"};
        crow::response res(200, body);
        return res;
    });

    CROW_ROUTE(app, "/xml")([] {
        crow::response res(200, "<user><id>1</id><name>Іван</name></user>");
        res.set_header("Content-Type", "application/xml; charset=utf-8");
        return res;
    });

    CROW_ROUTE(app, "/download")([] {
        crow::response res(200, "id,name\n1,Іван\n2,Марія\n");
        res.set_header("Content-Type", "text/csv; charset=utf-8");
        res.set_header("Content-Disposition", "attachment; filename=\"users.csv\"");
        return res;
    });

    // Перенаправлення: 302 + заголовок Location
    CROW_ROUTE(app, "/old")([] {
        crow::response res(302);
        res.set_header("Location", "/html");
        return res;
    });

    // Власні заголовки
    CROW_ROUTE(app, "/headers")([] {
        crow::response res(200, "Дивіться заголовки відповіді");
        res.set_header("X-Powered-By", "Crow");
        res.set_header("Cache-Control", "no-store");
        return res;
    });

    // Єдиний формат помилки
    CROW_ROUTE(app, "/api/users/<int>")([](int id) {
        if (id != 1) {
            crow::json::wvalue err;
            err["status"] = "error";
            err["message"] = "Користувача не знайдено";
            err["code"] = 404;
            crow::response res(404, err);
            return res;
        }
        crow::json::wvalue ok;
        ok["status"] = "success";
        ok["data"]["id"] = 1;
        ok["data"]["name"] = "Іван";
        return crow::response(200, ok);
    });

    // Власна сторінка для неіснуючих маршрутів
    CROW_CATCHALL_ROUTE(app)([](const crow::request& req, crow::response& res) {
        res.code = 404;
        res.set_header("Content-Type", "text/html; charset=utf-8");
        res.write("<h1>404</h1><p>Немає маршруту " + req.url + "</p>");
        res.end();
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
