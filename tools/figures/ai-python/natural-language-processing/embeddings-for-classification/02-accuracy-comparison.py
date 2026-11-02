"""Accuracy на повному тесті IMDB (25 000 відгуків), числа з виводів лекції."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

names = ["GloVe 100d\nнаївна токенізація", "GloVe 100d\nочищені токени", "GloVe 300d\nочищені токени", "Мішок слів\n5000 слів"]
vals = [78.4, 79.7, 83.4, 85.0]
fig, ax = plt.subplots(figsize=(9.5, 4.8))
bars = ax.bar(range(4), vals, color=["#94A3B8", "#16A34A", "#16A34A", "#2563EB"], width=0.6)
for i, v in enumerate(vals): ax.text(i, v + 0.3, f"{v}%".replace(".", ","), ha="center", fontsize=13, fontweight="bold")
ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=11.5)
ax.set_ylim(70, 88); ax.set_ylabel("accuracy на тесті, % (вісь з 70)")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
