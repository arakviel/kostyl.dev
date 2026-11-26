"""Трасування вкладених циклів з nested.cs: значення i і j на кожній перевірці внутрішньої умови."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save  # noqa: E402

COLORS = {1: BLUE, 2: GREEN, 3: AMBER, 4: GREY}
ROWS = [
    (1, "1", "1 <= 1 — true", "друк  1"),
    (1, "2", "2 <= 1 — false", "новий рядок"),
    (2, "1", "1 <= 2 — true", "друк  2"),
    (2, "2", "2 <= 2 — true", "друк  4"),
    (2, "3", "3 <= 2 — false", "новий рядок"),
    (3, "1", "1 <= 3 — true", "друк  3"),
    (3, "2", "2 <= 3 — true", "друк  6"),
    (3, "3", "3 <= 3 — true", "друк  9"),
    (3, "4", "4 <= 3 — false", "новий рядок"),
    (4, "—", "i <= 3: 4 <= 3 — false", "кінець"),
]
COLS = [(1, 7, "i"), (8, 7, "j"), (15, 31, "перевірка"), (46, 19, "дія")]
STEP = 8.0

fig, ax = canvas(15, 7.4)
y = 94
for x, w, title in COLS:
    ax.text(x + w / 2, y, title, ha="center", va="center", fontsize=13.5, fontweight="bold")
for r, (i, j, check, action) in enumerate(ROWS):
    y = 86 - r * STEP
    ax.add_patch(Rectangle((1, y - STEP / 2 + 0.4), 64, STEP - 0.8, fc=COLORS[i], ec="none"))
    false = "false" in check
    cells = [str(i), j, check, action]
    for (x, w, _), text in zip(COLS, cells):
        ax.text(x + w / 2, y, text, ha="center", va="center", fontsize=13, fontfamily="DejaVu Sans Mono",
                color="#DC2626" if false and text == check else INK)

# консоль
ax.text(82, 94, "вивід", ha="center", va="center", fontsize=13.5, fontweight="bold")
box(ax, 70, 52, 24, 34, "", fc="white")
for k, line in enumerate(["  1", "  2  4", "  3  6  9"]):
    ly = 79 - k * 9
    ax.add_patch(Rectangle((71.5, ly - 3.6), 21, 7.2, fc=COLORS[k + 1], ec="none"))
    ax.text(72.5, ly, line, va="center", fontsize=15, fontfamily="DejaVu Sans Mono")
ax.text(82, 38, "тіло внутрішнього циклу:\n1 + 2 + 3 = 6 разів;\nумова внутрішнього\nциклу: 9 перевірок",
        ha="center", va="center", fontsize=12.5, linespacing=1.4)
ax.set_ylim(8, 100)
save(fig, __file__)
