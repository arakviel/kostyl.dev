"""
Візуалізація обмеження усереднення: речення з різним порядком слів мають однаковий вектор.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/embeddings-for-classification")
output_dir.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(12, 7), dpi=200)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# Речення 1: "not good"
y1 = 7.5
ax.text(1, y1 + 0.5, 'Речення 1: "not good"', fontsize=12,
        fontweight="bold", color="#1E293B", family="DejaVu Sans")

# Слова
for i, (word, color) in enumerate([("not", "#DC2626"), ("good", "#16A34A")]):
    x = 1.5 + i * 2
    rect = patches.FancyBboxPatch((x - 0.4, y1 - 0.3), 0.8, 0.6,
                                  boxstyle="round,pad=0.05", linewidth=2,
                                  edgecolor=color, facecolor=f"{color}20")
    ax.add_patch(rect)
    ax.text(x, y1, word, ha="center", va="center", fontsize=11,
            fontweight="bold", color=color, family="DejaVu Sans")

# Стрілка до вектора
ax.annotate("", xy=(6, y1), xytext=(4, y1),
            arrowprops=dict(arrowstyle="->", color="#64748B", lw=2))

# Вектор
rect_v1 = patches.FancyBboxPatch((6, y1 - 0.4), 2.5, 0.8,
                                 boxstyle="round,pad=0.05", linewidth=2,
                                 edgecolor="#2563EB", facecolor="#DBEAFE", alpha=0.7)
ax.add_patch(rect_v1)
ax.text(7.25, y1, "[0.12, -0.34, ...]", ha="center", va="center",
        fontsize=10, fontweight="bold", color="#2563EB", family="DejaVu Sans")

# Речення 2: "good not"
y2 = 5
ax.text(1, y2 + 0.5, 'Речення 2: "good not"', fontsize=12,
        fontweight="bold", color="#1E293B", family="DejaVu Sans")

# Слова (зворотний порядок)
for i, (word, color) in enumerate([("good", "#16A34A"), ("not", "#DC2626")]):
    x = 1.5 + i * 2
    rect = patches.FancyBboxPatch((x - 0.4, y2 - 0.3), 0.8, 0.6,
                                  boxstyle="round,pad=0.05", linewidth=2,
                                  edgecolor=color, facecolor=f"{color}20")
    ax.add_patch(rect)
    ax.text(x, y2, word, ha="center", va="center", fontsize=11,
            fontweight="bold", color=color, family="DejaVu Sans")

# Стрілка
ax.annotate("", xy=(6, y2), xytext=(4, y2),
            arrowprops=dict(arrowstyle="->", color="#64748B", lw=2))

# Вектор (ідентичний)
rect_v2 = patches.FancyBboxPatch((6, y2 - 0.4), 2.5, 0.8,
                                 boxstyle="round,pad=0.05", linewidth=2,
                                 edgecolor="#2563EB", facecolor="#DBEAFE", alpha=0.7)
ax.add_patch(rect_v2)
ax.text(7.25, y2, "[0.12, -0.34, ...]", ha="center", va="center",
        fontsize=10, fontweight="bold", color="#2563EB", family="DejaVu Sans")

# Знак рівності
ax.text(7.25, 6.25, "=", ha="center", va="center", fontsize=24,
        fontweight="bold", color="#D97706", family="DejaVu Sans")

# Пояснення
ax.text(5, 3, "Проблема: усереднення не зберігає порядок слів!",
        ha="center", fontsize=13, fontweight="bold", color="#DC2626",
        family="DejaVu Sans",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF3C7", alpha=0.8))

ax.text(5, 2.1, "Речення з протилежним змістом отримують однаковий вектор",
        ha="center", fontsize=11, color="#64748B", family="DejaVu Sans",
        style="italic")

# Рішення
ax.text(5, 0.8, "Рішення: послідовні моделі (RNN, LSTM) — лекції 11–13",
        ha="center", fontsize=11, fontweight="bold", color="#16A34A",
        family="DejaVu Sans",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#DCFCE7", alpha=0.8))

plt.tight_layout()
plt.savefig(output_dir / "03-averaging-limitation.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '03-averaging-limitation.png'}")
