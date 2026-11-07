import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
nodes = [
    (1, 58, 28, "vcpkg.json", "залежності проєкту", BLUE),
    (36, 58, 28, "cmake -B build\n-DCMAKE_TOOLCHAIN_FILE=…", "vcpkg.cmake підхоплюється", GREEN),
    (71, 58, 28, "vcpkg install", "збірка у build/vcpkg_installed", AMBER),
    (71, 14, 28, "find_package(fmt CONFIG)", "знаходить пакет", GREEN),
    (36, 14, 28, "target_link_libraries\n(app PRIVATE fmt::fmt)", "підключає цілі", BLUE),
    (1, 14, 28, "AwesomeApp", "готовий виконуваний файл", GREY),
]
for x, y, w, t, note, color in nodes:
    box(ax, x, y, w, 24, t, fc=color, mono=True, size=10)
    if y > 40:
        ax.text(x + w / 2, y + 27, note, ha="center", va="bottom", fontsize=10.5)
    else:
        ax.text(x + w / 2, y - 3.5, note, ha="center", va="top", fontsize=10.5)
arrow(ax, 29, 70, 36, 70)
arrow(ax, 64, 70, 71, 70)
arrow(ax, 85, 58, 85, 38)
arrow(ax, 71, 26, 64, 26)
arrow(ax, 36, 26, 29, 26)
save(fig, __file__)
