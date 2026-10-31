"""Одне слово — кілька значень; одне поняття — кілька форм."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.4)
ax.text(25, 96, "Одне слово — різні значення", ha="center", fontsize=13, fontweight="bold")
box(ax, 17, 62, 16, 14, "ключ", fc=AMBER, weight="bold", size=14)
for i, t in enumerate(["від дверей", "скрипковий", "до розгадки"]):
    x = 1 + i * 16.5
    box(ax, x, 14, 15, 14, t, fc=BLUE, size=11)
    arrow(ax, 25, 61, x + 7.5, 30)
ax.text(78, 96, "Одне поняття — різні форми", ha="center", fontsize=13, fontweight="bold")
box(ax, 70, 62, 16, 14, "біг-", fc=GREEN, weight="bold", size=14)
for i, t in enumerate(["бігти", "біг", "бігав", "біжить"]):
    x = 52.5 + i * 11.8
    box(ax, x, 14, 10.5, 14, t, fc=GREY, size=11)
    arrow(ax, 78, 61, x + 5.25, 30)
save(fig, __file__)
