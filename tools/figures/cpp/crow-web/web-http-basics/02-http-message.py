import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
def msg(x, title, rows, color):
    ax.text(x + 22, 96, title, ha="center", fontsize=13, weight="bold")
    y = 84
    for text, c, h in rows:
        box(ax, x, y - h, 44, h, text, fc=c, mono=True, size=10.5)
        y -= h + 3
msg(3, "Запит", [("GET /users/2 HTTP/1.1", BLUE, 12), ("Host: localhost:8080\nAccept: application/json", GREEN, 18), ("(порожній рядок)", GREY, 10), ("тіло (для POST)", AMBER, 12)], BLUE)
msg(53, "Відповідь", [("HTTP/1.1 200 OK", BLUE, 12), ("Content-Type: application/json\nContent-Length: 28", GREEN, 18), ("(порожній рядок)", GREY, 10), ('{"id":2,"name":"Марія"}', AMBER, 12)], BLUE)
for x in (49,):
    pass
ax.text(25, 4, "стартовий рядок · заголовки · порожній рядок · тіло", ha="center", fontsize=10.5)
ax.text(75, 4, "рядок стану · заголовки · порожній рядок · тіло", ha="center", fontsize=10.5)
save(fig, __file__)
