"""Час циклу на 1 млрд ітерацій з unused-result.cs: Debug проти Release (медіана трьох запусків).

Дані з реального запуску на Apple M4 Pro, .NET 10.0.404 (runtime 10.0.15):
Release: з результатом 526/520/518, без результату 249/246/253, порожній 250/246/253 мс;
Debug:   з результатом 1547/1544/1589, без результату 1652/1399/2024, порожній 445/451/453 мс.
"""
import sys
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import INK, save  # noqa: E402

CATS = ["з результатом\n(sum += i % 7)", "без результату\n(int t = i % 7)", "порожній цикл"]
DEBUG = [median([1547, 1544, 1589]), median([1652, 1399, 2024]), median([445, 451, 453])]
RELEASE = [median([526, 520, 518]), median([249, 246, 253]), median([250, 246, 253])]
C_DEBUG, C_RELEASE = "#D97706", "#2563EB"
MUTED = "#475569"

fig, ax = plt.subplots(figsize=(11, 4.6))
h = 0.3
for k, (d, r) in enumerate(zip(DEBUG, RELEASE)):
    for value, dy, color in [(d, -h / 2 - 0.02, C_DEBUG), (r, h / 2 + 0.02, C_RELEASE)]:
        y = k + dy
        ax.add_patch(FancyBboxPatch((0, y - h / 2), value, h, boxstyle="round,pad=0,rounding_size=0.06",
                                    mutation_aspect=1 / 120, fc=color, ec="none"))
        ax.text(value + 25, y, f"{value:.0f} мс", va="center", fontsize=12.5, color=INK)
ax.set_yticks(range(len(CATS)), CATS, fontsize=12.5)
ax.set_ylim(len(CATS) - 0.5, -0.6)
ax.set_xlim(0, 2000)
ax.set_xticks([0, 500, 1000, 1500, 2000], ["0", "500", "1000", "1500", "2000 мс"], fontsize=11.5, color=MUTED)
ax.grid(axis="x", color="#E2E8F0", lw=1)
ax.set_axisbelow(True)
for side in ["top", "right", "left"]:
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#CBD5E1")
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", length=0)
ax.set_title("1 млрд ітерацій, медіана трьох запусків (Apple M4 Pro, .NET 10)", fontsize=13, color=MUTED,
             loc="left", pad=28)
for x, label, color in [(0.0, "Debug (dotnet run)", C_DEBUG), (0.3, "Release (dotnet run -c Release)", C_RELEASE)]:
    ax.add_patch(plt.Rectangle((x, 1.035), 0.018, 0.045, transform=ax.transAxes, fc=color, ec="none",
                               clip_on=False))
    ax.text(x + 0.026, 1.057, label, transform=ax.transAxes, va="center", fontsize=12, color=INK)
save(fig, __file__)
