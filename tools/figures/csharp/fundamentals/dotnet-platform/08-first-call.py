"""Час п'яти викликів SumTo(1000): перший містить JIT-компіляцію (реальний запуск tiered-jit.cs, .NET 10.0.15)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt  # noqa: E402
from _style import INK, save  # noqa: E402

calls = ["1", "2", "3", "4", "5"]
micros = [39.2, 2.2, 2.2, 2.2, 2.2]
colors = ["#D97706"] + ["#2563EB"] * 4

fig, ax = plt.subplots(figsize=(9, 4.2))
bars = ax.bar(calls, micros, color=colors, width=0.6)
for bar, value in zip(bars, micros):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 0.8, f"{value:.1f} мкс".replace(".", ","), ha="center", fontsize=12)

ax.set_xlabel("Номер виклику", fontsize=12)
ax.set_ylabel("Час, мкс", fontsize=12)
ax.set_ylim(0, 46)
ax.spines[["top", "right"]].set_visible(False)
ax.annotate("JIT-компіляція +\nвиконання", xy=(0.3, 30), xytext=(1.3, 30), fontsize=11.5,
            arrowprops=dict(arrowstyle="-|>", color=INK), va="center")
ax.text(3, 10, "лише виконання\nготового машинного коду", ha="center", fontsize=11.5)
save(fig, __file__)
