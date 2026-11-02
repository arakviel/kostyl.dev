"""Accuracy на тесті по епохах (реальний запуск: IMDB, 10 000 train, 5 000 test, 200 токенів, hidden = 64)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

ep = [1, 2, 3, 4, 5, 6]
data = {"усереднення": ([73.7, 79.6, 82.5, 83.6, 84.0, 84.6], "#2563EB", "o"),
        "GRU": ([68.5, 66.1, 76.5, 80.3, 82.3, 83.2], "#16A34A", "s"),
        "LSTM": ([53.6, 68.9, 70.5, 70.8, 76.3, 75.5], "#D97706", "^"),
        "RNN": ([63.3, 63.4, 59.1, 67.8, 67.2, 68.0], "#DC2626", "D")}
fig, ax = plt.subplots(figsize=(9, 4.8))
for name, (v, col, m) in data.items():
    ax.plot(ep, v, m + "-", color=col, lw=2.3, label=name)
    ax.text(6.1, v[-1], f"{name} {v[-1]}%", va="center", fontsize=11.5, color=col)
ax.set_xlim(0.8, 8.4); ax.set_xticks(ep)
ax.set_xlabel("епоха"); ax.set_ylabel("accuracy на тесті, %")
ax.grid(True, alpha=0.3)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
