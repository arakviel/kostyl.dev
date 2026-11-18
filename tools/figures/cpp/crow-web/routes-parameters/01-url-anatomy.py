import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.4)
parts = [("http", "схема", BLUE, 1, 9), ("://", "", None, 10, 5), ("localhost", "хост", GREEN, 16, 17), (":8080", "порт", AMBER, 35, 11), ("/users/2", "шлях\n(path)", BLUE, 48, 17), ("?q=Марія&limit=5", "рядок запиту\n(query)", GREEN, 67, 31)]
for t, n, c, x, w in parts:
    if c:
        box(ax, x, 48, w, 20, t, fc=c, mono=True, size=11.5)
        ax.text(x + w / 2, 32, n, ha="center", va="center", fontsize=11, linespacing=1.3)
    else:
        ax.text(x + w / 2, 58, t, ha="center", va="center", fontsize=12, family="DejaVu Sans Mono")
ax.text(50, 10, "Маршрут Crow зіставляється зі шляхом. Query-параметри читаються з req.url_params.", ha="center", fontsize=12)
save(fig, __file__)
