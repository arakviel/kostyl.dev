#pragma once
#include <chrono>
#include <map>
#include <mutex>
#include <string>

namespace auth {

// Захист від перебору паролів: після N невдач ключ (логін + IP) блокується на певний час.
class LoginThrottle {
    using Clock = std::chrono::steady_clock;

public:
    LoginThrottle(int max_failures, std::chrono::seconds lock_time)
        : max_failures_(max_failures), lock_time_(lock_time) {}

    // Скільки секунд ще діє блокування (0 — не заблоковано)
    int seconds_locked(const std::string& key) {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = entries_.find(key);
        if (it == entries_.end()) return 0;
        auto now = Clock::now();
        if (it->second.locked_until > now)
            return static_cast<int>(std::chrono::duration_cast<std::chrono::seconds>(it->second.locked_until - now).count()) + 1;
        return 0;
    }

    void record_failure(const std::string& key) {
        std::lock_guard<std::mutex> lock(mutex_);
        Entry& e = entries_[key];
        if (e.locked_until <= Clock::now() && e.locked_until != Clock::time_point{}) e = Entry{};  // блокування спливло
        if (++e.failures >= max_failures_) e.locked_until = Clock::now() + lock_time_;
    }

    void record_success(const std::string& key) {
        std::lock_guard<std::mutex> lock(mutex_);
        entries_.erase(key);
    }

private:
    struct Entry {
        int failures = 0;
        Clock::time_point locked_until{};
    };
    int max_failures_;
    std::chrono::seconds lock_time_;
    std::mutex mutex_;
    std::map<std::string, Entry> entries_;
};

}  // namespace auth
