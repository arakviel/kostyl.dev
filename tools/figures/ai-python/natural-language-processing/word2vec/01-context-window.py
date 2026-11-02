"""Вікно контексту C = 2 для слів processing і language."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

words = ["Natural", "language", "processing", "is", "fascinating"]
fig, ax = canvas(12, 5)
def row(y, center, label):
    ctx = {i for i in range(5) if i != center and abs(i - center) <= 2}
    for i, w in enumerate(words):
        fc = BLUE if i == center else (GREEN if i in ctx else "white")
        box(ax, 3 + i * 18.5, y, 16, 14, w, fc=fc, size=12.5, weight="bold" if i == center else "normal")
    x0, x1 = 3 + min(ctx | {center}) * 18.5 - 1, 3 + (max(ctx | {center}) + 1) * 18.5 - 3.5
    ax.plot([x0, x1], [y - 4, y - 4], color="#16A34A", lw=2.5)
    ax.text((x0 + x1) / 2, y - 12, label, ha="center", fontsize=12, color="#475569")
row(66, 2, "центр «processing»: контекст = Natural, language, is, fascinating (4 слова)")
row(22, 1, "центр «language»: контекст = Natural, processing, is (3 слова, зліва лише одне)")
ax.text(50, 98, "вікно C = 2: по два слова з кожного боку", ha="center", fontsize=13, fontweight="bold")
save(fig, __file__)
