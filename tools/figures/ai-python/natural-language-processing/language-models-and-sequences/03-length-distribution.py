"""Довжини 5000 випадкових відгуків IMDB (train, shuffle seed=42), реальні дані.
Запуск: uv run --python 3.13 --with matplotlib --with numpy --with datasets python <файл>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

from datasets import load_dataset
ds = load_dataset("stanfordnlp/imdb", split="train").shuffle(seed=42).select(range(5000))
L = np.array([len(t.split()) for t in ds["text"]])
mean, p95 = L.mean(), np.percentile(L, 95)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.hist(L, bins=50, color="#2563EB", alpha=0.85, edgecolor="white")
ax.axvline(mean, color="#DC2626", ls="--", lw=2.2, label=f"середня: {mean:.0f}")
ax.axvline(p95, color="#D97706", ls="--", lw=2.2, label=f"95-й перцентиль: {p95:.0f}")
ax.set_xlabel("довжина відгуку, слів"); ax.set_ylabel("кількість відгуків"); ax.legend(frameon=False, fontsize=12)
print("max", L.max())
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
