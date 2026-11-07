import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
box(ax, 1, 38, 20, 24, "main.cpp\nmath_utils.cpp\nstring_utils.cpp", fc=GREY, mono=True, size=11)
rows = [
    (74, "Windows · MSVC", "cl /EHsc main.cpp ... /Fe:myapp.exe", BLUE),
    (40, "Linux · GCC", "g++ main.cpp ... -o myapp", GREEN),
    (6, "macOS · Clang", "clang++ main.cpp ... -o myapp", AMBER),
]
for y, name, cmd, color in rows:
    box(ax, 30, y, 17, 20, name, fc=color, size=11)
    box(ax, 50, y, 49, 20, cmd, fc="white", mono=True, size=10.5)
    arrow(ax, 21, 50, 30, y + 10)
ax.text(50, 98, "Три платформи — три різні команди, які треба підтримувати вручну", ha="center", va="top", fontsize=12.5, weight="bold")
save(fig, __file__)
