import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
ax.text(25, 95, "Етап 1: обробники знають файл", ha="center", fontsize=12.5, weight="bold")
for i, n in enumerate(["GET /users", "POST /users", "GET /users/<id>"]):
    box(ax, 2, 70 - i * 22, 26, 16, n, fc=BLUE, mono=True, size=10)
    arrow(ax, 29, 78 - i * 22, 38, 50 - 0)
box(ax, 38, 38, 12, 24, "users\n.json", fc=AMBER, mono=True, size=10.5)
ax.text(75, 95, "Етап 3: обробники знають лише DAO", ha="center", fontsize=12.5, weight="bold")
for i, n in enumerate(["GET /users", "POST /users", "GET /users/<id>"]):
    box(ax, 54, 70 - i * 22, 20, 16, n, fc=BLUE, mono=True, size=9.5)
    arrow(ax, 75, 78 - i * 22, 80, 54)
box(ax, 80, 38, 18, 24, "UserDao\n→ users.json", fc=GREEN, mono=True, size=10)
save(fig, __file__)
