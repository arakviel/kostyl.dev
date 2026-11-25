"""Області видимості локальних змінних у scopes.cs: смуги показують рядки, де змінну можна використати."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, INK, canvas, save  # noqa: E402

CODE = [
    "int total = 0;",
    "for (int i = 1; i <= 2; i++)",
    "{",
    "    int square = i * i;",
    "    total += square;",
    "}",
    "{",
    "    int square = 100;",
    "    Console.WriteLine(square);",
    "}",
    "Console.WriteLine(total);",
]
fig, ax = canvas(15, 8.2)
TOP, STEP = 86, 7.2
MUTED = "#475569"


def y_of(line):  # line — номер рядка з 1
    return TOP - (line - 1) * STEP


# фон блоків
for first, last, color, label in [(2, 6, BLUE, "цикл for"), (7, 10, AMBER, "блок { }")]:
    y1, y2 = y_of(last) - STEP / 2 + 0.6, y_of(first) + STEP / 2 - 0.6
    ax.add_patch(FancyBboxPatch((3.5, y1), 41, y2 - y1, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=color, ec="none", alpha=0.75))
    ax.text(44, (y1 + y2) / 2, label, rotation=90, ha="right", va="center", fontsize=11, color=MUTED)

for n, text in enumerate(CODE, start=1):
    ax.text(1, y_of(n), f"{n:>2}", ha="left", va="center", fontsize=12, color="#94A3B8",
            fontfamily="DejaVu Sans Mono")
    ax.text(5, y_of(n), text, ha="left", va="center", fontsize=13.5, fontfamily="DejaVu Sans Mono")

# смуги областей видимості
BARS = [("total", 1, 11, GREEN), ("i", 2, 6, BLUE), ("square", 4, 6, BLUE), ("square", 8, 10, AMBER)]
for k, (name, first, last, color) in enumerate(BARS):
    x = 52 + k * 11.5
    y1, y2 = y_of(last) - 2.6, y_of(first) + 2.6
    ax.add_patch(FancyBboxPatch((x, y1), 7, y2 - y1, boxstyle="round,pad=0,rounding_size=1.5",
                                fc=color, ec=INK, lw=1.3))
    ax.text(x + 3.5, TOP + 7, name, ha="center", fontsize=13, fontweight="bold", fontfamily="DejaVu Sans Mono")
    ax.text(x + 3.5, y1 - 3, f"рядки {first}–{last}", ha="center", va="top", fontsize=11, color=MUTED)

ax.text(98, y_of(5), "дві різні змінні\nз одним іменем:\nблоки не вкладені\nодин в одний",
        ha="right", va="center", fontsize=12, color=INK, linespacing=1.35)
ax.add_patch(Rectangle((51, TOP + 5), 0.01, 0.01, fc="none", ec="none"))
save(fig, __file__)
