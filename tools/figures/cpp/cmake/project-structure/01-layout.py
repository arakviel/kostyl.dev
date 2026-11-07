import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 6.6)
ax.text(1, 99, "MyProject/", fontsize=14, weight="bold", family="DejaVu Sans Mono", va="top")
items = [
    ("CMakeLists.txt", "головний файл збірки", BLUE),
    ("include/myproject/", "публічні заголовки", GREEN),
    ("src/", "main.cpp та реалізація", GREEN),
    ("libs/", "внутрішні бібліотеки (кожна зі своїм CMakeLists.txt)", GREEN),
    ("external/", "сторонні залежності", AMBER),
    ("cmake/", "власні модулі .cmake", BLUE),
    ("tests/", "тести + CMakeLists.txt", GREY),
    ("examples/", "приклади використання", GREY),
    ("docs/ · scripts/", "документація та скрипти", GREY),
    ("build/", "результат збірки, не потрапляє в git", RED),
]
step = 8.6
top = 84
for i, (name, note, color) in enumerate(items):
    yc = top - i * step
    box(ax, 6, yc - 3.4, 30, 7.4, name, fc=color, mono=True, size=11)
    ax.text(39, yc + 0.3, note, va="center", fontsize=11.5)
    ax.plot([2.5, 6], [yc + 0.3, yc + 0.3], color=INK, lw=1.4)
ax.plot([2.5, 2.5], [93, top - (len(items) - 1) * step + 0.3], color=INK, lw=1.4)
save(fig, __file__)
