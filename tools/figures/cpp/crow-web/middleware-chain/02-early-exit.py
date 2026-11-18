import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.8)
for i, (n, c) in enumerate([("First", BLUE), ("Timer", GREEN), ("Gate", AMBER)]):
    box(ax, 4 + i * 22, 50, 18, 28, n, fc=c, weight="bold", size=12.5)
    if i < 2: arrow(ax, 22.5 + i * 22, 64, 25.5 + i * 22, 64)
box(ax, 76, 50, 21, 28, "Обробник\n(не викликається)", fc=GREY, size=11)
ax.plot([68, 75], [64, 64], color=INK, lw=1.6, linestyle=":")
ax.text(72, 70, "✕", ha="center", fontsize=16, color="#DC2626")
box(ax, 48, 12, 30, 20, "Gate: res.code = 403\nres.end()", fc=RED, mono=True, size=10.5)
arrow(ax, 57, 49, 57, 33)
ax.text(30, 22, "after_handle усіх трьох\nвсе одно виконуються", ha="center", va="center", fontsize=11)
save(fig, __file__)
