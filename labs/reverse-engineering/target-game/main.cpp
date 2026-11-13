// Навчальна гра-мішень для курсу з реверс-інжинірингу.
// Збірка: cmake -S . -B build && cmake --build build
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>
#ifdef _WIN32
#include <process.h>
#else
#include <unistd.h>
#endif

struct Weapon {
    int32_t ammo;
    int32_t magazine;
    float damage;
};

struct Player {
    char name[16];
    int32_t health;
    int32_t armor;
    float x;
    float y;
    Weapon weapon;
};

struct Game {
    int32_t score;
    Player* player; // вказівник: додатковий рівень непрямого доступу
};

#include <cstddef>
static_assert(offsetof(Player, health) == 16 && offsetof(Player, armor) == 20 &&
              offsetof(Player, weapon) == 32 && offsetof(Game, player) == 8,
              "зміщення полів використовуються в тренері і в уроках");

static bool g_show_addr = false;

static void print_state(const Game& g) {
    const Player& p = *g.player;
    std::printf("\n[%s] HP=%d  armor=%d  ammo=%d/%d  score=%d  pos=(%.1f, %.1f)\n",
                p.name, p.health, p.armor, p.weapon.ammo, p.weapon.magazine,
                g.score, p.x, p.y);
    if (g_show_addr) {
        std::printf("   Game*   = %p\n   Player* = %p\n", static_cast<const void*>(&g),
                    static_cast<const void*>(g.player));
    }
}

int main(int argc, char** argv) {
    g_show_addr = argc > 1 && std::strcmp(argv[1], "--show-addr") == 0;
    Game* game = new Game{};
    game->player = new Player{};
    std::strncpy(game->player->name, "Hero", sizeof(game->player->name) - 1);
    game->player->health = 100;
    game->player->armor = 50;
    game->player->x = 10.0f;
    game->player->y = 20.0f;
    game->player->weapon = {30, 30, 25.0f};

    std::printf("PID: %d\n", static_cast<int>(
#ifdef _WIN32
        _getpid()
#else
        ::getpid()
#endif
    ));
    std::puts("Команди: s = стрілити, d = отримати удар, h = лікування, m = рух, q = вихід");

    std::string cmd;
    for (;;) {
        print_state(*game);
        std::printf("> ");
        if (!(std::cin >> cmd) || cmd == "q") break;
        Player& p = *game->player;
        if (cmd == "s" && p.weapon.ammo > 0) { --p.weapon.ammo; game->score += 10; }
        else if (cmd == "d") { p.health -= 15; if (p.health < 0) { p.health = 0; std::puts("Ви загинули!"); } }
        else if (cmd == "h") { p.health += 10; if (p.health > 100) p.health = 100; }
        else if (cmd == "m") { p.x += 1.5f; p.y -= 0.5f; }
    }
    delete game->player;
    delete game;
}
