"""Вивід лекції 05: однаковий мішок слів для речень з різним порядком. Словник: bad bites but dog good man not."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

vocab = ["bad", "bites", "but", "dog", "good", "man", "not"]
rows = [("dog bites man", [0,1,0,1,0,1,0]), ("man bites dog", [0,1,0,1,0,1,0]),
        ("not good but not bad", [1,0,1,0,1,0,2]), ("not bad but not good", [1,0,1,0,1,0,2])]
fig, ax = canvas(12, 5.6)
for i, w in enumerate(vocab):
    ax.text(40 + i * 8.2 + 3.6, 96, w, ha="center", fontsize=11.5, fontfamily="DejaVu Sans Mono", rotation=0)
for r, (t, v) in enumerate(rows):
    y = 76 - r * 21 - (6 if r >= 2 else 0)
    ax.text(1, y + 7, f"«{t}»", fontsize=12.5, va="center")
    for i, x in enumerate(v):
        box(ax, 40 + i * 8.2, y, 7.2, 14, str(x), fc=AMBER if x else GREY, size=12.5, mono=True)
for ya, yb in [(55, 76), (34 - 6, 55 - 6 + 0)]:
    pass
ax.text(104, 66, "однаковий\nвектор", fontsize=12, color="#DC2626", fontweight="bold", va="center", ha="center")
ax.text(104, 24, "однаковий\nвектор", fontsize=12, color="#DC2626", fontweight="bold", va="center", ha="center")
ax.set_xlim(0, 112)
save(fig, __file__)
