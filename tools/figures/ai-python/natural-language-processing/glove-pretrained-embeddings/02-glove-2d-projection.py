"""Реальна 2D-проєкція (PCA) 30 слів із векторів GloVe (glove-wiki-gigaword-100).
Запуск: python 02-glove-2d-projection.py  (потрібні gensim, scikit-learn, matplotlib)"""
import numpy as np
import matplotlib.pyplot as plt
import gensim.downloader as api
from pathlib import Path
from sklearn.decomposition import PCA

output_dir = Path("public/images/ai-python/natural-language-processing/glove-pretrained-embeddings")
output_dir.mkdir(parents=True, exist_ok=True)

glove = api.load("glove-wiki-gigaword-100")
categories = {
    "Країни": (["france", "germany", "italy", "spain", "russia"], "#2563EB"),
    "Столиці": (["paris", "berlin", "rome", "madrid", "moscow"], "#16A34A"),
    "Технології": (["computer", "software", "internet", "technology", "digital"], "#D97706"),
    "Наука": (["physics", "chemistry", "biology", "mathematics", "science"], "#DC2626"),
    "Мистецтво": (["music", "art", "painting", "sculpture", "literature"], "#9333EA"),
    "Тварини": (["dog", "cat", "horse", "bird", "fish"], "#EC4899"),
}
words = [w for ws, _ in categories.values() for w in ws]
pca = PCA(n_components=2)
xy = pca.fit_transform(np.array([glove[w] for w in words]))
print(f"Пояснена дисперсія: {pca.explained_variance_ratio_.sum():.1%}")

fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
i = 0
for name, (ws, color) in categories.items():
    pts = xy[i:i + len(ws)]
    ax.scatter(pts[:, 0], pts[:, 1], c=color, label=name, s=120, alpha=0.7, edgecolors="black", linewidth=1.5)
    for (x, y), w in zip(pts, ws):
        ax.text(x + 0.06, y + 0.06, w, fontsize=9, alpha=0.85)
    i += len(ws)
ax.set_xlabel("Перша головна компонента", fontsize=12, fontweight="bold")
ax.set_ylabel("Друга головна компонента", fontsize=12, fontweight="bold")
ax.set_title(f"2D-проєкція векторів GloVe (PCA, 30 слів, пояснена дисперсія {pca.explained_variance_ratio_.sum():.1%})".replace(".", ","), fontsize=14, fontweight="bold", pad=15)
ax.legend(loc="best", fontsize=10, framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle="--")
plt.tight_layout()
plt.savefig(output_dir / "02-glove-2d-projection.png", dpi=200, bbox_inches="tight", facecolor="white")
np.save("/private/tmp/claude-501/-Users-arakviel-Work-kostyl-dev/ebbc32d9-081e-4ed0-877e-575426d309a1/scratchpad/glove_xy.npy", xy)
print("ok")
