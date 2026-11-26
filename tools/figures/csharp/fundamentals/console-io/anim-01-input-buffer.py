"""Буфер введення: ReadLine забирає рядок після Enter, Read — по одному символу (поведінка з read-codes.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import AMBER, BLUE, GREEN, INK, box, save_steps  # noqa: E402

MUTED = "#475569"
RED = "#DC2626"

# (виклик, що набрано в рядку терміналу, буфер, результат, підпис)
STEPS = [
    ("Console.ReadLine()", "", [], None, "ReadLine чекає: у буфері порожньо, програма зупинилася на цьому рядку."),
    ("Console.ReadLine()", "4", [], None, "Користувач набирає 4. Символ ще в терміналі, програма його не бачить."),
    ("Console.ReadLine()", "42", [], None, "Набрано 42. До натискання Enter текст можна виправити Backspace."),
    ("Console.ReadLine()", "", ["4", "2", "\\n"], None, "Enter: увесь рядок разом із символом нового рядка потрапляє в буфер."),
    ("Console.ReadLine()", "", [], '"42"', "ReadLine забрав символи до \\n і повернув рядок \"42\" — без \\n."),
    ("Console.Read()", "", ["A", "B", "\\n"], None, "Набрано AB і Enter. Тепер програма читає через Read."),
    ("Console.Read()", "", ["B", "\\n"], "65", "Read забрав один символ і повернув його код: 'A' = 65."),
    ("Console.Read()", "", ["\\n"], "66", "Наступний Read — 'B' = 66. Нове введення не потрібне: символ уже в буфері."),
    ("Console.Read()", "", [], "10", "Третій Read повертає код символу нового рядка: 10."),
    ("Console.Read()", "", [], None, "Буфер порожній — четвертий Read знову чекає на Enter.\nКоли введення закінчене (Ctrl+Z / Ctrl+D), Read повертає -1."),
]


def draw(ax, step):
    call, typed, buffer, result, caption = step
    ax.text(50, 95, "Звідки Console бере введення", ha="center", fontsize=18, fontweight="bold")

    # термінал
    box(ax, 2, 62, 30, 22, "", fc="#1E293B", ec="#1E293B")
    ax.text(4, 79, "термінал", fontsize=11, color="#94A3B8")
    ax.text(4, 70, "> " + typed + "▌", fontsize=16, color="#E2E8F0", fontfamily="DejaVu Sans Mono", va="center")
    ax.text(17, 56, "рядок, який набирають", ha="center", fontsize=11, color=MUTED)

    # буфер
    ax.text(37, 86, "буфер введення програми", fontsize=12.5, fontweight="bold")
    for k in range(6):
        filled = k < len(buffer)
        ax.add_patch(FancyBboxPatch((37 + k * 6.2, 66), 5.6, 13, boxstyle="round,pad=0,rounding_size=0.6",
                                    fc=GREEN if filled else "white", ec=INK if filled else "#CBD5E1", lw=1.2))
        if filled:
            ax.text(37 + k * 6.2 + 2.8, 72.5, buffer[k], ha="center", va="center", fontsize=16,
                    fontfamily="DejaVu Sans Mono")
    ax.annotate("", xy=(36.5, 72.5), xytext=(32.5, 72.5), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))

    # програма
    box(ax, 77, 62, 21, 22, "", fc="#F8FAFC", ec="#CBD5E1")
    ax.text(87.5, 79, "програма", ha="center", fontsize=11, color=MUTED)
    ax.text(87.5, 72.5, call, ha="center", va="center", fontsize=12, fontfamily="DejaVu Sans Mono")
    waiting = result is None
    ax.text(87.5, 66, "чекає…" if waiting else f"→ {result}", ha="center", va="center", fontsize=14,
            color=RED if waiting else "#15803D", fontweight="bold", fontfamily="DejaVu Sans Mono")
    ax.annotate("", xy=(76.5, 72.5), xytext=(74.5, 72.5), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))

    ax.text(50, 30, "ReadLine — усе до \\n, повертає string? (null — кінець введення)\n"
            "Read — один символ, повертає int (-1 — кінець введення)",
            ha="center", va="center", fontsize=13, color=MUTED, linespacing=1.6)
    ax.text(50, 9, caption, ha="center", va="center", fontsize=14, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 3.0) for s in STEPS[:-1]] + [(STEPS[-1], 5.0)], draw, poster=4)
