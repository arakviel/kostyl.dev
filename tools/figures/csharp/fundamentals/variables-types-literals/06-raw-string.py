"""Raw-рядок: закривальні лапки задають відступ, який компілятор прибирає з кожного рядка (strings.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, GREEN, RED, box, canvas, save  # noqa: E402

WIDTH = 15
fig, ax = canvas(WIDTH, 6.8)
SIZE = 15
AX_W = ax.get_position().width * WIDTH  # ширина осей у дюймах
CHAR = 0.602 * SIZE / 72 / AX_W * 100   # ширина символу DejaVu Sans Mono у координатах 0..100
MUTED = "#475569"
LINES = [
    'string json = """',
    '    {',
    '      "name": "Олена",',
    '      "age": 19',
    '    }',
    '    """;',
]
X0, TOP, STEP = 2, 80, 11
ax.text(X0, 94, "Код", fontsize=14, fontweight="bold")
for n, text in enumerate(LINES):
    y = TOP - n * STEP
    if 1 <= n <= 5:
        ax.add_patch(Rectangle((X0, y - 4.2), 4 * CHAR, 8.4, fc=RED, ec="none"))
    if n == 5:
        ax.add_patch(Rectangle((X0 + 4 * CHAR, y - 4.2), 3 * CHAR, 8.4, fc=AMBER, ec="none"))
    if n == 0:
        ax.add_patch(Rectangle((X0 + 14 * CHAR, y - 4.2), 3 * CHAR, 8.4, fc=AMBER, ec="none"))
    ax.text(X0, y, text, va="center", fontsize=SIZE, fontfamily="DejaVu Sans Mono")

notes = [
    (TOP, 'після """ — новий рядок:\nвміст починається з наступного'),
    (TOP - 2.5 * STEP, "лапки всередині — звичайні\nсимволи, escape не потрібен"),
    (TOP - 5 * STEP, 'позиція закривальних """ —\nвідступ, який буде прибрано'),
]
for y, text in notes:
    ax.text(40, y, text, va="center", fontsize=12, color=MUTED, linespacing=1.3)
ax.text(X0, TOP - 5 * STEP - 10, "червоне — 4 пробіли, які компілятор прибирає з кожного рядка", fontsize=12,
        color="#DC2626")

ax.text(84, 76, "Значення рядка", ha="center", fontsize=14, fontweight="bold")
box(ax, 70, 34, 28, 34, '{\n  "name": "Олена",\n  "age": 19\n}', fc=GREEN, mono=True, size=13.5, align="left")
save(fig, __file__)
