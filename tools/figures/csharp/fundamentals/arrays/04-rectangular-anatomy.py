"""Анатомія прямокутного масиву int[,] (рядки на зразок rectangular.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, anatomy, save  # noqa: E402

LINES = [
    "int[,] grid = new int[2, 3];",
    "grid[1, 2] = 6;",
]
MARKS = [(0, 0, 3, BLUE), (0, 3, 3, AMBER), (0, 22, 6, GREEN), (1, 4, 6, GREY)]
NOTES = [
    (0, 1.5, "тип елемента", 8, 95, "center"),
    (0, 4.5, "[,] — кома між дужками:\nдва виміри, Rank = 2", 32, 95, "center"),
    (0, 25, "2 рядки по 3 стовпці:\nGetLength(0) = 2, GetLength(1) = 3,\nLength = 6", 70, 92, "left"),
    (1, 7, "індекс: рядок і стовпець\nчерез кому в одних дужках", 58, 40, "left"),
]
fig, ax = anatomy(15, 3.2, LINES, MARKS, NOTES, y0=70, step=13, x0=24)
ax.set_ylim(28, 100)
save(fig, __file__)
