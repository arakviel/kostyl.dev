"""Top-level statements і класичний Main: що генерує компілятор (декомпіляція ilspycmd, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, arrow, box, canvas, save  # noqa: E402

fig, ax = canvas(15, 7)
ax.text(24, 95, "Що пише програміст", ha="center", fontsize=14, fontweight="bold")
ax.text(76, 95, "Що генерує компілятор (видно в IL)", ha="center", fontsize=14, fontweight="bold")

box(ax, 2, 66, 44, 22, 'Console.WriteLine("Hello, World!");', fc=AMBER, mono=True, size=12.5)
ax.text(2, 61, "Program.cs, top-level statements (dotnet new console)", fontsize=11, color="#475569")
box(ax, 54, 62, 44, 30,
    "internal class Program\n{\n  private static void <Main>\\$(string[] args)\n  {\n"
    "    Console.WriteLine(\"Hello, World!\");\n  }\n}", fc=GREEN, mono=True, size=11.5, align="left")
arrow(ax, 47, 77, 53, 77)

box(ax, 2, 8, 44, 42,
    "namespace Classic;\n\nclass Program\n{\n    static void Main(string[] args)\n    {\n"
    "        Console.WriteLine(\"Hello, World!\");\n    }\n}", fc=BLUE, mono=True, size=11.5, align="left")
ax.text(2, 3, "Program.cs, класичний Main (dotnet new console --use-program-main)", fontsize=11, color="#475569")
box(ax, 54, 10, 44, 38,
    "namespace Classic;\n\ninternal class Program\n{\n  private static void Main(string[] args)\n  {\n"
    "    Console.WriteLine(\"Hello, World!\");\n  }\n}", fc=GREEN, mono=True, size=11.5, align="left")
arrow(ax, 47, 29, 53, 29)
ax.text(76, 54, "різниця лише в імені методу (<Main>\\$ чи Main)\nі namespace", ha="center", fontsize=12, style="italic",
        color="#475569")
save(fig, __file__)
