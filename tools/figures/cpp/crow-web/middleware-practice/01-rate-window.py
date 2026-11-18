import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.4)
ax.plot([3, 97], [45, 45], color=INK, lw=1.6)
for i in range(7):
    x = 8 + i * 9.5
    ok = i < 5
    ax.add_patch(plt.Circle((x, 45), 3.2, fc=GREEN if ok else "#FCA5A5", ec=INK, lw=1.4))
    ax.text(x, 45, str(i + 1), ha="center", va="center", fontsize=11, weight="bold")
    ax.text(x, 30, "200" if ok else "429", ha="center", fontsize=11, family="DejaVu Sans Mono")
ax.plot([76, 76], [38, 62], color="#2563EB", lw=2, linestyle="--")
ax.text(76, 66, "вікно закінчилось,\nлічильник = 0", ha="center", fontsize=10.5, color="#2563EB")
ax.text(8, 66, "вікно 10 с, ліміт 5 запитів", fontsize=11.5)
ax.add_patch(plt.Circle((90, 45), 3.2, fc=GREEN, ec=INK, lw=1.4)); ax.text(90, 45, "1", ha="center", va="center", fontsize=11, weight="bold"); ax.text(90, 30, "200", ha="center", fontsize=11, family="DejaVu Sans Mono")
ax.text(50, 10, "Кожен IP має свій лічильник; після перевищення сервер повертає Retry-After", ha="center", fontsize=11.5)
save(fig, __file__)
