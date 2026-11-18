#pragma once
#include <map>
#include <sstream>
#include <string>

namespace auth {

// Розбір заголовка Cookie: "a=1; b=2" -> {a: 1, b: 2}
inline std::map<std::string, std::string> parse_cookies(const std::string& header) {
    std::map<std::string, std::string> result;
    std::istringstream in(header);
    std::string part;
    while (std::getline(in, part, ';')) {
        auto start = part.find_first_not_of(' ');
        if (start == std::string::npos) continue;
        part = part.substr(start);
        auto eq = part.find('=');
        if (eq == std::string::npos) continue;
        result[part.substr(0, eq)] = part.substr(eq + 1);
    }
    return result;
}

struct CookieOptions {
    int max_age = -1;               // секунди; -1 = сесійний cookie (зникає зі закриттям браузера)
    bool http_only = true;          // недоступний для JavaScript (document.cookie)
    bool secure = false;            // лише через HTTPS; на localhost без TLS вимкнено
    std::string same_site = "Lax";  // Strict | Lax | None
    std::string path = "/";
};

// Формує значення заголовка Set-Cookie
inline std::string make_set_cookie(const std::string& name, const std::string& value, const CookieOptions& o = {}) {
    std::string s = name + "=" + value + "; Path=" + o.path;
    if (o.max_age >= 0) s += "; Max-Age=" + std::to_string(o.max_age);
    if (o.http_only) s += "; HttpOnly";
    if (o.secure) s += "; Secure";
    if (!o.same_site.empty()) s += "; SameSite=" + o.same_site;
    return s;
}

}  // namespace auth
