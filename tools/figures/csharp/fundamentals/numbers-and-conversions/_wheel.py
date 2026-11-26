"""Коло 8-бітних значень: одні й ті самі біти як sbyte (всередині) і як byte (зовні)."""
import math

from matplotlib.patches import Circle, FancyArrowPatch

INK = "#1E293B"
MUTED = "#475569"
RED = "#DC2626"
BLUE = "#2563EB"

# точки на колі: значення бітів 0..255, кут відраховується від верху за годинниковою стрілкою
MARKS = [0, 32, 64, 96, 127, 128, 160, 192, 224, 255]
LABEL_SHIFT = {0: -9, 255: 9, 127: 9, 128: -9}  # розсунути підписи сусідніх точок, градуси


def angle(bits):
    return math.radians(90 - bits / 256 * 360)


def as_sbyte(bits):
    return bits - 256 if bits >= 128 else bits


def wheel(ax, cx, cy, r, highlight=None, size=11):
    ax.add_patch(Circle((cx, cy), r, fc="none", ec="#CBD5E1", lw=2.2))
    for bits in MARKS:
        a = angle(bits)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        hot = bits == highlight
        ax.plot([x], [y], marker="o", markersize=9 if hot else 5, color=RED if hot else INK, zorder=3)
        la = a + math.radians(LABEL_SHIFT.get(bits, 0))
        ax.text(cx + (r - 7) * math.cos(la), cy + (r - 7) * math.sin(la), str(as_sbyte(bits)), ha="center",
                va="center", fontsize=size, color=BLUE, fontweight="bold" if hot else "normal")
        ax.text(cx + (r + 7) * math.cos(la), cy + (r + 7) * math.sin(la), str(bits), ha="center", va="center",
                fontsize=size, color=MUTED, fontweight="bold" if hot else "normal")
    # межі переповнення
    for bits_from, label, where in [(127, "sbyte: 127 + 1 = −128", "bottom"), (255, "byte: 255 + 1 = 0", "top")]:
        a1, a2 = angle(bits_from + 0.15), angle(bits_from + 0.85)
        ax.add_patch(FancyArrowPatch((cx + r * math.cos(a1), cy + r * math.sin(a1)),
                                     (cx + r * math.cos(a2), cy + r * math.sin(a2)),
                                     arrowstyle="-|>", mutation_scale=14, color=RED, lw=2.4,
                                     connectionstyle="arc3,rad=-0.3"))
        ty = cy - r - 14 if where == "bottom" else cy + r + 14
        ax.text(cx, ty, label, ha="center", va="center", fontsize=size + 1, color=RED, fontweight="bold")
