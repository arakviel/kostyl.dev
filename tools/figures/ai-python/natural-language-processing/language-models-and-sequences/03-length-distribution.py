"""
Гістограма розподілу довжин речень IMDB.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/language-models-and-sequences")
output_dir.mkdir(parents=True, exist_ok=True)

# Симулюємо розподіл довжин (схожий на реальний IMDB)
np.random.seed(42)
# Два піки: короткі відгуки (100-200) і довгі (200-400)
lengths = np.concatenate([
    np.random.normal(150, 50, 2000).clip(10, 600),
    np.random.normal(280, 80, 3000).clip(10, 600)
])

mean_len = lengths.mean()
median_len = np.median(lengths)
p95 = np.percentile(lengths, 95)

fig, ax = plt.subplots(figsize=(11, 6), dpi=200)

ax.hist(lengths, bins=50, color="#2563EB", alpha=0.7, edgecolor="black", linewidth=0.8)

# Лінії статистики
ax.axvline(mean_len, color="#DC2626", linestyle="--", linewidth=2.5, label=f"Середня: {mean_len:.0f}")
ax.axvline(p95, color="#D97706", linestyle="--", linewidth=2.5, label=f"95-й перцентиль: {p95:.0f}")

ax.set_xlabel("Довжина речення (кількість слів)", fontsize=12, fontweight="bold", family="DejaVu Sans")
ax.set_ylabel("Кількість речень", fontsize=12, fontweight="bold", family="DejaVu Sans")
ax.set_title("Розподіл довжин відгуків IMDB",
             fontsize=14, fontweight="bold", color="#1E293B", family="DejaVu Sans", pad=15)

ax.legend(fontsize=11, loc="upper right", framealpha=0.95)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.set_xlim(0, 650)

# Анотація
ax.text(450, ax.get_ylim()[1] * 0.8,
        f"Медіана: {median_len:.0f}\nМакс: {lengths.max():.0f}",
        fontsize=10, color="#64748B", family="DejaVu Sans",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#E2E8F0", alpha=0.8))

plt.tight_layout()
plt.savefig(output_dir / "03-length-distribution.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '03-length-distribution.png'}")
