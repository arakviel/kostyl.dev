import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, arrow, box, canvas, save

fig, ax = canvas(10, 3.6)
box(ax, 1, 40, 17, 30, "Диск\nhello.py", GREY, size=12)
box(ax, 24, 40, 17, 30, "RAM\nкод і дані", BLUE, size=12)
box(ax, 47, 40, 17, 30, "Компілятор\nCPython", AMBER, size=12)
box(ax, 70, 40, 12, 30, "PVM", GREEN, size=12)
box(ax, 88, 40, 11, 30, "CPU", GREEN, size=12)
for a, b in [(19, 23), (42, 46), (65, 69), (83, 87)]:
    arrow(ax, a, 55, b, 55)
ax.text(50, 18, "Усе в пам'яті — числа  ·  Python компілює в байт-код  ·  PVM виконує команди", ha="center", fontsize=12)
save(fig, __file__)
