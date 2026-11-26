"""Array.Resize створює новий масив: змінна a веде до нового, b — до старого (resize.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

from _style import BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

MUTED = "#475569"
CW, H = 5.2, 11


def array(ax, x, y, values, fc=BLUE, faded=False):
    for i, v in enumerate(values):
        ax.add_patch(Rectangle((x + i * CW, y), CW, H, fc=fc, ec=INK, lw=1.2, alpha=0.5 if faded else 1))
        ax.text(x + i * CW + CW / 2, y + H / 2, str(v), ha="center", va="center", fontsize=13,
                fontfamily="DejaVu Sans Mono")
    return x, x + len(values) * CW


def var(ax, x, y, name):
    ax.add_patch(Rectangle((x, y), 7, H, fc=GREEN, ec=INK, lw=1.2))
    ax.text(x + 3.5, y + H / 2, name, ha="center", va="center", fontsize=14, fontfamily="DejaVu Sans Mono")


def link(ax, x1, y1, x2, y2, color=INK):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16, lw=1.5, color=color))


fig, ax = canvas(15, 4.4)
# до
ax.text(22, 95, "до Array.Resize", ha="center", fontsize=14, fontweight="bold")
var(ax, 3, 66, "a")
var(ax, 3, 36, "b")
x0, x1 = array(ax, 22, 51, [1, 2, 3])
link(ax, 10.2, 71.5, 21.6, 59)
link(ax, 10.2, 41.5, 21.6, 54)
ax.text(30, 40, "один масив,\nдва посилання", ha="center", va="top", fontsize=12, color=MUTED)

ax.plot([46, 46], [10, 92], color="#CBD5E1", lw=1.2)

# після
ax.text(74, 95, "після Array.Resize(ref a, 5) і a[0] = 100", ha="center", fontsize=14, fontweight="bold")
var(ax, 52, 66, "a")
var(ax, 52, 26, "b")
array(ax, 72, 66, [100, 2, 3, 0, 0])
array(ax, 72, 26, [1, 2, 3])
link(ax, 59.2, 71.5, 71.6, 71.5)
link(ax, 59.2, 31.5, 71.6, 31.5)
ax.text(72 + 2.5 * CW, 82, "новий масив: копія + нулі", ha="center", fontsize=12, color=MUTED)
ax.text(72 + 1.5 * CW, 20, "старий масив", ha="center", va="top", fontsize=12, color=MUTED)
save(fig, __file__)
