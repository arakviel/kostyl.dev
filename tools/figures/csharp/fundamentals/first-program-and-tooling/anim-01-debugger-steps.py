"""Покрокове виконання average.cs у налагоджувачі: рядок, що виконається наступним, і вікно Locals.

Значення відповідають реальному запуску average.cs (.NET 10): сума 18, середнє 4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, RED, box, save_steps  # noqa: E402

CODE = [
    "int[] grades = [5, 4, 3, 6];",
    "",
    "int sum = 0;",
    "for (int i = 0; i < grades.Length; i++)",
    "{",
    "    sum += grades[i];",
    "}",
    "",
    "double average = sum / grades.Length;",
    'Console.WriteLine($"Сума: {sum}");',
    'Console.WriteLine($"Середнє: {average}");',
]
BREAKPOINT = 2  # індекс рядка «int sum = 0;»

# (поточний рядок, locals {ім'я: значення}, змінене ім'я, клавіша, підпис)
STEPS = [
    (2, {"grades": "int[4]", "sum": "0", "average": "0"}, None, "F5",
     "F5: програма запущена і зупинилася на точці зупинки.\nРядок із жовтою стрілкою ще НЕ виконаний."),
    (3, {"grades": "int[4]", "sum": "0", "average": "0"}, "sum", "F10",
     "F10 (Step Over): рядок виконано, sum = 0."),
    (5, {"grades": "int[4]", "sum": "0", "i": "0", "average": "0"}, "i", "F10",
     "Цикл почався: i = 0, умова i < 4 істинна."),
    (5, {"grades": "int[4]", "sum": "5", "i": "1", "average": "0"}, "sum", "F10 ×2",
     "sum += grades[0] → sum = 5, потім i++ → i = 1."),
    (5, {"grades": "int[4]", "sum": "9", "i": "2", "average": "0"}, "sum", "F10 ×2",
     "sum = 9, i = 2."),
    (5, {"grades": "int[4]", "sum": "12", "i": "3", "average": "0"}, "sum", "F10 ×2",
     "sum = 12, i = 3."),
    (8, {"grades": "int[4]", "sum": "18", "average": "0"}, "sum", "F10 ×3",
     "sum = 18, i = 4: умова хибна, цикл завершено. Змінна i зникла з Locals:\nвона існує лише всередині for."),
    (9, {"grades": "int[4]", "sum": "18", "average": "4"}, "average", "F10",
     "average = 4, хоча очікували 4,5. sum і grades.Length — int,\nтому sum / grades.Length — ціле ділення: 18 / 4 = 4."),
    (9, {"grades": "int[4]", "sum": "18", "average": "4", "(double)sum / grades.Length": "4.5"}, "(double)sum / grades.Length",
     "Watch", "У вікні Watch перевіряємо гіпотезу: (double)sum / grades.Length = 4.5.\nПомилку знайдено без жодного Console.WriteLine."),
]


def draw(ax, step):
    line, local_vars, changed, key, caption = step
    ax.text(50, 95, "Дебагер: покрокове виконання average.cs", ha="center", fontsize=18, fontweight="bold")

    # редактор
    box(ax, 1.5, 22, 56, 66, "", fc="#F8FAFC", ec="#CBD5E1")
    for i, text in enumerate(CODE):
        y = 83 - i * 5.6
        if i == line:
            ax.add_patch(__import__("matplotlib.patches", fromlist=["Rectangle"]).Rectangle(
                (6.5, y - 2.5), 50.5, 5, fc=AMBER, ec="none"))
            ax.plot([4.9], [y], marker=">", color="#D97706", markersize=12)
        if i == BREAKPOINT:
            ax.plot([3.2], [y], marker="o", color="#DC2626", markersize=11)
        ax.text(7, y, f"{i + 1:>2}  {text}", fontsize=12, va="center", fontfamily="DejaVu Sans Mono", color=INK)

    # клавіша
    box(ax, 60, 77, 12, 9, key, fc=BLUE, size=15, weight="bold", mono=True)
    ax.text(74, 81.5, "остання команда", fontsize=11.5, va="center", color="#475569")

    # Locals / Watch
    title = "Watch" if key == "Watch" else "Locals"
    ax.text(60, 70, title, fontsize=14, fontweight="bold")
    ax.text(61, 64, "Ім'я", fontsize=11.5, color="#475569")
    ax.text(88, 64, "Значення", fontsize=11.5, color="#475569")
    y = 58
    for name, value in local_vars.items():
        hot = name == changed
        fc = (RED if value == "4" and name == "average" else GREEN) if hot else "white"
        box(ax, 60, y - 2.6, 38, 5.2, "", fc=fc, ec="#CBD5E1", lw=1)
        ax.text(61, y, name, fontsize=11.5 if len(name) < 12 else 10.5, va="center", fontfamily="DejaVu Sans Mono")
        ax.text(88, y, value, fontsize=12, va="center", fontfamily="DejaVu Sans Mono",
                fontweight="bold" if hot else "normal")
        y -= 6.6

    ax.text(50, 9, caption, ha="center", va="center", fontsize=14, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 3.2) for s in STEPS[:-2]] + [(STEPS[-2], 5.0), (STEPS[-1], 5.5)], draw, poster=7)
