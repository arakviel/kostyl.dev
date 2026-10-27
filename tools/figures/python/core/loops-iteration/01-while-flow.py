import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, RED, arrow, box, canvas, save
from matplotlib.patches import Polygon


fig, ax = canvas(10, 3.8)
box(ax, 2, 44, 18, 20, "n = 3", GREY, mono=True, size=13)
ax.add_patch(Polygon([(26, 54), (38, 78), (50, 54), (38, 30)], closed=True, fc=AMBER, ec=INK, lw=1.4))
ax.text(38, 54, "n > 0 ?", ha="center", va="center", fontsize=13, fontfamily="DejaVu Sans Mono")
box(ax, 60, 44, 36, 20, "тіло циклу:\ntotal += n; n -= 1", BLUE, mono=True, size=11)
box(ax, 26, 2, 24, 16, "вихід з циклу", GREEN, size=12)
arrow(ax, 21, 54, 25.5, 54)
arrow(ax, 50.5, 54, 59, 54)
ax.text(54.5, 58, "так", ha="center", fontsize=11)
arrow(ax, 38, 29.5, 38, 19)
ax.text(40, 24, "ні", fontsize=11)
ax.annotate("", xy=(38, 79), xytext=(78, 65), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6, connectionstyle="arc3,rad=0.25"))
ax.text(78, 32, "після тіла — назад\nдо перевірки умови", ha="center", fontsize=11)
save(fig, __file__)
