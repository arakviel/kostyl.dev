"""Хронологія .NET: три гілки (Framework, Mono, Core) і їх злиття в .NET 5+."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt  # noqa: E402
from _style import INK, save  # noqa: E402

LANES = {
    "fw": (3.0, ".NET Framework\n(лише Windows)", "#2563EB", "#DBEAFE"),
    "mono": (2.0, "Mono / Xamarin\n(стороння реалізація)", "#D97706", "#FEF3C7"),
    "core": (1.0, ".NET Core → .NET 5+\n(кросплатформна)", "#16A34A", "#DCFCE7"),
}

spans = [("fw", 2002, 2026.9), ("mono", 2004, 2020), ("core", 2016, 2026.9)]
events = [
    ("fw", 2002, "1.0\nC# 1.0", 1), ("fw", 2005, "2.0\nузагальнення", -1), ("fw", 2007.8, "3.5\nLINQ", 1),
    ("fw", 2010.3, "4.0", -1), ("fw", 2012.7, "4.5\nasync/await", 1), ("fw", 2019.3, "4.8\nостання\nмажорна", -1),
    ("mono", 2004.5, "Mono 1.0\n(Linux)", 1), ("mono", 2011.4, "Xamarin\n(iOS, Android)", 1),
    ("mono", 2016.2, "Microsoft\nкупує Xamarin", 1),
    ("core", 2016.5, "Core 1.0", 1), ("core", 2019.9, "Core 3.1", -1),
    ("core", 2020.9, "5", 1), ("core", 2021.9, "6\nLTS", -1), ("core", 2022.9, "7", 1),
    ("core", 2023.9, "8\nLTS", -1), ("core", 2024.9, "9", 1), ("core", 2025.9, "10\nLTS", -1), ("core", 2026.9, "11", 1),
]

fig, ax = plt.subplots(figsize=(16, 5.6))
ax.set_xlim(1995.0, 2027.8)
ax.set_ylim(0.2, 3.75)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.set_yticks([])
ax.set_xticks(range(2002, 2028, 2))
ax.tick_params(labelsize=12)

for key, start, end in spans:
    y, _, edge, fill = LANES[key]
    ax.plot([start, end], [y, y], color=edge, lw=7, solid_capstyle="round", alpha=0.35, zorder=1)

for key, (y, label, edge, fill) in LANES.items():
    ax.text(1995.1, y, label, ha="left", va="center", fontsize=11.5, fontweight="bold", color=edge)

for key, x, text, side in events:
    y, _, edge, fill = LANES[key]
    ax.scatter([x], [y], s=110, color=fill, edgecolor=edge, linewidth=2, zorder=3)
    ax.text(x, y + side * 0.13, text, ha="center", va="bottom" if side > 0 else "top",
            fontsize=10.5, color=INK, linespacing=1.15, zorder=4,
            bbox=dict(fc="white", ec="none", pad=1.5))

ax.annotate("", xy=(2020.7, 1.08), xytext=(2019.7, 1.9),
            arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=1.6, ls="--"))
ax.text(2020.5, 1.55, "злиття в\nєдиний .NET", fontsize=10, color="#92400E", ha="left")

ax.text(2023.4, 3.13, "лише виправлення\nбезпеки", fontsize=10, ha="center", va="bottom", color="#1E40AF")

ax.axvline(2014.85, color=INK, lw=1, ls=":", alpha=0.6)
ax.text(2014.95, 3.62, "2014: .NET стає відкритим\n(open source, GitHub)", fontsize=10, va="top", alpha=0.85)

save(fig, __file__)
