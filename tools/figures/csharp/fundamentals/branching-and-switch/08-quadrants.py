"""Кортежні шаблони (x, y) на координатній площині (вивід tuple-patterns.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(11, 8)
CX, CY, S = 50, 50, 5.2   # центр і масштаб: 1 одиниця = S


def P(x, y):
    return CX + x * S, CY + y * S


from matplotlib.patches import Rectangle  # noqa: E402

QUADS = [((0, 0), "(> 0, > 0)", "I чверть", BLUE), ((-1, 0), "(< 0, > 0)", "II чверть", GREEN),
         ((-1, -1), "(< 0, < 0)", "III чверть", AMBER), ((0, -1), "(> 0, < 0)", "IV чверть", GREY)]
for (qx, qy), pattern, name, color in QUADS:
    ax.add_patch(Rectangle((CX + qx * 8 * S, CY + qy * 8 * S), 8 * S, 8 * S, fc=color, ec="none", alpha=0.7))
    tx = CX + (qx + 0.5) * 8 * S
    ty = CY + (6.2 * S if qy == 0 else -6.2 * S)
    ax.text(tx, ty + 3, pattern, ha="center", va="center", fontsize=14, fontfamily="DejaVu Sans Mono",
            fontweight="bold")
    ax.text(tx, ty - 3, name, ha="center", va="center", fontsize=12.5)

ax.annotate("", xy=(CX + 8.6 * S, CY), xytext=(CX - 8.6 * S, CY), arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.4))
ax.annotate("", xy=(CX, CY + 8.6 * S), xytext=(CX, CY - 8.6 * S), arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.4))
ax.text(CX + 8.6 * S, CY - 3.5, "x", fontsize=13, ha="center")
ax.text(CX + 1.5, CY + 8.6 * S, "y", fontsize=13, va="center")
ax.text(CX + 6.2 * S, CY + 2.2, "(_, 0) — на осі X", fontsize=12, color="#B91C1C", ha="center", va="bottom",
        fontfamily="DejaVu Sans Mono", bbox=dict(fc="white", ec="none", pad=1))
ax.text(CX - 1.2, CY - 3 * S, "(0, _) — на осі Y", fontsize=12, color="#B91C1C", ha="right", va="center",
        fontfamily="DejaVu Sans Mono", bbox=dict(fc="white", ec="none", pad=1))

POINTS = [(3, 4), (-2, 5), (0, 7), (0, 0), (6, -1)]
for x, y in POINTS:
    px, py = P(x, y)
    ax.plot([px], [py], marker="o", ms=9, mfc="#1D4ED8", mec="white", mew=1.5, zorder=5)
    if (x, y) == (0, 0):
        continue
    ax.text(px + 1.5, py + 1.8, f"({x}, {y})", fontsize=11.5, fontfamily="DejaVu Sans Mono", color="#1D4ED8",
            zorder=5, bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.8))
ax.text(CX - 1.5, CY - 3, "(0, 0)\nпочаток", fontsize=11, ha="right", va="top", color="#B91C1C",
        fontfamily="DejaVu Sans Mono")
save(fig, __file__)
