import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.8)
box(ax, 2, 62, 96, 24, "Глобальні (для кожного запиту):  CORSHandler → AccessLog → RateLimit", fc=BLUE, size=11.5)
box(ax, 2, 28, 44, 24, "/public\nтільки глобальні", fc=GREEN, size=11.5, mono=False)
box(ax, 54, 28, 44, 24, "/admin\nглобальні + ApiKeyAuth", fc=AMBER, size=11.5)
arrow(ax, 24, 61, 24, 53); arrow(ax, 76, 61, 76, 53)
ax.text(50, 10, "Локальний middleware підключають до маршруту: .CROW_MIDDLEWARES(app, ApiKeyAuth)", ha="center", fontsize=11.5)
save(fig, __file__)
