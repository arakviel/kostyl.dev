#pragma once
#include <chrono>
#include <map>
#include <mutex>
#include <optional>
#include <string>

#include "auth/random.hpp"

namespace auth {

enum class Role { User = 1, Editor = 2, Admin = 3 };

inline const char* role_name(Role r) {
    switch (r) {
        case Role::User: return "user";
        case Role::Editor: return "editor";
        case Role::Admin: return "admin";
    }
    return "?";
}

struct SessionData {
    int user_id = 0;
    std::string username;
    Role role = Role::User;
    std::string csrf_token;  // випадковий токен, який клієнт мусить повертати в заголовку
};

// Сховище сесій із двома таймаутами: за бездіяльністю та абсолютним (від створення).
class SessionStore {
    using Clock = std::chrono::steady_clock;

public:
    SessionStore(std::chrono::seconds idle, std::chrono::seconds absolute) : idle_(idle), absolute_(absolute) {}

    std::string create(SessionData data) {
        std::lock_guard<std::mutex> lock(mutex_);
        data.csrf_token = random_token(16);
        std::string token = random_token();
        sessions_[token] = Entry{std::move(data), Clock::now(), Clock::now()};
        return token;
    }

    std::optional<SessionData> get(const std::string& token) {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = sessions_.find(token);
        if (it == sessions_.end()) return std::nullopt;
        const auto now = Clock::now();
        if (now - it->second.last_seen > idle_ || now - it->second.created > absolute_) {
            sessions_.erase(it);
            return std::nullopt;
        }
        it->second.last_seen = now;
        return it->second.data;
    }

    void destroy(const std::string& token) {
        std::lock_guard<std::mutex> lock(mutex_);
        sessions_.erase(token);
    }

    // Знищує всі сесії користувача (після зміни пароля чи видалення акаунта)
    void destroy_all_for(const std::string& username) {
        std::lock_guard<std::mutex> lock(mutex_);
        for (auto it = sessions_.begin(); it != sessions_.end();) {
            if (it->second.data.username == username) it = sessions_.erase(it);
            else ++it;
        }
    }

private:
    struct Entry {
        SessionData data;
        Clock::time_point created;
        Clock::time_point last_seen;
    };
    std::chrono::seconds idle_;
    std::chrono::seconds absolute_;
    std::mutex mutex_;
    std::map<std::string, Entry> sessions_;
};

}  // namespace auth
