import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, arrow, box, canvas, save

chain = [c.__name__ for c in reversed(bool.__mro__)]  # object, int, bool
fig, ax = canvas(10, 3.6)
ax.text(2, 92, "Ієрархія типів", fontsize=14, fontweight="bold")
for i, name in enumerate(chain):
    box(ax, 4 + i * 22, 45, 17, 24, name, [GREY, BLUE, GREEN][i], mono=True, size=14)
    if i:
        arrow(ax, 4 + (i - 1) * 22 + 18, 57, 4 + i * 22 - 1, 57)
ax.text(30, 30, "bool — окремий тип, але він наслідує int:\nTrue == 1, False == 0", ha="center", fontsize=11.5)
box(ax, 72, 45, 25, 24, "NoneType", AMBER, mono=True, size=13)
ax.text(84.5, 30, "None — єдиний об'єкт\nсвого типу", ha="center", fontsize=11.5)
save(fig, __file__)
