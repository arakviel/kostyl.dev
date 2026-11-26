"""int[][] у пам'яті: зовнішній масив посилань і окремі масиви-рядки різної довжини (jagged.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(15, 5.6)
CW, CH = 6.4, 11

# змінна
ax.add_patch(Rectangle((2, 44), 9, CH, fc=GREEN, ec=INK, lw=1.2))
ax.text(6.5, 44 + CH / 2, "rows", ha="center", va="center", fontsize=13, fontfamily="DejaVu Sans Mono")

# зовнішній масив
ox, oy = 18, 44
ax.text(ox + 12.6, 31, "зовнішній масив:\nLength і 3 посилання", ha="center", va="top", fontsize=12, color=MUTED, linespacing=1.3)
ax.add_patch(Rectangle((ox, oy), 5, CH, fc=GREY, ec=INK, lw=1.2))
ax.text(ox + 2.5, oy + CH / 2, "3", ha="center", va="center", fontsize=12, color=MUTED)
starts = []
for i in range(3):
    x = ox + 5 + i * CW
    ax.add_patch(Rectangle((x, oy), CW, CH, fc=AMBER, ec=INK, lw=1.2))
    ax.text(x + CW / 2, oy + CH / 2, "•", ha="center", va="center", fontsize=16)
    ax.text(x + CW / 2, oy - 4.5, f"[{i}]", ha="center", va="center", fontsize=11, fontfamily="DejaVu Sans Mono")
    starts.append((x + CW / 2, oy + CH if i < 2 else oy))
ax.add_patch(FancyArrowPatch((11.2, 49.5), (17.6, 49.5), arrowstyle="-|>", mutation_scale=16, lw=1.4, color=INK))

# рядки
rows = [[1], [2, 3], [0, 0, 0, 0]]
ys = [80, 58, 18]
for i, (values, y) in enumerate(zip(rows, ys)):
    rx = 58
    ax.add_patch(Rectangle((rx, y), 5, CH, fc=GREY, ec=INK, lw=1.2))
    ax.text(rx + 2.5, y + CH / 2, str(len(values)), ha="center", va="center", fontsize=12, color=MUTED)
    for j, v in enumerate(values):
        x = rx + 5 + j * CW
        ax.add_patch(Rectangle((x, y), CW, CH, fc=BLUE, ec=INK, lw=1.2))
        ax.text(x + CW / 2, y + CH / 2, str(v), ha="center", va="center", fontsize=14,
                fontfamily="DejaVu Sans Mono")
    ax.text(rx + 5 + len(values) * CW + 1.5, y + CH / 2, f"rows[{i}]: окремий int[{len(values)}]", va="center",
            fontsize=12)
    sx, sy = starts[i]
    ax.add_patch(FancyArrowPatch((sx, sy), (rx - 0.4, y + CH / 2), arrowstyle="-|>", mutation_scale=16, lw=1.4,
                                 color=INK, connectionstyle="arc3,rad=0.0"))
ax.text(58 + 2.5, 95, "Length", ha="center", fontsize=11, color=MUTED)
ax.set_ylim(0, 100)
ax.text(2, 4, "rows[1][0]: перший індекс вибирає посилання на рядок, другий — елемент у цьому рядку",
        ha="left", va="center", fontsize=12.5, color=INK)
save(fig, __file__)
