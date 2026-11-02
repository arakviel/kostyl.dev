"""20 найчастіших слів корпусу movie_reviews (реальні дані)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import *
import numpy as np
from _data import freq, all_words, vocab_growth

top = freq.most_common(20)
words, counts = zip(*top)
fig, ax = plt.subplots(figsize=(11, 4.8))
cols = ["#D97706" if w == "s" else ("#2563EB" if w == "film" else "#94A3B8") for w in words]
ax.bar(range(20), counts, color=cols)
for i in (0, 1, 19): ax.text(i, counts[i] + 800, f"{counts[i]:,}".replace(",", " "), ha="center", fontsize=11, fontweight="bold")
ax.set_xticks(range(20)); ax.set_xticklabels(words, rotation=45, ha="right", fontsize=12)
ax.set_ylabel("скільки разів зустрілося")
ax.text(9, 60000, "сірі — службові слова\nсиній — слово зі змістом (film)\nжовтий — залишок «'s» після токенізації", fontsize=11.5, color="#475569")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
