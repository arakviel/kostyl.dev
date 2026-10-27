import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, box, canvas, save

items = [42, 3.14, "Привіт", True, None]
colors = [BLUE, GREEN, AMBER, GREY, RED]
fig, ax = canvas(10, 3.2)
ax.text(50, 92, "Літерал у коді → тип об'єкта", ha="center", fontsize=14, fontweight="bold")
w, gap = 17, 2.8
for i, (v, c) in enumerate(zip(items, colors)):
    x = 2 + i * (w + gap)
    box(ax, x, 45, w, 25, repr(v), c, mono=True, size=13)
    ax.text(x + w / 2, 30, type(v).__name__, ha="center", fontsize=14, fontfamily="DejaVu Sans Mono", fontweight="bold")
ax.text(50, 8, "type(літерал) повертає назву типу", ha="center", fontsize=11.5)
save(fig, __file__)
