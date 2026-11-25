"""Покрокове виконання scopes.cs: які змінні існують після кожного рядка (вивід 100 і 5 — з реального запуску, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, INK, box, save_steps  # noqa: E402

CODE = [
    "int total = 0;",
    "for (int i = 1; i <= 2; i++)",
    "{",
    "    int square = i * i;",
    "    total += square;",
    "}",
    "{",
    "    int square = 100;",
    "    Console.WriteLine(square);",
    "}",
    "Console.WriteLine(total);",
]
SCOPE = {"total": ("уся програма", GREEN), "i": ("цикл for", BLUE), "square": ("тіло циклу", BLUE),
         "square ": ("блок { }, рядки 7–10", AMBER)}
MUTED = "#475569"

# (рядок з 1, змінні, змінена, вивід, підпис)
STEPS = [
    (1, {"total": "0"}, "total", [], "Змінна total створена. Її область видимості — до кінця програми."),
    (2, {"total": "0", "i": "1"}, "i", [], "Змінна i оголошена в for і існує лише всередині циклу.\nУмова 1 <= 2 істинна."),
    (4, {"total": "0", "i": "1", "square": "1"}, "square", [], "Перша ітерація: square = 1 * 1.\nsquare існує лише в тілі циклу."),
    (5, {"total": "1", "i": "1", "square": "1"}, "total", [], "total += square, тепер total = 1."),
    (6, {"total": "1", "i": "1"}, None, [], "Кінець тіла циклу: square більше не існує."),
    (2, {"total": "1", "i": "2"}, "i", [], "i++ дає 2, умова 2 <= 2 істинна."),
    (4, {"total": "1", "i": "2", "square": "4"}, "square", [], "Друга ітерація: нова змінна square = 2 * 2."),
    (5, {"total": "5", "i": "2", "square": "4"}, "total", [], "total = 1 + 4 = 5."),
    (6, {"total": "5", "i": "2"}, None, [], "Кінець тіла циклу: square знову зникла."),
    (2, {"total": "5", "i": "3"}, "i", [], "i++ дає 3, умова 3 <= 2 хибна: цикл завершується."),
    (7, {"total": "5"}, None, [], "Цикл завершено, i зникла разом із ним."),
    (8, {"total": "5", "square ": "100"}, "square ", [],
     "Інший блок: нова змінна square = 100. Ім'я можна повторити,\nбо цей блок не вкладений у тіло циклу."),
    (9, {"total": "5", "square ": "100"}, None, ["100"], "Друкується 100."),
    (10, {"total": "5"}, None, ["100"], "Кінець блоку: друга square теж зникла."),
    (11, {"total": "5"}, None, ["100", "5"], "Друкується 5. До кінця програми дожила лише total."),
]


def draw(ax, step):
    line, live, changed, output, caption = step
    ax.text(50, 95, "Область видимості: які змінні існують зараз", ha="center", fontsize=18, fontweight="bold")

    box(ax, 1.5, 22, 55, 66, "", fc="#F8FAFC", ec="#CBD5E1")
    top, row = 83, 5.6
    for first, last, color in [(2, 6, BLUE), (7, 10, AMBER)]:
        y1, y2 = top - (last - 1) * row - row / 2 + 0.4, top - (first - 1) * row + row / 2 - 0.4
        ax.add_patch(FancyBboxPatch((6, y1), 49.5, y2 - y1, boxstyle="round,pad=0,rounding_size=1",
                                    fc=color, ec="none", alpha=0.45))
    for n, text in enumerate(CODE, start=1):
        y = top - (n - 1) * row
        if n == line:
            ax.add_patch(Rectangle((6, y - 2.5), 49.5, 5, fc="#FDE68A", ec="none"))
            ax.plot([4.4], [y], marker=">", color="#D97706", markersize=12)
        ax.text(7, y, f"{n:>2}  {text}", fontsize=12.5, va="center", fontfamily="DejaVu Sans Mono", color=INK)

    ax.text(60, 84, "Існують зараз", fontsize=14, fontweight="bold")
    ax.text(61, 78.5, "Ім'я", fontsize=11.5, color=MUTED)
    ax.text(73, 78.5, "Значення", fontsize=11.5, color=MUTED)
    ax.text(84, 78.5, "Область", fontsize=11.5, color=MUTED)
    y = 72.5
    for name, value in live.items():
        where, color = SCOPE[name]
        hot = name == changed
        box(ax, 60, y - 2.6, 38, 5.2, "", fc="#DCFCE7" if hot else "white", ec="#CBD5E1", lw=1)
        ax.add_patch(Rectangle((60.2, y - 2.4), 1.2, 4.8, fc=color, ec=INK, lw=0.6))
        ax.text(62.5, y, name.strip(), fontsize=12, va="center", fontfamily="DejaVu Sans Mono")
        ax.text(73, y, value, fontsize=12, va="center", fontfamily="DejaVu Sans Mono",
                fontweight="bold" if hot else "normal")
        ax.text(84, y, where, fontsize=10.5, va="center", color=MUTED)
        y -= 6.6

    ax.text(60, 42, "Вивід", fontsize=14, fontweight="bold")
    box(ax, 60, 23, 38, 15, "", fc="#1E293B", ec="#1E293B")
    for k, text in enumerate(output):
        ax.text(62, 34 - k * 5, text, fontsize=12.5, va="center", color="#E2E8F0", fontfamily="DejaVu Sans Mono")

    ax.text(50, 9, caption, ha="center", va="center", fontsize=14, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 3.0) for s in STEPS[:-1]] + [(STEPS[-1], 5.0)], draw, poster=11)
