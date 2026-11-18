import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
ax.text(25, 95, "Дані в cookie", ha="center", fontsize=12.5, weight="bold")
box(ax, 4, 52, 42, 30, "visits=3\nдані зберігає клієнт", fc=RED, mono=True, size=10.5)
ax.text(25, 38, "Клієнт може змінити:\nvisits=999 → «Візитів: 1000»", ha="center", va="center", fontsize=11, linespacing=1.4)
ax.text(75, 95, "Серверна сесія", ha="center", fontsize=12.5, weight="bold")
box(ax, 54, 62, 42, 20, "cookie: sid=e584…ff84\n(випадковий ключ)", fc=AMBER, mono=True, size=10)
box(ax, 54, 22, 42, 28, "сервер: sid → {user_id: 1,\nusername: ivan}", fc=GREEN, mono=True, size=10)
arrow(ax, 75, 61, 75, 51)
ax.text(75, 10, "Підробити можна лише вгадавши\n256-бітний ключ", ha="center", va="center", fontsize=11, linespacing=1.4)
save(fig, __file__)
