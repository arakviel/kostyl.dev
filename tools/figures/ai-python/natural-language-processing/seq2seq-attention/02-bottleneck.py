"""Точність (точний збіг) на задачі «розвернути послідовність» залежно від довжини. Реальний запуск, 3000 кроків, hidden = 64, GRU + dot-product attention, по 500 прикладів на групу."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

labels = ["3–6", "7–12", "13–18", "19–24"]
noatt = [99.8, 82.8, 20.8, 0.2]
att = [99.8, 98.6, 96.2, 87.6]
import numpy as np
x = np.arange(4); w = 0.36
fig, ax = plt.subplots(figsize=(9, 4.6))
b1 = ax.bar(x - w / 2, noatt, w, color="#DC2626", label="без уваги (один вектор c)")
b2 = ax.bar(x + w / 2, att, w, color="#2563EB", label="з увагою")
for bars in (b1, b2):
    for b in bars: ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5, f"{b.get_height():.0f}%", ha="center", fontsize=12)
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_xlabel("довжина послідовності (символів)")
ax.set_ylabel("правильно відтворено, %"); ax.set_ylim(0, 118); ax.legend(frameon=False, loc="upper center", ncol=2)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
