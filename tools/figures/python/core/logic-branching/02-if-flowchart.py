import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, RED, arrow, box, canvas, save
from matplotlib.patches import Polygon


def diamond(ax, cx, cy, w, h, text, fc):
    ax.add_patch(Polygon([(cx - w, cy), (cx, cy + h), (cx + w, cy), (cx, cy - h)], closed=True, fc=fc, ec=INK, lw=1.4))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=11.5, fontfamily="DejaVu Sans Mono")


fig, ax = canvas(11, 4.4)
conds = [(14, "score >= 90"), (38, "score >= 75"), (62, "score >= 60")]
grades = ["A", "B", "C"]
for (cx, t), g in zip(conds, grades):
    diamond(ax, cx, 52, 11, 22, t, AMBER)
    box(ax, cx - 5, 8, 10, 14, f'"{g}"', GREEN, mono=True, size=12)
    arrow(ax, cx, 30, cx, 23)
    ax.text(cx + 1.2, 26, "так", fontsize=11)
for a, b in [(14, 38), (38, 62)]:
    arrow(ax, a + 11.5, 52, b - 11.5, 52)
    ax.text((a + b) / 2, 56, "ні", ha="center", fontsize=11)
arrow(ax, 73.5, 52, 80, 52)
ax.text(76.5, 56, "ні", ha="center", fontsize=11)
box(ax, 81, 44, 17, 16, 'else:\n"F"', RED, mono=True, size=12)
box(ax, 2, 84, 24, 12, "score = 82", GREY, mono=True, size=12)
arrow(ax, 14, 83, 14, 75)
save(fig, __file__)
