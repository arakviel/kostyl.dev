#if defined(__APPLE__)
#include "process.hpp"
#include <mach/mach.h>
#include <mach/mach_vm.h>
#include <cstdio>

Process::Process(int pid) : pid_(pid) {
    mach_port_t task = MACH_PORT_NULL;
    kern_return_t kr = task_for_pid(mach_task_self(), pid, &task);
    if (kr != KERN_SUCCESS) {
        std::fprintf(stderr, "task_for_pid не вдався: %s (запускайте через sudo)\n",
                     mach_error_string(kr));
        return;
    }
    task_ = task;
    ok_ = true;
}

Process::~Process() {
    if (ok_) mach_port_deallocate(mach_task_self(), task_);
}

bool Process::read(uintptr_t addr, void* out, size_t n) const {
    mach_vm_size_t got = 0;
    kern_return_t kr = mach_vm_read_overwrite(task_, addr, n, reinterpret_cast<mach_vm_address_t>(out), &got);
    return kr == KERN_SUCCESS && got == n;
}

bool Process::write(uintptr_t addr, const void* data, size_t n) const {
    // Сторінки коду/даних можуть бути лише для читання, тому тимчасово додаємо право запису.
    mach_vm_protect(task_, addr, n, FALSE, VM_PROT_READ | VM_PROT_WRITE | VM_PROT_COPY);
    return mach_vm_write(task_, addr, reinterpret_cast<vm_offset_t>(data), static_cast<mach_msg_type_number_t>(n)) == KERN_SUCCESS;
}

std::vector<Region> Process::writable_regions() const {
    std::vector<Region> out;
    mach_vm_address_t addr = 0;
    for (;;) {
        mach_vm_size_t size = 0;
        vm_region_basic_info_data_64_t info;
        mach_msg_type_number_t count = VM_REGION_BASIC_INFO_COUNT_64;
        mach_port_t object;
        if (mach_vm_region(task_, &addr, &size, VM_REGION_BASIC_INFO_64,
                           reinterpret_cast<vm_region_info_t>(&info), &count, &object) != KERN_SUCCESS)
            break;
        if ((info.protection & VM_PROT_READ) && (info.protection & VM_PROT_WRITE))
            out.push_back({static_cast<uintptr_t>(addr), static_cast<size_t>(size)});
        addr += size;
    }
    return out;
}
#endif
