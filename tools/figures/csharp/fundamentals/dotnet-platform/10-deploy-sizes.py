"""Розмір однієї й тієї самої програми при різних способах публікації (macOS arm64, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt  # noqa: E402
from _style import save  # noqa: E402

labels = [
    "Framework-dependent\nCsHello.dll + apphost",
    "Native AOT\nодин файл",
    "Self-contained\n191 файл",
]
kib = [4.5 + 121.8, 1.2 * 1024, 83 * 1024]
text = ["4,5 КБ + 122 КБ", "1,2 МБ", "83 МБ"]
colors = ["#16A34A", "#2563EB", "#D97706"]

fig, ax = plt.subplots(figsize=(11, 3.8))
bars = ax.barh(labels, kib, color=colors, height=0.55)
ax.set_xscale("log")
ax.set_xlim(50, 400_000)
for bar, t in zip(bars, text):
    ax.text(bar.get_width() * 1.25, bar.get_y() + bar.get_height() / 2, t, va="center", fontsize=12, fontweight="bold")
ax.invert_yaxis()
ax.set_xlabel("Розмір на диску, КБ (логарифмічна шкала)", fontsize=11.5)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="y", labelsize=11.5)
save(fig, __file__)
