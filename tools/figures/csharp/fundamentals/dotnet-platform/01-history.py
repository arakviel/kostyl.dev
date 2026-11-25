"""Етапи розвитку технологій програмування: що кожен етап вирішив і яку проблему залишив."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, RED, box, arrow, canvas, save  # noqa: E402

stages = [
    ("1950-ті", "Машинний код\nі асемблер", "Прив'язка до\nпроцесора", GREY),
    ("1972", "C:\nпроцедурне\nпрограмування", "Ручне керування\nпам'яттю", GREY),
    ("1985", "C++:\nоб'єктно-\nорієнтоване", "Немає спільного\nбінарного формату", BLUE),
    ("1993", "COM:\nкомпоненти\nміж мовами", "Реєстр, GUID,\n«DLL hell»", BLUE),
    ("1995", "Java і JVM:\nкерований код", "Одна мова,\nчужа платформа", AMBER),
    ("2002", ".NET і C#:\nкерований код\nдля багатьох мов", "", GREEN),
]

fig, ax = canvas(16, 4.8)
w, gap = 14.2, 2.6
for i, (year, title, problem, color) in enumerate(stages):
    x = 1 + i * (w + gap)
    ax.text(x + w / 2, 93, year, ha="center", va="center", fontsize=14, fontweight="bold")
    box(ax, x, 56, w, 28, title, fc=color, size=11.5, weight="bold")
    if problem:
        box(ax, x, 12, w, 24, problem, fc=RED, size=11)
        ax.annotate("", xy=(x + w / 2, 37.5), xytext=(x + w / 2, 54.5),
                    arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=1.4, ls="--"))
    if i < len(stages) - 1:
        arrow(ax, x + w + 0.5, 70, x + w + gap - 0.5, 70)

ax.text(1, 3, "Червоні блоки — проблема, яку етап залишив і яку розв'язував наступний.",
        fontsize=11, color=INK, alpha=0.75)
save(fig, __file__)
