"""Наочне порівняння: Пароль + 2FA проти Passkey (захист від фішингу)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import ACCENT, AMBER, BLUE, GREEN, GREY, INK, RED, arrow, box, canvas, save
from matplotlib.patches import FancyBboxPatch

fig, ax = canvas(12, 5.2)

ax.text(50, 94, "Чому Passkey захищає від фішингу краще за пароль і код", ha="center", va="center",
        fontsize=14.5, fontweight="bold", color=INK)

# Верхня смуга: Пароль + TOTP
ax.add_patch(FancyBboxPatch((2, 51), 96, 36, boxstyle="round,pad=0.5,rounding_size=2.5",
                            fc="#FFF7ED", ec="#FDBA74", lw=1.3))
ax.text(4, 83, "Сценарій А: Пароль + TOTP-код на фейковому сайті", ha="left", va="center",
        fontsize=11.5, fontweight="bold", color="#9A3412")

box(ax, 4, 56, 20, 20, "Користувач\nвводить пароль\nі 6-значний код", fc="white", ec="#94A3B8", size=10.5)
arrow(ax, 25, 66, 33, 66, color="#DC2626")
box(ax, 34, 56, 25, 20, "Фейковий сайт\nmy-bank-login.xyz\nперехоплює дані", fc=RED, ec="#DC2626", size=10.5)
arrow(ax, 60, 66, 68, 66, color="#DC2626")
box(ax, 69, 56, 27, 20, "Зловмисник одразу\nвводить їх на\nсправжньому my-bank.com", fc=RED, ec="#DC2626", size=10.5, weight="bold")

# Нижня смуга: Passkey
ax.add_patch(FancyBboxPatch((2, 7), 96, 38, boxstyle="round,pad=0.5,rounding_size=2.5",
                            fc="#F0FDF4", ec="#86EFAC", lw=1.3))
ax.text(4, 41, "Сценарій Б: Passkey (прив'язка до домену в браузері)", ha="left", va="center",
        fontsize=11.5, fontweight="bold", color="#166534")

box(ax, 4, 12, 24, 22, "Справжній my-bank.com\nнадсилає випадковий\nchallenge", fc=BLUE, ec=ACCENT, size=10.5)
arrow(ax, 29, 23, 36, 23, color="#16A34A")
box(ax, 37, 12, 28, 22, "Пристрій перевіряє\nдомен + Face ID / PIN\nі підписує challenge", fc=GREEN, ec="#16A34A", size=10.5)
arrow(ax, 66, 23, 73, 23, color="#16A34A")
box(ax, 74, 12, 22, 22, "На фейковому сайті\nmy-bank-login.xyz\nключ навіть не спрацює", fc=GREEN, ec="#16A34A", size=10.5, weight="bold")

save(fig, __file__)
