import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.6)
box(ax, 1, 28, 24, 46, "crow::request\nметод, url,\nurl_params,\nheaders, body", fc=BLUE, size=11.5)
box(ax, 38, 28, 24, 46, "Обробник\n(лямбда)\nвирішує, що\nвідповісти", fc=GREEN, size=11.5, weight="bold")
box(ax, 75, 28, 24, 46, "crow::response\nкод, заголовки,\nтіло", fc=AMBER, size=11.5)
arrow(ax, 26, 51, 37, 51)
arrow(ax, 63, 51, 74, 51)
ax.text(50, 10, "Обробник приймає request і повертає response (або рядок/JSON, який Crow загорне сам)", ha="center", fontsize=11.5)
save(fig, __file__)
