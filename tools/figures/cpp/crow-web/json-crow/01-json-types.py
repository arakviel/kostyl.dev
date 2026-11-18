import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
ax.text(4, 93, "JSON", fontsize=12.5, weight="bold"); ax.text(30, 93, "type()", fontsize=12.5, weight="bold"); ax.text(58, 93, "Читання з rvalue", fontsize=12.5, weight="bold")
rows = [('"Іван"', "String", ".s()", GREEN), ("25  або  4.75", "Number", ".i()  .d()", GREEN), ("true / false", "True / False", ".b()", GREEN), ("null", "Null", "перевірка t()", GREY), ("[1, 2]", "List", "for (auto& x : v)  .size()", BLUE), ('{"a": 1}', "Object", 'v["a"]  .has("a")  .keys()', BLUE)]
y = 80
for j, t, m, c in rows:
    box(ax, 1, y - 5.5, 98, 11, "", fc=c)
    ax.text(4, y, j, va="center", fontsize=11, family="DejaVu Sans Mono")
    ax.text(30, y, t, va="center", fontsize=11)
    ax.text(58, y, m, va="center", fontsize=10.5, family="DejaVu Sans Mono")
    y -= 13.5
save(fig, __file__)
