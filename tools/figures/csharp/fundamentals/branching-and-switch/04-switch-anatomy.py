"""Анатомія switch statement (рядки на зразок switch-statement.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, anatomy, save  # noqa: E402

LINES = [
    "switch (day)",
    "{",
    "    case 6:",
    "    case 7:",
    '        Console.WriteLine("вихідний");',
    "        break;",
    "    default:",
    '        Console.WriteLine("робочий");',
    "        break;",
    "}",
]
MARKS = [(0, 0, 6, AMBER), (0, 7, 5, BLUE), (2, 4, 7, GREEN), (3, 4, 7, GREEN), (4, 8, 30, GREY), (5, 8, 6, RED),
         (6, 4, 8, GREEN), (7, 8, 29, GREY), (8, 8, 6, RED)]
NOTES = [
    (0, 3, "ключове слово switch", 8, 98, "center"),
    (0, 9.5, "вираз у дужках:\nобчислюється один раз", 52, 97, "left"),
    (2, 4, "мітка: case, константа,\nдвокрапка", 8, 72, "center"),
    (3, 4, "кілька міток підряд —\nодна секція", 8, 52, "center"),
    (4, 38, "секція: інструкції, які\nвиконуються для 6 і 7", 74, 66, "left"),
    (5, 14, "break — кінець секції;\nбез нього CS0163", 74, 46, "left"),
    (6, 4, "default: усі інші\nзначення", 8, 30, "center"),
    (8, 14, "останню секцію теж\nзавершують явно", 74, 22, "left"),
]
fig, ax = anatomy(15, 8.2, LINES, MARKS, NOTES, size=16, x0=30, y0=88, step=8.6)
save(fig, __file__)
