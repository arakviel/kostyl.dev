import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
ax.text(25, 94, "Погано: дія в URL", ha="center", fontsize=12.5, weight="bold")
ax.text(75, 94, "Добре: ресурс + метод", ha="center", fontsize=12.5, weight="bold")
bad = ["GET /getUser?id=2", "POST /createUser", "POST /deleteUser/2", "GET /users/2/delete"]
good = ["GET /users/2", "POST /users", "DELETE /users/2", "GET /users/2/orders"]
y = 80
for b, g in zip(bad, good):
    box(ax, 2, y - 6, 46, 13, b, fc=RED, mono=True, size=11)
    box(ax, 52, y - 6, 46, 13, g, fc=GREEN, mono=True, size=11)
    y -= 19
ax.text(50, 3, "URL — іменник у множині, дію задає метод HTTP", ha="center", fontsize=12)
save(fig, __file__)
