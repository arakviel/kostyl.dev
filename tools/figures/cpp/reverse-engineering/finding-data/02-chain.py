import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 3.4)
box(ax, 0, 30, 20, 40, "Статична\nадреса\nGame*", AMBER, mono=True, size=11)
box(ax, 32, 30, 24, 40, "Game\n+8: player", BLUE, mono=True, size=11)
box(ax, 68, 30, 32, 40, "Player\n+16: health\n+32: ammo", GREEN, mono=True, size=11)
arrow(ax, 21, 50, 31, 50)
arrow(ax, 57, 50, 67, 50, "читаємо\nPlayer*")
ax.text(26, 78, "база", ha="center", fontsize=11)
ax.text(44, 18, "кожна гра: нова адреса Player", ha="center", fontsize=11)
save(fig, __file__)
