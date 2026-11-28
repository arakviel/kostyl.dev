"""Візуальне порівняння методів 2FA та Passkey: захищеність проти зручності."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import ACCENT, AMBER, BLUE, GREEN, GREY, INK, RED, save
from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10.5, 5.2))
fig.patch.set_facecolor("white")
ax.set_facecolor("#F8FAFC")

ax.set_xlim(0.5, 5.5)
ax.set_ylim(0.5, 5.5)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_xticklabels(["1\n(Низька)", "2", "3\n(Середня)", "4", "5\n(Максимальна)"], fontsize=10.5, color=INK)
ax.set_yticklabels(["1 (Низька)", "2", "3 (Середня)", "4", "5 (Найвища)"], fontsize=10.5, color=INK)
ax.set_xlabel("Зручність для користувача", fontsize=12, fontweight="bold", color=INK, labelpad=8)
ax.set_ylabel("Стійкість до атак і фішингу", fontsize=12, fontweight="bold", color=INK, labelpad=8)
ax.set_title("Порівняння методів другого фактора та Passkey", fontsize=14, fontweight="bold", color=INK, pad=12)

ax.grid(True, linestyle="--", alpha=0.45, color="#CBD5E1")
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["left"].set_color("#94A3B8")
ax.spines["bottom"].set_color("#94A3B8")

# Рекомендована зона
ax.add_patch(FancyBboxPatch((2.7, 3.6), 2.65, 1.75, boxstyle="round,pad=0.05,rounding_size=0.15",
                            fc="#DCFCE7", ec="#16A34A", lw=1.2, ls="--", alpha=0.45))
ax.text(4.02, 5.2, "Оптимальний вибір для нових систем", ha="center", va="center",
        fontsize=10, fontweight="bold", color="#166534")

points = [
    (4.6, 2.0, "SMS OTP\n(SIM-swap ризик)", RED, "#DC2626", (-12, -32)),
    (3.9, 2.9, "Email OTP\n(залежить від пошти)", AMBER, "#D97706", (12, -32)),
    (2.1, 3.2, "Recovery Codes\n(лише запасний вхід)", GREY, "#475569", (-15, -32)),
    (3.4, 4.2, "TOTP (Authenticator)\n(золотий стандарт 2FA)", BLUE, ACCENT, (-42, 24)),
    (4.8, 4.8, "Passkey (WebAuthn)\n(захист від фішингу)", GREEN, "#16A34A", (-65, -24)),
]

for x, y, label, fc, ec, offset in points:
    ax.scatter([x], [y], s=260, color=ec, edgecolors="white", linewidths=2, zorder=5)
    ax.annotate(label, (x, y), xytext=offset, textcoords="offset points",
                ha="center", va="center", fontsize=10, fontweight="bold", color=INK,
                arrowprops=dict(arrowstyle="-", color=ec, lw=1.1, alpha=0.7),
                bbox=dict(boxstyle="round,pad=0.35", fc=fc, ec=ec, lw=1.2),
                zorder=6)

save(fig, __file__)
