""".NET Standard як контракт: бібліотека під netstandard2.0 працює на всіх реалізаціях, що його підтримують."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save  # noqa: E402

fig, ax = canvas(14, 5.4)

box(ax, 30, 74, 40, 16, "Бібліотека\nTargetFramework = netstandard2.0", fc=AMBER, size=12.5, weight="bold")
box(ax, 20, 46, 60, 12, ".NET Standard 2.0 — перелік API (контракт), без реалізації", fc=GREY, size=12)
ax.annotate("", xy=(50, 59), xytext=(50, 73), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
ax.text(51.5, 65.5, "використовує лише ці API", fontsize=11)

impls = [
    (1, ".NET Framework\n4.6.1+", BLUE),
    (21, ".NET Core 2.0+,\n.NET 5–11", GREEN),
    (41, "Mono 5.4+", GREY),
    (61, "Xamarin.iOS /\nAndroid", GREY),
    (81, "Unity\n2018.1+", GREY),
]
for x, text, color in impls:
    box(ax, x, 8, 18, 16, text, fc=color, size=11.5)
    ax.annotate("", xy=(50, 45), xytext=(x + 9, 25),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=1.3, ls="--"))
ax.text(50, 30, "кожна реалізація має всі API стандарту", ha="center", fontsize=11, color="#15803D",
        bbox=dict(fc="white", ec="none", pad=2))
save(fig, __file__)
