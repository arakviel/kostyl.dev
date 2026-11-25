"""Що лежить у папці встановленого .NET 10 (SDK 10.0.404, macOS Arm64, du -sh)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, GREEN, GREY, box, canvas, save  # noqa: E402

fig, ax = canvas(14, 6.6)
rows = [  # (папка, розмір, колір, пояснення)
    ("host/ + dotnet", "0,4 МБ", GREY, "muxer: передає команду SDK або запускає .dll"),
    ("sdk/10.0.404/", "428 МБ", AMBER, "компілятор Roslyn, MSBuild, NuGet, шаблони, команди CLI"),
    ("packs/", "103 МБ", AMBER, "reference assemblies для компіляції, шаблон apphost"),
    ("shared/Microsoft.NETCore.App/", "83 МБ", GREEN, "CLR + BCL — runtime"),
    ("shared/Microsoft.AspNetCore.App/", "29 МБ", GREEN, "runtime для вебзастосунків"),
]
y = 88
for name, size, color, note in rows:
    box(ax, 9, y - 5.5, 34, 11, name, fc=color, mono=True, size=12, align="left")
    ax.text(46, y, size, fontsize=13, fontweight="bold", va="center")
    ax.text(57, y, note, fontsize=12, va="center")
    y -= 16

ax.plot([4, 4], [51, 93], color="#D97706", lw=4, solid_capstyle="round")
ax.text(2.5, 72, "SDK", rotation=90, ha="center", va="center", fontsize=13, fontweight="bold", color="#B45309")
ax.plot([4, 4], [19, 45], color="#16A34A", lw=4, solid_capstyle="round")
ax.text(2.5, 32, "Runtime", rotation=90, ha="center", va="center", fontsize=13, fontweight="bold",
        color="#15803D")
ax.text(9, 3, "Розробнику потрібен SDK, і він уже містить runtime. Користувачу програми достатньо runtime.",
        fontsize=12, style="italic")
save(fig, __file__)
