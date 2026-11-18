// Лекція 15. Той самий сервіс і той самий HTTP-шар, але сховище — SQLite.
//
//   sqlite_repository_api [порт] [memory | json <файл> | sqlite <файл.db>]

#include <cstdlib>
#include <iostream>
#include <memory>
#include <string>

#include "domain/user_service.hpp"
#include "http/user_api.hpp"
#include "infra/in_memory_user_repository.hpp"
#include "infra/json_file_user_repository.hpp"
#include "infra/sqlite_user_repository.hpp"

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    const std::string kind = argc > 2 ? argv[2] : "sqlite";
    const std::string path = argc > 3 ? argv[3] : (kind == "json" ? "users.json" : "users.db");

    std::unique_ptr<IUserRepository> repository;
    if (kind == "memory") {
        repository = std::make_unique<InMemoryUserRepository>();
    } else if (kind == "json") {
        repository = std::make_unique<JsonFileUserRepository>(path);
    } else {
        repository = std::make_unique<SqliteUserRepository>(path);
    }
    std::cout << "Сховище: " << kind << (kind == "memory" ? "" : " (" + path + ")") << "\n";

    UserService service(*repository);

    crow::SimpleApp app;
    api::register_user_routes(app, service);
    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
