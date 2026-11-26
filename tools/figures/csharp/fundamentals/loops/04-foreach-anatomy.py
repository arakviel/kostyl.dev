"""Анатомія foreach (рядки на зразок foreach-forms.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, anatomy, save  # noqa: E402

LINES = [
    "foreach (int score in scores)",
    "{",
    "    total += score;",
    "}",
]
MARKS = [(0, 0, 7, AMBER), (0, 9, 3, BLUE), (0, 13, 5, RED), (0, 19, 2, AMBER), (0, 22, 6, GREEN),
         (2, 4, 15, GREY)]
NOTES = [
    (0, 3.5, "ключове слово foreach", 8, 97, "center"),
    (0, 10.5, "тип елемента\nабо var", 27, 97, "center"),
    (0, 15.5, "змінна ітерації: новий\nелемент на кожному кроці,\nлише для читання", 47, 97, "center"),
    (0, 25, "in і колекція: масив, рядок, List,\nEnumerable.Range — тип\nз методом GetEnumerator", 70, 97, "left"),
    (2, 19, "тіло: виконується\nдля кожного елемента", 62, 52, "left"),
]
fig, ax = anatomy(15, 2.9, LINES, MARKS, NOTES, y0=74, step=11, x0=20)
ax.set_ylim(36, 100)   # нижня частина полотна порожня
save(fig, __file__)
