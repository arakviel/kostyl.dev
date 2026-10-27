import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, arrow, box, canvas, save

fig, ax = canvas(11, 4.2)
ax.text(2, 94, "0 and f()", fontsize=14, fontfamily="DejaVu Sans Mono", fontweight="bold")
box(ax, 2, 58, 14, 22, "0", AMBER, mono=True, size=15)
ax.text(9, 50, "хибне", ha="center", fontsize=11)
arrow(ax, 17, 69, 36, 69, "стоп", size=11)
box(ax, 37, 58, 22, 22, "результат: 0", GREEN, mono=True, size=13)
box(ax, 68, 58, 28, 22, "f() не викликається", GREY, mono=True, size=12)
ax.text(2, 36, "1 and f()", fontsize=14, fontfamily="DejaVu Sans Mono", fontweight="bold")
box(ax, 2, 4, 14, 22, "1", AMBER, mono=True, size=15)
ax.text(9, -3, "істинне", ha="center", fontsize=11)
arrow(ax, 17, 15, 36, 15, "далі", size=11)
box(ax, 37, 4, 22, 22, "f()", BLUE, mono=True, size=15)
arrow(ax, 60, 15, 67, 15)
box(ax, 68, 4, 28, 22, "результат: f()", GREEN, mono=True, size=13)
save(fig, __file__)
