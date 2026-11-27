"""Покрокова анімація: життєвий цикл токена та інвалідація через SecurityStamp."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import ACCENT, AMBER, BLUE, GREEN, GREY, INK, RED, arrow, box, save_steps

steps = [
    ("step1", 2.2),
    ("step2", 2.5),
    ("step3", 2.5),
    ("step4", 3.0),
]


def draw(ax, state):
    titles = {
        "step1": "Крок 1: Реєстрація користувача — початковий SecurityStamp",
        "step2": "Крок 2: Генерація токена підтвердження (містить SecurityStamp)",
        "step3": "Крок 3: Пароль змінено або скинуто — SecurityStamp оновився",
        "step4": "Крок 4: Перевірка старого токена — розбіжність SecurityStamp",
    }
    ax.text(50, 92, titles[state], ha="center", va="center", fontsize=14, fontweight="bold", color=INK)

    # Блок БД AspNetUsers
    stamp = "A1F9-88C1" if state in ("step1", "step2") else "B7C2-44E0"
    stamp_fc = BLUE if state in ("step1", "step2") else AMBER
    box(ax, 5, 52, 36, 28,
        f"AspNetUsers (БД)\n\nEmailConfirmed: false\nSecurityStamp: {stamp}",
        fc=stamp_fc, mono=True, size=11.5)

    if state == "step1":
        box(ax, 55, 52, 40, 28,
            "Токен ще не згенеровано.\nSecurityStamp зберігається у рядку\nкористувача в базі даних.",
            fc=GREY, size=11.5)
    elif state == "step2":
        arrow(ax, 42, 66, 54, 66, "Encrypt", size=11, color=ACCENT)
        box(ax, 55, 52, 40, 28,
            "Токен у листі (CfDJ8...)\n\nuserId: b59e059f...\nstamp:  A1F9-88C1\nTTL:    3 дні",
            fc=GREEN, mono=True, size=11.5)
    elif state == "step3":
        box(ax, 55, 52, 40, 28,
            "Старий токен у листі (CfDJ8...)\n\nuserId: b59e059f...\nstamp:  A1F9-88C1 (застарілий)",
            fc=GREY, mono=True, size=11.5)
        box(ax, 15, 16, 70, 22,
            "ResetPasswordAsync() або ChangePasswordAsync() автоматично\n"
            "записує новий SecurityStamp = B7C2-44E0 у базу даних.",
            fc=AMBER, size=12)
    elif state == "step4":
        box(ax, 55, 52, 40, 28,
            "Старий токен у листі (CfDJ8...)\n\nuserId: b59e059f...\nstamp:  A1F9-88C1",
            fc=RED, mono=True, size=11.5)
        arrow(ax, 54, 60, 42, 60, "Порівняння", size=11, color="#DC2626")
        box(ax, 12, 14, 76, 24,
            "A1F9-88C1 != B7C2-44E0\n\n"
            "ConfirmEmailAsync() повертає InvalidToken.\n"
            "Старий токен більше недійсний без жодної таблиці відкликання.",
            fc=RED, size=12, weight="bold")


save_steps(__file__, steps, draw, poster=3)
