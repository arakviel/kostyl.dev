"""UTF-16: літера кирилиці — один char, U+1D11E — сурогатна пара, й — одна або дві кодові точки (unicode.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, RED, canvas, save  # noqa: E402

MUTED = "#475569"
ROWS = [
    ("К", "U+041A", [("041A", BLUE)], "1 char: Length 1"),
    ("скрипковий ключ", "U+1D11E", [("D834", AMBER), ("DD1E", AMBER)],
     "сурогатна пара: Length 2, одна Rune"),
    ("й (складена)", "U+0439", [("0439", GREEN)], "Length 1"),
    ("й (розкладена)", "U+0438 + U+0306", [("0438", GREEN), ("0306", RED)],
     "и + бреве: Length 2, один текстовий елемент"),
]
fig, ax = canvas(15, 4.8)
ax.text(2, 95, "символ", fontsize=12.5, fontweight="bold")
ax.text(26, 95, "кодові точки Unicode", fontsize=12.5, fontweight="bold")
ax.text(48, 95, "char у рядку (UTF-16)", fontsize=12.5, fontweight="bold")
ax.text(72, 95, "що повертає", fontsize=12.5, fontweight="bold")
for r, (symbol, cp, units, note) in enumerate(ROWS):
    y = 76 - r * 19
    ax.text(2, y, symbol, fontsize=13.5, va="center")
    ax.text(26, y, cp, fontsize=12.5, va="center", fontfamily="DejaVu Sans Mono")
    for i, (unit, fc) in enumerate(units):
        ax.add_patch(Rectangle((48 + i * 10, y - 5), 10, 10, fc=fc, ec=INK, lw=1.2))
        ax.text(53 + i * 10, y, unit, ha="center", va="center", fontsize=13, fontfamily="DejaVu Sans Mono")
    ax.text(72, y, note, fontsize=12.5, va="center")
ax.set_ylim(10, 100)
save(fig, __file__)
