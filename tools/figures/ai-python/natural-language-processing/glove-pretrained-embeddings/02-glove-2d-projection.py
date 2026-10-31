"""
Візуалізація 2D-проєкції векторів GloVe через PCA.
Симулює результат для 30 слів із різних категорій.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/glove-pretrained-embeddings")
output_dir.mkdir(parents=True, exist_ok=True)

# Симульовані координати після PCA (для консистентності з лекцією)
np.random.seed(42)

# Категорії та їхні центри кластерів
categories = {
    "Країни": {"words": ["france", "germany", "italy", "spain", "russia"],
               "center": (-1.5, 0.2), "color": "#2563EB"},
    "Столиці": {"words": ["paris", "berlin", "rome", "madrid", "moscow"],
                "center": (-1.2, -0.8), "color": "#16A34A"},
    "Технології": {"words": ["computer", "software", "internet", "technology", "digital"],
                   "center": (0.3, 0.9), "color": "#D97706"},
    "Наука": {"words": ["physics", "chemistry", "biology", "mathematics", "science"],
              "center": (0.5, -0.5), "color": "#DC2626"},
    "Мистецтво": {"words": ["music", "art", "painting", "sculpture", "literature"],
                  "center": (1.8, 0.4), "color": "#9333EA"},
    "Тварини": {"words": ["dog", "cat", "horse", "bird", "fish"],
                "center": (1.5, -1.0), "color": "#EC4899"}
}

fig, ax = plt.subplots(figsize=(12, 8), dpi=200)

# Малюємо кластери
for cat_name, data in categories.items():
    center = np.array(data["center"])
    
    # Генеруємо точки навколо центру
    n_words = len(data["words"])
    points = center + np.random.randn(n_words, 2) * 0.25
    
    # Scatter
    ax.scatter(points[:, 0], points[:, 1], c=data["color"], label=cat_name,
               s=120, alpha=0.7, edgecolors="black", linewidth=1.5)
    
    # Підписи слів
    for i, word in enumerate(data["words"]):
        ax.text(points[i, 0] + 0.08, points[i, 1] + 0.08, word,
                fontsize=9, alpha=0.85, family="DejaVu Sans")

ax.set_xlabel("Перша головна компонента", fontsize=12, fontweight="bold", family="DejaVu Sans")
ax.set_ylabel("Друга головна компонента", fontsize=12, fontweight="bold", family="DejaVu Sans")
ax.set_title("2D-проєкція векторів GloVe (PCA, 30 слів)",
             fontsize=14, fontweight="bold", color="#1E293B", family="DejaVu Sans", pad=15)

ax.legend(loc="upper left", fontsize=10, framealpha=0.95, edgecolor="gray")
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.0, 2.0)

plt.tight_layout()
plt.savefig(output_dir / "02-glove-2d-projection.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '02-glove-2d-projection.png'}")
