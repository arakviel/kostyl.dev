"""Що з вихідного коду лишається у файлі після компіляції: C++ і .NET (перевірено ilspycmd 11.2 на License.dll)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import canvas, save  # noqa: E402
from _matrix import matrix  # noqa: E402

fig, ax = canvas(14, 7)
rows = ["Імена класів і методів", "Імена параметрів", "Імена локальних змінних", "Рядкові літерали",
        "Структура: if, цикли, виклики", "Коментарі"]
cols = ["C++ .exe\n(Release)", ".NET .dll\n(Release)", ".NET .dll\n+ .pdb"]
cells = [
    [("частково", "RTTI, експорт"), "так", "так"],
    ["ні", "так", "так"],
    ["ні", ("ні", "secret → text"), "так"],
    ["так", "так", "так"],
    [("частково", "з машинного коду"), ("так", "з IL"), ("так", "з IL")],
    ["ні", "ні", "ні"],
]
matrix(ax, rows, cols, cells, x0=36, y0=82, col_w=21, row_h=12.5)
save(fig, __file__)
