"""Файли в bin/Debug/net10.0 після dotnet build проєкту Hello (реальні розміри, macOS Arm64)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save  # noqa: E402

fig, ax = canvas(14, 6.4)
rows = [
    ("Hello", "122 КБ", AMBER, "apphost: нативна програма для цієї ОС,\nзнаходить .NET і запускає Hello.dll  (на Windows — Hello.exe)"),
    ("Hello.dll", "4,5 КБ", GREEN, "assembly: IL-код, метадані, маніфест"),
    ("Hello.pdb", "10,7 КБ", BLUE, "debug-символи: зв'язок IL з рядками Program.cs"),
    ("Hello.runtimeconfig.json", "259 Б", GREY, "яке середовище потрібне: Microsoft.NETCore.App 10.0"),
    ("Hello.deps.json", "387 Б", GREY, "перелік залежностей для завантажувача"),
]
ax.text(2, 95, "bin/Debug/net10.0/", fontsize=15, fontweight="bold", fontfamily="DejaVu Sans Mono")
y = 78
for name, size, color, note in rows:
    box(ax, 2, y - 6, 30, 12, name, fc=color, mono=True, size=12.5)
    ax.text(36, y, size, fontsize=13, va="center", fontweight="bold", ha="left")
    ax.text(48, y, note, fontsize=12, va="center", linespacing=1.3)
    y -= 17
save(fig, __file__)
