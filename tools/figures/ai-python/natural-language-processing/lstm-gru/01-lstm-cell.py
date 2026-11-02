"""Один крок LSTM: три вентилі керують cell state."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
from matplotlib.patches import Circle

fig, ax = canvas(12, 6.2)

def op(x, y, sym):
    ax.add_patch(Circle((x, y), 2.6, fc="white", ec=INK, lw=1.5, zorder=3))
    ax.text(x, y - 0.2, sym, ha="center", va="center", fontsize=15, zorder=4)

def line(xs, ys, head=True):
    if head:
        ax.plot(xs[:-1], ys[:-1], color=INK, lw=1.6, solid_capstyle="butt")
        arrow(ax, xs[-2], ys[-2], xs[-1], ys[-1])
    else:
        ax.plot(xs, ys, color=INK, lw=1.6)

# cell state
ax.plot([5, 95], [88, 88], color="#D97706", lw=4, zorder=1, solid_capstyle="butt")
arrow(ax, 94, 88, 97, 88)
ax.text(2, 88, "cₜ₋₁", ha="center", va="center", fontsize=14, color="#D97706")
ax.text(99.5, 88, "cₜ", ha="center", va="center", fontsize=14, color="#D97706")
ax.text(26, 95, "cell state: довга пам'ять", fontsize=12, color="#D97706", ha="center")
op(14, 88, "×"); op(38, 88, "+")

gates = [("f", 14, GREEN, "σ", "forget\n(забути)"), ("i", 30, BLUE, "σ", "input\n(записати)"),
         ("g", 46, AMBER, "tanh", "кандидат"), ("o", 70, RED, "σ", "output\n(видати)")]
for name, cx, col, act, label in gates:
    box(ax, cx - 6, 36, 12, 12, f"{act}\n{name}", fc=col, size=12)
    ax.text(cx, 30, label, ha="center", va="top", fontsize=10.5, color="#475569", linespacing=1.2, zorder=5, bbox=dict(fc="white", ec="none", pad=1.5))

# вхідна шина
ax.plot([14, 70], [14, 14], color=INK, lw=1.6)
for cx in (14, 30, 46, 70):
    arrow(ax, cx, 14, cx, 35)
box(ax, 26, 1, 32, 8, "[hₜ₋₁, xₜ]", fc=GREY, size=12)
ax.plot([42, 42], [9.6, 14], color=INK, lw=1.6)

# forget -> ×
arrow(ax, 14, 49, 14, 85)
# i, g -> × -> +
op(38, 62, "×")
line([30, 30, 35.2], [49, 62, 62])
line([46, 46, 40.8], [49, 62, 62])
arrow(ax, 38, 64.8, 38, 85)
# tanh(c) -> × o
ax.plot([84, 84], [88, 80.5], color=INK, lw=1.6)
box(ax, 78, 73, 12, 8, "tanh", fc=AMBER, size=11)
arrow(ax, 84, 73, 84, 64.8)
op(84, 62, "×")
line([70, 70, 81.2], [49, 62, 62])
arrow(ax, 86.6, 62, 96, 62)
ax.text(99.5, 62, "hₜ", ha="center", va="center", fontsize=14, color="#2563EB")
save(fig, __file__)
