"""Будова збірки CsHello.dll: що лежить усередині файлу (дані з реальної збірки .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save  # noqa: E402

fig, ax = canvas(14, 8.2)

ax.text(18, 97, "CsHello.dll — 4 608 байтів", ha="center", fontsize=14, fontweight="bold")

sections = [
    (84, 8, "PE-заголовок", GREY, "Формат Windows PE: ОС бачить звичайний файл\n(команда file: «PE32 executable … .Net assembly»)"),
    (74, 8, "CLR-заголовок", GREY, "Позначка «це керований код» і де шукати\nметадані та точку входу"),
    (52, 20, "Маніфест", AMBER, "Ім'я: CsHello, версія 1.0.0.0\nПосилання: System.Runtime 10.0.0.0,\n                    System.Console 10.0.0.0\nTarget framework: .NETCoreApp, v10.0"),
    (28, 22, "Метадані", BLUE, "Типи: Program\nМетоди: <Main>\\$, <<Main>\\$>g__Add|0_0\nЗовнішні виклики:\n  System.Console::WriteLine(int32)"),
    (10, 16, "IL-код", GREEN, "ldc.i4.2\nldc.i4.3\ncall  …Add\ncall  Console::WriteLine\nret"),
]
for y, h, title, color, detail in sections:
    box(ax, 4, y, 28, h - 1.5, title, fc=color, size=13, weight="bold")
    mono = title == "IL-код"
    ax.text(38, y + (h - 1.5) / 2, detail, va="center", fontsize=11.5,
            fontfamily="DejaVu Sans Mono" if mono else "DejaVu Sans", linespacing=1.35)
    ax.plot([32.8, 37], [y + (h - 1.5) / 2] * 2, color=INK, lw=1, ls=":")

ax.plot([2, 2], [10, 93], color=INK, lw=2)
ax.plot([2, 3.5], [93, 93], color=INK, lw=2)
ax.plot([2, 3.5], [10, 10], color=INK, lw=2)
save(fig, __file__)
