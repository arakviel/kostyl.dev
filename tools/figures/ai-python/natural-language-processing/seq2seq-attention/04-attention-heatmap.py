"""Ваги уваги реальної моделі seq2seq (GRU + dot-product attention) на задачі розвороту послідовності."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

import numpy as np
ids = [5, 9, 3, 4, 11, 4, 8, 3]
pred = [3, 8, 4, 11, 4, 3, 9, 5, 2]
W = np.array([[0.0, 0.0, 0.02, 0.01, 0.01, 0.02, 0.08, 0.85], [0.0, 0.0, 0.02, 0.01, 0.01, 0.02, 0.15, 0.78], [0.0, 0.01, 0.01, 0.02, 0.02, 0.08, 0.72, 0.14], [0.0, 0.01, 0.01, 0.12, 0.15, 0.6, 0.09, 0.02], [0.01, 0.03, 0.06, 0.07, 0.58, 0.21, 0.02, 0.02], [0.02, 0.05, 0.1, 0.47, 0.11, 0.21, 0.02, 0.02], [0.03, 0.1, 0.64, 0.13, 0.04, 0.02, 0.01, 0.03], [0.12, 0.66, 0.15, 0.02, 0.02, 0.01, 0.01, 0.0], [0.56, 0.28, 0.06, 0.03, 0.03, 0.02, 0.02, 0.01]])
sym = lambda i: "‹eos›" if i == 2 else str(i - 3)
fig, ax = plt.subplots(figsize=(7.2, 6))
im = ax.imshow(W, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(8)); ax.set_xticklabels([sym(i) for i in ids], fontsize=13)
ax.set_yticks(range(9)); ax.set_yticklabels([sym(i) for i in pred], fontsize=13)
ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")
ax.set_xlabel("вхід (що читає енкодер)", fontsize=13); ax.set_ylabel("вихід (що генерує декодер)", fontsize=13)
for i in range(9):
    for j in range(8):
        if W[i, j] >= 0.1:
            ax.text(j, i, f"{W[i, j]:.2f}", ha="center", va="center", fontsize=10.5, color="white" if W[i, j] > 0.5 else INK)
fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
save(fig, __file__)
