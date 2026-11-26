"""Анатомія елемента форматування {price,10:F2} і результат у 10 позиціях (format-numbers.cs, культура uk-UA)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save  # noqa: E402

WIDTH = 15
fig, ax = canvas(WIDTH, 7.6)
AX_W = ax.get_position().width * WIDTH
CHAR = 0.602 * 22 / 72 / AX_W * 100
MUTED = "#475569"
PINK = "#FCE7F3"

tokens = [("{", GREY, None), ("price", BLUE, "що вивести:\nзмінна чи вираз\n(у складеному\nформатуванні — номер {0})"),
          (",10", GREEN, "ширина: не менше\n10 символів;\n+ праворуч, − ліворуч"),
          (":F2", AMBER, "рядок формату:\nF2, N0, P1, X,\ndd.MM.yyyy …"), ("}", GREY, None)]
x, Y = 3, 70
for text, color, label in tokens:
    w = len(text) * CHAR + 4
    box(ax, x, Y, w, 12, text, fc=color, mono=True, size=22)
    if label:
        cx = x + w / 2
        ax.plot([cx, cx], [Y - 1.5, Y - 5], color=MUTED, lw=1.1)
        ax.text(cx, Y - 6, label, ha="center", va="top", fontsize=12, color=MUTED, linespacing=1.3)
    x += w + 9

ax.text(3, 26, "double price = 1234.5678;", fontsize=13, fontfamily="DejaVu Sans Mono")
ax.text(3, 18, "$\"[{price,10:F2}]\"", fontsize=13, fontfamily="DejaVu Sans Mono")

result = "   1234,57"
X0, CW = 52, 4.4
ax.text(X0 - 2, 22, "результат:", ha="right", va="center", fontsize=13)
for k, ch in enumerate(result):
    pad = ch == " "
    ax.add_patch(FancyBboxPatch((X0 + k * CW + 0.2, 16), CW - 0.4, 12, boxstyle="round,pad=0,rounding_size=0.5",
                                fc="#F1F5F9" if pad else PINK, ec="#94A3B8" if pad else INK, lw=0.9,
                                ls="--" if pad else "-"))
    ax.text(X0 + k * CW + CW / 2, 22, "·" if pad else ch, ha="center", va="center", fontsize=17,
            color="#94A3B8" if pad else INK, fontfamily="DejaVu Sans Mono")
    ax.text(X0 + k * CW + CW / 2, 12.5, str(k + 1), ha="center", fontsize=9.5, color=MUTED)
ax.text(X0 + 5 * CW, 5, "3 пробіли доповнення зліва + 7 символів числа = 10", ha="center", fontsize=12, color=MUTED)
save(fig, __file__)
