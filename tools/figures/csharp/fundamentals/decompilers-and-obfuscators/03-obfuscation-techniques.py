"""Три основні прийоми обфускації: до і після (перейменування і рядки — з реального запуску Obfuscar 2.2.50)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, GREEN, RED, arrow, box, canvas, save  # noqa: E402

fig, ax = canvas(15, 7.2)
panels = [
    ("Перейменування", "class Program\nstatic bool IsValidKey(\n    string? key)",
     "class A\nstatic bool A(\n    string? P_0)", "Obfuscar"),
    ("Приховування рядків", 'string secret =\n    "KOSTYL-2026-PRO";',
     "string text = b();\n// байти, XOR з i ^ 0xAA,\n// розшифровка при старті", "Obfuscar"),
    ("Заплутування потоку", "if (key == secret)\n    return true;\nreturn false;",
     "int s = 7;\nwhile (true) switch (s) {\n  case 7: s = key == x\n    ? 2 : 9; break;\n  case 2: return true;\n  case 9: return false; }",
     "спрощена ілюстрація"),
]
for i, (title, before, after, source) in enumerate(panels):
    x = 1 + i * 33.3
    ax.text(x + 15.5, 95, title, ha="center", fontsize=14, fontweight="bold")
    box(ax, x, 62, 31, 26, before, fc=GREEN, mono=True, size=11, align="left")
    arrow(ax, x + 15.5, 61, x + 15.5, 53)
    box(ax, x, 12, 31, 40, after, fc=AMBER if i < 2 else RED, mono=True, size=11, align="left")
    ax.text(x + 15.5, 6, source, ha="center", fontsize=11, style="italic", color="#475569")
save(fig, __file__)
