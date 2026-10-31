"""Токени (усі входження) і типи (унікальні слова)."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

toks = ["the", "cat", "sat", "on", "the", "mat", ".", "the", "dog", "sat", "on", "the", "log", "."]
seen = {}
pal = [BLUE, GREEN, AMBER, GREY, RED, "#EDE9FE", "#CFFAFE", "#FCE7F3"]
colors = []
for t in toks:
    if t not in seen:
        seen[t] = pal[len(seen) % len(pal)]
    colors.append(seen[t])
fig, ax = canvas(12, 4.4)
ax.text(1, 92, "14 токенів (кожне входження)", fontsize=13, fontweight="bold")
chips(ax, 1, 72, toks[:7], h=10, colors=colors[:7], char_w=2.0, pad=3.5)
chips(ax, 1, 58, toks[7:], h=10, colors=colors[7:], char_w=2.0, pad=3.5)
ax.text(1, 42, "8 типів (унікальні слова)", fontsize=13, fontweight="bold")
chips(ax, 1, 22, list(seen), h=10, colors=list(seen.values()), char_w=2.0, pad=3.5)
save(fig, __file__)
