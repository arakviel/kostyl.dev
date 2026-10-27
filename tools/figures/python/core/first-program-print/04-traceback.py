import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt
from _style import AMBER, BLUE, GREEN, GREY, INK, RED, canvas, save

fig, ax = canvas(11, 3.8)
mono = dict(fontfamily="DejaVu Sans Mono", fontsize=10.5, va="center")
rows = [
    (86, "Traceback (most recent call last):", GREY),
    (70, '  File "hello.py", line 1, in <module>', BLUE),
    (54, '    prnt("Hello")', GREEN),
    (38, "    ^^^^", GREEN),
    (22, "NameError: name 'prnt' is not defined. Did you mean: 'print'?", RED),
]
for y, text, color in rows:
    ax.add_patch(plt.Rectangle((1, y - 6), 76, 12, fc=color, ec="none"))
    ax.text(2, y, text, **mono)
notes = [
    (70, "файл і номер рядка"),
    (54, "рядок із помилкою"),
    (38, "підкреслено, де саме"),
    (22, "тип помилки і пояснення"),
]
for y, text in notes:
    ax.annotate(text, xy=(78, y), xytext=(81, y), fontsize=11, va="center",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3))
save(fig, __file__)
