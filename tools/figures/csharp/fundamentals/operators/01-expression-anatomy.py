"""Анатомія виразу: операнди, оператори, підвираз; унарні, бінарні і тернарний оператори."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, anatomy, box, save  # noqa: E402

MUTED = "#475569"
LINE = "int total = price * count - discount;"
MARKS = [(0, 4, 5, GREY), (0, 10, 1, AMBER), (0, 12, 5, BLUE), (0, 18, 1, AMBER), (0, 20, 5, BLUE),
         (0, 26, 1, AMBER), (0, 28, 8, BLUE)]
NOTES = [
    (0, 6.5, "змінна, яка отримає\nзначення виразу", 12, 96, "center"),
    (0, 10.5, "= теж оператор:\nприсвоєння, виконується\nостаннім", 34, 96, "center"),
    (0, 14.5, "операнди — значення, з якими\nпрацюють оператори: змінні,\nлітерали, виклики методів", 62, 96, "center"),
    (0, 18.5, "* і − — бінарні\nоператори", 88, 96, "center"),
]
SIZE = 20
fig, ax = anatomy(15, 6.6, [LINE], MARKS, NOTES, size=SIZE, x0=12, y0=66, step=12)
char = 0.602 * SIZE / 72 / (ax.get_position().width * 15) * 100


def bracket(c1, c2, y, text, color):
    x1, x2 = 12 + c1 * char, 12 + c2 * char
    ax.plot([x1, x1, x2, x2], [y + 2, y, y, y + 2], color=color, lw=1.8)
    ax.text((x1 + x2) / 2, y - 2.5, text, ha="center", va="top", fontsize=12.5, color=color, linespacing=1.3)


bracket(12, 25, 56, "підвираз price * count:\nмає власне значення", "#16A34A")
bracket(12, 36, 36, "", "#2563EB")
ax.text(12 + 37 * char, 39, "увесь вираз праворуч від =\nмає значення типу int", ha="left", va="top", fontsize=12.5,
        color="#2563EB", linespacing=1.3)

KINDS = [
    ("унарні — один операнд", "-x    !done    ~mask\n++i   i++", GREEN),
    ("бінарні — два операнди", "a + b    x < y\nok && ready", BLUE),
    ("тернарний — три операнди", "c ? a : b", AMBER),
]
for k, (title, code, color) in enumerate(KINDS):
    x = 4 + k * 32
    ax.text(x + 14, 22, title, ha="center", va="center", fontsize=13, fontweight="bold")
    box(ax, x, 2, 28, 15, code, fc=color, mono=True, size=13.5)
save(fig, __file__)
