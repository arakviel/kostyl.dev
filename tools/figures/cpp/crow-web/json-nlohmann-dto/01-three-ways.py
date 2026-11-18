import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.8)
items = [("crow::json", 'body["age"].i()\nвручну кожне поле', "є в Crow,\nбез залежностей", BLUE), ("nlohmann/json", 'j.at("age").get_to(d.age)\nабо get<User>()', "STL-стиль,\nавто-(де)серіалізація", GREEN)]
for i, (t, c, n, col) in enumerate(items):
    x = 3 + i * 49
    box(ax, x, 15, 45, 70, "", fc=col)
    ax.text(x + 22.5, 76, t, ha="center", fontsize=13, weight="bold")
    ax.text(x + 22.5, 54, c, ha="center", va="center", fontsize=11, family="DejaVu Sans Mono", linespacing=1.5)
    ax.text(x + 22.5, 28, n, ha="center", va="center", fontsize=11.5, linespacing=1.4)
save(fig, __file__)
