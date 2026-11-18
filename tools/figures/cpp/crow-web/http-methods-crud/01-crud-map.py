import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.4)
cols = [("Операція", 3, 18), ("HTTP-запит", 23, 36), ("Успіх", 61, 18), ("Помилки", 81, 18)]
for t, x, w in cols:
    ax.text(x, 92, t, fontsize=12.5, weight="bold")
rows = [("Create", "POST /todos", "201 + Location", "400"), ("Read (всі)", "GET /todos", "200", "—"), ("Read (один)", "GET /todos/1", "200", "404"), ("Update повний", "PUT /todos/1", "200", "400, 404"), ("Update частковий", "PATCH /todos/1", "200", "400, 404"), ("Delete", "DELETE /todos/1", "204", "404")]
y = 78
for i, r in enumerate(rows):
    c = [BLUE, GREEN, GREEN, AMBER, AMBER, RED][i]
    box(ax, 1, y - 5.5, 98, 11, "", fc=c)
    ax.text(3, y, r[0], va="center", fontsize=11.5)
    ax.text(23, y, r[1], va="center", fontsize=11, family="DejaVu Sans Mono")
    ax.text(61, y, r[2], va="center", fontsize=11)
    ax.text(81, y, r[3], va="center", fontsize=11)
    y -= 13.5
save(fig, __file__)
