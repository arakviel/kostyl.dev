"""25 найчастіших слів: перше і двадцять п'яте (реальні дані)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import *
import numpy as np
from _data import freq, all_words, vocab_growth

top = freq.most_common(25)
words, counts = zip(*top)
fig, ax = plt.subplots(figsize=(11, 4.6))
cols = ["#16A34A"] + ["#2563EB"] * 23 + ["#D97706"]
ax.bar(range(25), counts, color=cols)
ax.text(0, counts[0] + 800, f"{counts[0]:,}".replace(",", " "), ha="center", fontsize=11, fontweight="bold")
ax.text(24, counts[24] + 800, f"{counts[24]:,}".replace(",", " "), ha="center", fontsize=11, fontweight="bold")
ax.set_xticks(range(25)); ax.set_xticklabels(words, rotation=60, ha="right", fontsize=11.5)
ax.set_ylabel("скільки разів зустрілося")
for s in ("top", "right"): ax.spines[s].set_visible(False)
print(top[-1], counts[0] / counts[-1])
save(fig, __file__)
