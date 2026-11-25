"""Архітектура платформи .NET: мови → IL → BCL + CLR → ОС; CTS і CLS як правила для всіх шарів."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from _style import AMBER, BLUE, GREEN, GREY, INK, arrow, box, canvas, save  # noqa: E402

fig, ax = canvas(14, 9)

# Мови
for i, lang in enumerate(["C#", "F#", "Visual Basic"]):
    box(ax, 2 + i * 22, 88, 18, 8, lang, fc=GREY, size=13, weight="bold")
    arrow(ax, 11 + i * 22, 87, 20 + i * 13, 78.8)
ax.text(70, 92, "компілятори мов\n(Roslyn, fsc)", fontsize=11, va="center", alpha=0.8)

box(ax, 2, 70, 62, 8, "Assembly: IL-код + метадані (.dll)", fc=GREEN, size=13, weight="bold")
arrow(ax, 33, 69, 33, 64.5)

# Ваша програма + BCL
box(ax, 2, 54, 20, 9, "Ваша\nпрограма", fc=AMBER, size=12, weight="bold")
box(ax, 25, 54, 39, 9, "BCL: System.Console, System.IO,\nSystem.Collections, System.Net.Http…", fc=BLUE, size=11.5)

# CLR з компонентами
ax.add_patch(FancyBboxPatch((2, 18), 62, 32, boxstyle="round,pad=0.4,rounding_size=2",
                            fc="#F0FDF4", ec=INK, lw=1.6))
ax.text(33, 46, "CLR — runtime", ha="center", fontsize=13.5, fontweight="bold")
parts = [
    ("Завантажувач\nтипів", 4, 31), ("JIT-\nкомпілятор", 25, 31), ("Збирач\nсміття (GC)", 46, 31),
    ("Перевірка\nтипів і меж", 4, 20.5), ("Обробка\nвинятків", 25, 20.5), ("Потоки,\nбезпека", 46, 20.5),
]
for text, x, y in parts:
    box(ax, x, y, 16, 8.5, text, fc="white", size=11)

box(ax, 2, 6, 62, 8, "Операційна система: Windows / Linux / macOS", fc=GREY, size=12.5)
arrow(ax, 33, 17.3, 33, 14.7)

# CTS / CLS справа
ax.add_patch(FancyBboxPatch((70, 18), 13, 60, boxstyle="round,pad=0.4,rounding_size=2",
                            fc="#EEF2FF", ec="#4F46E5", lw=1.6, ls="--"))
ax.text(76.5, 48, "CTS\n\nякими\nбувають\nтипи:\nint, class,\nstruct,\nнаслідування…",
        ha="center", va="center", fontsize=11.5, linespacing=1.3)
ax.add_patch(FancyBboxPatch((86, 54), 12, 24, boxstyle="round,pad=0.4,rounding_size=2",
                            fc="#FDF4FF", ec="#A21CAF", lw=1.6, ls="--"))
ax.text(92, 66, "CLS\n\nспільна\nпідмножина\nдля всіх мов",
        ha="center", va="center", fontsize=11.5, linespacing=1.3)
ax.text(84, 12, "Правила,\nа не програми", ha="center", fontsize=11, style="italic", alpha=0.8)

save(fig, __file__)
