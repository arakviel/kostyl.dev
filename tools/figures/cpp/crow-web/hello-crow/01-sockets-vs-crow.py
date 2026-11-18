import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.4)
ax.text(27, 96, "Без фреймворку", ha="center", fontsize=13, weight="bold")
steps = ["socket()", "bind()", "listen()", "accept()", "recv() і розбір тексту запиту", "формування відповіді вручну", "send() і close()"]
y = 86
for s in steps:
    box(ax, 4, y - 9, 46, 9, s, fc=GREY, mono=True, size=10.5)
    y -= 12
ax.text(78, 96, "З Crow", ha="center", fontsize=13, weight="bold")
box(ax, 58, 52, 40, 34, "CROW_ROUTE(app, \"/\")\n([]{ return \"Hello\"; });\n\napp.port(8080).run();", fc=GREEN, mono=True, size=10.5)
ax.text(78, 34, "сокети, розбір HTTP,\nстатуси, багатопоточність —\nу фреймворку", ha="center", fontsize=11.5, linespacing=1.4)
arrow(ax, 51, 60, 57, 60)
save(fig, __file__)
