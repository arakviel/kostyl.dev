// Лекція 02. Перший сервер на Crow.
// Той самий сервер, що в демо 01, але сокети, парсинг і формування
// відповіді бере на себе фреймворк.

#include <cstdlib>

#include "crow.h"

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;

    crow::SimpleApp app;

    // Рядок, що повертається з обробника, стає тілом відповіді зі статусом 200.
    CROW_ROUTE(app, "/")([] {
        return "Hello, Crow! Привіт, світ!";
    });

    // crow::response дає змогу задати статус і заголовок Content-Type.
    CROW_ROUTE(app, "/about")([] {
        crow::response res(200, "<h1>Про сервер</h1><p>Працює на Crow.</p>");
        res.set_header("Content-Type", "text/html; charset=utf-8");
        return res;
    });

    // JSON-відповідь: wvalue перетворюється на текст автоматично.
    CROW_ROUTE(app, "/health")([] {
        crow::json::wvalue body;
        body["status"] = "ok";
        body["framework"] = "Crow";
        return body;
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
