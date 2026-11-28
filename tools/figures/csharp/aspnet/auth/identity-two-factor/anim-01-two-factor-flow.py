"""Покрокова анімація: дворівневий вхід із 2FA та cookie Remember Machine."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import ACCENT, AMBER, BLUE, GREEN, GREY, INK, arrow, box, save_steps

steps = [
    ("step1", 2.5),
    ("step2", 2.8),
    ("step3", 2.8),
    ("step4", 2.8),
]


def draw(ax, state):
    titles = {
        "step1": "Крок 1: Вхід із паролем — 2FA увімкнено",
        "step2": "Крок 2: Перевірка TOTP-коду + прапорець RememberMachine",
        "step3": "Крок 3: Наступний вхід із того самого браузера",
        "step4": "Крок 4: Вхід із нового браузера або після ForgetTwoFactorClientAsync()",
    }
    ax.text(50, 92, titles[state], ha="center", va="center", fontsize=13.5, fontweight="bold", color=INK)

    if state == "step1":
        box(ax, 5, 52, 34, 24, "Браузер\n\nPOST /auth/login\n{ email, password }", fc=BLUE, size=11)
        arrow(ax, 40, 64, 58, 64, "Перевірка пароля", size=10.5, color=ACCENT)
        box(ax, 59, 52, 36, 24, "SignInManager\n\nПароль правильний,\nале TwoFactorEnabled = true", fc=AMBER, size=11)
        box(ax, 12, 16, 76, 24,
            "Результат: SignInResult.RequiresTwoFactor\n"
            "Сервер НЕ пускає в акаунт, а ставить тимчасову cookie\n"
            "Identity.TwoFactorUserId і просить 2FA-код.",
            fc=GREY, size=11)
    elif state == "step2":
        box(ax, 5, 52, 36, 24, "Браузер\n\nPOST /auth/login/2fa\ncode + rememberMachine=true", fc=BLUE, size=11)
        arrow(ax, 42, 64, 56, 64, "Перевірка TOTP", size=10.5, color="#16A34A")
        box(ax, 57, 52, 38, 24, "SignInManager\n\nTwoFactorAuthenticatorSignInAsync\nвидає дві cookie", fc=GREEN, size=11)
        box(ax, 10, 16, 80, 24,
            "1) .AspNetCore.Identity.Application — основна сесія входу\n"
            "2) Identity.TwoFactorRememberMe — маркер довіреного пристрою",
            fc=GREEN, mono=True, size=10.5)
    elif state == "step3":
        box(ax, 5, 52, 36, 24, "Той самий браузер\n\nPOST /auth/login\n+ cookie RememberMe", fc=BLUE, size=11)
        arrow(ax, 42, 64, 56, 64, "Пароль + маркер", size=10.5, color="#16A34A")
        box(ax, 57, 52, 38, 24, "SignInManager\n\nБачить RememberMe cookie\nі пропускає другий фактор", fc=GREEN, size=11)
        box(ax, 14, 16, 72, 22,
            "Результат: SignInResult.Success\n"
            "Користувач одразу входить без повторного введення TOTP-коду.",
            fc=GREEN, size=11)
    elif state == "step4":
        box(ax, 5, 52, 36, 24, "Новий браузер\n\nPOST /auth/login\n(без RememberMe cookie)", fc=AMBER, size=11)
        arrow(ax, 42, 64, 56, 64, "Лише пароль", size=10.5, color="#D97706")
        box(ax, 57, 52, 38, 24, "SignInManager\n\nМаркера пристрою немає ->\nзнову RequiresTwoFactor", fc=AMBER, size=11)
        box(ax, 12, 16, 76, 22,
            "Безпека збережена: навіть якщо пароль відомий,\n"
            "чужий пристрій мусить ввести 2FA-код або резервний код.",
            fc=GREY, size=11)


save_steps(__file__, steps, draw, poster=1)
