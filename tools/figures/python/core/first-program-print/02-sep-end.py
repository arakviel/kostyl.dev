import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREY, INK, box, canvas, save

fig, ax = canvas(10, 3.6)
ax.text(50, 90, 'print("My", "name", "is", "Monty", sep="-")', ha="center", fontsize=13, fontfamily="DejaVu Sans Mono")
words = ["My", "name", "is", "Monty"]
x = 3
w = 15
for i, word in enumerate(words):
    box(ax, x, 40, w, 22, word, BLUE, mono=True, size=13)
    x += w
    if i < len(words) - 1:
        box(ax, x + 0.8, 40, 5, 22, "-", AMBER, mono=True, size=14, weight="bold")
        x += 6.6
box(ax, x + 1, 40, 8, 22, "\\n", GREY, mono=True, size=13)
ax.text(50, 22, "жовті блоки — sep між аргументами, сірий — end у кінці виводу", ha="center", fontsize=11)
ax.text(50, 8, "Вивід: My-name-is-Monty", ha="center", fontsize=12, fontfamily="DejaVu Sans Mono")
save(fig, __file__)
