"""
Схема padding і маски: три речення різної довжини.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/language-models-and-sequences")
output_dir.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
ax.set_xlim(0, 11)
ax.set_ylim(0, 10)
ax.axis("off")

# Три речення
sentences = [
    {"words": ["I", "love", "NLP"], "y": 7.5, "label": "Речення 1 (3 слова)"},
    {"words": ["Natural", "language", "processing", "is", "fascinating"], "y": 5, "label": "Речення 2 (5 слів)"},
    {"words": ["Text"], "y": 2.5, "label": "Речення 3 (1 слово)"},
]

max_len = 5

for sent in sentences:
    y = sent["y"]
    
    # Підпис
    ax.text(0.5, y + 0.6, sent["label"], fontsize=11, fontweight="bold",
            color="#1E293B", family="DejaVu Sans")
    
    # Слова
    for i, word in enumerate(sent["words"]):
        x = 1.5 + i * 1.5
        rect = patches.FancyBboxPatch((x - 0.5, y - 0.3), 1, 0.6,
                                      boxstyle="round,pad=0.05", linewidth=2,
                                      edgecolor="#16A34A", facecolor="#DCFCE7", alpha=0.8)
        ax.add_patch(rect)
        ax.text(x, y, word, ha="center", va="center", fontsize=10,
                fontweight="bold", color="#1E293B", family="DejaVu Sans")
    
    # Padding
    for i in range(len(sent["words"]), max_len):
        x = 1.5 + i * 1.5
        rect = patches.FancyBboxPatch((x - 0.5, y - 0.3), 1, 0.6,
                                      boxstyle="round,pad=0.05", linewidth=2,
                                      edgecolor="#64748B", facecolor="#E2E8F0", alpha=0.5)
        ax.add_patch(rect)
        ax.text(x, y, "<PAD>", ha="center", va="center", fontsize=9,
                color="#64748B", family="DejaVu Sans", style="italic")
    
    # Маска
    mask_y = y - 0.9
    ax.text(0.5, mask_y, "Маска:", fontsize=10, color="#2563EB",
            family="DejaVu Sans", fontweight="bold")
    
    for i in range(max_len):
        x = 1.5 + i * 1.5
        is_real = i < len(sent["words"])
        color = "#16A34A" if is_real else "#DC2626"
        text = "True" if is_real else "False"
        
        circle = patches.Circle((x, mask_y), 0.3, color=color, alpha=0.3, edgecolor=color, linewidth=2)
        ax.add_patch(circle)
        ax.text(x, mask_y, text, ha="center", va="center", fontsize=8,
                fontweight="bold", color=color, family="DejaVu Sans")

# Пояснення
ax.text(5.5, 0.5, "Маска: True = реальний токен, False = padding (ігноруємо в обчисленнях)",
        ha="center", fontsize=11, color="#64748B", family="DejaVu Sans",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF3C7", alpha=0.8))

ax.text(5.5, 9, "Padding: вирівнювання до довжини 5", ha="center",
        fontsize=13, fontweight="bold", color="#1E293B", family="DejaVu Sans")

plt.tight_layout()
plt.savefig(output_dir / "02-padding-and-mask.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '02-padding-and-mask.png'}")
