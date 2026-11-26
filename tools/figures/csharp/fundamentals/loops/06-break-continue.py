"""Куди переходять continue і break у for і в while."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch  # noqa: E402

from _style import AMBER, BLUE, GREY, INK, RED, box, canvas, save  # noqa: E402

W, H = 10.5, 3.0
GREEN_LINE, RED_LINE, AMBER_LINE = "#16A34A", "#DC2626", "#D97706"


def block(ax, cx, cy, text, fc, mono=True, ec=INK):
    box(ax, cx - W, cy - H, 2 * W, 2 * H, text, fc=fc, mono=mono, size=12.5, ec=ec)


def path(ax, points, color=INK, label=None, at=None, lw=1.6, ha="center"):
    xs, ys = zip(*points)
    ax.plot(xs[:-1], ys[:-1], color=color, lw=lw, solid_capstyle="round")
    ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>", mutation_scale=16, lw=lw, color=color))
    if label:
        ax.text(*at, label, fontsize=12.5, color=color, ha=ha, va="center", bbox=dict(fc="white", ec="none", pad=1))


fig, ax = canvas(15, 8.4)
G = 0.6

# for
x = 24
ax.text(x + 4, 99, "for: continue → ітератор, break → після циклу", fontsize=14.5, fontweight="bold", ha="center")
block(ax, x, 89, "int i = 0", BLUE)
block(ax, x, 75, "i < n ?", AMBER)
block(ax, x, 61, "if (…) continue;", GREY)
block(ax, x, 47, "if (…) break;", GREY)
block(ax, x, 33, "решта тіла", GREY, mono=False)
block(ax, x, 19, "i++", AMBER)
block(ax, x, 3, "після циклу", BLUE, mono=False)
path(ax, [(x, 89 - H - G), (x, 75 + H + G)])
path(ax, [(x, 75 - H - G), (x, 61 + H + G)], GREEN_LINE)
path(ax, [(x, 61 - H - G), (x, 47 + H + G)])
path(ax, [(x, 47 - H - G), (x, 33 + H + G)])
path(ax, [(x, 33 - H - G), (x, 19 + H + G)])
path(ax, [(x - W - G, 19), (x - W - 4, 19), (x - W - 4, 75), (x - W - G, 75)])
path(ax, [(x + W + G, 61), (x + W + 4, 61), (x + W + 4, 19), (x + W + G, 19)], AMBER_LINE, "continue",
      (x + W + 4.6, 40), lw=2.2, ha="left")
path(ax, [(x + W + G, 47), (x + W + 13, 47), (x + W + 13, 3), (x + W + G, 3)], RED_LINE, "break",
      (x + W + 13.6, 25), lw=2.2, ha="left")
path(ax, [(x + W + G, 75), (x + W + 20, 75), (x + W + 20, 6), (x + W + G, 6)], INK, "false",
      (x + W + 20, 66))

# while
x = 79
ax.text(x, 99, "while: continue → одразу умова", fontsize=14.5, fontweight="bold", ha="center")
block(ax, x, 75, "i < n ?", AMBER)
block(ax, x, 61, "if (…) continue;", GREY)
block(ax, x, 47, "решта тіла", GREY, mono=False)
block(ax, x, 33, "i++", AMBER)
block(ax, x, 3, "після циклу", BLUE, mono=False)
path(ax, [(x, 88), (x, 75 + H + G)])
path(ax, [(x, 75 - H - G), (x, 61 + H + G)], GREEN_LINE)
path(ax, [(x, 61 - H - G), (x, 47 + H + G)])
path(ax, [(x, 47 - H - G), (x, 33 + H + G)])
path(ax, [(x - W - G, 33), (x - W - 7, 33), (x - W - 7, 74), (x - W - G, 74)])
path(ax, [(x - W - G, 61), (x - W - 3, 61), (x - W - 3, 77), (x - W - G, 77)], AMBER_LINE, "continue",
      (x - W - 3.4, 66), lw=2.2, ha="right")
path(ax, [(x + W + G, 75), (x + W + 5, 75), (x + W + 5, 3), (x + W + G, 3)], INK, "false", (x + W + 5, 40))
ax.text(x - 3, 17, "continue пропускає i++\nу кінці тіла: i не змінюється,\nумова лишається true —\nцикл не завершується",
        ha="center", va="center", fontsize=12.5, linespacing=1.4,
        bbox=dict(fc=RED, ec="none", boxstyle="round,pad=0.5"))
ax.set_ylim(-3, 102)
save(fig, __file__)
