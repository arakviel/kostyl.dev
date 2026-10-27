import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, arrow, box, canvas, save

fig, ax = canvas(10, 3.4)
ax.text(2, 92, "У коді (2 знаки)", fontsize=13, fontweight="bold")
box(ax, 4, 55, 12, 25, "\\", BLUE, mono=True, size=20)
box(ax, 18, 55, 12, 25, "n", BLUE, mono=True, size=20)
ax.text(17, 44, '"\\n"', ha="center", fontsize=13, fontfamily="DejaVu Sans Mono")
arrow(ax, 33, 67, 54, 67, "один знак", size=11)
ax.text(58, 92, "У рядку (1 символ)", fontsize=13, fontweight="bold")
box(ax, 58, 55, 38, 25, "новий рядок", GREEN, size=13)
ax.text(77, 44, 'len("\\n") == 1', ha="center", fontsize=13, fontfamily="DejaVu Sans Mono")
ax.text(50, 14, 'У коді \\n займає два знаки, а в пам\'яті рядок містить один символ.', ha="center", fontsize=12)
save(fig, __file__)
