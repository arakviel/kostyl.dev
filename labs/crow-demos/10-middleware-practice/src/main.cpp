// Лекція 10. Middleware на практиці: журнал запитів, API-ключ (локальний middleware),
// обмеження частоти запитів (429), CORS (вбудований у Crow).

#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <map>
#include <mutex>
#include <sstream>
#include <string>

#include "crow.h"
#include "crow/middlewares/cors.h"

// Журнал: час, метод, шлях, IP, статус, тривалість
struct AccessLog {
    struct context {
        // Початкове значення потрібне: after_handle може виконатися без before_handle
        // (наприклад, для preflight-запиту OPTIONS, який обробляє CORS).
        std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    };
    void before_handle(crow::request&, crow::response&, context& ctx) {
        ctx.start = std::chrono::steady_clock::now();
    }
    void after_handle(crow::request& req, crow::response& res, context& ctx) {
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                      std::chrono::steady_clock::now() - ctx.start).count();
        std::cout << "[ACCESS] " << crow::method_name(req.method) << " " << req.raw_url << " from "
                  << req.remote_ip_address << " -> " << res.code << " (" << ms << " ms)\n";
    }
};

// Обмеження частоти: фіксоване вікно, лічильник на IP
struct RateLimit {
    struct context {
        int remaining = 0;
    };

    static constexpr int kMaxRequests = 5;
    static constexpr std::chrono::seconds kWindow{10};

    void before_handle(crow::request& req, crow::response& res, context& ctx) {
        const auto now = std::chrono::steady_clock::now();
        std::lock_guard<std::mutex> lock(mutex_);
        Bucket& b = buckets_[req.remote_ip_address];
        if (now - b.window_start >= kWindow) {
            b.window_start = now;
            b.count = 0;
        }
        ++b.count;

        ctx.remaining = std::max(0, kMaxRequests - b.count);

        if (b.count > kMaxRequests) {
            auto retry = std::chrono::duration_cast<std::chrono::seconds>(kWindow - (now - b.window_start)).count();
            res.code = 429;
            res.set_header("Retry-After", std::to_string(retry + 1));
            res.write("Забагато запитів. Повторіть пізніше.\n");
            res.end();
        }
    }
    // Заголовки ставимо в after_handle: тоді вони потрапляють у відповідь,
    // навіть якщо обробник повернув новий crow::response.
    void after_handle(crow::request&, crow::response& res, context& ctx) {
        res.set_header("X-RateLimit-Limit", std::to_string(kMaxRequests));
        res.set_header("X-RateLimit-Remaining", std::to_string(ctx.remaining));
    }

private:
    struct Bucket {
        std::chrono::steady_clock::time_point window_start{};
        int count = 0;
    };
    std::mutex mutex_;
    std::map<std::string, Bucket> buckets_;
};

// Локальний middleware: застосовується лише до маршрутів, які його явно підключили.
struct ApiKeyAuth : crow::ILocalMiddleware {
    struct context {
        std::string client;
    };
    void before_handle(crow::request& req, crow::response& res, context& ctx) {
        const std::string key = req.get_header_value("X-API-Key");
        if (key.empty()) {
            res.code = 401;
            res.write("Потрібен заголовок X-API-Key\n");
            res.end();
            return;
        }
        if (key != "secret-123") {
            res.code = 403;
            res.write("Невірний API-ключ\n");
            res.end();
            return;
        }
        ctx.client = "demo-client";
    }
    void after_handle(crow::request&, crow::response&, context&) {}
};

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;

    crow::App<crow::CORSHandler, AccessLog, RateLimit, ApiKeyAuth> app;

    // CORS налаштовується глобально, правила можна задавати й для окремих префіксів
    auto& cors = app.get_middleware<crow::CORSHandler>();
    cors.global().origin("http://localhost:3000").methods("GET"_method, "POST"_method).headers("Content-Type", "X-API-Key");

    CROW_ROUTE(app, "/public")([] { return "Публічний ресурс\n"; });

    CROW_ROUTE(app, "/admin").CROW_MIDDLEWARES(app, ApiKeyAuth)([&app](const crow::request& req) {
        auto& ctx = app.get_context<ApiKeyAuth>(req);
        return "Вітаю, " + ctx.client + "\n";
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
