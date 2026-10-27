import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import ACCENT, INK, canvas, save
STRONG_RED = "#DC2626"
import matplotlib.pyplot as plt

x = -7 / 2
q, r = -7 // 2, -7 % 2
fig, ax = plt.subplots(figsize=(10, 3.4))
ax.set_xlim(-6.5, 1.5)
ax.set_ylim(-1.5, 2.2)
ax.axis("off")
ax.annotate("", xy=(1.4, 0), xytext=(-6.4, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
for i in range(-6, 2):
    ax.plot([i, i], [-0.12, 0.12], color=INK, lw=1.4)
    ax.text(i, -0.45, str(i), ha="center", fontsize=12)
ax.plot([x], [0], "o", color=STRONG_RED, ms=11)
ax.text(x, 0.45, f"-7 / 2 = {x}", ha="center", fontsize=12, color=STRONG_RED)
ax.annotate("", xy=(q, 0.9), xytext=(x, 0.9), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=2))
ax.text((q + x) / 2 - 0.9, 1.15, "округлення вниз", ha="center", fontsize=11.5, color=ACCENT)
ax.plot([q], [0], "o", color=ACCENT, ms=11)
ax.text(q, -1.0, f"-7 // 2 = {q}", ha="center", fontsize=12, color=ACCENT, fontweight="bold")
ax.text(-1.1, 1.7, f"-7 = 2 · ({q}) + {r}  →  -7 % 2 = {r}", ha="center", fontsize=12.5, fontfamily="DejaVu Sans Mono")
save(fig, __file__)
