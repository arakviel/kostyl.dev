"""Біти double для 0.1: знак, порядок, мантиса (біти з ieee.cs: BitConverter.DoubleToInt64Bits, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import AMBER, BLUE, GREEN, INK, canvas, save  # noqa: E402

BITS = "0011111110111001100110011001100110011001100110011001100110011010"
MUTED = "#475569"
fig, ax = canvas(16, 5.0)
X0, CELL, Y = 1.5, 1.52, 62

for k, bit in enumerate(BITS):
    fc = BLUE if k == 0 else (AMBER if k <= 11 else GREEN)
    ax.add_patch(FancyBboxPatch((X0 + k * CELL + 0.08, Y), CELL - 0.16, 10, boxstyle="round,pad=0,rounding_size=0.3",
                                fc=fc, ec=INK, lw=0.7))
    ax.text(X0 + k * CELL + CELL / 2, Y + 5, bit, ha="center", va="center", fontsize=10.5, fontfamily="DejaVu Sans Mono")


def brace(first, last, text, color):
    x1, x2 = X0 + first * CELL + 0.2, X0 + (last + 1) * CELL - 0.2
    ax.plot([x1, x1, x2, x2], [Y - 2, Y - 4, Y - 4, Y - 2], color=color, lw=1.6)
    ax.text((x1 + x2) / 2, Y - 6.5, text, ha="center", va="top", fontsize=12, color=INK, linespacing=1.4)


ax.text(X0, Y + 13, "знак: 0 → +", ha="left", fontsize=12, color="#2563EB")
ax.plot([X0 + CELL / 2, X0 + CELL / 2], [Y + 10.5, Y + 12], color="#2563EB", lw=1.6)
brace(1, 11, "порядок, 11 бітів\n01111111011₂ = 1019\n1019 − 1023 = −4", "#B45309")
brace(12, 63, "мантиса, 52 біти: дробова частина числа 1.1001100110011…1010₂ ≈ 1.6\n"
      "двійковий дріб 0011 повторюється нескінченно, тому останні біти округлено", "#16A34A")

ax.text(50, 90, "0.1 у форматі double (IEEE 754, 64 біти)", ha="center", fontsize=15, fontweight="bold")
ax.text(50, 26, "значення = +1.6000000000000000888… × 2⁻⁴ = 0.1000000000000000055511151…", ha="center",
        fontsize=13.5, fontfamily="DejaVu Sans Mono")
ax.text(50, 18, "найближче до 0.1 число, яке можна записати в 64 біти; рівно 0.1 у двійковій системі не записується",
        ha="center", fontsize=12, color=MUTED)
save(fig, __file__)
