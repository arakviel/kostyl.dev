"""Дерево розбору a + b * c > d && !done: групування за пріоритетом і порядок обчислення операндів зліва направо."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Circle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(14, 8)

# вузли: ключ -> (x, y, текст, колір, значення)
NODES = {
    "and": (50, 84, "&&", AMBER, "true"),
    "gt": (30, 64, ">", BLUE, "true"),
    "not": (72, 64, "!", BLUE, "true"),
    "plus": (18, 44, "+", GREEN, "7"),
    "d": (42, 44, "d", GREY, "5"),
    "done": (72, 44, "done", GREY, "false"),
    "a": (8, 24, "a", GREY, "1"),
    "mul": (28, 24, "*", GREEN, "6"),
    "b": (20, 6, "b", GREY, "2"),
    "c": (36, 6, "c", GREY, "3"),
}
EDGES = [("and", "gt"), ("and", "not"), ("gt", "plus"), ("gt", "d"), ("not", "done"), ("plus", "a"),
         ("plus", "mul"), ("mul", "b"), ("mul", "c")]
ORDER = {"a": 1, "b": 2, "c": 3, "d": 4, "done": 5}

for p, c in EDGES:
    x1, y1 = NODES[p][:2]
    x2, y2 = NODES[c][:2]
    ax.plot([x1, x2], [y1 - 3.5, y2 + 3.5], color=INK, lw=1.3, zorder=1)
for key, (x, y, text, color, value) in NODES.items():
    w = max(7, len(text) * 2.2 + 3)
    box(ax, x - w / 2, y - 3.5, w, 7, text, fc=color, mono=True, size=15, weight="bold")
    ax.text(x + w / 2 + 1, y + 2.5, value, fontsize=11, color="#1D4ED8", fontfamily="DejaVu Sans Mono")
    if key in ORDER:
        ax.add_patch(Circle((x - w / 2 - 2.2, y + 3.2), 1.8, fc="#DC2626", ec="none", zorder=3))
        ax.text(x - w / 2 - 2.2, y + 3.2, str(ORDER[key]), ha="center", va="center", fontsize=10, color="white",
                fontweight="bold", zorder=4)

ax.text(88, 88, "a = 1, b = 2, c = 3,", fontsize=12, fontfamily="DejaVu Sans Mono", ha="center")
ax.text(88, 83, "d = 5, done = false", fontsize=12, fontfamily="DejaVu Sans Mono", ha="center")
ax.text(88, 70, "нижче у дереві —\nвищий пріоритет:\n* раніше за +,\n+ раніше за >,\n> раніше за &&",
        fontsize=12, ha="center", va="top", color=MUTED, linespacing=1.4)
ax.text(88, 34, "червоні номери —\nпорядок обчислення\nоперандів: завжди\nзліва направо", fontsize=12,
        ha="center", va="top", color="#DC2626", linespacing=1.4)
ax.text(88, 10, "сині числа — значення\nкожного вузла", fontsize=12, ha="center", va="center", color="#1D4ED8",
        linespacing=1.4)
save(fig, __file__)
