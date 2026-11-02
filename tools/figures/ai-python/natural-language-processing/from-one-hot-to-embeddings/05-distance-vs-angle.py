"""Два вектори в один бік, але різної довжини: відстань велика, косинус = 1."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

fig, ax = plt.subplots(figsize=(7, 5.6))
for (x, y), col, lab, off in [((1, 1), "#2563EB", "u = [1, 1]", (0.4, -1.0)), ((10, 10), "#DC2626", "v = [10, 10]", (-3.6, 0.6))]:
    ax.annotate("", xy=(x, y), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=2.6 if x > 5 else 4.5, color=col, mutation_scale=22 if x < 5 else 16), zorder=3 if x < 5 else 2)
    ax.text(x + off[0], y + off[1], lab, color=col, fontsize=13, fontweight="bold")
ax.text(6.2, 4.4, "відстань між кінцями = 12,73", color="#D97706", fontsize=12.5, rotation=45, ha="center", va="center")
ax.text(8.6, 1.8, "кут = 0°\nкосинус = 1", fontsize=13, ha="center", bbox=dict(fc=GREEN, ec=INK, boxstyle="round,pad=0.4"))
ax.set_xlim(-0.5, 11.5); ax.set_ylim(-0.5, 11.5); ax.set_aspect("equal"); ax.grid(alpha=0.25)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
