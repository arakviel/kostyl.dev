"""Метрики з виводу лекції 06 (тест 400 відгуків)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

cls = ["негативний", "позитивний"]
P = [0.867, 0.825]; R = [0.815, 0.875]; F = [0.840, 0.850]
fig, ax = plt.subplots(figsize=(9.5, 4.8))
x = np.arange(2); w = 0.25
for k, (vals, name, col) in enumerate([(P, "precision", "#2563EB"), (R, "recall", "#16A34A"), (F, "F1", "#D97706")]):
    b = ax.bar(x + (k - 1) * w, vals, w, color=col, label=name)
    for xi, v in zip(x + (k - 1) * w, vals): ax.text(xi, v + 0.008, f"{v:.3f}".replace(".", ","), ha="center", fontsize=11.5)
ax.set_xticks(x); ax.set_xticklabels(cls, fontsize=13); ax.set_ylim(0.7, 0.93); ax.set_ylabel("значення метрики (вісь з 0,7)")
ax.axhline(0.845, color="#64748B", ls="--", lw=1.6, label="accuracy = 0,845")
ax.legend(frameon=False, ncol=4, loc="upper center")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
