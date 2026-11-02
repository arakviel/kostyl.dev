"""F1 на навчанні й тесті залежно від розміру словника (вивід лекції 06)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

sizes = [500, 1000, 2000, 5000, 10000, 20000]
tr = [0.976, 1.0, 1.0, 1.0, 1.0, 1.0]; te = [0.726, 0.775, 0.832, 0.850, 0.846, 0.851]
fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.plot(range(6), tr, "o-", color="#2563EB", lw=2.4, label="навчання")
ax.plot(range(6), te, "s-", color="#16A34A", lw=2.4, label="тест")
for i, v in enumerate(te): ax.text(i, v - 0.035, f"{v:.3f}".replace(".", ","), ha="center", fontsize=11, color="#166534")
ax.fill_between(range(3, 6), te[3:], tr[3:], color="#FEE2E2", alpha=0.7); ax.text(4, 0.92, "розрив = перенавчання", ha="center", fontsize=12, color="#B91C1C")
ax.set_xticks(range(6)); ax.set_xticklabels([f"{s:,}".replace(",", " ") for s in sizes]); ax.set_xlabel("розмір словника (max_features)"); ax.set_ylabel("F1-score")
ax.set_ylim(0.65, 1.04); ax.grid(alpha=0.3); ax.legend(frameon=False, loc="center left")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
