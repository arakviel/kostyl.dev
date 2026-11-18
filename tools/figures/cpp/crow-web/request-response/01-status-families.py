import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.8)
fams = [("1xx", "інформаційні", "100", GREY), ("2xx", "успіх", "200 OK\n201 Created\n204 No Content", GREEN), ("3xx", "перенаправлення", "301, 302\n304 Not Modified", BLUE), ("4xx", "помилка клієнта", "400, 401, 403\n404, 409, 429", AMBER), ("5xx", "помилка сервера", "500\n502, 503", RED)]
for i, (c, n, ex, col) in enumerate(fams):
    x = 1 + i * 20
    box(ax, x, 18, 18, 72, "", fc=col)
    ax.text(x + 9, 80, c, ha="center", fontsize=18, weight="bold")
    ax.text(x + 9, 66, n, ha="center", fontsize=10.5)
    ax.text(x + 9, 40, ex, ha="center", va="center", fontsize=10, family="DejaVu Sans Mono", linespacing=1.5)
ax.text(50, 6, "Перша цифра коду показує, хто відповідає за результат", ha="center", fontsize=12)
save(fig, __file__)
