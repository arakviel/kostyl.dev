import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.6)
steps = [("Тіло запиту\n(текст)", AMBER), ("json::parse\n→ json", BLUE), ("get<Dto>()\n→ CreateUserDto", BLUE), ("Перевірка\nі логіка", GREEN), ("User → json\n→ dump()", BLUE)]
for i, (t, c) in enumerate(steps):
    x = 1 + i * 20
    box(ax, x, 32, 17, 36, t, fc=c, size=10.5)
    if i < 4: arrow(ax, x + 17.6, 50, x + 19.6, 50)
ax.text(18, 22, "parse_error", ha="center", fontsize=10.5, color="#DC2626", family="DejaVu Sans Mono")
ax.text(50, 22, "out_of_range, type_error", ha="center", va="top", fontsize=10.5, color="#DC2626", family="DejaVu Sans Mono")
ax.text(50, 4, "Кожен тип винятку відповідає своїй причині й стає відповіддю 400", ha="center", fontsize=12)
save(fig, __file__)
