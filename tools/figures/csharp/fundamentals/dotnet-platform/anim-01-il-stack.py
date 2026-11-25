"""Стек обчислень IL крок за кроком: Console.WriteLine(Add(2, 3)).

IL взято з реальної assembly CsHello (ilspycmd -il, .NET 10.0.15).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, box, save_steps  # noqa: E402

MAIN = ["ldc.i4.2", "ldc.i4.3", "call Add", "call WriteLine", "ret"]
ADD = ["ldarg.0", "ldarg.1", "add", "ret"]

# (метод, рядок, стек, аргументи Add, вивід консолі, підпис)
STEPS = [
    ("main", None, [], None, "", "Метод <Main>$ починається з порожнього стеку обчислень."),
    ("main", 0, [2], None, "", "ldc.i4.2 кладе на стек константу 2 типу int32."),
    ("main", 1, [2, 3], None, "", "ldc.i4.3 кладе на стек константу 3."),
    ("add", None, [], (2, 3), "",
     "call знімає два значення зі стеку і передає їх у Add як аргументи a і b.\nУ Add свій, порожній стек обчислень."),
    ("add", 0, [2], (2, 3), "", "ldarg.0 кладе на стек значення аргументу a."),
    ("add", 1, [2, 3], (2, 3), "", "ldarg.1 кладе на стек значення аргументу b."),
    ("add", 2, [5], (2, 3), "", "add знімає два верхні значення і кладе на стек їхню суму."),
    ("main", 2, [5], None, "",
     "ret повертає верхнє значення стеку: результат 5 опиняється на стеку <Main>$."),
    ("main", 3, [], None, "5", "call WriteLine знімає 5 зі стеку і виводить його в консоль."),
    ("main", 4, [], None, "5", "ret: стек порожній, метод <Main>$ завершено."),
]


def code_block(ax, x, y_top, title, lines, active, current):
    ax.text(x, y_top, title, fontsize=15, fontweight="bold", fontfamily="DejaVu Sans Mono",
            color=INK if active else "#94A3B8")
    for i, line in enumerate(lines):
        y = y_top - 7 - i * 5.8
        hit = active and i == current
        if hit:
            box(ax, x - 0.5, y - 2.3, 22, 4.6, "", fc=AMBER, ec="#D97706", lw=2)
            ax.plot([x - 2.6], [y], marker=">", color="#D97706", markersize=11)
        ax.text(x + 1, y, line, fontsize=14, va="center", fontfamily="DejaVu Sans Mono",
                color=INK if active else "#94A3B8")


def draw(ax, step):
    method, line, stack, args, console, caption = step
    ax.text(50, 95, "Стек обчислень IL: Console.WriteLine(Add(2, 3))", ha="center", fontsize=18,
            fontweight="bold")

    code_block(ax, 5, 82, "<Main>$", MAIN, method == "main", line)
    code_block(ax, 5, 40, "Add(a, b)", ADD, method == "add", line)

    # стек обчислень
    owner = "<Main>$" if method == "main" else "Add"
    ax.text(55, 82, f"Стек обчислень {owner}", ha="center", fontsize=14, fontweight="bold")
    ax.plot([45, 45, 65, 65], [70, 22, 22, 70], color=INK, lw=2)
    for i, value in enumerate(stack):
        fc = GREEN if value == 5 else BLUE
        box(ax, 46.5, 23.5 + i * 10, 17, 8, str(value), fc=fc, mono=True, size=18, weight="bold")
    if stack:
        ax.text(66.5, 27.5 + (len(stack) - 1) * 10, "← верхівка", fontsize=12, va="center", color="#475569")
    else:
        ax.text(55, 46, "порожній", ha="center", fontsize=13, color="#94A3B8", style="italic")

    # аргументи і консоль
    ax.text(85, 82, "Аргументи Add", ha="center", fontsize=14, fontweight="bold")
    for i, name in enumerate("ab"):
        value = "—" if args is None else str(args[i])
        box(ax, 76, 66 - i * 11, 18, 8, f"{name} = {value}", fc=GREY if args is None else BLUE, mono=True,
            size=15)
    ax.text(85, 40, "Консоль", ha="center", fontsize=14, fontweight="bold")
    box(ax, 76, 24, 18, 11, console, fc="#0F172A", mono=True, size=20, weight="bold")
    ax.texts[-1].set_color("#F8FAFC")

    ax.text(50, 8, caption, ha="center", va="center", fontsize=15, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 3.0) for s in STEPS[:-1]] + [(STEPS[-1], 4.0)], draw, poster=6)
