"""
Порівняння точності мішка слів і embeddings на IMDB.
"""
import matplotlib.pyplot as plt
from pathlib import Path

output_dir = Path("public/images/ai-python/natural-language-processing/embeddings-for-classification")
output_dir.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 6), dpi=200)

methods = ["Мішок слів\n(5000 слів)", "Усереднені вектори\n(GloVe 100d)"]
accuracies = [83.8, 86.7]
colors = ["#64748B", "#16A34A"]

bars = ax.bar(methods, accuracies, color=colors, alpha=0.8, edgecolor="black", linewidth=2, width=0.6)

# Значення на стовпчиках
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.5,
            f"{acc:.1f}%", ha="center", va="bottom",
            fontsize=14, fontweight="bold", color="#1E293B", family="DejaVu Sans")

# Стрілка покращення
ax.annotate("", xy=(1, 86.7), xytext=(1, 84.5),
            arrowprops=dict(arrowstyle="->", color="#D97706", lw=2.5))
ax.text(1.15, 85.5, "+2.9%", fontsize=13, fontweight="bold",
        color="#D97706", family="DejaVu Sans")

ax.set_ylabel("Точність на тесті (%)", fontsize=12, fontweight="bold", family="DejaVu Sans")
ax.set_title("Порівняння методів класифікації відгуків IMDB",
             fontsize=14, fontweight="bold", color="#1E293B", family="DejaVu Sans", pad=20)
ax.set_ylim(75, 90)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig(output_dir / "02-accuracy-comparison.png", dpi=200, bbox_inches="tight", facecolor="white")
print(f"✓ Збережено: {output_dir / '02-accuracy-comparison.png'}")
