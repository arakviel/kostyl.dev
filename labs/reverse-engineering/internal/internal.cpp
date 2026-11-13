// Internal-модуль: завантажується всередину процесу гри.
//   Linux:  LD_PRELOAD=./build/libinternal.so ../target-game/build/target_game
//   macOS:  DYLD_INSERT_LIBRARIES=./build/libinternal.dylib ../target-game/build/target_game
//   Windows: LoadLibrary з окремого інжектора (див. лекцію 11), DllMain викликає start().
#include "../trainer/process.hpp"
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <thread>
#ifdef _WIN32
#include <windows.h>
#include <process.h>
#else
#include <unistd.h>
#endif

// Шукаємо структуру Player за сигнатурою: ім'я "Hero", HP=100, броня=50.
static uintptr_t find_player(const Process& self) {
    std::vector<uint8_t> buf;
    for (const Region& r : self.writable_regions()) {
        buf.resize(r.size);
        if (!self.read(r.start, buf.data(), r.size)) continue;
        for (size_t i = 0; i + 36 <= r.size; i += 16) {
            if (std::memcmp(&buf[i], "Hero\0", 5) != 0) continue;
            int32_t hp, armor;
            std::memcpy(&hp, &buf[i + 16], 4);
            std::memcpy(&armor, &buf[i + 20], 4);
            if (hp == 100 && armor == 50) return r.start + i;
        }
    }
    return 0;
}

static void worker() {
#ifdef _WIN32
    Process self(static_cast<int>(_getpid()));
#else
    Process self(static_cast<int>(::getpid()));
#endif
    if (!self.ok()) return;
    std::this_thread::sleep_for(std::chrono::milliseconds(500)); // дати грі створити гравця
    uintptr_t player = find_player(self);
    if (!player) { std::fprintf(stderr, "[internal] гравця не знайдено\n"); return; }
    std::fprintf(stderr, "[internal] Player знайдено: %p\n", reinterpret_cast<void*>(player));
    for (;;) {
        // Усередині процесу можна було б писати через вказівник напряму; використовуємо Process для спільності.
        self.write_value<int32_t>(player + 16, 999);
        self.write_value<int32_t>(player + 32, 99);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
}

static void start() { std::thread(worker).detach(); }

#ifdef _WIN32
BOOL APIENTRY DllMain(HMODULE, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) start();
    return TRUE;
}
#else
__attribute__((constructor)) static void on_load() { start(); }
#endif
