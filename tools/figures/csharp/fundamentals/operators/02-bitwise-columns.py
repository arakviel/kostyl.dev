"""Бітові операції по стовпчиках для a = 202 і b = 166 (вивід bitwise.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, INK, canvas, save  # noqa: E402

A, B = 202, 166
ROWS = [("a", A, BLUE), ("b", B, BLUE), ("a & b", A & B, GREEN), ("a | b", A | B, GREEN),
        ("a ^ b", A ^ B, GREEN), ("~a", (~A) & 0xFF, AMBER)]
MUTED = "#475569"
fig, ax = canvas(13, 7.2)
X0, CELL, TOP, STEP = 22, 6.4, 84, 13

# підсвітка одного стовпчика (біт 6) для прикладу
col = 1
ax.add_patch(Rectangle((X0 + col * CELL - 0.3, TOP - 5 * STEP - 5.5), CELL + 0.6, 5 * STEP + 11.5,
                       fc="#FEF9C3", ec="#D97706", lw=1.2, ls="--"))
ax.text(X0 + col * CELL + CELL / 2, TOP + 9, "один стовпчик", ha="center", fontsize=11, color="#B45309")

for k, (name, value, color) in enumerate(ROWS):
    y = TOP - k * STEP
    if k == 2:
        ax.plot([X0 - 2, X0 + 8 * CELL + 2], [y + STEP / 2, y + STEP / 2], color=INK, lw=1.2)
    ax.text(X0 - 3, y, name, ha="right", va="center", fontsize=15, fontfamily="DejaVu Sans Mono")
    for b in range(8):
        bit = (value >> (7 - b)) & 1
        ax.add_patch(FancyBboxPatch((X0 + b * CELL + 0.3, y - 4.5), CELL - 0.6, 9,
                                    boxstyle="round,pad=0,rounding_size=0.6",
                                    fc=color if bit else "white", ec=INK, lw=1.0))
        ax.text(X0 + b * CELL + CELL / 2, y, str(bit), ha="center", va="center", fontsize=16,
                fontfamily="DejaVu Sans Mono")
    ax.text(X0 + 8 * CELL + 3, y, f"= {value}", va="center", fontsize=15, fontfamily="DejaVu Sans Mono")

ax.text(90, TOP - 2 * STEP, "1, якщо обидва 1", va="center", fontsize=12, color=MUTED)
ax.text(90, TOP - 3 * STEP, "1, якщо хоч один 1", va="center", fontsize=12, color=MUTED)
ax.text(90, TOP - 4 * STEP, "1, якщо різні", va="center", fontsize=12, color=MUTED)
ax.text(90, TOP - 5 * STEP, "інверсія кожного біта", va="center", fontsize=12, color=MUTED)
save(fig, __file__)
