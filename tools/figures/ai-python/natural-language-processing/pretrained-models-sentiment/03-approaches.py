"""Порівняння підходів на IMDB (реальні запуски). Тест: ті самі 5000 відгуків."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

names = ["усереднення\nembeddings", "GRU", "Transformer\n(2 шари)", "DistilBERT\nбез навчання", "DistilBERT\nfine-tuning"]
vals = [84.6, 83.2, 78.5, 87.7, 87.7]
train = ["10 000", "10 000", "10 000", "0", "2 000"]
cols = ["#2563EB", "#16A34A", "#D97706", "#94A3B8", "#DC2626"]
fig, ax = plt.subplots(figsize=(10, 4.8))
bars = ax.bar(range(5), vals, color=cols, width=0.62)
for i, (b, v, t) in enumerate(zip(bars, vals, train)):
    ax.text(i, v + 0.6, f"{v}%", ha="center", fontsize=13, fontweight="bold")
    ax.text(i, 61, f"навчання:\n{t}", ha="center", fontsize=10.5, color="white" if i != 3 else INK)
ax.set_xticks(range(5)); ax.set_xticklabels(names, fontsize=11.5)
ax.set_ylim(60, 92); ax.set_ylabel("accuracy на тесті, %")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
