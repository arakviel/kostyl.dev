#pragma once
#include <argon2.h>

#include <stdexcept>
#include <string>
#include <vector>

#include "auth/random.hpp"

namespace auth {

// Параметри Argon2id (рекомендація OWASP: 19 МіБ пам'яті, 2 ітерації, 1 потік).
constexpr uint32_t kTimeCost = 2;
constexpr uint32_t kMemoryKiB = 19456;
constexpr uint32_t kParallelism = 1;
constexpr size_t kSaltBytes = 16;
constexpr size_t kHashBytes = 32;

// Повертає рядок формату "$argon2id$v=19$m=19456,t=2,p=1$<сіль>$<хеш>":
// сіль і параметри зберігаються разом із хешем.
inline std::string hash_password(const std::string& password) {
    std::string salt_hex = random_token(kSaltBytes);
    std::vector<unsigned char> salt(kSaltBytes);
    for (size_t i = 0; i < kSaltBytes; ++i)
        salt[i] = static_cast<unsigned char>(std::stoi(salt_hex.substr(i * 2, 2), nullptr, 16));

    std::vector<char> encoded(argon2_encodedlen(kTimeCost, kMemoryKiB, kParallelism, kSaltBytes, kHashBytes,
                                                 Argon2_id));
    int rc = argon2id_hash_encoded(kTimeCost, kMemoryKiB, kParallelism, password.data(), password.size(),
                                   salt.data(), salt.size(), kHashBytes, encoded.data(), encoded.size());
    if (rc != ARGON2_OK) throw std::runtime_error(std::string("argon2: ") + argon2_error_message(rc));
    return std::string(encoded.data());
}

inline bool verify_password(const std::string& encoded, const std::string& password) {
    return argon2id_verify(encoded.c_str(), password.data(), password.size()) == ARGON2_OK;
}

}  // namespace auth
