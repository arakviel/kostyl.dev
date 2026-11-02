"""Розмір словника залежно від кількості відгуків (seed 42, як у клітинці лекції)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import *
import numpy as np
from _data import freq, all_words, vocab_growth

sizes, vs = vocab_growth()
fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.plot(sizes, vs, "o-", color="#2563EB", lw=2.4)
for x, v in zip(sizes, vs):
    if x in (10, 100, 1000, 2000): ax.annotate(f"{v:,}".replace(",", " "), (x, v), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=11.5, fontweight="bold")
ax.set_xlabel("кількість відгуків"); ax.set_ylabel("унікальних слів"); ax.grid(alpha=0.3)
print(vs)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
