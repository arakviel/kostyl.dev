"""Покрокове обчислення int r = k++ + ++k для k = 5 (вивід increment.cs: 12, k = 7)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, INK, box, save_steps  # noqa: E402

MUTED = "#475569"
EXPR = ["int r = ", "k++", " + ", "++k", ";"]
CHAR = 0.602 * 22 / 72 / 12 * 100  # ширина символу DejaVu Sans Mono 22 pt на полотні шириною 12 дюймів

# (підсвічена частина виразу, k, ліве значення, праве значення, r, підпис)
STEPS = [
    (None, 5, None, None, None, "Перед обчисленням k = 5."),
    (1, 6, 5, None, None, "Лівий операнд k++: значення виразу — старе k, тобто 5.\nПісля цього k збільшується до 6."),
    (3, 7, 5, 7, None, "Правий операнд ++k: спочатку k збільшується до 7,\nзначення виразу — нове k, тобто 7."),
    (2, 7, 5, 7, 12, "Додавання: 5 + 7 = 12. Операнди обчислено зліва направо,\nі результат визначений специфікацією C#."),
]


def draw(ax, step):
    part, k, left, right, r, caption = step
    ax.text(50, 95, "Префіксний і постфіксний ++ в одному виразі", ha="center", fontsize=18, fontweight="bold")

    x = 14
    for i, text in enumerate(EXPR):
        w = len(text) * CHAR
        if i == part:
            ax.add_patch(Rectangle((x - 0.3, 73), w + 0.6, 10, fc="#FDE68A", ec="none"))
        ax.text(x, 78, text, fontsize=22, fontfamily="DejaVu Sans Mono", va="center")
        x += w

    box(ax, 8, 30, 22, 26, "", fc="#F8FAFC", ec="#CBD5E1")
    ax.text(19, 51, "змінна k", ha="center", fontsize=13, color=MUTED)
    ax.text(19, 40, str(k), ha="center", va="center", fontsize=34, fontweight="bold", fontfamily="DejaVu Sans Mono")

    ax.text(57, 60, "значення операндів", ha="center", fontsize=13, color=MUTED)
    box(ax, 38, 34, 16, 18, "" if left is None else str(left), fc=BLUE if left is not None else "white", mono=True, size=26)
    ax.text(46, 30, "k++", ha="center", va="top", fontsize=12, color=MUTED, fontfamily="DejaVu Sans Mono")
    ax.text(57, 43, "+", ha="center", va="center", fontsize=26)
    box(ax, 60, 34, 16, 18, "" if right is None else str(right), fc=BLUE if right is not None else "white", mono=True, size=26)
    ax.text(68, 30, "++k", ha="center", va="top", fontsize=12, color=MUTED, fontfamily="DejaVu Sans Mono")

    box(ax, 82, 34, 14, 18, "" if r is None else str(r), fc=GREEN if r is not None else "white", mono=True, size=26)
    ax.text(89, 30, "r", ha="center", va="top", fontsize=12, color=MUTED, fontfamily="DejaVu Sans Mono")

    ax.text(50, 9, caption, ha="center", va="center", fontsize=14, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 3.5) for s in STEPS[:-1]] + [(STEPS[-1], 5.0)], draw, poster=3)
