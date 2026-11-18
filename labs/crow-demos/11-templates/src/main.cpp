// Лекція 11. Шаблони Mustache: контекст, цикли, умови, екранування, частини (partials), макет.

#include <cstdlib>
#include <string>
#include <vector>

#include "crow.h"

struct User {
    int id;
    std::string name;
    std::string email;
    std::string bio;
    bool admin;
};

static const std::vector<User> kUsers = {
    {1, "Іван Петренко", "ivan@example.com", "Любить <b>C++</b>", true},
    {2, "Марія Коваленко", "maria@example.com", "<script>alert('xss')</script>", false},
    {3, "Петро Сидоренко", "petro@example.com", "Пише на Crow", false},
};

// Макет: спочатку рендериться сторінка, її HTML передається в layout.html як content.
// Подвійні дужки екранують HTML, тому для готового фрагмента в макеті — потрійні {{{content}}}.
static crow::response render_page(const std::string& page, crow::mustache::context& ctx, const std::string& title) {
    std::string content = crow::mustache::load(page).render_string(ctx);

    crow::mustache::context layout_ctx;
    layout_ctx["title"] = title;
    layout_ctx["content"] = content;

    crow::response res(crow::mustache::load("layout.html").render_string(layout_ctx));
    res.set_header("Content-Type", "text/html; charset=utf-8");
    return res;
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    crow::SimpleApp app;
    // set_base діє на рівні маршруту і скидається перед кожним обробником; потрібен set_global_base.
    crow::mustache::set_global_base(TEMPLATES_DIR);

    CROW_ROUTE(app, "/")([] {
        crow::mustache::context ctx;
        ctx["heading"] = "Ласкаво просимо";
        ctx["count"] = static_cast<int>(kUsers.size());
        return render_page("home.html", ctx, "Головна");
    });

    CROW_ROUTE(app, "/users")([](const crow::request& req) {
        // ?empty=1 показує інвертовану секцію {{^has_users}}
        const bool empty = req.url_params.get("empty") != nullptr;
        crow::mustache::context ctx;
        ctx["has_users"] = !empty;
        if (!empty) {
            for (size_t i = 0; i < kUsers.size(); ++i) {
                ctx["users"][i]["id"] = kUsers[i].id;
                ctx["users"][i]["name"] = kUsers[i].name;
                ctx["users"][i]["admin"] = kUsers[i].admin;
            }
        }
        return render_page("users.html", ctx, "Користувачі");
    });

    CROW_ROUTE(app, "/users/<int>")([](int id) {
        for (const auto& u : kUsers) {
            if (u.id != id) continue;
            crow::mustache::context ctx;
            ctx["name"] = u.name;
            ctx["email"] = u.email;
            ctx["bio"] = u.bio;
            return render_page("user.html", ctx, u.name);
        }
        return crow::response(404, "Користувача не знайдено");
    });

    // Екранування в дії: значення з query потрапляє в HTML тільки через {{name}}
    CROW_ROUTE(app, "/greet")([](const crow::request& req) {
        const char* name = req.url_params.get("name");
        crow::mustache::context ctx;
        ctx["name"] = name ? name : "гість";
        return render_page("greet.html", ctx, "Привітання");
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
