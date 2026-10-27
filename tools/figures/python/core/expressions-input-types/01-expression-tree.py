import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save

fig, ax = canvas(10, 4.2)
ax.text(2, 94, "2 + 3 * 4", fontsize=15, fontfamily="DejaVu Sans Mono", fontweight="bold")
nodes = {"+": (40, 68), "2": (24, 38), "*": (56, 38), "3": (46, 8), "4": (66, 8)}
edges = [("+", "2"), ("+", "*"), ("*", "3"), ("*", "4")]
for a, b in edges:
    ax.plot([nodes[a][0] + 4, nodes[b][0] + 4], [nodes[a][1], nodes[b][1] + 14], color=INK, lw=1.5)
for k, (x, y) in nodes.items():
    box(ax, x, y, 8, 14, k, AMBER if k in "+*" else BLUE, mono=True, size=16, weight="bold")
ax.text(76, 78, "2. складаємо: 2 + 12 = 14", fontsize=12)
ax.text(76, 46, "1. спершу множимо: 3 * 4 = 12", fontsize=12)
ax.text(76, 14, "множення має вищий пріоритет,\nтому воно глибше в дереві", fontsize=11)
save(fig, __file__)
