#if defined(_WIN32)
#include "process.hpp"
#include <windows.h>
#include <cstdio>

Process::Process(int pid) : pid_(pid) {
    handle_ = OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION |
                              PROCESS_QUERY_INFORMATION,
                          FALSE, static_cast<DWORD>(pid));
    if (!handle_) {
        std::fprintf(stderr, "OpenProcess не вдався, код %lu\n", GetLastError());
        return;
    }
    ok_ = true;
}

Process::~Process() {
    if (handle_) CloseHandle(handle_);
}

bool Process::read(uintptr_t addr, void* out, size_t n) const {
    SIZE_T got = 0;
    return ReadProcessMemory(handle_, reinterpret_cast<LPCVOID>(addr), out, n, &got) && got == n;
}

bool Process::write(uintptr_t addr, const void* data, size_t n) const {
    DWORD old = 0;
    VirtualProtectEx(handle_, reinterpret_cast<LPVOID>(addr), n, PAGE_EXECUTE_READWRITE, &old);
    SIZE_T put = 0;
    bool r = WriteProcessMemory(handle_, reinterpret_cast<LPVOID>(addr), data, n, &put) && put == n;
    VirtualProtectEx(handle_, reinterpret_cast<LPVOID>(addr), n, old, &old);
    return r;
}

std::vector<Region> Process::writable_regions() const {
    std::vector<Region> out;
    MEMORY_BASIC_INFORMATION mbi;
    uintptr_t addr = 0;
    while (VirtualQueryEx(handle_, reinterpret_cast<LPCVOID>(addr), &mbi, sizeof(mbi)) == sizeof(mbi)) {
        bool rw = (mbi.State == MEM_COMMIT) && !(mbi.Protect & (PAGE_GUARD | PAGE_NOACCESS)) &&
                  (mbi.Protect & (PAGE_READWRITE | PAGE_EXECUTE_READWRITE));
        if (rw) out.push_back({reinterpret_cast<uintptr_t>(mbi.BaseAddress), mbi.RegionSize});
        addr = reinterpret_cast<uintptr_t>(mbi.BaseAddress) + mbi.RegionSize;
    }
    return out;
}
#endif
