#if defined(__linux__)
#include "process.hpp"
#include <cstdio>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <sys/uio.h>

Process::Process(int pid) : pid_(pid) {
    // Для process_vm_readv/writev потрібні ті самі права, що й для ptrace
    // (той самий користувач і kernel.yama.ptrace_scope=0, або root).
    ok_ = true;
}

Process::~Process() = default;

bool Process::read(uintptr_t addr, void* out, size_t n) const {
    iovec local{out, n};
    iovec remote{reinterpret_cast<void*>(addr), n};
    return process_vm_readv(pid_, &local, 1, &remote, 1, 0) == static_cast<ssize_t>(n);
}

bool Process::write(uintptr_t addr, const void* data, size_t n) const {
    iovec local{const_cast<void*>(data), n};
    iovec remote{reinterpret_cast<void*>(addr), n};
    return process_vm_writev(pid_, &local, 1, &remote, 1, 0) == static_cast<ssize_t>(n);
}

std::vector<Region> Process::writable_regions() const {
    std::vector<Region> out;
    std::ifstream maps("/proc/" + std::to_string(pid_) + "/maps");
    std::string line;
    while (std::getline(maps, line)) {
        unsigned long long a = 0, b = 0;
        char perms[8] = {};
        if (std::sscanf(line.c_str(), "%llx-%llx %7s", &a, &b, perms) != 3) continue;
        if (perms[0] == 'r' && perms[1] == 'w')
            out.push_back({static_cast<uintptr_t>(a), static_cast<size_t>(b - a)});
    }
    return out;
}
#endif
