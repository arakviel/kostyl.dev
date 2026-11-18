import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
rows = [("/users/2", "/users/<int>", "збіг, id = 2", GREEN), ("/users/abc", "/users/<int>", "немає збігу → 404", RED), ("/hello/Ola", "/hello/<string>", "збіг, name = \"Ola\"", GREEN), ("/files/a/b.txt", "/files/<path>", "збіг, p = \"a/b.txt\"", GREEN), ("/files/a/b.txt", "/files/<string>", "немає збігу: <string> без слешів", RED)]
ax.text(4, 94, "Запитаний шлях", fontsize=12, weight="bold")
ax.text(36, 94, "Шаблон маршруту", fontsize=12, weight="bold")
ax.text(70, 94, "Результат", fontsize=12, weight="bold")
y = 82
for p, t, r, c in rows:
    ax.text(4, y, p, fontsize=11, family="DejaVu Sans Mono", va="center")
    ax.text(36, y, t, fontsize=11, family="DejaVu Sans Mono", va="center")
    box(ax, 68, y - 5, 30, 10, r, fc=c, size=10)
    y -= 15
save(fig, __file__)
