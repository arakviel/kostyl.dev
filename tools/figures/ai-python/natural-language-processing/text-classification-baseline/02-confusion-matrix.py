"""Матриця помилок з виводу лекції 06: 163, 37, 25, 175."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

cm = np.array([[163, 37], [25, 175]])
fig, ax = plt.subplots(figsize=(6.4, 5.6))
ax.imshow(np.array([[1, 0], [0, 1]]), cmap="Greens", vmin=0, vmax=2.2)
names = [["TN", "FP"], ["FN", "TP"]]; expl = [["правильно\nнегативні", "помилково\nпозитивні"], ["помилково\nнегативні", "правильно\nпозитивні"]]
for i in range(2):
    for j in range(2):
        ok = i == j
        ax.text(j, i - 0.12, str(cm[i, j]), ha="center", va="center", fontsize=30, fontweight="bold", color="#166534" if ok else "#B91C1C")
        ax.text(j, i + 0.22, f"{names[i][j]}: {expl[i][j]}", ha="center", va="center", fontsize=11, color=INK)
ax.set_xticks([0, 1]); ax.set_xticklabels(["negative", "positive"], fontsize=13); ax.set_yticks([0, 1]); ax.set_yticklabels(["negative", "positive"], fontsize=13)
ax.set_xlabel("передбачено", fontsize=13); ax.set_ylabel("справжній клас", fontsize=13); ax.xaxis.set_label_position("top"); ax.xaxis.tick_top()
fig.text(0.5, 0.02, "правильно 338 з 400 (84,5%), помилок 62", ha="center", fontsize=12, color="#475569")
save(fig, __file__)
