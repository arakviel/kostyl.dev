"""CBOW: контекст (I, love, language, processing) -> центральне слово natural."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

fig, ax = canvas(10, 8)
ctx = ["I", "love", "language", "processing"]
xs = [20 + i * 19.5 for i in range(4)]
for x, w in zip(xs, ctx):
    box(ax, x, 86, 17, 9, w, fc=GREEN, size=12.5, mono=True)
    arrow(ax, x + 8.5, 85.5, x + 8.5, 76.5)
    box(ax, x, 66, 17, 9, "вектор v", fc=BLUE, size=12)
    arrow(ax, x + 8.5, 65.5, 52, 55.5)
ax.text(1, 91, "контекст", fontsize=11, color="#475569", ha="left", va="center")
ax.text(1, 70.5, "embedding", fontsize=11, color="#475569", ha="left", va="center")
box(ax, 34, 46, 36, 9, "h = (v₁ + v₂ + v₃ + v₄) / 4", fc=AMBER, size=12)
arrow(ax, 52, 45.5, 52, 36.5)
box(ax, 34, 27, 36, 9, "лінійний шар: W·h + b", fc=GREY, size=12)
arrow(ax, 52, 26.5, 52, 17.5)
box(ax, 34, 8, 36, 9, "softmax → P(natural)", fc=GREEN, size=12)
ax.text(1, 50.5, "усереднення", fontsize=11, color="#475569", va="center")
ax.text(1, 31.5, "оцінки слів", fontsize=11, color="#475569", va="center")
ax.text(1, 12.5, "ймовірності", fontsize=11, color="#475569", va="center")
save(fig, __file__)
