import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.4)
ax.text(25, 95, "Конкатенація (небезпечно)", ha="center", fontsize=12.5, weight="bold")
box(ax, 2, 62, 46, 22, "\"... WHERE email = '\" + email + \"'\"", fc=RED, mono=True, size=9.5)
ax.text(25, 52, "email = x' OR '1'='1", ha="center", fontsize=10.5, family="DejaVu Sans Mono")
box(ax, 2, 20, 46, 24, "WHERE email = 'x' OR '1'='1'\nумова завжди істинна:\nповернуто 2 рядки з 2", fc=RED, mono=False, size=10.5)
arrow(ax, 25, 49, 25, 45)
ax.text(75, 95, "Підготовлений запит", ha="center", fontsize=12.5, weight="bold")
box(ax, 52, 62, 46, 22, "\"... WHERE email = ?\"\nbind(1, email)", fc=GREEN, mono=True, size=9.5)
ax.text(75, 52, "email = x' OR '1'='1", ha="center", fontsize=10.5, family="DejaVu Sans Mono")
box(ax, 52, 20, 46, 24, "значення — лише дані:\nшукається email з такими\nсимволами; знайдено 0", fc=GREEN, mono=False, size=10.5)
arrow(ax, 75, 49, 75, 45)
save(fig, __file__)
