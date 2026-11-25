"""Як декомпілятор відновлює C# з assembly."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, arrow, box, canvas, save  # noqa: E402

fig, ax = canvas(15, 4.6)
steps = [
    ("License.dll", "метадані + IL", GREY),
    ("Читає метадані", "типи, методи,\nпараметри, рядки", BLUE),
    ("Розбирає IL", "блоки інструкцій\nі переходи між ними", BLUE),
    ("Впізнає шаблони", "цикли, if, top-level,\nінтерполяцію рядків", AMBER),
    ("Друкує C#", "обраної версії мови:\nLatest або CSharp1", GREEN),
]
w, gap = 16.5, 3.9
for i, (title, note, color) in enumerate(steps):
    x = 1 + i * (w + gap)
    box(ax, x, 50, w, 26, title, fc=color, size=13, weight="bold")
    ax.text(x + w / 2, 40, note, ha="center", va="top", fontsize=11.5, linespacing=1.35)
    if i < len(steps) - 1:
        arrow(ax, x + w + 0.4, 63, x + w + gap - 0.4, 63)
ax.text(50, 4, "Результат — еквівалентний код, а не оригінал: коментарів, імен локальних змінних і форматування в assembly немає.",
        ha="center", fontsize=12, style="italic")
save(fig, __file__)
