"""Анатомія файлу проєкту Hello.csproj, створеного dotnet new console (.NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

fig, ax = canvas(15, 6.6)
lines = [
    ('<Project Sdk="Microsoft.NET.Sdk">', BLUE,
     "SDK проєкту: підключає стандартні правила build для C#"),
    ("  <PropertyGroup>", None, None),
    ("    <OutputType>Exe</OutputType>", GREEN, "результат — програма (Exe), а не бібліотека (Library)"),
    ("    <TargetFramework>net10.0</TargetFramework>", AMBER, "target framework: .NET 10"),
    ("    <ImplicitUsings>enable</ImplicitUsings>", GREY, "неявні using: System, System.IO, System.Linq…"),
    ("    <Nullable>enable</Nullable>", GREY, "попередження про можливий null для посилань"),
    ("  </PropertyGroup>", None, None),
    ("</Project>", None, None),
]
y = 90
for code, color, note in lines:
    if color:
        ax.add_patch(__import__("matplotlib.patches", fromlist=["FancyBboxPatch"]).FancyBboxPatch(
            (1, y - 4.2), 50, 8.4, boxstyle="round,pad=0.2,rounding_size=1.2", fc=color, ec="none"))
    ax.text(2, y, code, fontsize=13, fontfamily="DejaVu Sans Mono", va="center")
    if note:
        ax.annotate(note, xy=(51.5, y), xytext=(57, y), fontsize=12.5, va="center",
                    arrowprops=dict(arrowstyle="-", color="#94A3B8", lw=1.2))
    y -= 11.5
save(fig, __file__)
