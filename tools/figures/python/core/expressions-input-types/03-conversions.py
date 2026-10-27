import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, arrow, box, canvas, save

fig, ax = canvas(11, 3.8)
box(ax, 2, 40, 22, 28, '"42"\nstr', AMBER, mono=True, size=14)
box(ax, 39, 40, 22, 28, "42\nint", BLUE, mono=True, size=14)
box(ax, 76, 40, 22, 28, "42.0\nfloat", GREEN, mono=True, size=14)
arrow(ax, 25, 60, 38, 60, "int()", size=12)
arrow(ax, 38, 48, 25, 48, "str()", size=12)
arrow(ax, 62, 60, 75, 60, "float()", size=12)
arrow(ax, 75, 48, 62, 48, "int()", size=12)
ax.text(50, 16, 'int("3.5") — помилка ValueError;  int(3.9) = 3 (дробова частина відкидається)', ha="center", fontsize=11.5)
ax.text(50, 4, "Кожне перетворення створює новий об'єкт, а старий лишається без змін.", ha="center", fontsize=11.5)
save(fig, __file__)
