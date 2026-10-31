"""Скільки слів потрібно, щоб покрити задану частку тексту."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import *
from _data import counts

f = np.array(sorted(counts.values(), reverse=True))
cum = np.cumsum(f) / f.sum()
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.semilogx(np.arange(1, len(f) + 1), cum * 100, color="#2563EB", lw=2.4)
for p, c in ((50, "#16A34A"), (80, "#D97706"), (90, "#DC2626"), (95, "#7C3AED")):
    n = int(np.searchsorted(cum, p / 100)) + 1
    ax.plot([n], [p], "o", color=c, ms=9)
    ax.annotate(f"{p}% тексту\n= {n:,} слів".replace(",", " "), (n, p), textcoords="offset points", xytext=(12, -34), fontsize=11, color=c, fontweight="bold")
ax.set_xlabel("кількість найчастіших слів (логарифмічна шкала)")
ax.set_ylabel("частка тексту, %")
ax.set_ylim(0, 105)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
save(fig, __file__)
