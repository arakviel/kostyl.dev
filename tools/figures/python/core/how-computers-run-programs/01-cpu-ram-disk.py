import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import BLUE, GREEN, GREY, arrow, box, canvas, save

fig, ax = canvas(10, 3.4)
box(ax, 1, 25, 20, 50, "Диск\nзберігає\nфайли постійно\nповільний", GREY, size=12)
box(ax, 40, 25, 20, 50, "Оперативна\nпам'ять (RAM)\nкод і дані\nпід час роботи", BLUE, size=12)
box(ax, 79, 25, 20, 50, "Процесор\n(CPU)\nвиконує\nінструкції", GREEN, size=12)
arrow(ax, 23, 55, 38, 55, "1. завантажити", size=10)
arrow(ax, 62, 62, 77, 62, "2. прочитати", size=10)
arrow(ax, 77, 40, 62, 40, "3. записати", size=10)
save(fig, __file__)
