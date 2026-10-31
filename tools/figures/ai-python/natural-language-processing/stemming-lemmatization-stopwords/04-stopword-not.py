"""Видалення стоп-слів прибирає «not» і перевертає зміст."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

before = "this is a very good movie and i really enjoyed the acting but the ending was not good".split()
stop = {"this", "is", "a", "very", "and", "i", "the", "but", "was", "not"}
fig, ax = canvas(12, 4.6)
ax.text(1, 93, "До видалення (18 слів)", fontsize=13, fontweight="bold")
cols = [RED if w == "not" else (GREY if w in stop else GREEN) for w in before]
chips(ax, 1, 70, before[:10], colors=cols[:10], char_w=1.45, pad=2.4)
chips(ax, 1, 56, before[10:], colors=cols[10:], char_w=1.45, pad=2.4)
after = [w for w in before if w not in stop]
ax.text(1, 38, "Після видалення (7 слів): «not» зник разом зі «службовими» словами", fontsize=13, fontweight="bold")
chips(ax, 1, 20, after, fc=GREEN, char_w=1.45, pad=2.4)
ax.text(1, 4, "Відгук із запереченням став схожим на позитивний", fontsize=13, color="#DC2626", fontweight="bold")
save(fig, __file__)
