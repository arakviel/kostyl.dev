"""Анатомія while і do-while (рядки на зразок while-forms.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, anatomy, save  # noqa: E402

LINES = [
    "while (number > 0)",
    "{",
    "    number /= 10;",
    "}",
    "",
    "do",
    "{",
    "    number /= 10;",
    "} while (number > 0);",
]
MARKS = [(0, 0, 5, AMBER), (0, 6, 12, GREEN), (2, 4, 13, GREY),
         (5, 0, 2, AMBER), (7, 4, 13, GREY), (8, 2, 5, AMBER), (8, 8, 12, GREEN), (8, 20, 1, RED)]
NOTES = [
    (0, 0, "while — цикл\nз передумовою", 10, 88, "center"),
    (0, 18, "умова bool перед тілом:\nякщо вона одразу false,\nтіло не виконається жодного разу", 62, 88, "left"),
    (2, 17, "тіло", 50, 70.8, "left"),
    (5, 0, "do — цикл\nз післяумовою", 10, 45, "center"),
    (7, 17, "тіло виконується хоча б раз", 50, 27.8, "left"),
    (8, 14, "умова після тіла", 40, 2, "center"),
    (8, 20.5, "; після умови обов'язкова", 64, 8, "left"),
]
fig, ax = anatomy(14, 7.6, LINES, MARKS, NOTES, y0=88, step=8.6, x0=24, size=17)
save(fig, __file__)
