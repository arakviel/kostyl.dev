"""One-hot і embedding для слів king і cat з лекції (словник із 6 слів, embedding із 2 чисел)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

vocab = ["king", "queen", "man", "woman", "cat", "dog"]
emb = {"king": [0.8, 0.6], "cat": [-0.3, 0.5]}
fig, ax = canvas(12, 5.4)
ax.text(2, 96, "One-hot: 6 чисел, одна 1", fontsize=14, fontweight="bold")
ax.text(66, 96, "Embedding: 2 числа", fontsize=14, fontweight="bold")
for r, w in enumerate(["king", "cat"]):
    y = 66 - r * 36
    ax.text(1, y + 6, w, fontsize=13, va="center", fontfamily="DejaVu Sans Mono", fontweight="bold")
    for i in range(6):
        hot = vocab[i] == w
        box(ax, 12 + i * 7.6, y, 6.8, 12, "1" if hot else "0", fc=AMBER if hot else GREY, size=13, mono=True)
    arrow(ax, 59, y + 6, 66, y + 6)
    for j, val in enumerate(emb[w]):
        box(ax, 68 + j * 14, y, 13, 12, f"{val:+.1f}", fc=BLUE, size=13, mono=True)
ax.text(30, 8, "жодна клітинка не говорить про зміст слова", ha="center", fontsize=11.5, color="#475569")
ax.text(82, 8, "числа описують слово", ha="center", fontsize=11.5, color="#475569")
ax.text(50, -6, "У реальних моделях: one-hot має довжину словника (тисячі), embedding — 50–300 чисел", ha="center", fontsize=11.5, color="#475569")
save(fig, __file__)
