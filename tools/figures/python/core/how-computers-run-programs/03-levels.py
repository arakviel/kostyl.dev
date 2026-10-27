import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, arrow, box, canvas, save

fig, ax = canvas(10, 4.2)
box(ax, 4, 66, 92, 24, 'Мова високого рівня\nprint("Hello")', GREEN, size=14)
box(ax, 4, 34, 92, 24, "Переклад (компіляція, інтерпретація)", AMBER, size=13)
box(ax, 4, 2, 92, 24, "Машинний код\nчислові команди, які розуміє лише конкретний процесор", BLUE, size=13)
arrow(ax, 50, 66, 50, 59)
arrow(ax, 50, 34, 50, 27)
save(fig, __file__)
