"""Матриця співустрічності 6×6 для трьох речень лекції, вікно C = 2. Рахується прямо тут, без вигаданих чисел."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

sents = ["I love natural language processing", "Natural language is fascinating", "I love processing data"]
vocab = ["i", "love", "natural", "language", "processing", "data"]
idx = {w: i for i, w in enumerate(vocab)}
X = np.zeros((6, 6), int)
for s in sents:
    w = s.lower().split()
    for i, a in enumerate(w):
        for j in range(max(0, i - 2), min(len(w), i + 3)):
            if j != i and a in idx and w[j] in idx:
                X[idx[a], idx[w[j]]] += 1

fig, ax = plt.subplots(figsize=(7.4, 6.4))
ax.imshow(X, cmap="Blues", vmin=0, vmax=3)
ax.set_xticks(range(6)); ax.set_xticklabels(vocab, fontsize=12.5, rotation=35, ha="left"); ax.xaxis.tick_top()
ax.set_yticks(range(6)); ax.set_yticklabels(vocab, fontsize=12.5)
for i in range(6):
    for j in range(6):
        ax.text(j, i, str(X[i, j]), ha="center", va="center", fontsize=14, color="white" if X[i, j] >= 2 else INK, fontweight="bold" if X[i, j] else "normal")
ax.set_xlabel("слово в контексті", fontsize=12); ax.xaxis.set_label_position("top")
ax.set_ylabel("центральне слово", fontsize=12)
save(fig, __file__)
