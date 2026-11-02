"""Речення «this movie is great»: мішок слів проти усередненого вектора (числа embedding — умовні, середнє рахується тут)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

words = ["this", "movie", "is", "great"]
V = np.array([[0.1, -0.2, 0.3], [0.4, 0.5, -0.1], [0.0, 0.1, 0.2], [0.9, 0.6, 0.4]])
avg = V.mean(0)
fig, ax = canvas(12, 6)
ax.text(1, 97, "Мішок слів: довжина = словник (10 000)", fontsize=13, fontweight="bold")
for i in range(14):
    hot = i in (2, 5, 9, 12)
    box(ax, 1 + i * 6.2, 72, 5.4, 11, "1" if hot else "0", fc=AMBER if hot else GREY, size=11, mono=True)
ax.text(1 + 14 * 6.2, 77.5, "… усього 10 000 клітинок, ненульових 4", fontsize=11, va="center", color="#475569")
ax.text(1, 56, "Усереднений вектор: довжина = d (тут 3, у GloVe 100)", fontsize=13, fontweight="bold")
for r, w in enumerate(words):
    y = 40 - r * 0 
    box(ax, 1 + r * 17, 36, 15, 12, w, fc=GREEN, size=12, mono=True)
    for j in range(3):
        pass
    ax.text(8.5 + r * 17, 31, "[" + ", ".join(f"{x:+.1f}" for x in V[r]) + "]", ha="center", fontsize=9.5, fontfamily="DejaVu Sans Mono")
    arrow(ax, 8.5 + r * 17, 28, 36, 20)
box(ax, 18, 6, 36, 12, "середнє: [" + ", ".join(f"{x:+.2f}" for x in avg) + "]", fc=BLUE, size=11.5, mono=True)
ax.text(62, 12, "← усі числа ненульові;\n    вектор речення", fontsize=11.5, va="center", color="#475569")
save(fig, __file__)
