"""Символ, код Unicode і байти UTF-8 для чотирьох знаків."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

items = [("c", "U+0063", "63", 1, BLUE), ("ї", "U+0457", "D1 97", 2, GREEN),
         ("€", "U+20AC", "E2 82 AC", 3, AMBER), ("🐱", "U+1F431", "F0 9F 90 B1", 4, RED)]
fig, ax = canvas(11, 4.4)
for i, (ch, cp, hx, n, fc) in enumerate(items):
    x = 2 + i * 25
    ax.text(x + 10, 88, ch, ha="center", va="center", fontsize=30, fontfamily="DejaVu Sans")
    ax.text(x + 10, 68, cp, ha="center", fontsize=12, fontfamily="DejaVu Sans Mono")
    arrow(ax, x + 10, 63, x + 10, 52)
    for k in range(n):
        w = 20 / 4
        box(ax, x + (20 - n * w) / 2 + k * w, 28, w - 0.6, 20, "", fc=fc)
    ax.text(x + 10, 17, hx, ha="center", fontsize=12, fontfamily="DejaVu Sans Mono")
    ax.text(x + 10, 6, f"{n} байт" if n > 1 else "1 байт", ha="center", fontsize=12, fontweight="bold")
save(fig, __file__)
