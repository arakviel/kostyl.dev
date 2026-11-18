// Лекція 09. Middleware: ланцюжок, порядок виконання, ранній вихід, контекст.
//
// Кожен middleware має before_handle (до обробника) й after_handle (після).
// Порядок before_handle збігається з порядком у crow::App<...>,
// порядок after_handle — зворотний.

#include <chrono>
#include <cstdlib>
#include <iostream>
#include <string>

#include "crow.h"

// Допоміжна функція: дописує мітку в заголовок X-Trace, щоб порядок було видно в curl.
static void trace(crow::response& res, const std::string& label) {
    std::string current = res.get_header_value("X-Trace");
    res.set_header("X-Trace", current.empty() ? label : current + " > " + label);
}

struct First {
    struct context {};
    void before_handle(crow::request&, crow::response& res, context&) { trace(res, "First.before"); }
    void after_handle(crow::request&, crow::response& res, context&) { trace(res, "First.after"); }
};

// Контекст: дані, які middleware залишає для наступних учасників ланцюжка й обробника.
struct Timer {
    struct context {
        std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    };
    void before_handle(crow::request&, crow::response& res, context& ctx) {
        ctx.start = std::chrono::steady_clock::now();
        trace(res, "Timer.before");
    }
    void after_handle(crow::request& req, crow::response& res, context& ctx) {
        auto us = std::chrono::duration_cast<std::chrono::microseconds>(
                      std::chrono::steady_clock::now() - ctx.start).count();
        res.set_header("X-Elapsed-Us", std::to_string(us));
        trace(res, "Timer.after");
        std::cout << req.url << " оброблено за " << us << " мкс\n";
    }
};

// Ранній вихід: якщо запит не пройшов перевірку, відповідь формується тут,
// і обробник маршруту не викликається.
struct Gate {
    struct context {};
    void before_handle(crow::request& req, crow::response& res, context&) {
        trace(res, "Gate.before");
        if (req.url_params.get("deny")) {
            res.code = 403;
            res.write("Доступ заборонено middleware Gate\n");
            res.end();
        }
    }
    void after_handle(crow::request&, crow::response& res, context&) { trace(res, "Gate.after"); }
};

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;

    crow::App<First, Timer, Gate> app;

    // Обробник із параметром crow::response& змінює ТОЙ САМИЙ об'єкт відповіді,
    // який уже бачили before_handle. Якщо ж обробник повертає новий crow::response
    // (або рядок), заголовки, поставлені в before_handle, губляться.
    CROW_ROUTE(app, "/")([&app](const crow::request& req, crow::response& res) {
        auto& timer_ctx = app.get_context<Timer>(req);  // контекст іншого middleware
        (void)timer_ctx;
        trace(res, "handler");
        res.write("Відповідь обробника\n");
        res.end();
    });

    // Для порівняння: обробник повертає значення. Мітки before_handle зникають.
    CROW_ROUTE(app, "/returns")([] {
        crow::response res(200, "Обробник повернув нову відповідь\n");
        trace(res, "handler");
        return res;
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
