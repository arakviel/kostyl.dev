"""Довгий хвіст: скільки слів мають частоту 1, 2, 3, ... (реальні дані)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import *
import numpy as np
from _data import freq, all_words, vocab_growth

from collections import Counter
ff = Counter(freq.values())
xs = list(range(1, 31)); ys = [ff[x] for x in xs]
le5 = sum(ff[x] for x in range(1, 6))
fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.bar(xs, ys, color=["#16A34A"] + ["#2563EB"] * 29)
ax.text(1.8, ys[0], f"{ys[0]:,} слів — лише 1 раз".replace(",", " "), fontsize=12, color="#16A34A", va="center", fontweight="bold")
ax.text(12, ys[0] * 0.55, f"частота ≤ 5: {le5:,} слів\n= {le5 / len(freq) * 100:.1f}% словника".replace(",", " ").replace(".", ","), fontsize=12.5, color="#D97706", fontweight="bold",
        bbox=dict(fc="white", ec="#D97706", boxstyle="round,pad=0.4"))
ax.set_xlabel("скільки разів слово зустрілося (показано до 30)"); ax.set_ylabel("кількість таких слів")
print(ys[0], le5, le5 / len(freq))
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
