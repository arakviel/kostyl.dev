import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.8)
box(ax, 2, 30, 20, 42, "Браузер\nабо curl\n(клієнт)", fc=BLUE, weight="bold")
box(ax, 40, 30, 22, 42, "Веб-сервер\n(Crow)", fc=GREEN, weight="bold")
box(ax, 80, 30, 18, 42, "Дані\n(файл, БД)", fc=AMBER, weight="bold")
arrow(ax, 23, 62, 39, 62, "запит")
ax.text(31, 74, "GET /users HTTP/1.1", ha="center", fontsize=10.5, family="DejaVu Sans Mono")
arrow(ax, 39, 40, 23, 40)
ax.text(31, 28, "200 OK + JSON", ha="center", fontsize=10.5, family="DejaVu Sans Mono")
arrow(ax, 63, 56, 79, 56)
arrow(ax, 79, 44, 63, 44)
ax.text(71, 62, "читання", ha="center", fontsize=11)
ax.text(50, 8, "Клієнт завжди починає першим. Сервер лише відповідає на запити.", ha="center", fontsize=12)
save(fig, __file__)
