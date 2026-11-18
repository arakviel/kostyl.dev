import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.4)
box(ax, 2, 62, 28, 28, 'title: "A"\ndescription: "d"\ncompleted: false', fc=GREY, mono=True, size=10)
ax.text(16, 94, "Стан до запиту", ha="center", fontsize=12.5, weight="bold")
ax.text(66, 96, "Запит і результат", ha="center", fontsize=12.5, weight="bold")
box(ax, 36, 62, 28, 28, 'PUT\n{"title":"B"}', fc=AMBER, mono=True, size=10.5)
box(ax, 70, 62, 28, 28, '400: не вистачає\nполів description\nі completed', fc=RED, size=10.5)
arrow(ax, 31, 76, 35, 76); arrow(ax, 65, 76, 69, 76)
box(ax, 36, 14, 28, 28, 'PATCH\n{"title":"B"}', fc=BLUE, mono=True, size=10.5)
box(ax, 70, 14, 28, 28, 'title: "B"\ndescription: "d"\ncompleted: false', fc=GREEN, mono=True, size=10)
arrow(ax, 31, 40, 35, 30); arrow(ax, 65, 28, 69, 28)
box(ax, 2, 14, 28, 28, "той самий\nстартовий стан", fc=GREY, size=11)
save(fig, __file__)
