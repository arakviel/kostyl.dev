"""Косинус як кут: 0°, 90°, 180°."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
def panel(ax, vecs, title, note):
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-0.3, 1.25); ax.set_aspect("equal"); ax.axis("off")
    for (x, y), col, lw in vecs:
        ax.annotate("", xy=(x, y), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=lw, color=col))
    ax.set_title(title, fontsize=13, pad=4)
    ax.text(0, -0.25, note, ha="center", fontsize=13, color=INK, fontweight="bold")
panel(axes[0], [((1.2, 0.0), "#2563EB", 2.6), ((0.7, 0.0), "#DC2626", 2.6)], "кут 0° — один напрямок", "cos = 1")
panel(axes[1], [((1, 0), "#2563EB", 2.6), ((0, 1), "#DC2626", 2.6)], "кут 90° — перпендикулярні", "cos = 0")
panel(axes[2], [((1, 0), "#2563EB", 2.6), ((-1, 0), "#DC2626", 2.6)], "кут 180° — протилежні", "cos = −1")
save(fig, __file__)
