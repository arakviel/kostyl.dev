"""Багаторівнева компіляція: один метод Square компілюється тричі (дані DOTNET_JitDisasmSummary, .NET 10.0.15)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, INK, arrow, box, canvas, save  # noqa: E402

fig, ax = canvas(15, 4.6)

stages = [
    (2, "Tier0", "швидко скомпілювати,\nбез оптимізацій", "32 байти\nмашинного коду", BLUE),
    (36, "Instrumented Tier0", "той самий код +\nлічильники: що і як\nчасто виконується", "32 байти", AMBER),
    (70, "Tier1", "повні оптимізації\nз урахуванням\nзібраного профілю", "20 байтів", GREEN),
]
for x, name, what, size, color in stages:
    box(ax, x, 40, 28, 40, f"{name}\n\n{what}", fc=color, size=11.5)
    ax.text(x + 14, 28, size, ha="center", va="center", fontsize=12, fontweight="bold",
            fontfamily="DejaVu Sans Mono", linespacing=1.2)

arrow(ax, 30.8, 60, 35.2, 60)
arrow(ax, 64.8, 60, 69.2, 60)
ax.text(33, 85, "≥ 30 викликів", ha="center", fontsize=11)
ax.text(67, 85, "профіль зібрано,\nкомпіляція у фоні", ha="center", fontsize=11)
ax.text(2, 92, "Перший виклик Square(x)", fontsize=12, fontweight="bold")
ax.text(2, 8, "Програма весь час працює: новий код підміняє старий між викликами, зупинки немає.",
        fontsize=11, style="italic", color=INK)
save(fig, __file__)
