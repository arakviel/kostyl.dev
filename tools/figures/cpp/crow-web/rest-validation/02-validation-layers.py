import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.0)
layers = [("Формат", "Content-Type\n= JSON?", "415", AMBER), ("Синтаксис", "тіло — це\nкоректний\nJSON?", "400", AMBER), ("Дані", "типи,\nобов'язковість,\nдіапазони", "400", AMBER), ("Бізнес-правила", "email\nунікальний?", "409", RED), ("Збереження", "запис у\nсховище", "201", GREEN)]
for i, (n, d, code, c) in enumerate(layers):
    x = 1 + i * 20
    box(ax, x, 22, 18, 62, "", fc=c)
    ax.text(x + 9, 76, n, ha="center", fontsize=11.5, weight="bold")
    ax.text(x + 9, 54, d, ha="center", va="center", fontsize=10.2, linespacing=1.4)
    ax.text(x + 9, 32, code, ha="center", va="center", fontsize=20, weight="bold")
    if i < 4:
        arrow(ax, x + 18.4, 53, x + 19.6, 53)
ax.text(50, 8, "Перша ж невдала перевірка зупиняє запит і повертає відповідний код", ha="center", fontsize=12)
save(fig, __file__)
