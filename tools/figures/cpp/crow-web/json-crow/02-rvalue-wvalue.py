import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.6)
box(ax, 1, 30, 20, 40, "Текст JSON\nу req.body", fc=AMBER, size=11.5)
box(ax, 28, 30, 20, 40, "crow::json::\nrvalue\n(лише читання)", fc=BLUE, size=11, mono=True)
box(ax, 55, 30, 20, 40, "Значення C++\nі логіка\nобробника", fc=GREEN, size=11.5)
box(ax, 80, 30, 19, 40, "crow::json::\nwvalue\n(створення)", fc=BLUE, size=11, mono=True)
arrow(ax, 22, 50, 27, 50); arrow(ax, 49, 50, 54, 50); arrow(ax, 76, 50, 79, 50)
ax.text(24.5, 56, "load", ha="center", fontsize=10.5); 
ax.text(51.5, 56, "читання", ha="center", fontsize=10.5); ax.text(50, 20, "", ha="center")
ax.text(50, 8, "wvalue перетворюється на текст у конструкторі crow::response", ha="center", fontsize=12)
save(fig, __file__)
