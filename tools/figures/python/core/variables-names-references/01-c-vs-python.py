import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, arrow, box, canvas, save

fig, ax = canvas(11, 3.8)
ax.plot([50, 50], [8, 88], color=GREY, lw=2)
ax.text(25, 92, "Мова C: змінна — комірка", ha="center", fontsize=13, fontweight="bold")
box(ax, 8, 40, 34, 28, "x\n5", AMBER, mono=True, size=16)
ax.text(25, 28, "значення лежить у самій змінній", ha="center", fontsize=11)
ax.text(25, 14, "x = 7 → у комірці стало 7", ha="center", fontsize=11, fontfamily="DejaVu Sans Mono")
ax.text(75, 92, "Python: ім'я вказує на об'єкт", ha="center", fontsize=13, fontweight="bold")
box(ax, 56, 44, 12, 22, "x", BLUE, mono=True, size=16)
box(ax, 80, 40, 17, 30, "int\n5", GREEN, mono=True, size=14)
arrow(ax, 69, 55, 79, 55)
ax.text(75, 28, "ім'я — стрілка, значення — в об'єкті", ha="center", fontsize=11)
ax.text(75, 14, "x = 7 → стрілка перейшла на інший об'єкт", ha="center", fontsize=11, fontfamily="DejaVu Sans Mono")
save(fig, __file__)
