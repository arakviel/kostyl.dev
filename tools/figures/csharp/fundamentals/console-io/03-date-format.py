"""Рядок формату дати dd.MM.yyyy HH:mm: що означає кожен специфікатор (dates.cs, 25.11.2026 14:30:05)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, arrow, box, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(15, 6.8)
PARTS = [("dd", "25", "день,\n2 цифри", BLUE), (".", ".", None, GREY), ("MM", "11", "місяць —\nвеликі M", GREEN),
         (".", ".", None, GREY), ("yyyy", "2026", "рік,\n4 цифри", BLUE), (" ", " ", None, GREY),
         ("HH", "14", "години\n0–23", AMBER), (":", ":", None, GREY), ("mm", "30", "хвилини —\nмалі m", AMBER)]
x = 6
for spec, value, label, color in PARTS:
    w = 4 + 2.2 * len(spec) if spec.strip() else 2.5
    if spec.strip() and label:
        box(ax, x, 74, w, 10, spec, fc=color, mono=True, size=17)
        box(ax, x, 44, w, 10, value, fc="white", mono=True, size=17)
        arrow(ax, x + w / 2, 73, x + w / 2, 55.5)
        ax.text(x + w / 2, 40, label, ha="center", va="top", fontsize=11.5, color=MUTED, linespacing=1.3)
    else:
        ax.text(x + w / 2, 79, spec, ha="center", va="center", fontsize=17, fontfamily="DejaVu Sans Mono")
        ax.text(x + w / 2, 49, value, ha="center", va="center", fontsize=17, fontfamily="DejaVu Sans Mono")
    x += w + 1.2

ax.text(6, 92, "формат", fontsize=13, fontweight="bold")
ax.text(22, 92, "для моменту 25.11.2026 14:30:05", fontsize=12, color=MUTED)
box(ax, 62, 6, 36, 12, "yyyy-mm-dd  →  2026-30-25", fc=RED, mono=True, size=14)
ax.text(60, 12, "пастка: mm — хвилини, а не місяць", ha="right", va="center", fontsize=12.5, color="#DC2626")
save(fig, __file__)
