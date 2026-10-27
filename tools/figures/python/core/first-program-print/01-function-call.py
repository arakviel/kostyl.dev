import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, arrow, box, canvas, save

fig, ax = canvas(10, 3.6)
box(ax, 2, 35, 34, 30, 'print("Hello")', GREY, mono=True, size=15)
ax.text(19, 74, "виклик функції", ha="center", fontsize=12)
box(ax, 56, 62, 42, 26, "Ефект\nтекст Hello з'являється в терміналі", GREEN, size=12)
box(ax, 56, 12, 42, 26, "Результат\nNone (значення немає)", AMBER, size=12)
arrow(ax, 37, 55, 55, 72)
arrow(ax, 37, 45, 55, 28)
save(fig, __file__)
