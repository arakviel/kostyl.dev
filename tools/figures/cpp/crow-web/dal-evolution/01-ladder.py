import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
steps = [("1. Прямий доступ", "кожен обробник\nчитає файл сам", RED), ("2. Функції", "load_users /\nsave_users", AMBER), ("3. DAO", "клас UserDao\nховає сховище", BLUE), ("4. Active Record", "модель сама\nзберігає себе", BLUE), ("5. Repository", "інтерфейс +\nреалізації", GREEN)]
for i, (t, d, c) in enumerate(steps):
    x = 1 + i * 20
    h = 28 + i * 9
    box(ax, x, 12, 18, h, "", fc=c)
    ax.text(x + 9, 12 + h - 5, t, ha="center", va="top", fontsize=10.5, weight="bold")
    ax.text(x + 9, 12 + h / 2 - 5, d, ha="center", va="center", fontsize=10.5, linespacing=1.4)
ax.text(50, 3, "Кожен крок відокремлює більше: дублювання, формат, сховище, залежність від конкретної реалізації", ha="center", fontsize=11)
save(fig, __file__)
