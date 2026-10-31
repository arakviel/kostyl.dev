"""
Візуалізація аналогії king - man + woman ≈ queen як паралелограм у 2D просторі.
Показує, що вектори відношень паралельні.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/word2vec")
output_dir.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(9, 7), dpi=200)

# Іграшкові координати векторів
vectors = {
    "man": np.array([1, 1]),
    "woman": np.array([1, 3]),
    "king": np.array([4, 2]),
    "queen": np.array([4, 4])
}

# Малюємо вектори
for name, vec in vectors.items():
    color = "#2563EB" if "king" in name or "queen" in name else "#16A34A"
    ax.arrow(0, 0, vec[0], vec[1], head_width=0.15, head_length=0.15,
             fc=color, ec=color, lw=2, alpha=0.7, length_includes_head=True)
    
    # Підпис
    offset_x = 0.3 if vec[0] > 2 else -0.5
    offset_y = 0.3
    ax.text(vec[0] + offset_x, vec[1] + offset_y, name,
            fontsize=13, fontweight="bold", color=color, family="DejaVu Sans")

# Малюємо відношення (різниці векторів)
# man → woman
diff_gender = vectors["woman"] - vectors["man"]
ax.arrow(vectors["man"][0], vectors["man"][1],
         diff_gender[0], diff_gender[1],
         head_width=0.12, head_length=0.12,
         fc="#D97706", ec="#D97706", lw=2.5, linestyle="--", alpha=0.8,
         length_includes_head=True)
ax.text(1.5, 2.5, "жіночість", fontsize=11, color="#D97706",
        style="italic", family="DejaVu Sans", rotation=60)

# king → queen (має бути паралельним)
diff_royalty = vectors["queen"] - vectors["king"]
ax.arrow(vectors["king"][0], vectors["king"][1],
         diff_royalty[0], diff_royalty[1],
         head_width=0.12, head_length=0.12,
         fc="#D97706", ec="#D97706", lw=2.5, linestyle="--", alpha=0.8,
         length_includes_head=True)
ax.text(4.5, 3.5, "жіночість", fontsize=11, color="#D97706",
        style="italic", family="DejaVu Sans", rotation=60)

# Паралелограм (пунктирні лінії)
ax.plot([vectors["man"][0], vectors["king"][0]],
        [vectors["man"][1], vectors["king"][1]],
        "k--", lw=1, alpha=0.3)
ax.plot([vectors["woman"][0], vectors["queen"][0]],
        [vectors["woman"][1], vectors["queen"][1]],
        "k--", lw=1, alpha=0.3)

# Формула
ax.text(2.5, 0.3, "king − man + woman ≈ queen",
        fontsize=12, fontweight="bold", color="#1E293B",
        family="DejaVu Sans", bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF3C7", alpha=0.8))

# Налаштування осей
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-0.5, 5)
ax.set_xlabel("Вимір 1", fontsize=11, family="DejaVu Sans")
ax.set_ylabel("Вимір 2", fontsize=11, family="DejaVu Sans")
ax.grid(True, alpha=0.2)
ax.set_aspect("equal")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.title("Аналогія як паралельні вектори відношень", fontsize=13, fontweight="bold",
          color="#1E293B", family="DejaVu Sans", pad=15)
plt.tight_layout()
plt.savefig(output_dir / "04-analogy-parallelogram.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '04-analogy-parallelogram.png'}")
