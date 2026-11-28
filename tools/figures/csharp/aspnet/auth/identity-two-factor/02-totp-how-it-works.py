"""Наочна схема: як телефон і сервер незалежно отримують однаковий TOTP-код."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import ACCENT, AMBER, BLUE, GREEN, GREY, INK, arrow, box, canvas, save
from matplotlib.patches import FancyBboxPatch

fig, ax = canvas(12, 5.4)

ax.text(50, 94, "Як працює TOTP без інтернету між телефоном і сервером", ha="center", va="center",
        fontsize=14.5, fontweight="bold", color=INK)
ax.text(50, 88, "Обидві сторони мають один спільний секрет (із QR-коду) і дивляться на один і той самий годинник",
        ha="center", va="center", fontsize=11, color="#475569")

# Ліва зона — Телефон
ax.add_patch(FancyBboxPatch((3, 14), 40, 68, boxstyle="round,pad=0.6,rounding_size=3",
                            fc="#F8FAFC", ec="#94A3B8", lw=1.3, ls="--"))
ax.text(23, 78, "Телефон (Authenticator)", ha="center", va="center", fontsize=12, fontweight="bold", color=INK)

box(ax, 6, 61, 34, 11, "Секретний ключ із QR\nSMYX 2J7U 3PSA ...", fc=AMBER, mono=True, size=10)
box(ax, 6, 46, 34, 11, "Поточний час (UTC)\nокруглений до 30 секунд", fc=BLUE, size=10.5)
arrow(ax, 23, 45, 23, 37, color=ACCENT)
box(ax, 9, 27, 28, 9, "Формула HMAC-SHA1", fc=GREY, size=10.5, weight="bold")
arrow(ax, 23, 26, 23, 19, color="#16A34A")
box(ax, 10, 8, 26, 10, "Код: 995 505", fc=GREEN, ec="#16A34A", lw=1.8, mono=True, size=13, weight="bold")

# Права зона — Сервер
ax.add_patch(FancyBboxPatch((57, 14), 40, 68, boxstyle="round,pad=0.6,rounding_size=3",
                            fc="#F8FAFC", ec="#94A3B8", lw=1.3, ls="--"))
ax.text(77, 78, "Ваш сервер (ASP.NET Core)", ha="center", va="center", fontsize=12, fontweight="bold", color=INK)

box(ax, 60, 61, 34, 11, "Той самий ключ у БД\nAspNetUserTokens", fc=AMBER, mono=True, size=10)
box(ax, 60, 46, 34, 11, "Поточний час (UTC)\nокруглений до 30 секунд", fc=BLUE, size=10.5)
arrow(ax, 77, 45, 77, 37, color=ACCENT)
box(ax, 63, 27, 28, 9, "Формула HMAC-SHA1", fc=GREY, size=10.5, weight="bold")
arrow(ax, 77, 26, 77, 19, color="#16A34A")
box(ax, 64, 8, 26, 10, "Код: 995 505", fc=GREEN, ec="#16A34A", lw=1.8, mono=True, size=13, weight="bold")

# Центральне порівняння
ax.text(50, 56, "Синхронізуються\nлише один раз\nчерез QR-код", ha="center", va="center",
        fontsize=10, color="#475569", bbox=dict(fc="white", ec="#CBD5E1", boxstyle="round,pad=0.4"))
arrow(ax, 37, 13, 63, 13, color="#16A34A", lw=2.0)
ax.text(50, 13, "995 505 == 995 505", ha="center", va="center",
        fontsize=11, fontweight="bold", color="#15803D",
        bbox=dict(fc="white", ec="#16A34A", boxstyle="round,pad=0.35"))

save(fig, __file__)
