"""Будова токена DataProtectionTokenProvider і кодування Base64Url."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import ACCENT, AMBER, BLUE, GREEN, GREY, INK, arrow, box, canvas, save

fig, ax = canvas(11.5, 4.8)

ax.text(50, 94, "Як формується токен підтвердження для URL", ha="center", va="center",
        fontsize=14, fontweight="bold", color=INK)

# Корисне навантаження
box(ax, 3, 66, 22, 18, "userId\n\"b59e059f-...\"", fc=BLUE, mono=True, size=11)
box(ax, 27, 66, 22, 18, "purpose\n\"EmailConfirmation\"", fc=BLUE, mono=True, size=11)
box(ax, 51, 66, 22, 18, "SecurityStamp\n\"A1F9...\"", fc=AMBER, mono=True, size=11)
box(ax, 75, 66, 22, 18, "timestamp\nUTC ticks", fc=GREY, mono=True, size=11)

# Стрілка до DataProtection
arrow(ax, 50, 64, 50, 48, color=ACCENT)
ax.text(50, 56, "DataProtector.Protect() + Base64", ha="center", va="center",
        fontsize=10.5, bbox=dict(fc="white", ec="none", pad=2.5))

# Зашифрований токен
box(ax, 10, 33, 80, 13, "CfDJ8Dh59uYNkaBAjlCi1AXPHKGI55/yBIjC3OTL2TrPXeqyX...", fc=GREY, mono=True, size=11)

# Стрілка до Base64Url
arrow(ax, 50, 31, 50, 15, color=ACCENT)
ax.text(50, 23, "WebEncoders.Base64UrlEncode(): '+' -> '-', '/' -> '_', без '='", ha="center", va="center",
        fontsize=10.5, bbox=dict(fc="white", ec="none", pad=2.5))

# Фінальний URL-безпечний токен
box(ax, 6, 2, 88, 11, "?userId=b59e059f-...&token=Q2ZESjhEaDU5dVlOa2FCQWpsQ2kx...", fc=GREEN, mono=True, size=10.5)

save(fig, __file__)
