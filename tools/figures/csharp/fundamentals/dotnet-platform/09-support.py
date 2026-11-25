"""Строки підтримки .NET 6–11 (дані: dotnet/core releases-index.json)."""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from _style import INK, save  # noqa: E402

releases = [
    (".NET 6", "LTS", date(2021, 11, 8), date(2024, 11, 12)),
    (".NET 7", "STS", date(2022, 11, 8), date(2024, 5, 14)),
    (".NET 8", "LTS", date(2023, 11, 14), date(2026, 11, 10)),
    (".NET 9", "STS", date(2024, 11, 12), date(2026, 11, 10)),
    (".NET 10", "LTS", date(2025, 11, 11), date(2028, 11, 14)),
    (".NET 11", "STS", date(2026, 11, 10), date(2028, 11, 14)),
]
color = {"LTS": "#2563EB", "STS": "#D97706"}

fig, ax = plt.subplots(figsize=(13, 4.6))
for i, (name, kind, start, end) in enumerate(releases):
    y = len(releases) - 1 - i
    ax.barh(y, mdates.date2num(end) - mdates.date2num(start), left=mdates.date2num(start),
            height=0.55, color=color[kind], alpha=0.85 if name == ".NET 10" else 0.45,
            edgecolor=INK if name == ".NET 10" else "none", linewidth=2)
    ax.text(mdates.date2num(end) + 20, y, f"{kind}, до {end:%m.%Y}", va="center", fontsize=11,
            bbox=dict(fc="white", ec="none", pad=1.5), zorder=5)

ax.set_yticks(range(len(releases)))
ax.set_yticklabels([r[0] for r in reversed(releases)], fontsize=12)
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_xlim(mdates.date2num(date(2021, 6, 1)), mdates.date2num(date(2029, 10, 1)))
today = mdates.date2num(date(2026, 11, 24))
ax.axvline(today, color="#DC2626", lw=1.6, ls="--")
ax.text(today - 15, 5.75, "листопад 2026", ha="right", color="#DC2626", fontsize=11)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.text(mdates.date2num(date(2021, 6, 1)), -1.55,
        "LTS — 3 роки підтримки, STS — 2 роки. Нова версія щороку в листопаді.", fontsize=11, style="italic")
save(fig, __file__)
