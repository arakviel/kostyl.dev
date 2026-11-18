#pragma once
#include <random>
#include <string>

namespace auth {

// Випадковий токен із crypto-стійкого джерела ОС (std::random_device на macOS/Linux
// читає /dev/urandom). 32 байти = 256 біт ентропії, запис у hex.
inline std::string random_token(size_t bytes = 32) {
    static const char* hex = "0123456789abcdef";
    std::random_device rd;
    std::string token;
    token.reserve(bytes * 2);
    for (size_t i = 0; i < bytes; ++i) {
        unsigned char b = static_cast<unsigned char>(rd());
        token += hex[b >> 4];
        token += hex[b & 0x0F];
    }
    return token;
}

}  // namespace auth
