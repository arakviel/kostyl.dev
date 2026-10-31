"""
Таблиця ймовірностей біграм (невелика матриця для демонстрації).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/language-models-and-sequences")
output_dir.mkdir(parents=True, exist_ok=True)

# Невеликий словник
words = ["i", "love", "natural", "language", "processing", "is"]

# Симульована матриця ймовірностей біграм (рядок → стовпець)
# На основі корпусу з лекції
probs = np.array([
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # i → love (100%)
    [0.0, 0.0, 0.5, 0.0, 0.5, 0.0],  # love → natural/processing
    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  # natural → language
    [0.0, 0.0, 0.0, 0.0, 0.33, 0.33],  # language → processing/is
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.33],  # processing → (various)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # is → fascinating (не в таблиці)
])

fig, ax = plt.subplots(figsize=(9, 8), dpi=200)

# Теплова карта
im = ax.imshow(probs, cmap="YlOrRd", alpha=0.8, vmin=0, vmax=1)

# Підписи
ax.set_xticks(np.arange(len(words)))
ax.set_yticks(np.arange(len(words)))
ax.set_xticklabels(words, fontsize=11, fontweight="bold", family="DejaVu Sans")
ax.set_yticklabels(words, fontsize=11, fontweight="bold", family="DejaVu Sans")

plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Значення в клітинках
for i in range(len(words)):
    for j in range(len(words)):
        if probs[i, j] > 0:
            text = ax.text(j, i, f"{probs[i, j]:.2f}",
                           ha="center", va="center",
                           color="white" if probs[i, j] > 0.5 else "black",
                           fontsize=11, fontweight="bold", family="DejaVu Sans")

ax.set_xlabel("Наступне слово →", fontsize=12, fontweight="bold", family="DejaVu Sans", labelpad=10)
ax.set_ylabel("← Попереднє слово", fontsize=12, fontweight="bold", family="DejaVu Sans", labelpad=10)
ax.set_title("Таблиця ймовірностей біграм: P(наступне | попереднє)",
             fontsize=13, fontweight="bold", color="#1E293B", family="DejaVu Sans", pad=20)

# Колорбар
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Ймовірність", rotation=270, labelpad=20, fontsize=11, family="DejaVu Sans")

# Сітка
ax.set_xticks(np.arange(len(words)) - 0.5, minor=True)
ax.set_yticks(np.arange(len(words)) - 0.5, minor=True)
ax.grid(which="minor", color="gray", linestyle="-", linewidth=1.5)
ax.tick_params(which="minor", size=0)

plt.tight_layout()
plt.savefig(output_dir / "01-bigram-probabilities.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '01-bigram-probabilities.png'}")
