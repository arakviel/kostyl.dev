"""
Візуалізація вікна контексту Word2Vec.
Показує речення з центральним словом і контекстними словами в вікні розміром 2.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Налаштування виводу
output_dir = Path("public/images/ai-python/natural-language-processing/word2vec")
output_dir.mkdir(parents=True, exist_ok=True)

# Речення
words = ["Natural", "language", "processing", "is", "fascinating"]
center_idx = 2  # "processing"
window = 2

fig, ax = plt.subplots(figsize=(12, 3), dpi=200)
ax.axis("off")

# Малюємо слова
x_start = 0.5
x_step = 2.0
y = 1.5

for i, word in enumerate(words):
    x = x_start + i * x_step
    
    # Центральне слово — синє
    if i == center_idx:
        color = "#2563EB"
        fontweight = "bold"
        label_color = "#2563EB"
    # Контекст — зелене
    elif abs(i - center_idx) <= window:
        color = "#16A34A"
        fontweight = "normal"
        label_color = "#16A34A"
    # Інші — сіре
    else:
        color = "#64748B"
        fontweight = "normal"
        label_color = "#64748B"
    
    # Рамка навколо слова
    rect = patches.FancyBboxPatch(
        (x - 0.7, y - 0.3), 1.4, 0.6,
        boxstyle="round,pad=0.05",
        linewidth=2,
        edgecolor=color,
        facecolor="#FFFFFF" if i != center_idx else "#DBEAFE",
        alpha=0.9
    )
    ax.add_patch(rect)
    
    # Текст слова
    ax.text(x, y, word, ha="center", va="center", fontsize=14,
            fontweight=fontweight, color="#1E293B", family="DejaVu Sans")

# Підписи
ax.text(x_start + center_idx * x_step, y - 0.8, "центральне слово",
        ha="center", fontsize=11, color="#2563EB", style="italic", family="DejaVu Sans")

# Стрілки до контексту
for i in range(len(words)):
    if i != center_idx and abs(i - center_idx) <= window:
        x = x_start + i * x_step
        x_center = x_start + center_idx * x_step
        
        # Стрілка від контексту до центру
        ax.annotate("", xy=(x_center - 0.7 if i < center_idx else x_center + 0.7, y),
                    xytext=(x + 0.7 if i < center_idx else x - 0.7, y),
                    arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.5, alpha=0.6))

# Позначка вікна
ax.text(x_start - 0.5, y + 0.9, f"Вікно контексту (C = {window})",
        fontsize=12, fontweight="bold", color="#1E293B", family="DejaVu Sans")

ax.set_xlim(0, x_start + len(words) * x_step)
ax.set_ylim(0, 3)

plt.tight_layout()
plt.savefig(output_dir / "01-context-window.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '01-context-window.png'}")
