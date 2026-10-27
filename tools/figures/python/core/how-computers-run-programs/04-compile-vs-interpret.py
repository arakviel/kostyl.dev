import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import BLUE, GREEN, GREY, arrow, box, canvas, save

fig, ax = canvas(10, 4.6)
ax.text(2, 93, "Компіляція", fontsize=14, fontweight="bold")
box(ax, 2, 62, 20, 22, "program.c", GREY, mono=True)
box(ax, 30, 62, 22, 22, "Компілятор\n(один раз)", BLUE)
box(ax, 60, 62, 20, 22, "program.exe", GREY, mono=True)
box(ax, 88, 62, 10, 22, "CPU", GREEN)
arrow(ax, 23, 73, 29, 73)
arrow(ax, 53, 73, 59, 73)
arrow(ax, 81, 73, 87, 73)
ax.text(2, 45, "Інтерпретація", fontsize=14, fontweight="bold")
box(ax, 2, 12, 20, 22, "program.py", GREY, mono=True)
box(ax, 30, 12, 32, 22, "Інтерпретатор\n(при кожному запуску)", BLUE)
box(ax, 88, 12, 10, 22, "CPU", GREEN)
arrow(ax, 23, 23, 29, 23)
arrow(ax, 63, 23, 87, 23)
save(fig, __file__)
