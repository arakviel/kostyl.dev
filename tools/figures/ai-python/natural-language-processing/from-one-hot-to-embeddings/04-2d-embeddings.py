"""Іграшкові вектори з лекції на площині; підписані реальні відстані."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

E = {"king": (0.8, 0.6), "queen": (0.7, 0.7), "man": (0.6, 0.3), "woman": (0.5, 0.6), "cat": (-0.3, 0.5), "dog": (-0.2, 0.4)}
fig, ax = plt.subplots(figsize=(8.4, 6))
for w, (x, y) in E.items():
    col = "#2563EB" if w in ("king", "queen", "man", "woman") else "#16A34A"
    ax.scatter([x], [y], s=260, color=col, edgecolor=INK, lw=1.4, zorder=3)
    ax.annotate(w, (x, y), xytext=(0, 14), textcoords="offset points", ha="center", fontsize=13)
def link(a, b, label, pos, col="#D97706"):
    (x1, y1), (x2, y2) = E[a], E[b]
    ax.plot([x1, x2], [y1, y2], color=col, lw=1.6, ls="--", zorder=2)
    ax.text(pos[0], pos[1], label, ha="center", fontsize=12, color=col, fontweight="bold")
link("king", "queen", "0,141", (0.9, 0.67))
link("cat", "dog", "0,141", (-0.36, 0.45))
link("king", "cat", "1,105", (0.1, 0.585))
ax.set_xlim(-0.6, 1.1); ax.set_ylim(0.1, 0.95)
ax.set_xlabel("ознака 1: людина (+) чи тварина (−)"); ax.set_ylabel("ознака 2: жива істота, що діє")
ax.grid(alpha=0.25)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
