"""Пам'ять для батча 32 × 50 слів: one-hot і embedding (словник 10 000, d = 100)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

fig, ax = plt.subplots(figsize=(8, 3.6))
ax.barh(["one-hot", "embedding"], [61.0, 0.62], color=["#DC2626", "#16A34A"], height=0.5)
ax.text(62, 0, "61,0 МБ", va="center", fontsize=13, fontweight="bold")
ax.text(1.6, 1, "0,62 МБ", va="center", fontsize=13, fontweight="bold")
ax.set_xlim(0, 80); ax.set_xlabel("МБ"); ax.invert_yaxis()
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
