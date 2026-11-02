"""Encoder-decoder: стиснення речення в один вектор і генерація перекладу."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 4.6); ax.set_xlim(0, 108)
words = ["I", "am", "a", "student"]
for i, w in enumerate(words):
    x = 1 + i * 11.5
    box(ax, x, 48, 9.5, 14, "GRU", fc=BLUE, size=12)
    arrow(ax, x + 4.75, 30, x + 4.75, 47.5)
    ax.text(x + 4.75, 24, w, ha="center", va="center", fontsize=13, fontfamily="DejaVu Sans Mono")
    if i < 3: arrow(ax, x + 10, 55, x + 11.2, 55)
ax.text(24, 82, "енкодер читає речення", ha="center", fontsize=12, color="#475569")
arrow(ax, 47.5, 55, 52.5, 55)
box(ax, 53, 46, 14, 18, "контекст\nвектор c", fc=AMBER, size=12)
arrow(ax, 67.6, 55, 71, 55)
outs = ["Я", "студент", "‹eos›"]; ins = ["‹bos›", "Я", "студент"]
for i in range(3):
    x = 72 + i * 10.2
    box(ax, x, 48, 8.6, 14, "GRU", fc=GREEN, size=11)
    arrow(ax, x + 4.3, 30, x + 4.3, 47.5)
    ax.text(x + 4.3, 24, ins[i], ha="center", va="center", fontsize=11.5, fontfamily="DejaVu Sans Mono")
    arrow(ax, x + 4.3, 63, x + 4.3, 76)
    ax.text(x + 4.3, 82, outs[i], ha="center", va="center", fontsize=12, fontfamily="DejaVu Sans Mono")
    if i < 2: arrow(ax, x + 9, 55, x + 10, 55)
ax.text(87, 94, "декодер генерує переклад", ha="center", fontsize=12, color="#475569")
ax.text(60, 38, "усе речення — в одному\nвекторі фіксованого розміру", ha="center", va="top", fontsize=11, color="#D97706")
save(fig, __file__)
