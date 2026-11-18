// Лекція 14. Repository + dependency injection.
// Сховище обирається в одному місці (тут), решта коду працює з IUserRepository.
//
//   repository_api [порт] [memory | json <файл>]

#include <cstdlib>
#include <iostream>
#include <memory>
#include <string>

#include "domain/user_service.hpp"
#include "http/user_api.hpp"
#include "infra/in_memory_user_repository.hpp"
#include "infra/json_file_user_repository.hpp"

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    const std::string kind = argc > 2 ? argv[2] : "memory";

    // Єдине місце, яке знає про конкретні реалізації
    std::unique_ptr<IUserRepository> repository;
    if (kind == "json") {
        const std::string path = argc > 3 ? argv[3] : "users.json";
        repository = std::make_unique<JsonFileUserRepository>(path);
        std::cout << "Сховище: JSON-файл " << path << "\n";
    } else {
        repository = std::make_unique<InMemoryUserRepository>();
        std::cout << "Сховище: пам'ять\n";
    }

    UserService service(*repository);

    crow::SimpleApp app;
    api::register_user_routes(app, service);
    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
