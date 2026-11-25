"""Що видно з License у трьох варіантах (реальні запуски: ilspycmd 11.2, Obfuscar 2.2.50, find-utf16.cs; .NET 10, macOS Arm64)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import canvas, save  # noqa: E402
from _matrix import matrix  # noqa: E402

fig, ax = canvas(14, 4.8)
rows = ["Release .dll", "Після Obfuscar", "Native AOT"]
cols = ["Декомпілятор\nпоказує C#", "Видно імена\nметодів", "Пошук у файлі\nзнаходить ключ"]
cells = [
    ["так", ("так", "IsValidKey"), "так"],
    [("так", "але імена A, b()"), "ні", ("ні", "але XOR знімається")],
    [("ні", "немає IL"), "ні", ("так", "KOSTYL-2026-PR…")],
]
matrix(ax, rows, cols, cells, x0=28, y0=74, col_w=24, row_h=21, size=12.5)
save(fig, __file__)
