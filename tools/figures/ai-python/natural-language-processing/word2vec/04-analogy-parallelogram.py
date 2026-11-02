"""Ілюстрація аналогії king − man + woman ≈ queen з вигаданими координатами (щоб показати геометрію)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

P = {"man": (1, 1), "woman": (1, 3), "king": (4, 2), "queen": (4, 4)}
fig, ax = plt.subplots(figsize=(7.4, 5.8))
for w, (x, y) in P.items():
    col = "#16A34A" if w in ("man", "woman") else "#2563EB"
    ax.scatter([x], [y], s=240, color=col, edgecolor=INK, lw=1.4, zorder=3)
    ax.annotate(w, (x, y), xytext=(10, 8), textcoords="offset points", fontsize=14, fontweight="bold", color=col)
def vec(a, b, col, lab, off):
    ax.annotate("", xy=P[b], xytext=P[a], arrowprops=dict(arrowstyle="-|>", lw=2.4, color=col), zorder=2)
    mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
    ax.text(mx + off[0], my + off[1], lab, color=col, fontsize=12, fontweight="bold", va="center")
vec("man", "woman", "#D97706", "+ «жіночість»", (0.08, 0))
vec("king", "queen", "#D97706", "те саме зміщення", (0.08, 0))
ax.plot([1, 4], [1, 2], color="#94A3B8", lw=1.2, ls="--"); ax.plot([1, 4], [3, 4], color="#94A3B8", lw=1.2, ls="--")
ax.set_xlim(0, 5.6); ax.set_ylim(0, 5); ax.set_xlabel("вимір 1"); ax.set_ylabel("вимір 2"); ax.grid(alpha=0.25)
ax.text(2.4, 0.4, "king − man + woman = (4, 2) − (1, 1) + (1, 3) = (4, 4) = queen", fontsize=11.5, ha="center", bbox=dict(fc=AMBER, ec=INK, boxstyle="round,pad=0.35"))
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
