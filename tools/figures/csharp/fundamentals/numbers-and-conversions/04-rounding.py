"""Куди ведуть різні способи округлення для 2.5 і −2.7 (значення з rounding.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch  # noqa: E402

from _style import INK, canvas, save  # noqa: E402

MUTED = "#475569"
ROWS = [  # (назва, результат для 2.5, результат для -2.7)
    ("(int)x — відкинути дробову частину", 2, -2),
    ("Math.Floor — вниз", 2, -3),
    ("Math.Ceiling — вгору", 3, -2),
    ("Math.Round — до найближчого, .5 — до парного", 2, -3),
    ("Math.Round(x, AwayFromZero) — .5 від нуля", 3, -3),
]
fig, ax = canvas(15, 7.2)
LX0, LX1 = 44, 98          # координати осі на полотні
VMIN, VMAX = -4, 4


def X(v):
    return LX0 + (v - VMIN) / (VMAX - VMIN) * (LX1 - LX0)


TOP, STEP = 82, 15
ax.text(X(2.5), TOP + 10, "x = 2.5", ha="center", fontsize=12.5, color="#2563EB", fontweight="bold")
ax.text(X(-2.7), TOP + 10, "x = −2.7", ha="center", fontsize=12.5, color="#D97706", fontweight="bold")
for k, (label, r1, r2) in enumerate(ROWS):
    y = TOP - k * STEP
    ax.text(1, y, label, va="center", fontsize=12)
    ax.plot([LX0, LX1], [y, y], color="#CBD5E1", lw=1.5)
    for v in range(VMIN, VMAX + 1):
        ax.plot([X(v), X(v)], [y - 1, y + 1], color="#94A3B8", lw=1)
        ax.text(X(v), y - 3.6, str(v).replace("-", "−"), ha="center", fontsize=9.5, color=MUTED)
    for start, result, color in [(2.5, r1, "#2563EB"), (-2.7, r2, "#D97706")]:
        ax.plot([X(start)], [y], marker="o", color=color, markersize=6)
        ax.add_patch(FancyArrowPatch((X(start), y + 0.8), (X(result), y + 0.8), arrowstyle="-|>", mutation_scale=13,
                                     color=color, lw=1.8, connectionstyle=f"arc3,rad={-0.6 if result > start else 0.6}", shrinkA=1, shrinkB=1))
        ax.plot([X(result)], [y], marker="s", color=color, markersize=7)
save(fig, __file__)
