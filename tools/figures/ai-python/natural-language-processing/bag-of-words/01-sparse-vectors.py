"""Перші 20 позицій вектора для трьох речень лекції 05 (значення з виводу) і кількість ненульових із 5000."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

rows = [("this movie is excellent", [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0], "4 / 5000 (0,08%)"),
        ("bad movie bad acting", [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0], "3 / 5000 (0,06%)"),
        ("the film was not good but not terrible either", [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], "7 / 5000 (0,14%)")]
fig, ax = canvas(12, 5.2)
ax.text(1, 97, "перші 20 позицій із 5000", fontsize=12.5, fontweight="bold"); ax.text(99, 97, "ненульових", fontsize=12.5, fontweight="bold", ha="right")
for r, (t, v, nz) in enumerate(rows):
    y = 66 - r * 31
    ax.text(1, y + 20, f"«{t}»", fontsize=12, color="#475569")
    for i, x in enumerate(v):
        box(ax, 1 + i * 3.7, y, 3.3, 14, str(x), fc=AMBER if x else GREY, size=9.5, mono=True)
    ax.text(76.5, y + 7, "…", fontsize=16, color="#475569", va="center")
    ax.text(98, y + 7, nz, fontsize=11.5, ha="right", va="center", fontweight="bold")
save(fig, __file__)
