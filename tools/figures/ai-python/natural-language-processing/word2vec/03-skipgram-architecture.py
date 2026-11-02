"""Skip-gram: слово natural -> контекст (I, love, language, processing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

fig, ax = canvas(10, 8)
box(ax, 38, 86, 24, 9, "natural", fc=BLUE, size=13, mono=True)
arrow(ax, 50, 85.5, 50, 76.5)
box(ax, 38, 67, 24, 9, "вектор v", fc=BLUE, size=12)
arrow(ax, 50, 66.5, 50, 57.5)
box(ax, 30, 48, 40, 9, "лінійний шар: W·v + b", fc=GREY, size=12)
outs = ["I", "love", "language", "processing"]
xs = [8 + i * 22 for i in range(4)]
for x, w in zip(xs, outs):
    arrow(ax, 50, 47.5, x + 9, 36.5)
    box(ax, x, 27, 18, 9, "softmax", fc=AMBER, size=12)
    arrow(ax, x + 9, 26.5, x + 9, 17.5)
    box(ax, x, 8, 18, 9, w, fc=GREEN, size=12.5, mono=True)
ax.text(1, 90.5, "слово", fontsize=11, color="#475569", va="center")
ax.text(1, 71.5, "embedding", fontsize=11, color="#475569", va="center")
ax.text(1, 52.5, "оцінки слів", fontsize=11, color="#475569", va="center")
ax.text(50, 0, "чотири окремі передбачення — по одному на кожне слово контексту", ha="center", fontsize=11.5, color="#475569")
save(fig, __file__)
