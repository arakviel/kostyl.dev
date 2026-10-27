import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import ACCENT, INK, canvas, save
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 3.2))
ax.set_xlim(-2, 13)
ax.set_ylim(-1.6, 2.4)
ax.axis("off")
ax.annotate("", xy=(12.8, 0), xytext=(-1.8, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
for i in range(-1, 13):
    ax.plot([i, i], [-0.1, 0.1], color=INK, lw=1.2)
    ax.text(i, -0.45, str(i), ha="center", fontsize=11)
ax.fill_between([0, 10], -0.18, 0.18, color="#DBEAFE", zorder=0)
ax.plot([0], [0], "o", mfc="white", mec=INK, ms=11)
ax.plot([10], [0], "o", mfc="white", mec=INK, ms=11)
ax.plot([7], [0], "o", color=ACCENT, ms=12)
ax.text(7, 0.5, "x = 7", ha="center", fontsize=13, color=ACCENT, fontweight="bold")
ax.text(5, 1.4, "0 < x < 10   —   те саме, що   0 < x and x < 10", ha="center", fontsize=13, fontfamily="DejaVu Sans Mono")
ax.text(5, -1.2, "порожні кружки: межі 0 і 10 не входять", ha="center", fontsize=11)
save(fig, __file__)
