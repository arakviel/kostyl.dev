"""Анатомія if / else (рядки на зразок if-forms.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, anatomy, save  # noqa: E402

LINES = [
    "if (temperature < 0)",
    "{",
    '    Console.WriteLine("мороз");',
    "}",
    "else",
    "{",
    '    Console.WriteLine("не мороз");',
    "}",
]
MARKS = [(0, 0, 2, AMBER), (0, 3, 17, BLUE), (2, 4, 27, GREEN), (4, 0, 4, AMBER), (6, 4, 30, RED),
         (1, 0, 1, GREY), (3, 0, 1, GREY)]
NOTES = [
    (0, 1, "ключове слово if", 6, 96, "center"),
    (0, 12, "умова в круглих дужках:\nвираз типу bool;\nдужки обов'язкові", 62, 94, "left"),
    (2, 31, "гілка «так»: виконується,\nякщо умова true", 70, 61, "left"),
    (4, 2, "else — необов'язкова\nгілка «ні»", 6, 42, "center"),
    (6, 34, "гілка «ні»: виконується,\nякщо умова false", 70, 23, "left"),
    (3, 0.5, "{ } — блок; для однієї\nінструкції дужки можна\nпропустити", 6, 66, "center"),
]
fig, ax = anatomy(15, 7.6, LINES, MARKS, NOTES, y0=84, step=9.2, x0=26)
save(fig, __file__)
