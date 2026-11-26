"""Анатомія рваного масиву int[][] (рядки на зразок jagged.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, anatomy, save  # noqa: E402

LINES = [
    "int[][] rows = new int[3][];",
    "rows[1] = [2, 3];",
    "int x = rows[1][0];",
]
MARKS = [(0, 0, 3, BLUE), (0, 3, 4, AMBER), (0, 22, 3, GREEN), (0, 25, 2, RED), (1, 0, 7, GREY),
         (2, 12, 3, GREEN), (2, 15, 3, AMBER)]
NOTES = [
    (0, 1.5, "тип елемента\nрядка", 8, 97, "center"),
    (0, 5, "[][] — масив масивів:\nкожен елемент — int[]", 30, 97, "center"),
    (0, 23.5, "3 рядки", 52, 97, "center"),
    (0, 27.8, "довжини рядків не задано:\nусі три рядки — null", 72, 80, "left"),
    (1, 17, "кожен рядок створюється окремо\nі має власну довжину", 50, 67, "left"),
    (2, 13.5, "[1] — номер рядка", 36, 22, "center"),
    (2, 16.5, "[0] — номер елемента в рядку", 56, 22, "left"),
]
fig, ax = anatomy(15, 4.2, LINES, MARKS, NOTES, y0=78, step=11, x0=22)
ax.set_ylim(12, 100)
save(fig, __file__)
