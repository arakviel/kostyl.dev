#pragma once
// Кросплатформна обгортка над доступом до пам'яті чужого процесу.
#include <cstddef>
#include <cstdint>
#include <vector>

struct Region {
    uintptr_t start;
    size_t size;
};

class Process {
public:
    explicit Process(int pid);
    ~Process();
    Process(const Process&) = delete;
    Process& operator=(const Process&) = delete;

    bool ok() const { return ok_; }
    bool read(uintptr_t addr, void* out, size_t n) const;
    bool write(uintptr_t addr, const void* data, size_t n) const;
    // Усі області пам'яті, доступні для читання і запису.
    std::vector<Region> writable_regions() const;

    template <class T>
    bool read_value(uintptr_t addr, T& out) const { return read(addr, &out, sizeof(T)); }
    template <class T>
    bool write_value(uintptr_t addr, const T& v) const { return write(addr, &v, sizeof(T)); }

private:
    int pid_;
    bool ok_ = false;
#if defined(_WIN32)
    void* handle_ = nullptr;
#elif defined(__APPLE__)
    unsigned int task_ = 0;
#endif
};
