"""Час від запуску до завершення CsHello різними способами (медіана 40 запусків, 15 для dotnet run).

Реальні заміри: .NET 10.0.15, SDK 10.0.404, macOS, Apple M4 Pro.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt  # noqa: E402
from _style import INK, save  # noqa: E402

rows = [
    ("dotnet run hello.cs\n(file-based, без змін у файлі)", 147.3, "#94A3B8"),
    ("Framework-dependent\n./CsHello", 20.5, "#2563EB"),
    ("Self-contained\n./CsHello", 20.5, "#2563EB"),
    ("Self-contained + ReadyToRun\n./CsHello", 20.8, "#2563EB"),
    ("Native AOT\n./CsHello", 4.3, "#16A34A"),
]

fig, ax = plt.subplots(figsize=(12, 4.8))
labels = [r[0] for r in rows][::-1]
values = [r[1] for r in rows][::-1]
colors = [r[2] for r in rows][::-1]
bars = ax.barh(labels, values, color=colors, height=0.6)
for bar, value in zip(bars, values):
    ax.text(value + 2, bar.get_y() + bar.get_height() / 2, f"{value:.1f} мс".replace(".", ","), va="center",
            fontsize=12.5, color=INK)
ax.set_xlabel("Час від запуску процесу до завершення, мс (менше — краще)", fontsize=12)
ax.set_xlim(0, 168)
ax.tick_params(axis="y", labelsize=12, length=0)
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, __file__)
