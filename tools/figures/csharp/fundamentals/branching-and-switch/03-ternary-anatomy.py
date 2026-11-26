"""Анатомія умовного оператора ?: (рядок на зразок ternary.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, anatomy, save  # noqa: E402

LINES = ['string text = t < 0 ? "мороз" : "не мороз";']
MARKS = [(0, 0, 13, GREY), (0, 14, 5, BLUE), (0, 20, 1, AMBER), (0, 22, 7, GREEN), (0, 30, 1, AMBER), (0, 32, 10, RED)]
NOTES = [
    (0, 6.5, "результат ?: — значення:\nйого присвоюють, передають\nв аргумент, повертають", 10, 88, "center"),
    (0, 16.5, "умова: вираз\nтипу bool", 36, 88, "center"),
    (0, 20.5, "? — після умови", 52, 88, "center"),
    (0, 25.5, "значення,\nякщо умова true", 34, 14, "center"),
    (0, 30.5, ": — розділяє\nдва значення", 56, 14, "center"),
    (0, 37, "значення,\nякщо умова false", 80, 14, "center"),
]
fig, ax = anatomy(15, 4.4, LINES, MARKS, NOTES, size=20, x0=8, y0=52, step=16)
save(fig, __file__)
