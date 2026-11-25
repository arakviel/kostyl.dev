"""Анатомія оголошення змінної: явний тип, var і const."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, box, canvas, save  # noqa: E402

WIDTH = 15
fig, ax = canvas(WIDTH, 8.2)
CHAR = 0.602 * 19 / 72 / WIDTH * 100  # ширина символу DejaVu Sans Mono 19 pt у координатах 0..100
MUTED = "#475569"

ROWS = [
    ("Явний тип", 80, [("int", BLUE, "тип"), ("age", GREEN, "ім'я\n(camelCase)"), ("=", GREY, None),
                       ("19", AMBER, "ініціалізатор:\nлітерал типу int"), (";", GREY, None)]),
    ("var", 48, [("var", BLUE, "тип виводить\nкомпілятор: string"), ("title", GREEN, "ім'я"), ("=", GREY, None),
                 ('"Звіт"', AMBER, "ініціалізатор\nобов'язковий"), (";", GREY, None)]),
    ("const", 16, [("const", RED, "змінити\nне можна"), ("int", BLUE, "тип"),
                   ("MaxScore", GREEN, "ім'я\n(PascalCase)"), ("=", GREY, None),
                   ("100", AMBER, "значення відоме\nпід час компіляції"), (";", GREY, None)]),
]

for title, y, tokens in ROWS:
    ax.text(2, y + 4.5, title, fontsize=15, fontweight="bold", va="center")
    x = 22
    for text, color, label in tokens:
        w = len(text) * CHAR + 4.5
        box(ax, x, y, w, 9, text, fc=color, mono=True, size=19)
        if label:
            cx = x + w / 2
            ax.plot([cx, cx], [y - 1.2, y - 4.5], color=MUTED, lw=1.1)
            ax.text(cx, y - 5.3, label, ha="center", va="top", fontsize=12, color=MUTED, linespacing=1.25)
        x += w + 2.2

save(fig, __file__)
