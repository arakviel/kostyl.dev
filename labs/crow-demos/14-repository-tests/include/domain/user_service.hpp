#pragma once
#include <mutex>
#include <optional>
#include <string>
#include <vector>

#include "domain/user.hpp"
#include "domain/user_repository.hpp"

enum class Status { Ok, Created, NotFound, Conflict, Invalid };

struct Result {
    Status status = Status::Ok;
    std::optional<User> user;
    std::string message;
};

// Бізнес-логіка. Залежить від інтерфейсу IUserRepository, а не від конкретного сховища:
// залежність передається в конструктор (dependency injection).
class UserService {
public:
    explicit UserService(IUserRepository& repository) : repo_(repository) {}

    std::vector<User> list() const { return repo_.find_all(); }

    Result get(int id) const {
        auto user = repo_.find_by_id(id);
        if (!user) return {Status::NotFound, std::nullopt, "Користувача не знайдено"};
        return {Status::Ok, user, ""};
    }

    Result create(const NewUser& input) {
        const std::string problems = validate(input);
        if (!problems.empty()) return {Status::Invalid, std::nullopt, problems};

        // Перевірка унікальності й додавання — одна неподільна дія
        std::lock_guard<std::mutex> lock(mutex_);
        if (repo_.find_by_email(input.email))
            return {Status::Conflict, std::nullopt, "Користувач із таким email уже існує"};
        return {Status::Created, repo_.add(input), ""};
    }

    Result change_email(int id, const std::string& email) {
        if (!email_looks_valid(email)) return {Status::Invalid, std::nullopt, "email: некоректний формат"};

        std::lock_guard<std::mutex> lock(mutex_);
        auto user = repo_.find_by_id(id);
        if (!user) return {Status::NotFound, std::nullopt, "Користувача не знайдено"};
        auto other = repo_.find_by_email(email);
        if (other && other->id != id)
            return {Status::Conflict, std::nullopt, "Користувач із таким email уже існує"};

        user->email = email;
        repo_.update(*user);
        return {Status::Ok, user, ""};
    }

    Result remove(int id) {
        if (!repo_.remove(id)) return {Status::NotFound, std::nullopt, "Користувача не знайдено"};
        return {Status::Ok, std::nullopt, ""};
    }

private:
    static bool email_looks_valid(const std::string& email) {
        auto at = email.find('@');
        return at != std::string::npos && at > 0 && email.find('.', at) != std::string::npos &&
               email.find('@', at + 1) == std::string::npos;
    }

    static size_t utf8_length(const std::string& s) {
        size_t n = 0;
        for (unsigned char c : s)
            if ((c & 0xC0) != 0x80) ++n;
        return n;
    }

    static std::string validate(const NewUser& u) {
        std::string errors;
        auto add = [&errors](const std::string& e) { errors += (errors.empty() ? "" : "; ") + e; };
        size_t len = utf8_length(u.name);
        if (len < 2 || len > 50) add("name: довжина від 2 до 50 символів");
        if (!email_looks_valid(u.email)) add("email: некоректний формат");
        if (u.age < 0 || u.age > 150) add("age: значення від 0 до 150");
        return errors;
    }

    IUserRepository& repo_;
    std::mutex mutex_;
};
