"""Анатомія оголошення і створення масиву (рядки на зразок array-forms.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, anatomy, save  # noqa: E402

LINES = [
    "int[] scores = new int[5];",
    "int[] primes = [2, 3, 5, 7];",
    "scores[0] = 90;",
]
MARKS = [(0, 0, 3, BLUE), (0, 3, 2, AMBER), (0, 6, 6, GREEN), (0, 15, 3, RED), (0, 22, 3, GREY),
         (1, 15, 12, GREY), (2, 6, 3, AMBER)]
NOTES = [
    (0, 1.5, "тип елемента", 8, 97, "center"),
    (0, 4, "[] після типу — масив;\nрозмір у тип не входить", 27, 97, "center"),
    (0, 9, "змінна: посилання\nна масив", 46.5, 97, "center"),
    (0, 16.5, "new створює масив\nу купі", 67.5, 97, "center"),
    (0, 23.5, "5 елементів,\nкожен дорівнює 0", 86, 97, "center"),
    (1, 28, "вираз колекції: елементи\nзадано, Length = 4", 70, 64, "left"),
    (2, 9, "індекс від 0 до Length − 1;\nпоза межами — виняток", 44, 28, "left"),
]
fig, ax = anatomy(15, 4.2, LINES, MARKS, NOTES, y0=75, step=11, x0=24)
ax.set_ylim(15, 100)
save(fig, __file__)
