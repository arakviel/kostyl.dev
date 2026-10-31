"""Один рядок — три токенізатори."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 4.2)
ax.text(1, 95, "Рядок:", fontsize=12, fontweight="bold")
ax.text(11, 95, "Don't stop, it's 3.5 USD!", fontsize=13, fontfamily="DejaVu Sans Mono")
rows = [
    ("split()", ["Don't", "stop,", "it's", "3.5", "USD!"], AMBER),
    ("word_tokenize", ["Do", "n't", "stop", ",", "it", "'s", "3.5", "USD", "!"], GREEN),
    ("wordpunct", ["Don", "'", "t", "stop", ",", "it", "'", "s", "3", ".", "5", "USD", "!"], RED),
]
for i, (name, toks, fc) in enumerate(rows):
    y = 62 - i * 24
    ax.text(1, y + 4.5, f"{name}\n{len(toks)} токенів", fontsize=12, fontweight="bold", va="center", linespacing=1.5)
    chips(ax, 21, y, toks, fc=fc, h=9, size=11, char_w=1.25, pad=1.8, gap=0.8)
save(fig, __file__)
