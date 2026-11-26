"""Ланцюжок методів рядка: кожен виклик створює новий рядок у купі, input не змінюється (modify.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save  # noqa: E402

MUTED = "#475569"
STEPS = [
    ("", "··НОВИЙ···звіт··", BLUE),
    ("Trim()", "НОВИЙ···звіт", GREY),
    ("ToLower()", "новий···звіт", GREY),
    ('Replace("··", "·")', "новий··звіт", GREY),
    ('Replace("··", "·")', "новий·звіт", GREEN),
]
fig, ax = canvas(15, 5.4)
ax.text(64, 96, "купа: п'ять окремих рядків", ha="center", fontsize=13, color=MUTED)
y = 82
for i, (call, value, fc) in enumerate(STEPS):
    yy = y - i * 17
    box(ax, 46, yy - 5, 34, 10, f"\"{value}\"", fc=fc, mono=True, size=14)
    if call:
        ax.add_patch(FancyArrowPatch((63, yy + 12), (63, yy + 5.8), arrowstyle="-|>", mutation_scale=14, lw=1.3,
                                     color=INK))
        ax.text(66, yy + 9, call, fontsize=12, fontfamily="DejaVu Sans Mono", va="center", color="#B45309")
    if 0 < i < 4:
        ax.text(83, yy, "проміжний: стає сміттям", fontsize=11.5, va="center", color=MUTED)

for name, yy, fc in [("input", 82, BLUE), ("result", 82 - 4 * 17, GREEN)]:
    ax.add_patch(Rectangle((6, yy - 5), 14, 10, fc=fc, ec=INK, lw=1.2))
    ax.text(13, yy, name, ha="center", va="center", fontsize=14, fontfamily="DejaVu Sans Mono")
    ax.add_patch(FancyArrowPatch((20.5, yy), (45.4, yy), arrowstyle="-|>", mutation_scale=16, lw=1.4, color=INK))
ax.text(13, 94, "змінні", ha="center", fontsize=13, color=MUTED)
ax.text(6, 40, "пробіли\nпоказано як ·", fontsize=11.5, color=MUTED, linespacing=1.3)
ax.set_ylim(8, 100)
save(fig, __file__)
