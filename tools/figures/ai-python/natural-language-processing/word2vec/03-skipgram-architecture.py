"""
Візуалізація архітектури skip-gram.
Центральне слово → embedding → лінійний шар → softmax → чотири передбачення контексту.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/word2vec")
output_dir.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 8), dpi=200)
ax.axis("off")

# Шари
layers = [
    {"y": 7, "label": "Центральне слово", "items": ["natural"], "color": "#DBEAFE"},
    {"y": 5.5, "label": "Embedding (d=100)", "items": ["v"], "color": "#DCFCE7"},
    {"y": 4, "label": "Лінійний шар", "items": ["W × v + b"], "color": "#E2E8F0"},
    {"y": 2.5, "label": "Softmax (×4)", "items": ["P(w₁)", "P(w₂)", "P(w₃)", "P(w₄)"], "color": "#FEF3C7"},
    {"y": 1, "label": "Контекстні слова", "items": ["I", "love", "language", "processing"], "color": "#DCFCE7"},
]

x_positions = [2, 4, 6, 8]

# Малюємо шари
for layer in layers:
    y = layer["y"]
    
    if len(layer["items"]) == 1:
        # Один елемент
        x = 5
        rect = patches.FancyBboxPatch(
            (x - 1, y - 0.25), 2, 0.5,
            boxstyle="round,pad=0.05",
            linewidth=1.5,
            edgecolor="#1E293B",
            facecolor=layer["color"],
            alpha=0.8
        )
        ax.add_patch(rect)
        ax.text(x, y, layer["items"][0], ha="center", va="center",
                fontsize=11, fontweight="bold", color="#1E293B", family="DejaVu Sans")
    else:
        # Кілька елементів
        for i, item in enumerate(layer["items"]):
            x = x_positions[i]
            rect = patches.FancyBboxPatch(
                (x - 0.6, y - 0.25), 1.2, 0.5,
                boxstyle="round,pad=0.05",
                linewidth=1.5,
                edgecolor="#1E293B",
                facecolor=layer["color"],
                alpha=0.8
            )
            ax.add_patch(rect)
            ax.text(x, y, item, ha="center", va="center",
                    fontsize=10, fontweight="bold", color="#1E293B", family="DejaVu Sans")
    
    # Підпис шару
    ax.text(0.3, y, layer["label"], ha="left", va="center",
            fontsize=10, color="#64748B", family="DejaVu Sans", style="italic")

# Стрілки між шарами
for i in range(len(layers) - 1):
    y_from = layers[i]["y"] - 0.3
    y_to = layers[i + 1]["y"] + 0.3
    
    if len(layers[i]["items"]) == 1 and len(layers[i + 1]["items"]) > 1:
        # Розгалуження від одного до багатьох
        for x in x_positions:
            ax.annotate("", xy=(x, y_to), xytext=(5, y_from),
                        arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2, alpha=0.5))
    elif len(layers[i]["items"]) == 1 and len(layers[i + 1]["items"]) == 1:
        # Один до одного
        ax.annotate("", xy=(5, y_to), xytext=(5, y_from),
                    arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.5))
    elif len(layers[i]["items"]) > 1 and len(layers[i + 1]["items"]) > 1:
        # Багато до багатьох (вертикально)
        for j, x in enumerate(x_positions):
            ax.annotate("", xy=(x, y_to), xytext=(x, y_from),
                        arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2))

# Заголовок
ax.text(5, 8, "Skip-gram: центральне слово → контекст", ha="center",
        fontsize=14, fontweight="bold", color="#1E293B", family="DejaVu Sans")

ax.set_xlim(0, 10)
ax.set_ylim(0, 8.5)

plt.tight_layout()
plt.savefig(output_dir / "03-skipgram-architecture.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '03-skipgram-architecture.png'}")
