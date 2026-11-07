import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
ax.text(24, 98, "Без пакетного менеджера", ha="center", va="top", fontsize=13, weight="bold")
ax.text(76, 98, "З пакетним менеджером", ha="center", va="top", fontsize=13, weight="bold")
manual = ["знайти бібліотеку", "скачати вихідний код", "прочитати інструкцію збірки", "скомпілювати", "прописати шляхи в CMake", "повторити для кожної залежності"]
y = 82
for i, t in enumerate(manual):
    box(ax, 2, y - 4, 44, 11, t, fc=RED, size=11)
    if i < len(manual) - 1:
        arrow(ax, 24, y - 4, 24, y - 7.2)
    y -= 15
box(ax, 56, 62, 40, 16, "vcpkg.json\nперелік залежностей", fc=BLUE, mono=True, size=11)
box(ax, 56, 36, 40, 16, "vcpkg install\nскачує і збирає все", fc=GREEN, size=11)
box(ax, 56, 10, 40, 16, "find_package +\ntarget_link_libraries", fc=AMBER, mono=True, size=11)
arrow(ax, 76, 62, 76, 52)
arrow(ax, 76, 36, 76, 26)
save(fig, __file__)
