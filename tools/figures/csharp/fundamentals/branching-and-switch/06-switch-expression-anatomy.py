"""Анатомія switch expression (рядки з relational.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

MUTED = "#475569"
W, H = 15, 7.2
fig, ax = canvas(W, H)
SIZE = 17
CHAR = 0.602 * SIZE / 72 / (ax.get_position().width * W) * 100
LINE = 9.5
X0, Y0 = 24, 80
LINES = [
    'string kind = t switch',
    '{',
    '    < 0 => "мороз",',
    '    >= 10 and < 25 => "тепло",',
    '    _ => "немає даних",',
    '};',
]
# (рядок, початок, довжина, колір)
MARKS = [
    (0, 14, 1, BLUE), (0, 16, 6, AMBER),
    (2, 4, 3, GREEN), (2, 8, 2, GREY), (2, 11, 7, BLUE),
    (3, 4, 14, GREEN), (3, 29, 1, GREY),
    (4, 4, 1, GREEN),
    (5, 1, 1, GREY),
]
for line, start, length, color in MARKS:
    y = Y0 - line * LINE
    ax.add_patch(Rectangle((X0 + start * CHAR - 0.2, y - LINE / 2 + 0.6), length * CHAR + 0.4, LINE - 1.2, fc=color,
                           ec="none", zorder=1))
for i, text in enumerate(LINES):
    ax.text(X0, Y0 - i * LINE, text, fontsize=SIZE, fontfamily="DejaVu Sans Mono", va="center", zorder=2)


def note(line, col, text, tx, ty, ha="left"):
    x = X0 + col * CHAR
    y = Y0 - line * LINE
    ax.annotate(text, xy=(x, y + (LINE / 2 - 0.6) * (1 if ty > y else -1)), xytext=(tx, ty), fontsize=12.5,
                ha=ha, va="center", color=INK, linespacing=1.3,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.1))


note(0, 14.5, "вхідний вираз:\nщо перевіряється", 8, 97, ha="center")
note(0, 19, "switch стоїть\nпісля виразу", 52, 97)
note(2, 5.5, "шаблон", 4, 64, ha="center")
note(2, 9, "=> відділяє шаблон\nвід результату", 64, 66)
note(3, 11, "логічний шаблон:\nобидві умови", 4, 45, ha="center")
note(3, 29.5, "кома після\nкожної гілки", 75, 52)
note(4, 4.5, "_ — усе інше\n(discard)", 4, 29, ha="center")
note(5, 1.5, "; — кінець оператора:\nswitch тут є виразом", 44, 20)
ax.text(85, 30, "гілки (arms)\nперевіряються\nзгори вниз;\nрезультат — від\nпершої, що підійшла", fontsize=12.5,
        ha="center", va="center", color=MUTED, linespacing=1.35)
save(fig, __file__)
