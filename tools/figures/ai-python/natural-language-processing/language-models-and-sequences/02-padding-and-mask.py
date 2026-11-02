"""Padding і маска для трьох речень лекції (індекси з виводу лекції)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

seqs = [[4, 5, 1], [6, 7, 8, 9, 10], [16]]
names = ["I love NLP", "Natural language processing is fascinating", "Text"]
fig, ax = canvas(12, 5.2)
ax.text(1, 96, "після padding (max_len = 5)", fontsize=13, fontweight="bold"); ax.text(62, 96, "маска (True = справжнє слово)", fontsize=13, fontweight="bold")
for r, (s, n) in enumerate(zip(seqs, names)):
    y = 66 - r * 28
    for i in range(5):
        real = i < len(s)
        box(ax, 1 + i * 10.5, y, 9.5, 16, str(s[i]) if real else "0", fc=GREEN if real else GREY, size=13, mono=True)
        box(ax, 62 + i * 7.5, y, 6.8, 16, "T" if real else "F", fc=GREEN if real else RED, size=12.5, mono=True)
    ax.text(1, y - 5, n, fontsize=10.5, color="#475569")
ax.text(56, 40, "→", fontsize=24, ha="center", va="center")
ax.text(81, 6, "довжини = 3, 5, 1", fontsize=12, ha="center", color="#475569")
save(fig, __file__)
