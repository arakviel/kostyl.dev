import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, arrow, box, canvas, save

fig, ax = canvas(11, 3.8)
states = [
    ("a = [1, 2]", ["a"], "1 стрілка", GREEN),
    ("b = a", ["a", "b"], "2 стрілки", GREEN),
    ("a = 0; b = 0", [], "0 стрілок", RED),
]
for i, (code, names, label, color) in enumerate(states):
    x0 = 2 + i * 32
    ax.text(x0 + 14, 92, code, ha="center", fontsize=12, fontfamily="DejaVu Sans Mono", fontweight="bold")
    box(ax, x0 + 15, 42, 14, 24, "[1, 2]", color, mono=True, size=12)
    for j, n in enumerate(names):
        y = 66 - j * 24 if len(names) > 1 else 54
        box(ax, x0, y - 8, 7, 16, n, BLUE, mono=True, size=13)
        arrow(ax, x0 + 8, y, x0 + 14, 54)
    ax.text(x0 + 22, 28, label, ha="center", fontsize=12)
ax.text(50, 10, "Об'єкт без жодної стрілки Python видаляє з пам'яті", ha="center", fontsize=11)
save(fig, __file__)
