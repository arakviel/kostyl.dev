#pragma once
#include <algorithm>
#include <mutex>

#include "domain/user_repository.hpp"

// Сховище в пам'яті: швидке, без файлів. Підходить для тестів і прототипів.
class InMemoryUserRepository : public IUserRepository {
public:
    std::vector<User> find_all() const override {
        std::lock_guard<std::mutex> lock(mutex_);
        return users_;
    }

    std::optional<User> find_by_id(int id) const override {
        std::lock_guard<std::mutex> lock(mutex_);
        for (const auto& u : users_)
            if (u.id == id) return u;
        return std::nullopt;
    }

    std::optional<User> find_by_email(const std::string& email) const override {
        std::lock_guard<std::mutex> lock(mutex_);
        for (const auto& u : users_)
            if (u.email == email) return u;
        return std::nullopt;
    }

    User add(const NewUser& input) override {
        std::lock_guard<std::mutex> lock(mutex_);
        User u{next_id_++, input.name, input.email, input.age};
        users_.push_back(u);
        return u;
    }

    bool update(const User& user) override {
        std::lock_guard<std::mutex> lock(mutex_);
        for (auto& u : users_) {
            if (u.id == user.id) {
                u = user;
                return true;
            }
        }
        return false;
    }

    bool remove(int id) override {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = std::remove_if(users_.begin(), users_.end(), [id](const User& u) { return u.id == id; });
        if (it == users_.end()) return false;
        users_.erase(it, users_.end());
        return true;
    }

private:
    mutable std::mutex mutex_;
    std::vector<User> users_;
    int next_id_ = 1;
};
