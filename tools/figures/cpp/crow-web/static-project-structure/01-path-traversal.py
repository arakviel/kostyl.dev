import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.8)
box(ax, 4, 20, 40, 60, "", fc=GREEN)
ax.text(24, 74, "downloads/ (дозволена папка)", ha="center", fontsize=11.5, weight="bold")
ax.text(24, 56, "report.csv\nreadme.txt\ndata.json", ha="center", va="center", fontsize=11, family="DejaVu Sans Mono", linespacing=1.5)
box(ax, 56, 50, 40, 30, "src/main.cpp\n/etc/hosts\n(поза папкою)", fc=RED, mono=True, size=10.5)
ax.text(76, 84, "Не можна віддавати", ha="center", fontsize=11.5, weight="bold")
arrow(ax, 45, 66, 55, 66)
ax.text(50, 72, "../", ha="center", fontsize=12, family="DejaVu Sans Mono")
ax.text(76, 30, "weakly_canonical(downloads / шлях)\nмає починатися з шляху downloads", ha="center", fontsize=10.8, linespacing=1.5)
save(fig, __file__)
