"""Три категорії факторів автентифікації та принцип 2FA."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import ACCENT, AMBER, BLUE, GREEN, GREY, INK, RED, box, canvas, save
from matplotlib.patches import FancyBboxPatch

fig, ax = canvas(12, 5.4)

ax.text(50, 94, "Три категорії факторів автентифікації", ha="center", va="center",
        fontsize=15, fontweight="bold", color=INK)
ax.text(50, 88, "2FA вимагає підтвердження з двох різних категорій", ha="center", va="center",
        fontsize=11.5, color="#475569")

cols = [
    (3,  "1. Щось, що ви знаєте", BLUE,  "#2563EB",
     "Приклади:\n• Пароль\n• PIN-код\n• Секретне питання",
     "Ризик:\nФішинг, витік бази,\nповтор паролів", RED),
    (35, "2. Щось, що ви маєте",  AMBER, "#D97706",
     "Приклади:\n• Смартфон (TOTP / SMS)\n• Фізичний ключ (YubiKey)\n• Ноутбук із Passkey",
     "Ризик:\nКрадіжка пристрою,\nSIM-swapping (для SMS)", AMBER),
    (67, "3. Хто ви є (біометрія)", GREEN, "#16A34A",
     "Приклади:\n• Відбиток пальця\n• Face ID / Windows Hello\n• Сітківка ока",
     "Особливість:\nПрацює локально на\nвашому пристрої", GREY),
]

for x, title, fc_head, ec_head, body, risk, fc_risk in cols:
    ax.add_patch(FancyBboxPatch((x, 22), 30, 58, boxstyle="round,pad=0.5,rounding_size=2.5",
                                fc="#F8FAFC", ec="#CBD5E1", lw=1.2))
    box(ax, x + 1.5, 68, 27, 10, title, fc=fc_head, ec=ec_head, lw=1.6, size=11.5, weight="bold")
    box(ax, x + 1.5, 43, 27, 22, body, fc="white", ec="#CBD5E1", lw=1.0, size=10.5, align="left")
    box(ax, x + 1.5, 24, 27, 16, risk, fc=fc_risk, ec="#94A3B8", lw=1.0, size=10, align="left")

# Підсумок внизу
box(ax, 3, 3, 94, 13,
    "Приклад надійного 2FA:  Пароль (категорія 1)  +  Код із телефона чи Passkey (категорія 2/3)\n"
    "Навіть якщо пароль витек із бази, без вашого пристрою вхід заблоковано.",
    fc=BLUE, ec=ACCENT, lw=1.6, size=10.5, weight="bold")

save(fig, __file__)
