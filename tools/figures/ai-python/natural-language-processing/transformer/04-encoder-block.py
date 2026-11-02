"""Блок енкодера Transformer."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(7, 7.2)
box(ax, 25, 2, 50, 7, "embedding + позиція", fc=GREY, size=12)
box(ax, 25, 24, 50, 12, "Multi-Head\nSelf-Attention", fc=BLUE, size=13)
box(ax, 25, 42, 50, 7, "Add & Norm", fc=AMBER, size=12)
box(ax, 25, 56, 50, 12, "Feed-Forward\n(кожне слово окремо)", fc=GREEN, size=12.5)
box(ax, 25, 74, 50, 7, "Add & Norm", fc=AMBER, size=12)
arrow(ax, 50, 9.8, 50, 23.5); arrow(ax, 50, 36.8, 50, 41.5); arrow(ax, 50, 49.8, 50, 55.5)
arrow(ax, 50, 68.8, 50, 73.5); arrow(ax, 50, 81.8, 50, 92)
ax.text(50, 96, "вектори слів із урахуванням контексту", ha="center", fontsize=11.5, color="#475569")
for y1, y2 in [(14, 45.5), (52, 77.5)]:
    ax.plot([50, 12, 12], [y1, y1, y2], color="#D97706", lw=1.8)
    arrow(ax, 12, y2, 24.5, y2)
    ax.text(10, (y1 + y2) / 2, "залишкове\nз'єднання", ha="right", va="center", fontsize=10.5, color="#D97706")
ax.text(88, 50, "× N шарів", fontsize=13, rotation=90, va="center", color="#475569")
ax.plot([86, 86], [18, 84], color="#94A3B8", lw=1.2)
save(fig, __file__)
