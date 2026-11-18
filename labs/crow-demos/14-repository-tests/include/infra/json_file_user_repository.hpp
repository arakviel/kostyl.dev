#pragma once
#include <algorithm>
#include <fstream>
#include <mutex>

#include "domain/user_repository.hpp"

// Сховище у JSON-файлі: читається при створенні, записується після кожної зміни.
class JsonFileUserRepository : public IUserRepository {
public:
    explicit JsonFileUserRepository(std::string path) : path_(std::move(path)) { load(); }

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
        save();
        return u;
    }

    bool update(const User& user) override {
        std::lock_guard<std::mutex> lock(mutex_);
        for (auto& u : users_) {
            if (u.id == user.id) {
                u = user;
                save();
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
        save();
        return true;
    }

private:
    void load() {
        std::ifstream in(path_);
        if (!in) return;
        auto j = nlohmann::json::parse(in, nullptr, false);
        if (j.is_discarded()) return;
        users_ = j.get<std::vector<User>>();
        for (const auto& u : users_) next_id_ = std::max(next_id_, u.id + 1);
    }

    void save() const {
        std::ofstream out(path_);
        out << nlohmann::json(users_).dump(2);
    }

    std::string path_;
    mutable std::mutex mutex_;
    std::vector<User> users_;
    int next_id_ = 1;
};
