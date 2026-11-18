// Лекція 01. HTTP без фреймворку: мінімальний сервер на сокетах.
// Показує, що HTTP — це текст у TCP-з'єднанні: сервер читає запит,
// друкує його як є і відповідає рядком із заголовками та тілом.

#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
using socket_t = SOCKET;
static void close_socket(socket_t s) { closesocket(s); }
#else
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
using socket_t = int;
static void close_socket(socket_t s) { close(s); }
constexpr socket_t INVALID_SOCKET = -1;
#endif

// Збирає HTTP-відповідь: стартовий рядок, заголовки, порожній рядок, тіло.
static std::string build_response(int status, const std::string& reason,
                                  const std::string& content_type,
                                  const std::string& body) {
    std::ostringstream out;
    out << "HTTP/1.1 " << status << ' ' << reason << "\r\n"
        << "Content-Type: " << content_type << "\r\n"
        << "Content-Length: " << body.size() << "\r\n"
        << "Connection: close\r\n"
        << "\r\n"
        << body;
    return out.str();
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;

#ifdef _WIN32
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cerr << "WSAStartup не вдався\n";
        return 1;
    }
#endif

    socket_t server = socket(AF_INET, SOCK_STREAM, 0);
    if (server == INVALID_SOCKET) {
        std::cerr << "Не вдалося створити сокет\n";
        return 1;
    }

    int yes = 1;
    setsockopt(server, SOL_SOCKET, SO_REUSEADDR, reinterpret_cast<const char*>(&yes), sizeof(yes));

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(static_cast<unsigned short>(port));

    if (bind(server, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) < 0) {
        std::cerr << "bind не вдався: порт " << port << " зайнятий?\n";
        return 1;
    }
    if (listen(server, 16) < 0) {
        std::cerr << "listen не вдався\n";
        return 1;
    }

    std::cout << "Сервер слухає http://localhost:" << port << " (Ctrl+C для зупинки)\n";

    while (true) {
        socket_t client = accept(server, nullptr, nullptr);
        if (client == INVALID_SOCKET) continue;

        char buffer[4096];
        int n = static_cast<int>(recv(client, buffer, sizeof(buffer) - 1, 0));
        if (n <= 0) {
            close_socket(client);
            continue;
        }
        std::string request(buffer, static_cast<size_t>(n));

        // Стартовий рядок запиту: "GET /path HTTP/1.1"
        std::istringstream first_line(request.substr(0, request.find("\r\n")));
        std::string method, target, version;
        first_line >> method >> target >> version;

        std::cout << "---- запит ----\n" << request << "---------------\n";

        std::string response;
        if (method == "GET" && target == "/") {
            response = build_response(200, "OK", "text/html; charset=utf-8",
                                      "<h1>Привіт з сирого HTTP-сервера</h1>");
        } else if (method == "GET" && target == "/echo") {
            // Повертає сам запит назад, щоб студент бачив, що надіслав клієнт.
            response = build_response(200, "OK", "text/plain; charset=utf-8", request);
        } else if (method == "GET") {
            response = build_response(404, "Not Found", "text/plain; charset=utf-8",
                                      "Немає сторінки " + target);
        } else {
            response = build_response(405, "Method Not Allowed", "text/plain; charset=utf-8",
                                      "Метод " + method + " не підтримується");
        }

        send(client, response.data(), static_cast<int>(response.size()), 0);
        close_socket(client);
    }
}
