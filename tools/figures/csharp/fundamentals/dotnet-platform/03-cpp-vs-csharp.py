"""Конвеєр C++ і C#: де саме з'являється машинний код."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402
from _style import AMBER, BLUE, GREEN, GREY, INK, arrow, box, canvas, save  # noqa: E402

fig, ax = canvas(16, 6.2)

# Фон: машина розробника / машина користувача
ax.add_patch(Rectangle((0, 2), 57, 86, fc="#F8FAFC", ec="none", zorder=0))
ax.add_patch(Rectangle((57, 2), 43, 86, fc="#F0FDF4", ec="none", zorder=0))
ax.text(28.5, 94, "Машина розробника (один раз)", ha="center", fontsize=13, fontweight="bold")
ax.text(78.5, 94, "Машина користувача (при кожному запуску)", ha="center", fontsize=13, fontweight="bold")

h = 17
# C++
y = 58
ax.text(1, y + h + 5, "C++", fontsize=14, fontweight="bold", color="#1D4ED8")
box(ax, 1, y, 10, h, "main.cpp", fc=GREY, mono=True, size=12)
arrow(ax, 11.8, y + h / 2, 14.2, y + h / 2)
box(ax, 15, y, 11, h, "Компілятор\ng++ / MSVC", fc=BLUE, size=11.5)
arrow(ax, 26.8, y + h / 2, 29.2, y + h / 2)
box(ax, 30, y, 11, h, "main.obj\nмашинний\nкод x64", fc=AMBER, size=11)
arrow(ax, 41.8, y + h / 2, 44.2, y + h / 2)
box(ax, 45, y, 10.5, h, "Лінкер\n→ app.exe", fc=BLUE, size=11.5)
arrow(ax, 56.3, y + h / 2, 68.2, y + h / 2, label="копіюємо .exe")
box(ax, 69, y, 13, h, "ОС завантажує\nготовий\nмашинний код", fc=AMBER, size=11)
arrow(ax, 82.8, y + h / 2, 85.2, y + h / 2)
box(ax, 86, y, 12.5, h, "Процесор\nx64", fc=GREY, size=12, weight="bold")

# C#
y = 14
ax.text(1, y + h + 5, "C#", fontsize=14, fontweight="bold", color="#15803D")
box(ax, 1, y, 10, h, "Program.cs", fc=GREY, mono=True, size=11.5)
arrow(ax, 11.8, y + h / 2, 14.2, y + h / 2)
box(ax, 15, y, 11, h, "Компілятор\nRoslyn", fc=BLUE, size=11.5)
arrow(ax, 26.8, y + h / 2, 29.2, y + h / 2)
box(ax, 30, y, 25.5, h, "app.dll\nIL-код + метадані\n(не залежить від процесора)", fc=GREEN, size=11)
arrow(ax, 56.3, y + h / 2, 61.2, y + h / 2)
box(ax, 62, y, 20.5, h, "CLR: JIT компілює\nметод при першому\nвиклику", fc=GREEN, size=11)
arrow(ax, 83.3, y + h / 2, 85.2, y + h / 2)
box(ax, 86, y, 12.5, h, "Процесор\nx64 або Arm64", fc=GREY, size=11.5, weight="bold")

ax.plot([57, 57], [2, 88], color=INK, lw=1.2, ls="--")
save(fig, __file__)
