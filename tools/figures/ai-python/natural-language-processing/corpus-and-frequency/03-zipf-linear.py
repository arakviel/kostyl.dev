"""Частота від рангу для перших 100 слів, лінійна шкала."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import *
import numpy as np
from _data import freq, all_words, vocab_growth

top = freq.most_common(100)
f = [c for _, c in top]
fig, ax = plt.subplots(figsize=(9.5, 4.6))
ax.plot(range(1, 101), f, "o-", color="#2563EB", ms=3.5, lw=1.8)
ax.annotate(f"ранг 1: {f[0]:,}".replace(",", " "), (1, f[0]), xytext=(12, f[0] - 4000), fontsize=12, color="#16A34A", arrowprops=dict(arrowstyle="-", color="#16A34A"))
ax.annotate(f"ранг 100: {f[99]:,}".replace(",", " "), (100, f[99]), xytext=(70, 14000), fontsize=12, color="#D97706", arrowprops=dict(arrowstyle="-", color="#D97706"))
ax.set_xlabel("ранг слова"); ax.set_ylabel("частота"); ax.grid(alpha=0.3)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
