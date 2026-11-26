"""Доповняльний код: ті самі 8 бітів як byte і як sbyte (значення з twos.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import AMBER, BLUE, GREEN, INK, canvas, save  # noqa: E402

ROWS = [0, 1, 127, 128, 254, 255]
MUTED = "#475569"
fig, ax = canvas(14, 7.4)
X0, CELL, TOP, STEP = 6, 5.2, 80, 12.5

ax.text(X0 + 4 * CELL, TOP + 12, "біти (8)", ha="center", fontsize=13, fontweight="bold")
ax.text(X0 + 0.5 * CELL, TOP + 7, "знак", ha="center", fontsize=11, color="#B45309")
ax.text(62, TOP + 12, "як byte", ha="center", fontsize=13, fontweight="bold")
ax.text(80, TOP + 12, "як sbyte", ha="center", fontsize=13, fontweight="bold")

for k, bits in enumerate(ROWS):
    y = TOP - k * STEP
    for b in range(8):
        bit = (bits >> (7 - b)) & 1
        fc = AMBER if b == 0 else (BLUE if bit else "white")
        ax.add_patch(FancyBboxPatch((X0 + b * CELL + 0.2, y - 4), CELL - 0.4, 8,
                                    boxstyle="round,pad=0,rounding_size=0.6", fc=fc, ec=INK, lw=1.0))
        ax.text(X0 + b * CELL + CELL / 2, y, str(bit), ha="center", va="center", fontsize=15,
                fontfamily="DejaVu Sans Mono")
    sb = bits - 256 if bits >= 128 else bits
    ax.text(62, y, str(bits), ha="center", va="center", fontsize=15, fontfamily="DejaVu Sans Mono")
    ax.text(80, y, str(sb), ha="center", va="center", fontsize=15, fontfamily="DejaVu Sans Mono",
            color="#DC2626" if sb < 0 else INK, fontweight="bold" if sb < 0 else "normal")

ax.text(50, 3, "Старший біт sbyte має вагу −128: 1000_0000 = −128, 1111_1111 = −128 + 127 = −1.\n"
        "Від'ємне число = інвертувати біти додатного і додати 1: 0000_0001 → 1111_1110 → 1111_1111.",
        ha="center", va="center", fontsize=12, color=MUTED, linespacing=1.5)
save(fig, __file__)
