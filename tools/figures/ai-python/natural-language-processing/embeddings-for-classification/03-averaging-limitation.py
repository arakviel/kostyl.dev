"""Усереднення не бачить порядку. Косинуси — з виводу лекції (GloVe 100d)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw=dict(width_ratios=[1.1, 1]))
ax = axes[0]; ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
for r, ws in enumerate([("not", "good"), ("good", "not")]):
    y = 62 - r * 42
    for i, w in enumerate(ws):
        box(ax, 2 + i * 22, y, 19, 16, w, fc=RED if w == "not" else GREEN, size=13, mono=True)
    arrow(ax, 45, y + 8, 55, y + 8)
    box(ax, 57, y, 38, 16, "середнє", fc=BLUE, size=13)
ax.text(76, 40, "однаково", ha="center", fontsize=13, color="#DC2626", fontweight="bold")
ax.text(50, 95, "ті самі слова, інший порядок", ha="center", fontsize=12, color="#475569")
ax = axes[1]
labels = ["not good ↔ good not", "good, not bad ↔\nnot bad, good", "The movie is not terrible ↔\nThe movie is terrible"]
vals = [1.000, 0.938, 0.988]
ax.barh(range(3), vals, color="#2563EB", height=0.5)
for i, v in enumerate(vals): ax.text(v - 0.02, i, f"{v:.3f}".replace(".", ","), ha="right", va="center", color="white", fontsize=13, fontweight="bold")
ax.set_yticks(range(3)); ax.set_yticklabels(labels, fontsize=11); ax.invert_yaxis()
ax.set_xlim(0.8, 1.0); ax.set_xlabel("косинусна подібність усереднених векторів (вісь з 0,8)")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
