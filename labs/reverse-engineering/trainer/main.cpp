// Зовнішній тренер: сканує пам'ять процесу і змінює значення.
//   trainer scan  <pid> <int>              — знайти всі адреси зі значенням
//   trainer read  <pid> <addr> [int|float] — прочитати значення
//   trainer write <pid> <addr> <int>       — записати int
//   trainer chain <pid> <Game*>            — пройти ланцюжок Game -> Player і показати поля
//   trainer god   <pid> <Game*>            — тримати HP=999 і набої=99 (Ctrl+C для виходу)
//   trainer ac    <pid> <addr_of_player1> <ptr_size 4|8> <health_off> — режим для AssaultCube
#include "process.hpp"
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <thread>

// Зміщення полів у структурах цілі (див. target-game/main.cpp).
constexpr uintptr_t OFF_GAME_PLAYER = 8;   // Game::player
constexpr uintptr_t OFF_HEALTH = 16;       // Player::health
constexpr uintptr_t OFF_ARMOR = 20;        // Player::armor
constexpr uintptr_t OFF_AMMO = 32;         // Player::weapon.ammo

static uintptr_t parse_addr(const char* s) { return static_cast<uintptr_t>(std::strtoull(s, nullptr, 0)); }

static int scan(const Process& p, int32_t value) {
    int found = 0;
    std::vector<uint8_t> buf;
    for (const Region& r : p.writable_regions()) {
        buf.resize(r.size);
        if (!p.read(r.start, buf.data(), r.size)) continue;
        for (size_t i = 0; i + 4 <= r.size; i += 4) {
            int32_t v;
            std::memcpy(&v, &buf[i], 4);
            if (v == value) {
                std::printf("0x%llx\n", static_cast<unsigned long long>(r.start + i));
                ++found;
            }
        }
    }
    std::fprintf(stderr, "знайдено: %d\n", found);
    return 0;
}

static bool resolve_player(const Process& p, uintptr_t game, uintptr_t& player) {
    return p.read_value(game + OFF_GAME_PLAYER, player) && player != 0;
}

int main(int argc, char** argv) {
    if (argc < 3) { std::fprintf(stderr, "Використання: див. коментар у main.cpp\n"); return 1; }
    std::string cmd = argv[1];
    Process p(std::atoi(argv[2]));
    if (!p.ok()) return 2;

    if (cmd == "scan" && argc >= 4) return scan(p, std::atoi(argv[3]));

    if (cmd == "read" && argc >= 4) {
        uintptr_t a = parse_addr(argv[3]);
        bool as_float = argc >= 5 && std::string(argv[4]) == "float";
        if (as_float) { float f; if (!p.read_value(a, f)) return 3; std::printf("%f\n", f); }
        else { int32_t v; if (!p.read_value(a, v)) return 3; std::printf("%d\n", v); }
        return 0;
    }

    if (cmd == "write" && argc >= 5) {
        int32_t v = std::atoi(argv[4]);
        return p.write_value(parse_addr(argv[3]), v) ? 0 : 3;
    }

    if ((cmd == "chain" || cmd == "god") && argc >= 4) {
        uintptr_t game = parse_addr(argv[3]), player = 0;
        if (!resolve_player(p, game, player)) { std::fprintf(stderr, "не вдалося прочитати Game::player\n"); return 3; }
        if (cmd == "chain") {
            int32_t hp = 0, armor = 0, ammo = 0;
            p.read_value(player + OFF_HEALTH, hp);
            p.read_value(player + OFF_ARMOR, armor);
            p.read_value(player + OFF_AMMO, ammo);
            std::printf("Player* = 0x%llx  HP=%d armor=%d ammo=%d\n",
                        static_cast<unsigned long long>(player), hp, armor, ammo);
            return 0;
        }
        for (;;) {
            // Адресу гравця перечитуємо щоразу: після перезапуску гри вона зміниться.
            if (!resolve_player(p, game, player)) return 3;
            p.write_value<int32_t>(player + OFF_HEALTH, 999);
            p.write_value<int32_t>(player + OFF_AMMO, 99);
            std::this_thread::sleep_for(std::chrono::milliseconds(50));
        }
    }
    if (cmd == "ac" && argc >= 7) {
        // Загальний режим «ланцюжок з одним вказівником»: [addr] -> player, player+health_off -> health.
        // Далі за розкладкою playerstate: armour +4, ammo[i] = +24 + 4*i (див. лекцію 12).
        uintptr_t slot = parse_addr(argv[3]);
        int ptr_size = std::atoi(argv[4]);
        uintptr_t health_off = parse_addr(argv[5]);
        constexpr uintptr_t AMMO_ASSAULT = 24 + 4 * 6;
        for (;;) {
            uintptr_t player = 0;
            bool ok = ptr_size == 4 ? [&] { uint32_t v = 0; bool r = p.read_value(slot, v); player = v; return r; }()
                                    : p.read_value(slot, player);
            if (!ok || !player) { std::this_thread::sleep_for(std::chrono::milliseconds(200)); continue; }
            p.write_value<int32_t>(player + health_off, 100);
            p.write_value<int32_t>(player + health_off + 4, 100);
            p.write_value<int32_t>(player + health_off + AMMO_ASSAULT, 20);
            std::this_thread::sleep_for(std::chrono::milliseconds(50));
        }
    }
    std::fprintf(stderr, "невідома команда\n");
    return 1;
}
