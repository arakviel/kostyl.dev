import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.6)
steps = [
    (1, "1. Конфігурація", "cmake -S . -B build", "читає CMakeLists.txt,\nгенерує Makefile / .sln", BLUE),
    (35, "2. Збірка", "cmake --build build", "компілює .cpp,\nлінкує виконуваний файл", GREEN),
    (69, "3. Запуск", "./build/HelloCMake", "Привіт, CMake!", AMBER),
]
for x, title, cmd, note, color in steps:
    box(ax, x, 40, 30, 52, "", fc=color)
    ax.text(x + 15, 85, title, ha="center", va="top", fontsize=13, weight="bold")
    ax.text(x + 15, 66, cmd, ha="center", va="center", fontsize=10.5, family="DejaVu Sans Mono")
    ax.text(x + 15, 48, note, ha="center", va="center", fontsize=11, linespacing=1.4)
arrow(ax, 31, 66, 35, 66)
arrow(ax, 65, 66, 69, 66)
ax.text(50, 20, "Вихідний код лишається чистим: усе згенероване потрапляє в окрему папку build/", ha="center", va="center", fontsize=12)
save(fig, __file__)
