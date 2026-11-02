"""Accuracy на тесті по епохах: усереднення embeddings проти RNN (реальний запуск: 10 000 train, 5 000 test)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

ep = [1, 2, 3, 4, 5, 6]
avg = [73.7, 79.6, 82.5, 83.6, 84.0, 84.6]
rnn = [63.3, 63.4, 59.1, 67.8, 67.2, 68.0]
fig, ax = plt.subplots(figsize=(8.5, 4.4))
ax.plot(ep, avg, "o-", color="#2563EB", lw=2.4, label="усереднення embeddings")
ax.plot(ep, rnn, "s-", color="#D97706", lw=2.4, label="RNN")
ax.text(6.08, avg[-1], f"{avg[-1]}%", va="center", fontsize=12)
ax.text(6.08, rnn[-1], f"{rnn[-1]}%", va="center", fontsize=12)
ax.set_xlabel("епоха"); ax.set_ylabel("accuracy на тесті, %"); ax.set_xlim(0.8, 6.7)
ax.grid(True, alpha=0.3); ax.legend(frameon=False, loc="center right")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
