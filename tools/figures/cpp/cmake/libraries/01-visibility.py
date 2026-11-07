import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
box(ax, 2, 8, 44, 84, "", fc=GREY)
ax.text(24, 88, "MyLib (бібліотека)", ha="center", va="top", fontsize=13, weight="bold")
box(ax, 5, 56, 38, 18, "PRIVATE\nтільки всередині MyLib", fc=RED, size=11.5)
box(ax, 5, 33, 38, 18, "PUBLIC\nу MyLib і в користувачів", fc=GREEN, size=11.5)
box(ax, 5, 11, 38, 18, "INTERFACE\nтільки в користувачів", fc=BLUE, size=11.5)
box(ax, 58, 8, 40, 84, "", fc=AMBER)
ax.text(78, 88, "MyApp (програма)", ha="center", va="top", fontsize=13, weight="bold")
box(ax, 61, 42, 34, 18, "бачить PUBLIC", fc=GREEN, size=11.5)
box(ax, 61, 19, 34, 18, "бачить INTERFACE", fc=BLUE, size=11.5)
ax.text(78, 70, "НЕ бачить PRIVATE", ha="center", va="center", fontsize=11.5, color="#DC2626", weight="bold")
arrow(ax, 43, 42, 61, 51)
arrow(ax, 43, 20, 61, 28)
save(fig, __file__)
