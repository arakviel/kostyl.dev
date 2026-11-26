"""Покроково: у якому порядку виконуються частини for (код з for-steps.cs без друку в тілі)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, RED, box, save_steps  # noqa: E402

W = 12
SIZE = 21
LINES = [
    "int sum = 0;",
    "for (int i = 0; i < 3; i++)",
    "{",
    "    sum += i;",
    "}",
    "Console.WriteLine(sum);",
]
# частина: (рядок, колонка, довжина, колір)
PARTS = {
    "pre": (0, 0, 12, GREY),
    "init": (1, 5, 9, BLUE),
    "cond": (1, 16, 5, GREEN),
    "false": (1, 16, 5, RED),
    "body": (3, 4, 9, GREY),
    "iter": (1, 23, 3, AMBER),
    "exit": (5, 0, 23, GREY),
}
NAMES = {"pre": "до циклу", "init": "ініціалізатор", "cond": "умова", "false": "умова", "body": "тіло",
         "iter": "ітератор", "exit": "після циклу"}
# (частина, i, sum, підпис)
STEPS = [
    ("pre", None, 0, "sum = 0. Цикл ще не почався."),
    ("init", 0, 0, "Ініціалізатор виконується один раз: i = 0."),
    ("cond", 0, 0, "Умова 0 < 3 — true: виконується тіло."),
    ("body", 0, 0, "Тіло: sum += 0, sum = 0."),
    ("iter", 1, 0, "Ітератор виконується після тіла: i = 1."),
    ("cond", 1, 0, "Умова перевіряється знову: 1 < 3 — true."),
    ("body", 1, 1, "Тіло: sum += 1, sum = 1."),
    ("iter", 2, 1, "Ітератор: i = 2."),
    ("cond", 2, 1, "Умова 2 < 3 — true."),
    ("body", 2, 3, "Тіло: sum += 2, sum = 3."),
    ("iter", 3, 3, "Ітератор: i = 3."),
    ("false", 3, 3, "Умова 3 < 3 — false: цикл завершено, тіло не виконується."),
    ("exit", None, 3, "Після циклу друкується 3. Змінна i існувала лише всередині for."),
]


def draw(ax, state):
    part, i, total, caption = state
    pos = ax.get_position()
    char = 0.602 * SIZE / 72 / (pos.width * W) * 100
    x0, y0, step = 5, 80, 9.6
    ax.text(50, 95.5, "Порядок виконання for", ha="center", fontsize=18, fontweight="bold")
    line, col, length, color = PARTS[part]
    y = y0 - line * step
    ax.add_patch(Rectangle((x0 + col * char - 0.3, y - step / 2 + 0.8), length * char + 0.6, step - 1.6,
                           fc=color, ec="none", zorder=1))
    for k, text in enumerate(LINES):
        ax.text(x0, y0 - k * step, text, fontsize=SIZE, fontfamily="DejaVu Sans Mono", va="center", zorder=2)
    # панель змінних
    ax.text(74, 80, "зараз: " + NAMES[part], fontsize=15, va="center", color="#475569")
    box(ax, 74, 58, 20, 9, "i = " + ("—" if i is None else str(i)), fc="white", mono=True, size=18)
    box(ax, 74, 43, 20, 9, f"sum = {total}", fc="white", mono=True, size=18)
    if part == "exit":
        box(ax, 74, 28, 20, 9, "вивід: 3", fc=GREEN, mono=False, size=16)
    ax.text(50, 9, caption, ha="center", va="center", fontsize=16,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


steps = [(s, 2.4) for s in STEPS]
steps[0] = (STEPS[0], 2.6)
steps[-1] = (STEPS[-1], 5.0)
save_steps(__file__, steps, draw, poster=-1)
