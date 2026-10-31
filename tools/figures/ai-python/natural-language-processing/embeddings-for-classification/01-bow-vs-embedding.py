"""
Порівняння мішка слів і усередненого вектора embeddings.
Показує різницю між розрідженим і щільним представленням.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/embeddings-for-classification")
output_dir.mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=200)

# Мішок слів (розріджений)
ax1.set_title("Мішок слів (Bag-of-Words)", fontsize=13, fontweight="bold",
              color="#1E293B", family="DejaVu Sans", pad=15)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

# Вектор
vocab_size = 10000
nonzero_words = 8
rect1 = patches.FancyBboxPatch((1, 4), 8, 2, boxstyle="round,pad=0.1",
                               linewidth=2, edgecolor="#2563EB",
                               facecolor="#E2E8F0", alpha=0.7)
ax1.add_patch(rect1)

# Кілька ненульових позицій
for i in range(nonzero_words):
    x = 1.5 + i * 0.9
    ax1.text(x, 5, "1", ha="center", va="center", fontsize=10,
             fontweight="bold", color="#DC2626", family="DejaVu Sans")

# Нулі
for i in range(5):
    x = 2.5 + nonzero_words * 0.9 + i * 0.6
    ax1.text(x, 5, "0", ha="center", va="center", fontsize=9,
             color="#64748B", alpha=0.4, family="DejaVu Sans")

ax1.text(5, 3, f"Розмір: {vocab_size:,}", ha="center", fontsize=11,
         color="#64748B", family="DejaVu Sans")
ax1.text(5, 2.2, f"Ненульових: ~{nonzero_words}", ha="center", fontsize=11,
         color="#64748B", family="DejaVu Sans")
ax1.text(5, 7, "Розріджений вектор", ha="center", fontsize=12,
         fontweight="bold", color="#2563EB", family="DejaVu Sans")

# Усереднений вектор (щільний)
ax2.set_title("Усереднений вектор embeddings", fontsize=13, fontweight="bold",
              color="#1E293B", family="DejaVu Sans", pad=15)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")

# Вектор
embed_size = 100
rect2 = patches.FancyBboxPatch((1, 4), 8, 2, boxstyle="round,pad=0.1",
                               linewidth=2, edgecolor="#16A34A",
                               facecolor="#DCFCE7", alpha=0.7)
ax2.add_patch(rect2)

# Усі ненульові
np.random.seed(42)
values = np.random.randn(10) * 0.5
for i in range(10):
    x = 1.5 + i * 0.8
    val = values[i]
    ax2.text(x, 5, f"{val:.2f}", ha="center", va="center", fontsize=9,
             fontweight="bold", color="#16A34A", family="DejaVu Sans")

ax2.text(5, 3, f"Розмір: {embed_size}", ha="center", fontsize=11,
         color="#64748B", family="DejaVu Sans")
ax2.text(5, 2.2, "Усі числа ненульові", ha="center", fontsize=11,
         color="#64748B", family="DejaVu Sans")
ax2.text(5, 7, "Щільний вектор", ha="center", fontsize=12,
         fontweight="bold", color="#16A34A", family="DejaVu Sans")

plt.tight_layout()
plt.savefig(output_dir / "01-bow-vs-embedding.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '01-bow-vs-embedding.png'}")
