"""Стоп-слова: майже половина токенів, але мізерна частка словника."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.4))
tok = [1331109, 702899]; typ = [39341, 39190]
for ax, vals, title, unit in ((a1, tok, "Токенів у корпусі", "тис."), (a2, typ, "Унікальних слів (типів)", "")):
    b = ax.bar(["усі", "без стоп-слів"], vals, color=["#94A3B8", "#2563EB"], edgecolor=INK, lw=1.2)
    for r, v in zip(b, vals):
        ax.text(r.get_x() + r.get_width() / 2, v * 1.02, f"{v:,}".replace(",", " "), ha="center", fontweight="bold")
    ax.set_title(title, fontweight="bold")
    ax.set_ylim(0, max(vals) * 1.15)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", " ")))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
a1.text(0.5, 0.93, "−47,2%", transform=a1.transAxes, ha="center", fontsize=16, color=ACCENT, fontweight="bold")
a2.text(0.5, 0.93, "−0,4%", transform=a2.transAxes, ha="center", fontsize=16, color=ACCENT, fontweight="bold")
fig.tight_layout()
save(fig, __file__)
