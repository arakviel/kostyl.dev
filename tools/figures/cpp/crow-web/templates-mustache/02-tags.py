import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
ax.text(2, 94, "Тег", fontsize=12.5, weight="bold"); ax.text(30, 94, "Дія", fontsize=12.5, weight="bold"); ax.text(70, 94, "Приклад", fontsize=12.5, weight="bold")
rows = [("{{name}}", "значення, HTML екранується", "&lt;b&gt;", GREEN), ("{{{name}}}", "значення без екранування", "<b>", RED), ("{{#users}}…{{/users}}", "цикл або умова", "<li>…</li>", BLUE), ("{{^users}}…{{/users}}", "якщо порожньо чи false", "«немає»", AMBER), ("{{>nav.html}}", "вставка частини (partial)", "<nav>…", GREY)]
y = 80
for t, d, e, c in rows:
    box(ax, 1, y - 6, 98, 12, "", fc=c)
    ax.text(3, y, t, va="center", fontsize=10.5, family="DejaVu Sans Mono")
    ax.text(30, y, d, va="center", fontsize=11)
    ax.text(70, y, e, va="center", fontsize=10.5, family="DejaVu Sans Mono")
    y -= 15
save(fig, __file__)
