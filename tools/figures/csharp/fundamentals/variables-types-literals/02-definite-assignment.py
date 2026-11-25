"""Definite assignment: компілятор перевіряє кожен шлях від оголошення до читання змінної (CS0165, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Polygon  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, RED, arrow, box, canvas, save  # noqa: E402

fig, ax = canvas(15, 8.5)
RED_INK = "#DC2626"
GREEN_INK = "#16A34A"


def panel(ox, with_else):
    title = "Присвоєно на кожному шляху: компілюється" if with_else else "Є шлях без присвоєння: помилка CS0165"
    ax.text(ox + 24, 96, title, ha="center", fontsize=14, fontweight="bold",
            color=GREEN_INK if with_else else RED_INK)
    box(ax, ox + 13, 81, 22, 7, "string grade;", fc=GREY, mono=True, size=12.5)
    # ромб умови
    cx, cy = ox + 24, 64
    ax.add_patch(Polygon([(cx - 11, cy), (cx, cy + 8), (cx + 11, cy), (cx, cy - 8)], closed=True,
                         fc=BLUE, ec=INK, lw=1.4))
    ax.text(cx, cy, "score >= 60", ha="center", va="center", fontsize=12.5, fontfamily="DejaVu Sans Mono")
    arrow(ax, cx, 80, cx, cy + 8.6)

    box(ax, ox + 0.5, 37, 21, 8, 'grade =\n"зараховано";', fc=GREEN, mono=True, size=11.5)
    arrow(ax, cx - 11, cy, ox + 11, 45.8)
    ax.text(ox + 9, cy + 1, "так", ha="center", fontsize=12)

    bottom_fc = GREEN if with_else else RED
    box(ax, ox + 8, 8, 32, 8, "Console.WriteLine(grade);", fc=bottom_fc, mono=True, size=12)
    arrow(ax, ox + 11, 36.2, ox + 18, 16.8)

    if with_else:
        box(ax, ox + 26.5, 37, 21, 8, 'grade =\n"не зараховано";', fc=GREEN, mono=True, size=11.5)
        arrow(ax, cx + 11, cy, ox + 37, 45.8)
        arrow(ax, ox + 37, 36.2, ox + 30, 16.8)
        ax.text(ox + 39, cy + 1, "ні", ha="center", fontsize=12)
    else:
        arrow(ax, cx + 11, cy, ox + 33, 16.8, color=RED_INK, ls="--", lw=1.8)
        ax.text(ox + 39, cy + 1, "ні", ha="center", fontsize=12)
        ax.text(ox + 34.5, 40, "grade нічого\nне присвоєно", fontsize=12, color=RED_INK, ha="left",
                va="center", bbox=dict(fc="white", ec="none"))
        ax.text(ox + 24, 2, "Use of unassigned local variable 'grade'", ha="center", fontsize=11.5,
                color=RED_INK, fontfamily="DejaVu Sans Mono")


panel(1, True)
panel(52, False)
ax.plot([50, 50], [4, 92], color="#CBD5E1", lw=1.2)
save(fig, __file__)
