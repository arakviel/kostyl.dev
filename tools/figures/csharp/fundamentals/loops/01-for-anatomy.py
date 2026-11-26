"""Анатомія for (рядки на зразок for-forms.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, anatomy, save  # noqa: E402

LINES = [
    "for (int i = 0; i < 5; i++)",
    "{",
    "    Console.WriteLine(i);",
    "}",
]
MARKS = [(0, 0, 3, AMBER), (0, 5, 9, BLUE), (0, 16, 5, GREEN), (0, 23, 3, RED), (2, 4, 21, GREY),
         (0, 14, 1, GREY), (0, 21, 1, GREY)]
NOTES = [
    (0, 0, "ключове слово for", 14, 78, "center"),
    (0, 9, "ініціалізатор: виконується один раз;\nзмінна i існує лише в циклі", 26, 97, "center"),
    (0, 18.5, "умова: вираз bool, перевіряється\nперед кожною ітерацією", 50, 97, "left"),
    (0, 26, "ітератор: виконується\nпісля кожної ітерації", 72, 78, "left"),
    (2, 25, "тіло: блок або одна інструкція;\nвиконується, поки умова true", 72, 56, "left"),
    (0, 14.5, "; розділяє частини,\nбудь-яку можна\nпропустити: for (;;)", 14, 45, "center"),
]
fig, ax = anatomy(15, 3.5, LINES, MARKS, NOTES, y0=78, step=11, x0=30)
ax.set_ylim(28, 100)   # нижня частина полотна порожня
save(fig, __file__)
