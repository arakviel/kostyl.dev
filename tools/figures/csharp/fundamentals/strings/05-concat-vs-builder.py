"""Склеювання += проти StringBuilder: час і виділена пам'ять (concat-vs-builder.cs, Release, перший прогін).

Дані з реального запуску на Apple M4 Pro, .NET 10.0.404:
n:          5000   10000   20000   40000
+= мс:       1.4     4.0    13.2    49.6
+= МБ:      25.1   100.3   400.5  1601.0
SB мс:      0.07    0.31    0.05    0.07
SB МБ:      0.03    0.05    0.09    0.16
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt  # noqa: E402

from _style import INK, save  # noqa: E402

N = [5_000, 10_000, 20_000, 40_000]
CONCAT_MS = [1.4, 4.0, 13.2, 49.6]
CONCAT_MB = [25.1, 100.3, 400.5, 1601.0]
SB_MS = [0.07, 0.31, 0.05, 0.07]
SB_MB = [0.03, 0.05, 0.09, 0.16]
C_CONCAT, C_SB = "#D97706", "#2563EB"
MUTED = "#475569"

fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
for ax, concat, sb, title, unit, fmt in [
    (axes[0], CONCAT_MS, SB_MS, "час", "мс", "{:.1f}"),
    (axes[1], CONCAT_MB, SB_MB, "виділено пам'яті", "МБ", "{:.0f}"),
]:
    ax.plot(N, concat, color=C_CONCAT, lw=2, marker="o", markersize=7, solid_capstyle="round")
    ax.plot(N, sb, color=C_SB, lw=2, marker="o", markersize=7)
    for x, v in zip(N, concat):
        ax.text(x, v + max(concat) * 0.04, fmt.format(v).replace(".", ","), ha="center", va="bottom", fontsize=11, color=INK)
    ax.text(N[-1], sb[-1] + max(concat) * 0.05, f"StringBuilder: {str(sb[-1]).replace('.', ',')} {unit}", ha="right", va="bottom",
            fontsize=11, color=INK)
    ax.set_title(f"{title}, {unit}", loc="left", fontsize=13, color=INK, pad=10)
    ax.set_xticks(N, ["5 000", "10 000", "20 000", "40 000"], fontsize=11, color=MUTED)
    ax.tick_params(axis="y", labelsize=11, colors=MUTED, length=0)
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, max(concat) * 1.18)
    ax.grid(axis="y", color="#E2E8F0", lw=1)
    ax.set_axisbelow(True)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.set_xlabel("кількість дописаних символів n", fontsize=11.5, color=MUTED)
for x, label, color in [(0.0, "result += \"x\"", C_CONCAT), (0.22, "StringBuilder.Append(\"x\")", C_SB)]:
    fig.patches.append(plt.Rectangle((0.06 + x, 0.98), 0.012, 0.03, transform=fig.transFigure, fc=color, ec="none"))
    fig.text(0.076 + x, 0.995, label, va="center", fontsize=12, color=INK, fontfamily="DejaVu Sans Mono")
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, __file__)
