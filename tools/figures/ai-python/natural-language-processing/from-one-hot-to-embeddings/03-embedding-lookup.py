"""Таблиця embedding 6×4 з лекції (torch.manual_seed(0)) і вибір рядків 0, 2, 5."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

M = np.array([[-1.1258, -1.1524, -0.2506, -0.4339], [0.8487, 0.6920, -0.3160, -2.1152],
              [0.4681, -0.1577, 1.4437, 0.2660], [0.1665, 0.8744, -0.1435, -0.1116],
              [0.9318, 1.2590, 2.0050, 0.0537], [0.6181, -0.4128, -0.8411, -2.3160]])
words = ["king", "queen", "man", "woman", "cat", "dog"]
pick = [0, 2, 5]
fig, ax = canvas(13, 6)
ax.set_xlim(0, 112)
ax.text(30, 98, "embedding.weight (6 × 4)", ha="center", fontsize=13, fontweight="bold")
ax.text(88, 98, "embedding([0, 2, 5])", ha="center", fontsize=13, fontweight="bold")
cw, ch = 9.6, 11
for i in range(6):
    y = 80 - i * 14
    ax.text(3, y + ch / 2, str(i), ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(7, y + ch / 2, words[i], ha="left", va="center", fontsize=11, color="#475569", fontfamily="DejaVu Sans Mono")
    for j in range(4):
        box(ax, 22 + j * (cw + 0.8), y, cw, ch, f"{M[i, j]:+.2f}", fc=AMBER if i in pick else "white", size=10.5, mono=True)
for k, i in enumerate(pick):
    y = 80 - k * 14
    for j in range(4):
        box(ax, 68 + j * (cw + 0.8), y, cw, ch, f"{M[i, j]:+.2f}", fc=AMBER, size=10.5, mono=True)
    ax.text(65, y + ch / 2, f"[{i}]", ha="right", va="center", fontsize=11, color="#475569")
ax.text(30, 4, "номер слова = номер рядка", ha="center", fontsize=12, color="#475569")
ax.text(88, 38, "три слова — три вектори", ha="center", fontsize=12, color="#475569")
save(fig, __file__)
