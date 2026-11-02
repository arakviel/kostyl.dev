"""Матриця уваги: звичайна (енкодер) і з причинною маскою (декодер). Числа з реального обчислення (seed 1)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

import numpy as np
words = ["the", "cat", "sat", "down"]
A = np.array([[0.10,0.52,0.36,0.02],[0.60,0.19,0.09,0.13],[0.26,0.14,0.24,0.36],[0.12,0.31,0.55,0.02]])
Ac = np.array([[1.0,0,0,0],[0.76,0.24,0,0],[0.41,0.22,0.38,0],[0.12,0.31,0.55,0.02]])
fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
for ax, M, t in zip(axes, (A, Ac), ("без маски (енкодер)", "з причинною маскою (декодер)")):
    ax.imshow(M, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(4)); ax.set_xticklabels(words, fontsize=13); ax.set_yticks(range(4)); ax.set_yticklabels(words, fontsize=13)
    ax.xaxis.tick_top(); ax.set_title(t, fontsize=13, pad=34)
    for i in range(4):
        for j in range(4):
            lbl = "×" if (M is Ac and j > i) else f"{M[i, j]:.2f}"
            ax.text(j, i, lbl, ha="center", va="center", fontsize=12, color="white" if M[i, j] > 0.5 else (("#94A3B8") if lbl == "×" else INK))
axes[0].set_ylabel("слово-запит", fontsize=12)
fig.text(0.5, -0.02, "стовпець — слово, на яке дивимось", ha="center", fontsize=12)
save(fig, __file__)
