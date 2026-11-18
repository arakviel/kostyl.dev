#pragma once
#include <chrono>
#include <map>
#include <mutex>
#include <optional>
#include <string>

#include "auth/random.hpp"

namespace auth {

struct SessionData {
    int user_id = 0;
    std::string username;
};

// Серверне сховище сесій: у cookie лежить лише випадковий ідентифікатор,
// а дані користувача залишаються на сервері.
class SessionStore {
    using Clock = std::chrono::steady_clock;

public:
    explicit SessionStore(std::chrono::seconds idle_timeout = std::chrono::minutes(30))
        : idle_timeout_(idle_timeout) {}

    std::string create(SessionData data) {
        std::lock_guard<std::mutex> lock(mutex_);
        std::string token = random_token();
        sessions_[token] = Entry{std::move(data), Clock::now()};
        return token;
    }

    // Повертає дані сесії й продовжує її життя; прострочену сесію видаляє.
    std::optional<SessionData> get(const std::string& token) {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = sessions_.find(token);
        if (it == sessions_.end()) return std::nullopt;
        if (Clock::now() - it->second.last_seen > idle_timeout_) {
            sessions_.erase(it);
            return std::nullopt;
        }
        it->second.last_seen = Clock::now();
        return it->second.data;
    }

    void destroy(const std::string& token) {
        std::lock_guard<std::mutex> lock(mutex_);
        sessions_.erase(token);
    }

    size_t size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return sessions_.size();
    }

private:
    struct Entry {
        SessionData data;
        Clock::time_point last_seen;
    };
    std::chrono::seconds idle_timeout_;
    mutable std::mutex mutex_;
    std::map<std::string, Entry> sessions_;
};

}  // namespace auth
