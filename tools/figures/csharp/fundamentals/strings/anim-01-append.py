"""Покроково: += створює новий рядок і копіює всі символи, StringBuilder дописує в буфер."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, save_steps  # noqa: E402

MUTED = "#475569"
LETTERS = "abcde"
CW = 4.6


def draw(ax, k):
    ax.text(50, 95, "Дописати 5 символів по одному", ha="center", fontsize=18, fontweight="bold")
    # += : кожен крок — новий об'єкт
    ax.text(25, 87, "s += символ", ha="center", fontsize=16, fontfamily="DejaVu Sans Mono", color="#B45309")
    copied = 0
    for step in range(1, k + 1):
        y = 77 - (step - 1) * 10
        current = step == k
        for i in range(step):
            fc = AMBER if current else GREY
            ax.add_patch(Rectangle((5 + i * CW, y), CW, 8, fc=fc, ec=INK, lw=1.0, alpha=1 if current else 0.55))
            ax.text(5 + i * CW + CW / 2, y + 4, LETTERS[i], ha="center", va="center", fontsize=14,
                    fontfamily="DejaVu Sans Mono", alpha=1 if current else 0.5)
        copied += step
        ax.text(5 + step * CW + 1.5, y + 4, "новий рядок" if current else "сміття", va="center", fontsize=11.5,
                color=INK if current else MUTED)
    ax.text(25, 21, f"скопійовано символів: {copied}", ha="center", fontsize=15)

    ax.plot([50, 50], [14, 89], color="#CBD5E1", lw=1.2)

    # StringBuilder: один буфер
    ax.text(75, 87, "sb.Append(символ)", ha="center", fontsize=16, fontfamily="DejaVu Sans Mono", color="#2563EB")
    for i in range(16):
        x = 57 + (i % 8) * CW
        y = 70 - (i // 8) * 10
        filled = i < k
        ax.add_patch(Rectangle((x, y), CW, 8, fc=BLUE if filled else "white", ec=INK, lw=1.0))
        if filled:
            ax.text(x + CW / 2, y + 4, LETTERS[i], ha="center", va="center", fontsize=14,
                    fontfamily="DejaVu Sans Mono")
    ax.text(75, 82, "буфер Capacity 16, той самий об'єкт", ha="center", fontsize=12, color=MUTED)
    ax.text(75, 21, f"скопійовано символів: {k}", ha="center", fontsize=15)

    if k == 5:
        caption = "n дописувань: += копіює 1 + 2 + … + n = n(n + 1)/2 символів, StringBuilder — n.\n" \
                  "Для n = 40 000: += копіює 800 мільйонів символів (1,6 ГБ), StringBuilder — 40 000 (80 КБ)."
    elif k == 0:
        caption = "Рядок незмінний: += створює новий рядок і копіює в нього старий.\nStringBuilder має буфер із запасом."
    else:
        caption = f"Крок {k}: += створив рядок з {k} символів, StringBuilder записав один символ у буфер."
    ax.text(50, 7.5, caption, ha="center", va="center", fontsize=14, linespacing=1.45,
            bbox=dict(fc=GREEN if k == 5 else AMBER, ec="none", boxstyle="round,pad=0.5"))


steps = [(0, 3.5)] + [(k, 2.4) for k in range(1, 5)] + [(5, 6.0)]
save_steps(__file__, steps, draw, poster=-1)
