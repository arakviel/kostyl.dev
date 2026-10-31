"""
Візуалізація матриці співустрічності (co-occurrence matrix).
Показує невелику таблицю 6×6 для демонстрації концепції.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/glove-pretrained-embeddings")
output_dir.mkdir(parents=True, exist_ok=True)

# Невеликий словник
words = ["I", "love", "natural", "language", "processing", "data"]

# Симульована матриця співустрічності (на основі трьох речень)
# I love natural language processing.
# Natural language is fascinating.
# I love processing data.
matrix = np.array([
    [0, 2, 0, 0, 0, 0],  # I
    [2, 0, 1, 0, 2, 1],  # love
    [0, 1, 0, 2, 1, 0],  # natural
    [0, 0, 2, 0, 1, 0],  # language
    [0, 2, 1, 1, 0, 1],  # processing
    [0, 1, 0, 0, 1, 0],  # data
])

fig, ax = plt.subplots(figsize=(9, 8), dpi=200)

# Малюємо таблицю
im = ax.imshow(matrix, cmap="Blues", alpha=0.7, vmin=0, vmax=3)

# Підписи осей
ax.set_xticks(np.arange(len(words)))
ax.set_yticks(np.arange(len(words)))
ax.set_xticklabels(words, fontsize=12, fontweight="bold", family="DejaVu Sans")
ax.set_yticklabels(words, fontsize=12, fontweight="bold", family="DejaVu Sans")

# Обертаємо X-підписи
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Значення в клітинках
for i in range(len(words)):
    for j in range(len(words)):
        text = ax.text(j, i, matrix[i, j],
                       ha="center", va="center", color="black" if matrix[i, j] < 2 else "white",
                       fontsize=14, fontweight="bold", family="DejaVu Sans")

# Підписи осей
ax.set_xlabel("Контекстне слово →", fontsize=12, fontweight="bold", family="DejaVu Sans", labelpad=10)
ax.set_ylabel("← Центральне слово", fontsize=12, fontweight="bold", family="DejaVu Sans", labelpad=10)

# Заголовок
ax.set_title("Матриця співустрічності (вікно C=2)", 
             fontsize=14, fontweight="bold", color="#1E293B", family="DejaVu Sans", pad=20)

# Колорбар
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Кількість співустрічень", rotation=270, labelpad=20, fontsize=11, family="DejaVu Sans")

# Сітка
ax.set_xticks(np.arange(len(words)) - 0.5, minor=True)
ax.set_yticks(np.arange(len(words)) - 0.5, minor=True)
ax.grid(which="minor", color="gray", linestyle="-", linewidth=1.5)
ax.tick_params(which="minor", size=0)

plt.tight_layout()
plt.savefig(output_dir / "01-cooccurrence-matrix.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '01-cooccurrence-matrix.png'}")
