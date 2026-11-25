"""Перший виклик методу через заглушку і JIT, наступні — напряму в машинний код.

Числа з реального запуску tiered-jit.cs (.NET 10.0.15, macOS Arm64): 39,2 мкс, далі 2,2 мкс;
розмір і перші інструкції машинного коду — з DOTNET_JitDisasm='*SumTo*' (172 байти, ARM64).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, arrow, box, save_steps  # noqa: E402

TIMES = [39.2, 2.2, 2.2, 2.2, 2.2]
HOT = "#D97706"
OK = "#16A34A"
MUTED = "#CBD5E1"

# (етап, кількість завершених викликів, підпис)
STEPS = [
    ("start", 0, "Перед першим викликом запис методу SumTo\nвказує на stub:\nмашинного коду ще немає."),
    ("call1", 0, "Виклик 1 іде за адресою\nіз запису методу — у stub."),
    ("jit", 0, "Stub передає IL методу SumTo\nJIT-компілятору."),
    ("code", 0, "JIT створює машинний код ARM64\n(172 байти) у пам'яті процесу."),
    ("patch", 1, "Запис методу тепер вказує на готовий код.\nВиклик 1 виконується: 39,2 мкс\nразом із компіляцією."),
    ("call2", 2, "Виклик 2 іде одразу в машинний код:\n2,2 мкс. Stub і JIT не задіяні."),
    ("rest", 5, "Виклики 3–5 так само.\nЦіна JIT платиться один раз за запуск."),
]


def draw(ax, step):
    stage, done, caption = step
    compiled = stage in ("code", "patch", "call2", "rest")
    patched = stage in ("patch", "call2", "rest")

    ax.text(50, 95, "Перший виклик методу: stub → JIT → машинний код", ha="center", fontsize=18,
            fontweight="bold")

    # учасники
    box(ax, 3, 66, 20, 14, "<Main>\\$\nцикл: 5 викликів\nSumTo(1000)", fc=GREY, size=13)
    box(ax, 32, 66, 20, 14, "Запис методу\nSumTo\n(адреса коду)", fc=AMBER if stage == "patch" else BLUE,
        size=13, ec=HOT if stage == "patch" else INK, lw=2.4 if stage == "patch" else 1.4)
    stub_active = stage in ("call1", "jit")
    box(ax, 62, 78, 16, 9, "Stub", fc=AMBER if stub_active else GREY, size=13,
        ec=HOT if stub_active else INK, lw=2.4 if stub_active else 1.4, alpha=0.45 if patched else 1)
    jit_active = stage in ("jit", "code")
    box(ax, 84, 78, 13, 9, "JIT", fc=AMBER if jit_active else GREY, size=14, weight="bold",
        ec=HOT if jit_active else INK, lw=2.4 if jit_active else 1.4, alpha=0.45 if patched else 1)
    if compiled:
        lines = ["машинний код SumTo, ARM64", "", "stp  fp, lr, [sp, #-0x30]!", "mov  fp, sp", "...",
                 "ret  lr", "", "усього 172 байти"]
        code = "\n".join(line.ljust(27) for line in lines)
        box(ax, 62, 40, 35, 28, code, fc=GREEN, mono=True, size=12,
            ec=OK if stage in ("code", "call2", "rest") else INK, lw=2.4 if stage in ("code", "call2") else 1.4)
    else:
        box(ax, 62, 40, 35, 28, "машинного коду\nще немає", fc="white", size=13, ec=MUTED, ls="--")
        ax.texts[-1].set_color("#94A3B8")

    # стрілки
    calling = stage in ("call1", "call2", "rest")
    arrow(ax, 23.8, 73, 31.2, 73, color=HOT if calling else INK, lw=2.6 if calling else 1.6)
    if patched:
        arrow(ax, 52.8, 70, 61.2, 60, color=OK if stage != "patch" else HOT, lw=2.6)
        ax.text(57.5, 68.5, "нова адреса", fontsize=11, color=OK, rotation=-38, ha="center")
    else:
        arrow(ax, 52.8, 76, 61.2, 81, color=HOT if stage == "call1" else INK, lw=2.6 if stage == "call1" else 1.6)
    if stage == "jit":
        arrow(ax, 78.8, 82.5, 83.2, 82.5, color=HOT, lw=2.6)
        ax.text(81, 90, "IL методу", fontsize=11, ha="center", color=HOT)
    if stage == "code":
        arrow(ax, 90.5, 77, 85, 69, color=OK, lw=2.6)

    # час викликів
    ax.text(3, 55, "Час виклику, мкс", fontsize=13, fontweight="bold")
    base, scale = 16, 0.82
    for i, value in enumerate(TIMES):
        x = 5 + i * 10
        ax.text(x + 3, base - 4, f"{i + 1}", ha="center", fontsize=12)
        if i < done:
            ax.add_patch(__import__("matplotlib.patches", fromlist=["Rectangle"]).Rectangle(
                (x, base), 6, value * scale, fc=HOT if i == 0 else "#2563EB"))
            ax.text(x + 3, base + value * scale + 1.2, f"{value:.1f}".replace(".", ","), ha="center", fontsize=12)
    ax.plot([3, 53], [base, base], color=INK, lw=1.2)
    ax.text(28, base - 9, "номер виклику", ha="center", fontsize=11, color="#475569")

    ax.text(78.5, 24, caption, ha="center", va="center", fontsize=13, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 3.2) for s in STEPS[:-1]] + [(STEPS[-1], 4.5)], draw, poster=5)
