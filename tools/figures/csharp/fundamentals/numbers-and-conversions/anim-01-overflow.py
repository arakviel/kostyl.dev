"""Лічильник sbyte проходить через 127: біти, значення і позиція на колі (поведінка з overflow.cs, .NET 10)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Ellipse, FancyBboxPatch  # noqa: E402

from _style import AMBER, BLUE, INK, box, save_steps  # noqa: E402

RED = "#DC2626"
MUTED = "#475569"
ASPECT = 6.75 / 12          # полотно 12×6.75: по x одиниця коротша
CX, CY, R = 24, 55, 28
MARKS = [0, 32, 64, 96, 127, 128, 160, 192, 224, 255]
SHIFT = {0: -9, 255: 9, 127: 9, 128: -9}


def to_sbyte(b):
    return b - 256 if b >= 128 else b


def pos(bits, radius):
    a = math.radians(90 - bits / 256 * 360)
    return CX + radius * ASPECT * math.cos(a), CY + radius * math.sin(a)


def draw_wheel(ax, current):
    ax.add_patch(Ellipse((CX, CY), 2 * R * ASPECT, 2 * R, fc="none", ec="#CBD5E1", lw=2.2))
    for b in MARKS:
        x, y = pos(b, R)
        ax.plot([x], [y], marker="o", markersize=4, color=INK)
        a = math.radians(90 - b / 256 * 360 + SHIFT.get(b, 0))
        ax.text(CX + (R - 6.5) * ASPECT * math.cos(a), CY + (R - 6.5) * math.sin(a), str(to_sbyte(b)),
                ha="center", va="center", fontsize=10, color="#2563EB")
    x, y = pos(current, R)
    ax.plot([x], [y], marker="o", markersize=15, color=RED, zorder=4)
    ax.plot([CX, x], [CY, y], color=RED, lw=2)
    ax.text(CX, CY + R + 7, "byte: 255 → 0", ha="center", fontsize=10.5, color=MUTED)
    ax.text(CX, CY - R - 7, "sbyte: 127 → −128", ha="center", fontsize=10.5, color=RED)


STEPS = [
    (125, "s = 125: старший біт (знак) — 0, число додатне."),
    (126, "s++ — 126."),
    (127, "s++ — 127, це sbyte.MaxValue: усі біти, крім знакового, — одиниці."),
    (128, "s++: перенос дійшов до знакового біта. 1000_0000 у sbyte — це −128.\nПомилки немає: значення «перескочило» на інший бік кола."),
    (129, "s++ — −127: лічильник іде далі по колу від мінімуму."),
    (130, "s++ — −126. У checked-контексті крок 127 → −128 кинув би OverflowException."),
]


def draw(ax, step):
    bits, caption = step
    value = to_sbyte(bits)
    ax.text(50, 95, "Переповнення sbyte: s++ після 127", ha="center", fontsize=18, fontweight="bold")
    draw_wheel(ax, bits)

    box(ax, 50, 72, 46, 10, "sbyte s = 125;\ns++;  // кілька разів", fc="#F8FAFC", mono=True, size=13, align="left")
    ax.text(50, 60, "біти", fontsize=12.5, color=MUTED)
    for k in range(8):
        bit = (bits >> (7 - k)) & 1
        fc = AMBER if k == 0 else (BLUE if bit else "white")
        ax.add_patch(FancyBboxPatch((50 + k * 5.6, 47), 5.0, 9, boxstyle="round,pad=0,rounding_size=0.6",
                                    fc=fc, ec=RED if (k == 0 and bit) else INK, lw=2 if (k == 0 and bit) else 1))
        ax.text(50 + k * 5.6 + 2.5, 51.5, str(bit), ha="center", va="center", fontsize=16, fontfamily="DejaVu Sans Mono")
    ax.text(50, 39, "як sbyte:", fontsize=13, color=MUTED, va="center")
    ax.text(66, 39, str(value), fontsize=26, fontweight="bold", va="center", color=RED if value < 0 else INK,
            fontfamily="DejaVu Sans Mono")
    ax.text(50, 30, f"ті самі біти як byte: {bits}", fontsize=13, color=MUTED, va="center")

    ax.text(50, 9, caption, ha="center", va="center", fontsize=14, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 2.6) for s in STEPS[:3]] + [(STEPS[3], 5.0)] + [(s, 2.6) for s in STEPS[4:]], draw, poster=3)
