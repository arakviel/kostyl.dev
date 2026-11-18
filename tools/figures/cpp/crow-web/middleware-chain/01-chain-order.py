import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
names = [("First", BLUE), ("Timer", GREEN), ("Gate", AMBER)]
ax.text(1, 94, "Запит", fontsize=12.5, weight="bold"); ax.text(99, 94, "Відповідь", fontsize=12.5, weight="bold", ha="right")
for i, (n, c) in enumerate(names):
    x = 8 + i * 22
    box(ax, x, 40, 18, 30, n, fc=c, weight="bold", size=12.5)
    ax.text(x + 9, 76, "before_handle", ha="center", fontsize=10, family="DejaVu Sans Mono")
    ax.text(x + 9, 30, "after_handle", ha="center", fontsize=10, family="DejaVu Sans Mono")
    arrow(ax, x + 19, 58, x + 21.5, 58)
    arrow(ax, x + 21.5, 46, x + 19, 46)
box(ax, 76, 40, 21, 30, "Обробник\nмаршруту", fc=GREY, weight="bold", size=12)
arrow(ax, 1, 58, 7, 58)
arrow(ax, 7, 46, 1, 46)
ax.text(50, 10, "before виконується за порядком реєстрації, after — у зворотному", ha="center", fontsize=12)
save(fig, __file__)
