"""RNN: згорнута схема і розгортка в часі."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 4.6)

# згорнута форма
box(ax, 6, 40, 14, 20, "RNN", fc=BLUE, weight="bold", size=15)
arrow(ax, 13, 18, 13, 39, "")
ax.text(13, 8, "xₜ", ha="center", fontsize=14)
arrow(ax, 13, 61, 13, 82)
ax.text(13, 87, "hₜ", ha="center", fontsize=14)
ax.add_patch(FancyArrowPatch((20.5, 55), (20.5, 45), connectionstyle="arc3,rad=-1.6",
                             arrowstyle="-|>", mutation_scale=18, lw=1.6, color=INK))
ax.text(24, 50, "hₜ₋₁", ha="left", va="center", fontsize=12)
ax.text(13, 98, "згорнута форма", ha="center", fontsize=12, color="#475569")

ax.plot([34, 34], [5, 95], color="#CBD5E1", lw=1.2, ls="--")

# розгортка
xs = [46, 64, 82]
labels = ["t = 1", "t = 2", "t = 3"]
words = ["not", "very", "good"]
ax.text(67, 98, "розгортка в часі: ті самі ваги W на кожному кроці", ha="center", fontsize=12, color="#475569")
ax.text(39.5, 56, "h₀ = 0", ha="center", va="center", fontsize=12)
for i, x in enumerate(xs):
    box(ax, x, 40, 14, 20, "RNN", fc=BLUE, weight="bold", size=14)
    arrow(ax, x + 7, 22, x + 7, 39)
    ax.text(x + 7, 14, f"x{'₁₂₃'[i]}", ha="center", fontsize=13)
    ax.text(x + 7, 6, f"«{words[i]}»", ha="center", fontsize=12, color="#475569")
    arrow(ax, x + 7, 61, x + 7, 78)
    ax.text(x + 7, 83, f"h{'₁₂₃'[i]}", ha="center", fontsize=13)
    if i < 2:
        arrow(ax, x + 14.6, 50, xs[i + 1] - 0.6, 50)
ax.annotate("", xy=(45.4, 50), xytext=(36.5, 50), arrowprops=dict(arrowstyle="-|>", lw=1.6, color=INK))
save(fig, __file__)
