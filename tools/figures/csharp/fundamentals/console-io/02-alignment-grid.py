"""Вирівнювання в таблиці: {name,-10} доповнює праворуч, {score,6:F2} — ліворуч (вивід alignment.cs, культура uk-UA)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import BLUE, GREEN, INK, canvas, save  # noqa: E402

ROWS = ["Прізвище  |   Бал|", "Бондар    |  4,75|", "Ко        |  5,00|", "Шевченко  |  3,50|"]
MUTED = "#475569"
fig, ax = canvas(14, 6.4)
X0, CW, TOP, RH = 6, 4.6, 74, 15

ax.text(X0 + 5 * CW, TOP + 16, "{name,-10}", ha="center", fontsize=14, fontfamily="DejaVu Sans Mono", color="#1D4ED8")
ax.text(X0 + 5 * CW, TOP + 11, "ліворуч, доповнення справа", ha="center", fontsize=11.5, color=MUTED)
ax.text(X0 + 14 * CW, TOP + 16, "{score,6:F2}", ha="center", fontsize=14, fontfamily="DejaVu Sans Mono", color="#15803D")
ax.text(X0 + 14 * CW, TOP + 11, "праворуч, доповнення зліва", ha="center", fontsize=11.5, color=MUTED)

for r, row in enumerate(ROWS):
    y = TOP - r * RH
    for k, ch in enumerate(row):
        pad = ch == " "
        sep = ch == "|"
        fc = "white" if sep else ("#F1F5F9" if pad else (BLUE if k < 10 else GREEN))
        ax.add_patch(FancyBboxPatch((X0 + k * CW + 0.2, y - 5), CW - 0.4, 10, boxstyle="round,pad=0,rounding_size=0.5",
                                    fc=fc, ec="#94A3B8" if pad else INK, lw=0.8, ls="--" if pad else "-"))
        ax.text(X0 + k * CW + CW / 2, y, "·" if pad else ch, ha="center", va="center", fontsize=15,
                color="#94A3B8" if pad else INK, fontfamily="DejaVu Sans Mono", fontweight="bold" if sep else "normal")
ax.text(X0 + 18 * CW + 4, TOP - 1.5 * RH, "сірі клітинки з крапкою —\nпробіли, які додало\nвирівнювання", fontsize=12,
        color=MUTED, va="center", linespacing=1.4)
save(fig, __file__)
