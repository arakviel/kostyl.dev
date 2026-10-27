import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, arrow, box, canvas, save

fig, ax = canvas(10, 3.6)
box(ax, 1, 35, 20, 36, 'Текст\nprint("Hello")', GREY, size=11)
box(ax, 29, 35, 20, 36, "Компіляція\n(CPython)", BLUE, size=12)
box(ax, 57, 35, 20, 36, "Байт-код\n.pyc", AMBER, size=12)
box(ax, 84, 35, 15, 36, "PVM\nвиконує", GREEN, size=12)
arrow(ax, 22, 53, 28, 53)
arrow(ax, 50, 53, 56, 53)
arrow(ax, 78, 53, 83, 53)
ax.text(50, 14, "Python спершу компілює у байт-код, потім віртуальна машина його виконує", ha="center", fontsize=12)
save(fig, __file__)
