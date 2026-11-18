import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.4)
items = [(1, "vcpkg.json", "перелік залежностей:\ncrow", AMBER), (26, "CMakeLists.txt", "find_package(Crow)\ntarget_link_libraries", BLUE), (51, "cmake --build", "компіляція main.cpp\nі лінкування", GREEN), (76, "./hello_crow", "сервер слухає\nпорт 8080", GREY)]
for x, t, n, c in items:
    box(ax, x, 30, 22, 52, "", fc=c)
    ax.text(x + 11, 74, t, ha="center", fontsize=11.5, weight="bold", family="DejaVu Sans Mono")
    ax.text(x + 11, 50, n, ha="center", va="center", fontsize=11, linespacing=1.4)
for x in (23.5, 48.5, 73.5):
    arrow(ax, x, 56, x + 2.5, 56)
ax.text(50, 12, "vcpkg завантажує Crow при конфігурації, CMake підключає його до цілі", ha="center", fontsize=12)
save(fig, __file__)
