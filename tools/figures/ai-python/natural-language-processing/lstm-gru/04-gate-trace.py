"""Середнє значення вентилів LSTM (по 64 нейронах) на кожному слові відгуку. Реальний запуск: LSTM, 5 епох на IMDB."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

toks = "the plot was boring but the acting was not good at all and i loved the ending".split()
rows = [[0.58,0.38,0.40,0.21],[0.53,0.45,0.46,0.34],[0.55,0.42,0.46,0.34],[0.45,0.53,0.51,0.49],
        [0.46,0.54,0.43,0.45],[0.60,0.38,0.40,0.46],[0.61,0.42,0.49,0.54],[0.59,0.43,0.47,0.66],
        [0.61,0.54,0.56,0.83],[0.59,0.45,0.50,0.80],[0.56,0.49,0.55,0.79],[0.56,0.47,0.49,0.77],
        [0.63,0.44,0.48,0.76],[0.62,0.42,0.40,0.70],[0.63,0.50,0.51,0.53],[0.60,0.39,0.42,0.55],[0.56,0.48,0.48,0.53]]
import numpy as np
r = np.array(rows)
fig, ax = plt.subplots(figsize=(11, 4.6))
x = range(len(toks))
for i, (name, col, st) in enumerate([("forget f", "#16A34A", "o-"), ("input i", "#2563EB", "s-"),
                                      ("output o", "#DC2626", "^-"), ("сила пам'яті |c|", "#D97706", "D--")]):
    ax.plot(x, r[:, i if i < 3 else 3], st, color=col, lw=2.2, label=name)
ax.set_xticks(list(x)); ax.set_xticklabels(toks, rotation=40, ha="right")
ax.set_ylim(0.1, 0.95); ax.grid(True, alpha=0.3); ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.14))
ax.annotate("«not good»: пам'ять росте", (8.9, 0.84), xytext=(10.3, 0.9), fontsize=12,
            arrowprops=dict(arrowstyle="-|>", color=INK))
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
