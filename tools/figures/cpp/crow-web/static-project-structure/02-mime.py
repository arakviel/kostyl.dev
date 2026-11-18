import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
ax.text(4, 94, "Розширення", fontsize=12.5, weight="bold"); ax.text(30, 94, "Content-Type", fontsize=12.5, weight="bold"); ax.text(72, 94, "Браузер", fontsize=12.5, weight="bold")
rows = [(".html", "text/html; charset=utf-8", "показує сторінку", GREEN), (".css", "text/css", "застосовує стилі", GREEN), (".js", "application/javascript", "виконує скрипт", GREEN), (".svg", "image/svg+xml", "малює зображення", GREEN), (".bin", "application/octet-stream", "пропонує зберегти", AMBER)]
y = 80
for e, t, b, c in rows:
    box(ax, 1, y - 6, 98, 12, "", fc=c)
    ax.text(4, y, e, va="center", fontsize=11, family="DejaVu Sans Mono")
    ax.text(30, y, t, va="center", fontsize=10.8, family="DejaVu Sans Mono")
    ax.text(72, y, b, va="center", fontsize=11)
    y -= 15
save(fig, __file__)
