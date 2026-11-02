"""Біграмні ймовірності P(наступне | попереднє) для п'яти речень лекції. Рахуються тут."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

from collections import Counter
corpus = ["I love natural language processing", "natural language is fascinating", "I love processing data",
          "language models predict next word", "processing text with models"]
pairs = Counter(); prev = Counter()
for s in corpus:
    w = s.lower().split()
    for a, b in zip(w, w[1:]):
        pairs[(a, b)] += 1; prev[a] += 1
rows = ["i", "love", "natural", "language", "processing", "models"]
cols = sorted({b for (a, b) in pairs if a in rows}, key=lambda x: x)
M = np.array([[pairs[(a, b)] / prev[a] if prev[a] else 0 for b in cols] for a in rows])
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.imshow(M, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=40, ha="left", fontsize=12); ax.xaxis.tick_top()
ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows, fontsize=12.5)
for i in range(len(rows)):
    for j in range(len(cols)):
        if M[i, j]: ax.text(j, i, f"{M[i, j]:.2f}".replace(".", ","), ha="center", va="center", fontsize=11, color="white" if M[i, j] > 0.6 else INK)
ax.set_ylabel("попереднє слово", fontsize=12); ax.set_xlabel("наступне слово", fontsize=12); ax.xaxis.set_label_position("top")
save(fig, __file__)
