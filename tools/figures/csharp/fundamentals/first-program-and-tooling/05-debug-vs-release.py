"""SumTo(100 000 000) у Debug і Release: медіана 5 запусків (.NET 10.0.15, macOS, Apple M4 Pro)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt  # noqa: E402
from _style import INK, save  # noqa: E402

fig, ax = plt.subplots(figsize=(9, 4.2))
names = ["Debug\n(dotnet run)", "Release\n(dotnet run -c Release)"]
values = [173, 24]
bars = ax.bar(names, values, color=["#D97706", "#16A34A"], width=0.5)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 4, f"{v} мс", ha="center", fontsize=13)
ax.set_ylabel("Час циклу, мс", fontsize=12)
ax.set_ylim(0, 200)
ax.tick_params(axis="x", labelsize=12)
ax.spines[["top", "right"]].set_visible(False)
ax.text(1.35, 120, "у 7 разів\nшвидше", fontsize=13, color="#15803D", ha="center", fontweight="bold")
save(fig, __file__)
