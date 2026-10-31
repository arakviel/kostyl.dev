"""
Візуалізація динаміки loss під час навчання Word2Vec.
Показує типову криву: швидке падіння на початку, потім плато.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/word2vec")
output_dir.mkdir(parents=True, exist_ok=True)

# Симульовані значення loss за епоху (типова крива навчання)
epochs = np.arange(1, 21)
# Експоненціальне затухання + шум
base_loss = 3_800_000 * np.exp(-0.15 * epochs) + 800_000
noise = np.random.RandomState(42).normal(0, 50_000, len(epochs))
loss_per_epoch = base_loss + noise

fig, ax = plt.subplots(figsize=(10, 5), dpi=200)

ax.plot(epochs, loss_per_epoch, marker="o", linewidth=2.5, markersize=7,
        color="#2563EB", markerfacecolor="#DBEAFE", markeredgecolor="#2563EB",
        markeredgewidth=2)

# Анотація критичних точок
ax.annotate("Швидке навчання", xy=(3, loss_per_epoch[2]), xytext=(6, 3_000_000),
            arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.5),
            fontsize=11, color="#D97706", family="DejaVu Sans", fontweight="bold")

ax.annotate("Плато", xy=(17, loss_per_epoch[16]), xytext=(14, 1_500_000),
            arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.5),
            fontsize=11, color="#16A34A", family="DejaVu Sans", fontweight="bold")

ax.set_xlabel("Епоха", fontsize=12, fontweight="bold", family="DejaVu Sans")
ax.set_ylabel("Loss за епоху", fontsize=12, fontweight="bold", family="DejaVu Sans")
ax.set_title("Динаміка навчання Word2Vec (skip-gram)",
             fontsize=14, fontweight="bold", color="#1E293B", family="DejaVu Sans", pad=15)

ax.grid(True, alpha=0.3, linestyle="--")
ax.set_xlim(0, 21)
ax.set_ylim(0, 4_200_000)

# Форматування осі Y (мільйони)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e6:.1f}M"))

plt.tight_layout()
plt.savefig(output_dir / "05-loss-dynamics.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '05-loss-dynamics.png'}")
