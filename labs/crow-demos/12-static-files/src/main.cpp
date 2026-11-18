// Лекція 12. Статичні файли: вбудований маршрут /static/<path>, MIME-типи,
// власна видача файлів із захистом від виходу за межі папки, Cache-Control.

#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iterator>
#include <map>
#include <sstream>
#include <string>

#include "crow.h"

namespace fs = std::filesystem;

static std::string mime_type(const fs::path& path) {
    static const std::map<std::string, std::string> types = {
        {".html", "text/html; charset=utf-8"}, {".css", "text/css; charset=utf-8"},
        {".js", "application/javascript; charset=utf-8"}, {".json", "application/json"},
        {".txt", "text/plain; charset=utf-8"}, {".csv", "text/csv; charset=utf-8"},
        {".svg", "image/svg+xml"}, {".png", "image/png"}, {".jpg", "image/jpeg"},
    };
    auto it = types.find(path.extension().string());
    return it == types.end() ? "application/octet-stream" : it->second;
}

// Перевіряє, що файл після нормалізації лежить усередині base.
static bool is_inside(const fs::path& base, const fs::path& file) {
    auto b = base.begin();
    auto f = file.begin();
    for (; b != base.end(); ++b, ++f) {
        if (f == file.end() || *f != *b) return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    const int port = argc > 1 ? std::atoi(argv[1]) : 8080;
    crow::SimpleApp app;

    const fs::path downloads = fs::weakly_canonical(DOWNLOADS_DIR);

    // Вбудований маршрут /static/<path> додається автоматично.
    // set_static_file_info очищає ім'я файлу й шукає його відносно робочої папки, тому для
    // абсолютного шляху, який складає сам сервер (не клієнт), беремо _unsafe-варіант.
    CROW_ROUTE(app, "/")([](crow::response& res) {
        res.set_static_file_info_unsafe(std::string(CROW_STATIC_DIRECTORY) + "index.html");
        res.end();
    });

    // Власна видача: ми самі визначаємо MIME-тип, заголовки кешування та безпеку шляху.
    CROW_ROUTE(app, "/files/<path>")([&downloads](const std::string& relative) {
        fs::path requested = fs::weakly_canonical(downloads / relative);
        if (!is_inside(downloads, requested))
            return crow::response(403, "Вихід за межі папки заборонено");
        if (!fs::is_regular_file(requested))
            return crow::response(404, "Файл не знайдено");

        std::ifstream in(requested, std::ios::binary);
        std::string body((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());

        crow::response res(200, body);
        res.set_header("Content-Type", mime_type(requested));
        res.set_header("Cache-Control", "public, max-age=3600");
        return res;
    });

    app.port(static_cast<uint16_t>(port)).multithreaded().run();
}
