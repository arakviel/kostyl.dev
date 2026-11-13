import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 3.4)
fields = [("name[16]", "+0", 0, 30, GREY), ("health", "+16", 30, 14, RED), ("armor", "+20", 44, 14, BLUE),
          ("x", "+24", 58, 10, GREY), ("y", "+28", 68, 10, GREY), ("weapon.ammo", "+32", 78, 22, GREEN)]
for name, off, x, w, c in fields:
    box(ax, x + 0.5, 35, w - 1.2, 30, name, c, mono=True, size=10)
    ax.text(x + 0.5, 22, off, fontsize=11, fontfamily="DejaVu Sans Mono")
ax.text(0, 85, "Player* = 0x...a70  →  адреса поля = Player* + зміщення", fontsize=13)
save(fig, __file__)
