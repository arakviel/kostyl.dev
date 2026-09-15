#!/usr/bin/env python3
"""
Скрипт для автоматичної генерації всіх графіків та візуалізацій для:
- 16.ai-python/04.statistics-basics/
- 16.ai-python/07.linear-regression-theory/
"""

import os
import sys
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy import stats

# Налаштування стилю та шрифтів
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = False
plt.rcParams['figure.facecolor'] = '#FFFFFF'
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['savefig.facecolor'] = '#FFFFFF'

BASE_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "public", "images", "ai-python"
)

def save_fig(fig, rel_dir, name, dpi=200):
    folder = os.path.join(BASE_IMAGES_DIR, rel_dir)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{name}.png")
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Generated: {filepath}")

# ==============================================================================
# 1. СПЕЦІАЛЬНА ДІАГРАМА: Аналогія числової прямої (станції метро vs континуум)
# ==============================================================================
def generate_random_variables_analogy():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 7.4), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')

    fig.suptitle(
        "Аналогія числової прямої: Дискретна vs Неперервна випадкова величина",
        fontsize=15,
        fontweight="bold",
        color="#0F172A",
        y=0.98
    )

    # 1. Дискретна величина
    ax1.set_facecolor('#FFFFFF')
    ax1.set_title(
        "1. Дискретна величина — окремі станції метро (ізольовані точки)",
        fontsize=12,
        fontweight="bold",
        color="#1E40AF",
        loc="left",
        pad=12
    )

    ax1.annotate('', xy=(6.6, 0), xytext=(0.4, 0),
                 arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.75", color="#64748B", lw=2.4))
    ax1.text(6.75, -0.02, "X", fontsize=13, fontweight="bold", color="#334155", va="center")

    stations = [1, 2, 3, 4, 5, 6]
    for st in stations:
        ax1.plot([st, st], [-0.15, 0.15], color="#3B82F6", lw=1.5, zorder=3)
        ax1.scatter(st, 0, s=280, facecolor="#DBEAFE", edgecolor="#1D4ED8", linewidth=2.6, zorder=5)
        ax1.scatter(st, 0, s=70, facecolor="#1D4ED8", zorder=6)
        ax1.text(st, -0.36, f"X = {st}", fontsize=11, fontweight="bold", ha="center", color="#1E3A8A")
        ax1.text(st, 0.32, f"Станція {st}", fontsize=9, ha="center", color="#475569")

    ax1.scatter(2.5, 0, marker='x', s=160, color="#DC2626", linewidth=3.2, zorder=6)
    ax1.annotate(
        "Точка 2.5 не існує!\n(поїзд тут не зупиняється)",
        xy=(2.5, 0.08),
        xytext=(2.5, 0.68),
        fontsize=9,
        fontweight="bold",
        color="#991B1B",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#FEE2E2", edgecolor="#EF4444", lw=1.2),
        arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.6)
    )

    ax1.annotate(
        "Порожній простір між значеннями\n(проміжних точок не існує)",
        xy=(4.5, 0.04),
        xytext=(4.5, 0.68),
        fontsize=8.5,
        color="#475569",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#F8FAFC", edgecolor="#94A3B8", lw=1),
        arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.3)
    )

    ax1.set_xlim(0.2, 7.2)
    ax1.set_ylim(-0.65, 1.05)
    ax1.axis('off')

    # 2. Неперервна величина
    ax2.set_facecolor('#FFFFFF')
    ax2.set_title(
        "2. Неперервна величина — вся пряма цілком (зупинка в будь-якій точці)",
        fontsize=12,
        fontweight="bold",
        color="#065F46",
        loc="left",
        pad=12
    )

    rect = patches.FancyBboxPatch(
        (0.8, -0.1), 5.4, 0.2,
        boxstyle="round,pad=0.03",
        linewidth=1.6,
        edgecolor="#059669",
        facecolor="#D1FAE5",
        alpha=0.95,
        zorder=2
    )
    ax2.add_patch(rect)

    ax2.annotate('', xy=(6.6, 0), xytext=(0.4, 0),
                 arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.75", color="#059669", lw=2.6))
    ax2.text(6.75, -0.02, "X", fontsize=13, fontweight="bold", color="#065F46", va="center")

    for val in [1, 2, 3, 4, 5, 6]:
        ax2.plot([val, val], [-0.09, 0.09], color="#047857", lw=1.5, zorder=3)
        ax2.text(val, -0.28, str(val), fontsize=10.5, ha="center", color="#334155", fontweight="bold")

    sample_points = [
        (1.42, "1.42\n(дробове)", 0.62),
        (2.718, "e ≈ 2.718\n(ірраціональне)", -0.68),
        (3.1415, "π ≈ 3.1415\n(нескінченна точність)", 0.62),
        (4.85, "4.8502...\n(будь-яка позиція)", 0.62),
        (5.62, "5.62\n(мікрокрок)", -0.68)
    ]

    for pt_x, pt_label, text_y in sample_points:
        ax2.scatter(pt_x, 0, s=120, facecolor="#10B981", edgecolor="#064E3B", linewidth=2, zorder=5)
        arrow_direction = (pt_x, 0.08) if text_y > 0 else (pt_x, -0.08)
        ax2.annotate(
            pt_label,
            xy=arrow_direction,
            xytext=(pt_x, text_y),
            fontsize=8.5,
            fontweight="bold",
            color="#064E3B",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#ECFDF5", edgecolor="#10B981", lw=1.1),
            arrowprops=dict(arrowstyle="->", color="#059669", lw=1.3)
        )

    ax2.text(
        3.5, -1.08,
        "✦ Нескінченна щільність: між будь-якими двома числами існує нескінченно багато інших значень ✦",
        fontsize=9.5,
        fontstyle="italic",
        color="#047857",
        ha="center"
    )

    ax2.set_xlim(0.2, 7.2)
    ax2.set_ylim(-1.25, 1.05)
    ax2.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    save_fig(fig, "statistics-basics/random-variables", "01")


# ==============================================================================
# 2. ВІЗУАЛІЗАЦІЇ ДЛЯ CENTRAL TENDENCY (02, 03, 04, 05)
# ==============================================================================

def generate_central_tendency_salaries_outlier():
    """
    02.png: Вплив аутлайера на вибірку зарплат (9 працівників vs 1 CEO)
    """
    fig, ax = plt.subplots(figsize=(11.5, 4.4), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    salaries = [25, 30, 30, 32, 35, 35, 35, 40, 45, 200]
    median_val = 35.0
    mean_val = 50.7
    mean_without = 34.1

    # Горизонтальна числова вісь
    ax.annotate('', xy=(212, 0), xytext=(15, 0),
                arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.75", color="#64748B", lw=2.2))
    ax.text(215, 0, "Зарплата (тис. грн)", fontsize=11, fontweight="bold", color="#334155", va="center")

    # Розмітка точок зі стеком однакових значень
    seen = {}
    for s in salaries:
        seen[s] = seen.get(s, 0) + 1
        y_pos = 0.13 * (seen[s] - 1)
        if s == 200:
            # Аутлайер (CEO)
            ax.scatter(s, y_pos, s=280, facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2.5, zorder=5)
            ax.scatter(s, y_pos, s=70, facecolor="#DC2626", zorder=6)
            ax.annotate(
                "Директор (CEO)\n200 000 грн (Аутлайер)",
                xy=(s, y_pos + 0.08),
                xytext=(s - 14, y_pos + 0.65),
                fontsize=9.5,
                fontweight="bold",
                color="#991B1B",
                ha="center",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF2F2", edgecolor="#EF4444", lw=1.2),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5)
            )
        else:
            # Звичайні працівники
            ax.scatter(s, y_pos, s=180, facecolor="#DBEAFE", edgecolor="#2563EB", linewidth=2.0, zorder=5)
            ax.scatter(s, y_pos, s=45, facecolor="#1D4ED8", zorder=6)

    # Кластер звичайних працівників
    ax.annotate(
        "9 звичайних працівників\n(від 25 до 45 тис. грн)",
        xy=(35, -0.15),
        xytext=(35, -0.58),
        fontsize=9,
        fontweight="bold",
        color="#1E40AF",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.1),
        arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.3)
    )

    # Лінія Медіани (вертикальний відрізок вгору від осі)
    ax.plot([median_val, median_val], [0, 0.8], color="#059669", linestyle="-", linewidth=2.4, zorder=4)
    ax.annotate(
        f"МЕДІАНА = {median_val:.0f} тис. грн\n✓ Типова зарплата\n(не реагує на CEO)",
        xy=(median_val, 0.45),
        xytext=(median_val - 12, 0.95),
        fontsize=9.5,
        fontweight="bold",
        color="#065F46",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor="#10B981", lw=1.3),
        arrowprops=dict(arrowstyle="->", color="#059669", lw=1.6)
    )

    # Лінія Середнього (вертикальний відрізок вгору від осі)
    ax.plot([mean_val, mean_val], [0, 0.8], color="#DC2626", linestyle="--", linewidth=2.4, zorder=4)
    ax.annotate(
        f"СЕРЕДНЄ = {mean_val:.1f} тис. грн\n✗ Спотворено викидом!\n(ніхто стільки не отримує)",
        xy=(mean_val, 0.35),
        xytext=(mean_val + 24, 0.95),
        fontsize=9.5,
        fontweight="bold",
        color="#991B1B",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF2F2", edgecolor="#EF4444", lw=1.3),
        arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.6)
    )

    # Стрілка спотворення
    ax.annotate(
        "Зсув +16.6 тис. грн (+49%) →",
        xy=(mean_val, 0.05),
        xytext=(mean_without + 3, 0.05),
        fontsize=8.5,
        fontweight="bold",
        color="#B91C1C"
    )

    # Підписи значень на осі
    for tick in [25, 35, 50, 75, 100, 150, 200]:
        ax.plot([tick, tick], [-0.04, 0.04], color="#64748B", lw=1.2)
        ax.text(tick, -0.15, str(tick), fontsize=9, ha="center", color="#475569")

    ax.set_title("Чому середнє оманливе: 9 співробітників + 1 директор (CEO)",
                 fontsize=13, fontweight="bold", color="#0F172A", pad=12)
    ax.set_xlim(12, 222)
    ax.set_ylim(-0.85, 1.45)
    ax.axis('off')

    plt.tight_layout()
    save_fig(fig, "statistics-basics/central-tendency", "02")


def generate_central_tendency_balance_beam():
    """
    03.png: Фізична аналогія — важіль / лінійка: Середнє як точка опори (центр ваги)
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6.6), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')

    fig.suptitle(
        "Аналогія «Центр ваги»: Чому аутлайер зміщує середнє на важелі",
        fontsize=14.5,
        fontweight="bold",
        color="#0F172A",
        y=0.98
    )

    weights1 = [25, 30, 30, 32, 35, 35, 35, 40, 45]

    # --------------------------------------------------------------------------
    # 1. Станція без викидів (збалансована група)
    # --------------------------------------------------------------------------
    ax1.set_facecolor('#FFFFFF')
    ax1.set_title("1. Без викиду: симетрична група — опора (середнє) знаходиться в центрі типових значень",
                  fontsize=11.5, fontweight="bold", color="#1E40AF", loc="left", pad=10)

    # Центрована лінійка
    ax1.plot([18, 52], [0, 0], color="#334155", lw=4.5, solid_capstyle='round')

    # Вантажі (квадрати на лінійці)
    for w in set(weights1):
        count = weights1.count(w)
        for c in range(count):
            rect = patches.Rectangle((w - 1.2, 0.05 + c * 0.18), 2.4, 0.15,
                                     facecolor="#3B82F6", edgecolor="#1D4ED8", lw=1.2, zorder=4)
            ax1.add_patch(rect)
            ax1.text(w, 0.12 + c * 0.18, f"{w}k", fontsize=7.5, ha="center", va="center", color="white", fontweight="bold")

    # Точка опори (Fulcrum - трикутник)
    fulcrum1 = 34.1
    triangle1 = patches.Polygon([[fulcrum1 - 1.6, -0.32], [fulcrum1 + 1.6, -0.32], [fulcrum1, -0.02]],
                                closed=True, facecolor="#059669", edgecolor="#047857", lw=1.5, zorder=5)
    ax1.add_patch(triangle1)

    ax1.annotate(
        f"Точка опори: Середнє = 34.1k ≈ Медіана = 35k\n(Ідеальний баланс у центрі натовпу!)",
        xy=(fulcrum1, -0.34),
        xytext=(fulcrum1, -0.72),
        fontsize=9.5,
        fontweight="bold",
        color="#065F46",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#ECFDF5", edgecolor="#10B981", lw=1.2),
        arrowprops=dict(arrowstyle="->", color="#059669", lw=1.4)
    )

    ax1.set_xlim(12, 58)
    ax1.set_ylim(-0.95, 0.85)
    ax1.axis('off')

    # --------------------------------------------------------------------------
    # 2. Станція з викидом 200k (величезний важіль)
    # --------------------------------------------------------------------------
    ax2.set_facecolor('#FFFFFF')
    ax2.set_title("2. З викидом (200k): велике плече сили змушує опору (середнє) зміститися далеко вправо",
                  fontsize=11.5, fontweight="bold", color="#B91C1C", loc="left", pad=10)

    # Довга планка
    ax2.plot([18, 208], [0, 0], color="#334155", lw=4.5, solid_capstyle='round')

    # Звичайні вантажі зліва
    for w in set(weights1):
        count = weights1.count(w)
        for c in range(count):
            rect = patches.Rectangle((w - 1.2, 0.05 + c * 0.18), 2.4, 0.15,
                                     facecolor="#3B82F6", edgecolor="#1D4ED8", lw=1.2, zorder=4)
            ax2.add_patch(rect)

    # Величезний вантаж (CEO 200k)
    rect_ceo = patches.Rectangle((195, 0.05), 10, 0.45,
                                 facecolor="#EF4444", edgecolor="#B91C1C", lw=1.8, zorder=5)
    ax2.add_patch(rect_ceo)
    ax2.text(200, 0.27, "CEO\n200k", fontsize=9, ha="center", va="center", color="white", fontweight="bold")

    # Медіана залишається на 35k
    ax2.plot([35, 35], [-0.15, 0.15], color="#059669", lw=2.2, linestyle="--", zorder=3)
    ax2.annotate(
        "Медіана = 35k\n(не рухається)",
        xy=(35, -0.16),
        xytext=(35, -0.68),
        fontsize=9,
        fontweight="bold",
        color="#065F46",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#ECFDF5", edgecolor="#10B981", lw=1),
        arrowprops=dict(arrowstyle="->", color="#059669", lw=1.3)
    )

    # Нова точка опори (зсунута на 50.7k)
    fulcrum2 = 50.7
    triangle2 = patches.Polygon([[fulcrum2 - 2.8, -0.32], [fulcrum2 + 2.8, -0.32], [fulcrum2, -0.02]],
                                closed=True, facecolor="#DC2626", edgecolor="#991B1B", lw=1.5, zorder=5)
    ax2.add_patch(triangle2)

    ax2.annotate(
        f"Нова точка опори: Середнє = 50.7k\n(змістилася на +16.6k праворуч, де немає людей!)",
        xy=(fulcrum2, -0.34),
        xytext=(fulcrum2 + 42, -0.68),
        fontsize=9.5,
        fontweight="bold",
        color="#991B1B",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#FEF2F2", edgecolor="#EF4444", lw=1.2),
        arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5)
    )

    ax2.set_xlim(12, 218)
    ax2.set_ylim(-0.95, 0.85)
    ax2.axis('off')

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    save_fig(fig, "statistics-basics/central-tendency", "03")


def generate_central_tendency_skewness_trio():
    """
    04.png: Тріо розподілів: Left-skewed, Symmetric, Right-skewed з Mode, Median, Mean
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.6), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')

    fig.suptitle(
        "Взаємне розташування Mean, Median та Mode при різних формах розподілу",
        fontsize=14,
        fontweight="bold",
        color="#0F172A",
        y=0.98
    )

    x = np.linspace(0, 10, 500)

    # 1. Лівостороння асиметрія (Left-skewed / Negative skew)
    ax1.set_facecolor('#FFFFFF')
    y1 = stats.beta.pdf(x / 10, 5, 2)
    ax1.plot(x, y1, color="#3B82F6", lw=2.4)
    ax1.fill_between(x, y1, color="#DBEAFE", alpha=0.5)

    mode1 = 8.0
    median1 = 7.3
    mean1 = 7.1

    ax1.axvline(mode1, color="#7C3AED", linestyle="-", lw=2, label="Mode (пік)")
    ax1.axvline(median1, color="#059669", linestyle="--", lw=2, label="Median (50%)")
    ax1.axvline(mean1, color="#DC2626", linestyle=":", lw=2.2, label="Mean (хвіст)")

    ax1.set_title("Лівостороння асиметрія\n(Left-skewed / Negative)", fontsize=11, fontweight="bold", color="#1E3A8A")
    ax1.text(5, -0.4, "Mean < Median < Mode", fontsize=10, fontweight="bold", color="#1E3A8A", ha="center",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1))
    ax1.annotate("Довгий лівий хвіст\nтягне середнє вліво ←", xy=(2.5, 0.4), xytext=(0.5, 1.2),
                 fontsize=8.5, color="#DC2626", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.2))
    ax1.set_ylim(-0.6, 3.2)
    ax1.axis('off')
    ax1.legend(loc="upper left", fontsize=8.5, framealpha=0.9)

    # 2. Симетричний розподіл (Symmetric / Normal)
    ax2.set_facecolor('#FFFFFF')
    y2 = stats.norm.pdf(x, loc=5, scale=1.5)
    ax2.plot(x, y2, color="#10B981", lw=2.4)
    ax2.fill_between(x, y2, color="#D1FAE5", alpha=0.5)

    center2 = 5.0
    ax2.axvline(center2, color="#0F172A", linestyle="-", lw=2.5, label="Mean = Median = Mode")

    ax2.set_title("Симетричний розподіл\n(Symmetric / Normal)", fontsize=11, fontweight="bold", color="#065F46")
    ax2.text(5, -0.06, "Mean ≈ Median ≈ Mode", fontsize=10, fontweight="bold", color="#065F46", ha="center",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#ECFDF5", edgecolor="#10B981", lw=1))
    ax2.annotate("Ідеальний баланс:\nвсі 3 міри збігаються", xy=(5, 0.28), xytext=(5, 0.35),
                 fontsize=8.5, color="#065F46", fontweight="bold", ha="center")
    ax2.set_ylim(-0.09, 0.42)
    ax2.axis('off')
    ax2.legend(loc="upper left", fontsize=8.5, framealpha=0.9)

    # 3. Правостороння асиметрія (Right-skewed / Positive skew)
    ax3.set_facecolor('#FFFFFF')
    y3 = stats.beta.pdf(x / 10, 2, 5)
    ax3.plot(x, y3, color="#F59E0B", lw=2.4)
    ax3.fill_between(x, y3, color="#FEF3C7", alpha=0.5)

    mode3 = 2.0
    median3 = 2.7
    mean3 = 2.9

    ax3.axvline(mode3, color="#7C3AED", linestyle="-", lw=2, label="Mode (пік)")
    ax3.axvline(median3, color="#059669", linestyle="--", lw=2, label="Median (50%)")
    ax3.axvline(mean3, color="#DC2626", linestyle=":", lw=2.2, label="Mean (хвіст)")

    ax3.set_title("Правостороння асиметрія\n(Right-skewed / Positive)", fontsize=11, fontweight="bold", color="#92400E")
    ax3.text(5, -0.4, "Mode < Median < Mean", fontsize=10, fontweight="bold", color="#92400E", ha="center",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFBEB", edgecolor="#F59E0B", lw=1))
    ax3.annotate("Довгий правий хвіст\nтягне середнє вправо →", xy=(7.5, 0.4), xytext=(5.5, 1.2),
                 fontsize=8.5, color="#DC2626", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.2))
    ax3.set_ylim(-0.6, 3.2)
    ax3.axis('off')
    ax3.legend(loc="upper right", fontsize=8.5, framealpha=0.9)

    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    save_fig(fig, "statistics-basics/central-tendency", "04")


def generate_central_tendency_housing_distribution():
    """
    05.png: Гістограма розподілу цін на 100 квартир (типове житло vs елітка)
    """
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    np.random.seed(123)
    regular_apartments = np.random.normal(1.5, 0.4, 90)
    elite_apartments = np.random.uniform(5, 10, 10)
    prices = np.concatenate([regular_apartments, elite_apartments])
    prices = np.clip(prices, 0.8, None)

    mean_price = prices.mean()
    median_price = np.median(prices)

    # Гістограма
    counts, bins, patches_list = ax.hist(prices, bins=25, edgecolor="black", alpha=0.75, lw=1.1)

    # Фарбуємо звичайні квартири в синій, елітні в червоний
    for p, bin_left in zip(patches_list, bins[:-1]):
        if bin_left < 4.0:
            p.set_facecolor("#60A5FA")
        else:
            p.set_facecolor("#F87171")

    # Медіана та Середнє
    ax.axvline(median_price, color="#059669", linestyle="-", linewidth=2.6,
               label=f"Медіана = {median_price:.2f} млн грн (типова ціна)")
    ax.axvline(mean_price, color="#DC2626", linestyle="--", linewidth=2.6,
               label=f"Середнє = {mean_price:.2f} млн грн (+47% завищення)")

    # Анотації
    ax.annotate(
        "85% квартир коштують до 2 млн грн\n(реальний вибір покупця)",
        xy=(1.5, 25),
        xytext=(2.6, 26),
        fontsize=9.5,
        fontweight="bold",
        color="#1E40AF",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.2),
        arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5)
    )

    ax.annotate(
        "10 елітних квартир (5-10 млн)\nстворюють довгий хвіст\nі тягнуть середнє вгору",
        xy=(7.2, 3),
        xytext=(6.0, 15),
        fontsize=9,
        fontweight="bold",
        color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF2F2", edgecolor="#EF4444", lw=1.2),
        arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5)
    )

    ax.set_title("Розподіл цін на 100 квартир у місті: Медіана vs Середнє", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Ціна квартири (млн грн)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Кількість квартир", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 33)
    ax.grid(alpha=0.3, linestyle="--")
    ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

    plt.tight_layout()
    save_fig(fig, "statistics-basics/central-tendency", "05")


# ==============================================================================
# 2.3. ВАРІАБЕЛЬНІСТЬ ТА РОЗСІЮВАННЯ ДАНИХ (03.variability.md)
# ==============================================================================

def generate_variability_shooters():
    """
    01.png: Два стрільці (Олексій vs Борис).
    Однакова середня відстань (8.0 см), але кардинально різна варіація та купчастість.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')

    fig.suptitle(
        "Порівняння стабільності двох стрільців: однакове середнє, але різна варіація",
        fontsize=14,
        fontweight="bold",
        color="#0F172A",
        y=0.98
    )

    oleksiy = np.array([8, 7, 9, 8, 8, 7, 9, 8, 8, 8])
    borys = np.array([2, 5, 15, 12, 3, 18, 1, 10, 4, 10])

    rng = np.random.RandomState(42)
    angles_o = rng.uniform(0, 2 * np.pi, len(oleksiy))
    angles_b = rng.uniform(0, 2 * np.pi, len(borys))

    x_o, y_o = oleksiy * np.cos(angles_o), oleksiy * np.sin(angles_o)
    x_b, y_b = borys * np.cos(angles_b), borys * np.sin(angles_b)

    def draw_target(ax, title, x_pts, y_pts, distances, dot_color, is_stable):
        ax.set_facecolor('#F8FAFC')
        max_r = 20
        # Кільця мішені
        for r in range(2, max_r + 1, 2):
            alpha = 0.08 if (r // 2) % 2 == 0 else 0.03
            circle = plt.Circle((0, 0), r, color='#64748B', fill=True, alpha=alpha)
            ax.add_patch(circle)
            edge_alpha = 0.4 if r in [4, 8, 12, 16, 20] else 0.15
            circle_edge = plt.Circle((0, 0), r, color='#64748B', fill=False, lw=1.0, alpha=edge_alpha)
            ax.add_patch(circle_edge)
            if r in [4, 8, 12, 16, 20]:
                ax.text(0.3, r - 0.7, f"{r} см", fontsize=7.5, color="#64748B", fontweight="medium")

        # Кільце середнього (8 см)
        mean_ring = plt.Circle((0, 0), 8, color='#EF4444', fill=False, lw=2.0, linestyle='--', zorder=4)
        ax.add_patch(mean_ring)

        # Центр
        ax.scatter(0, 0, s=80, color="#DC2626", marker='+', lw=2.5, zorder=6)
        ax.text(0, -1.5, "Центр", fontsize=8, ha="center", color="#DC2626", fontweight="bold")

        # Постріли
        ax.scatter(x_pts, y_pts, s=110, color=dot_color, edgecolor='#0F172A', linewidth=1.5, zorder=5, label='Постріли')

        ax.set_xlim(-22, 22)
        ax.set_ylim(-22, 22)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])

        mean_val = distances.mean()
        std_val = distances.std(ddof=0)
        range_val = distances.max() - distances.min()

        status_text = "[ВИСОКА СТАБІЛЬНІСТЬ]" if is_stable else "[НЕСТАБІЛЬНИЙ РОЗКИД]"
        status_color = "#065F46" if is_stable else "#991B1B"
        status_bg = "#ECFDF5" if is_stable else "#FEF2F2"
        status_border = "#10B981" if is_stable else "#EF4444"

        info_box = (
            f"{status_text}\n"
            f"Середнє (Mean): {mean_val:.1f} см\n"
            f"Розмах (Range): {range_val} см ({distances.min()}..{distances.max()} см)\n"
            f"Стандартне відхилення (σ): {std_val:.2f} см"
        )
        ax.text(
            0, -26.5, info_box,
            ha='center', va='top', fontsize=9.5, fontweight='bold',
            color=status_color,
            bbox=dict(boxstyle="round,pad=0.6", facecolor=status_bg, edgecolor=status_border, lw=1.5)
        )
        ax.set_title(title, fontsize=12, fontweight="bold", pad=10)

    draw_target(ax1, "Олексій: купчаста стрільба навколо 8 см", x_o, y_o, oleksiy, "#2563EB", True)
    draw_target(ax2, "Борис: великий розкид від 1 до 18 см", x_b, y_b, borys, "#EA580C", False)

    fig.subplots_adjust(bottom=0.25)
    save_fig(fig, "statistics-basics/variability", "01")


def generate_variability_geometric_variance():
    """
    02.png: Геометрична інтуїція дисперсії.
    Числова вісь із відхиленнями (x_i - mean) та буквальними квадратами площею (x_i - mean)^2.
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Дані: 4 точки із середнім 6.0
    pts = np.array([2, 5, 7, 10])
    mean_val = pts.mean()  # 6.0
    diffs = pts - mean_val  # [-4, -1, +1, +4]
    sq_diffs = diffs ** 2    # [16, 1, 1, 16]

    # Вісь X
    ax.axhline(0, color="#334155", lw=2, zorder=2)
    ax.set_xlim(0, 12)
    ax.set_ylim(-1.5, 6.5)

    # Вертикальна лінія середнього
    ax.axvline(mean_val, color="#DC2626", lw=2.2, linestyle="--", zorder=3)
    ax.text(mean_val, 5.8, f"Середнє $\\bar{{x}} = {mean_val:.0f}$",
            ha="center", fontsize=11, fontweight="bold", color="#DC2626",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF2F2", edgecolor="#DC2626", lw=1))

    colors = ["#3B82F6", "#06B6D4", "#10B981", "#8B5CF6"]

    # Квадрати відхилень
    for i, (p, d, sq, col) in enumerate(zip(pts, diffs, sq_diffs, colors)):
        side = abs(d)
        x_start = p if d < 0 else mean_val
        rect = patches.Rectangle(
            (x_start, 0), side, side,
            linewidth=1.8, edgecolor=col, facecolor=col, alpha=0.25, zorder=2
        )
        ax.add_patch(rect)

        # Центр квадрата для тексту площі
        center_x = x_start + side / 2.0
        center_y = side / 2.0
        label_text = f"Площа = {sq:.0f}\n$({p}-{mean_val:.0f})^2$"
        ax.text(center_x, center_y, label_text, ha="center", va="center",
                fontsize=8.5, fontweight="bold", color="#0F172A",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=col, lw=0.8, alpha=0.9))

        # Точка на осі
        ax.scatter(p, 0, s=140, color=col, edgecolor="#0F172A", lw=2, zorder=5)
        ax.text(p, -0.6, f"$x_{i+1} = {p}$", ha="center", fontsize=10, fontweight="bold", color="#1E293B")
        sign_str = f"{d:+.0f}"
        ax.text(p, -1.1, f"відхил: {sign_str}", ha="center", fontsize=8.5, color="#64748B")

    # Підсумкова формула та пояснення
    summary_text = (
        "Сума площ усіх 4 квадратів = $16 + 1 + 1 + 16 = 34$ кв. од.\n"
        "Дисперсія $\\sigma^2$ (середня площа квадрата) = $\\frac{34}{4} = 8.50$ кв. од.\n"
        "Стандартне відхилення $\\sigma$ (сторона умовного середнього квадрата) = $\\sqrt{8.50} \\approx 2.92$ од."
    )
    ax.text(
        6.0, 5.0, summary_text,
        ha="center", va="top", fontsize=9.5, fontweight="bold", color="#1E3A8A",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.4)
    )

    ax.set_title("Геометрична інтуїція дисперсії: Чому квадрат відхилення?", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(range(0, 13))
    ax.set_yticks([])
    ax.set_xlabel("Значення ознаки $X$", fontsize=10, fontweight="bold")
    ax.grid(axis='x', alpha=0.3, linestyle=":")

    plt.tight_layout()
    save_fig(fig, "statistics-basics/variability", "02")


def generate_variability_three_levels():
    """
    03.png: Три ступені варіації при однаковому середньому (~50).
    Низька (std=0.63), середня (std=3.02), висока (std=11.34).
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 7.5), dpi=200, sharex=True)
    fig.patch.set_facecolor('#FFFFFF')

    fig.suptitle(
        r"Три ступені варіації при однаковому середньому ($\mu \approx 50$)",
        fontsize=14,
        fontweight="bold",
        color="#0F172A",
        y=0.98
    )

    datasets = [
        {
            "name": "1. Низька варіація: висока передбачуваність, дані щільно згруповані",
            "data": np.array([50, 49, 51, 50, 50, 49, 51, 50, 50, 50]),
            "color": "#059669",
            "bg": "#ECFDF5",
            "ax": ax1
        },
        {
            "name": "2. Середня варіація: помірне розсіювання, нормальний робочий діапазон",
            "data": np.array([45, 48, 52, 47, 53, 46, 54, 48, 52, 50]),
            "color": "#2563EB",
            "bg": "#EFF6FF",
            "ax": ax2
        },
        {
            "name": "3. Висока варіація: велика невизначеність, дані сильно розкидані",
            "data": np.array([30, 40, 60, 35, 65, 45, 55, 50, 60, 55]),
            "color": "#DC2626",
            "bg": "#FEF2F2",
            "ax": ax3
        }
    ]

    x_grid = np.linspace(20, 80, 500)

    for item in datasets:
        ax = item["ax"]
        data = item["data"]
        col = item["color"]
        ax.set_facecolor('#FFFFFF')

        mean_val = data.mean()
        std_val = data.std(ddof=0)

        # Нормальна крива для ілюстрації щільності
        pdf = stats.norm.pdf(x_grid, mean_val, std_val)
        ax.plot(x_grid, pdf, color=col, lw=2.2, label="Щільність розподілу")
        ax.fill_between(x_grid, 0, pdf, color=col, alpha=0.15)

        # Інтервал mean +- 1 std
        std_mask = (x_grid >= mean_val - std_val) & (x_grid <= mean_val + std_val)
        ax.fill_between(x_grid[std_mask], 0, pdf[std_mask], color=col, alpha=0.35,
                        label=f"Інтервал $\\mu \\pm 1\\sigma$ [{mean_val-std_val:.1f}, {mean_val+std_val:.1f}]")

        # Вертикальна лінія середнього
        ax.axvline(mean_val, color="#0F172A", lw=1.8, linestyle="--", zorder=4)

        # Точки вибірки на осі y = 0
        y_pts = np.zeros_like(data) - 0.015 * pdf.max()
        ax.scatter(data, y_pts, s=60, color=col, edgecolor="#0F172A", lw=1.2, zorder=5, label="Точки даних")

        # Інформаційний бейдж
        info_str = f"Середнє $\\mu = {mean_val:.1f}$\nСтанд. відхилення $\\sigma = {std_val:.2f}$\nДіапазон: [{data.min()}, {data.max()}]"
        ax.text(
            77, pdf.max() * 0.7, info_str,
            ha="right", va="center", fontsize=9, fontweight="bold", color=col,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=item["bg"], edgecolor=col, lw=1.2)
        )

        ax.set_title(item["name"], fontsize=10.5, fontweight="bold", color="#1E293B", loc="left", pad=6)
        ax.set_ylim(-0.04 * pdf.max(), pdf.max() * 1.25)
        ax.set_yticks([])
        ax.grid(alpha=0.3, linestyle="--")
        ax.legend(loc="upper left", fontsize=8, framealpha=0.9)

    ax3.set_xlabel("Значення спостережень", fontsize=11, fontweight="bold")
    ax3.set_xticks(range(20, 85, 5))

    plt.tight_layout()
    save_fig(fig, "statistics-basics/variability", "03")


def generate_variability_quartiles():
    """
    04.png: Квартилі (Q1, Q2, Q3) та п'ятичисловий підсумок для 20 оцінок студентів.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6.2), dpi=200, gridspec_kw={'height_ratios': [1.8, 1]})
    fig.patch.set_facecolor('#FFFFFF')

    fig.suptitle(
        "Квартилі та 5-числовий підсумок: 4 чверті по 25% даних (20 студентів)",
        fontsize=14,
        fontweight="bold",
        color="#0F172A",
        y=0.98
    )

    grades = np.array([62, 65, 68, 70, 72, 74, 76, 78, 80, 82,
                       84, 85, 86, 88, 90, 91, 92, 94, 96, 98])

    q_min = grades.min()  # 62
    q1 = float(np.percentile(grades, 25))  # 73.5
    q2 = float(np.median(grades))  # 83.0
    q3 = float(np.percentile(grades, 75))  # 90.75
    q_max = grades.max()  # 98

    # 1. Верхній панель: точки даних та 4 кольорові зони
    ax1.set_facecolor('#FFFFFF')
    ax1.set_xlim(58, 102)
    ax1.set_ylim(-1.0, 3.2)

    zones = [
        (q_min, q1, "#3B82F6", f"1-ша чверть (25%)\nНижчі оцінки: {q_min:.0f}–{int(q1)}"),
        (q1, q2, "#059669", f"2-га чверть (25%)\nНижче медіани: {int(q1)+1}–{int(q2)}"),
        (q2, q3, "#F59E0B", f"3-тя чверть (25%)\nВище медіани: {int(q2)+1}–{int(q3)}"),
        (q3, q_max, "#8B5CF6", f"4-та чверть (25%)\nНайвищі оцінки: {int(q3)+1}–{q_max:.0f}"),
    ]

    for start, end, col, title in zones:
        ax1.axvspan(start, end, alpha=0.15, color=col)
        mid = (start + end) / 2.0
        ax1.text(mid, 2.5, title, ha="center", va="center", fontsize=8.5, fontweight="bold",
                 color=col, bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor=col, lw=1))

    # Точки оцінок
    y_dots = np.zeros_like(grades) + 0.9
    ax1.scatter(grades, y_dots, s=90, color="#1E293B", edgecolor="#FFFFFF", lw=1.5, zorder=5)

    # Підписи значень над точками
    for g in grades:
        ax1.text(g, 1.3, f"{g}", ha="center", fontsize=7.5, color="#475569", rotation=90)

    # Маркери 5-числового підсумку
    five_summary = [
        (q_min, f"Мінімум\n{q_min}", "#3B82F6"),
        (q1, f"Q1 (25%)\n{q1:.1f}", "#059669"),
        (q2, f"Q2 / Медіана\n{q2:.1f}", "#DC2626"),
        (q3, f"Q3 (75%)\n{q3:.1f}", "#F59E0B"),
        (q_max, f"Максимум\n{q_max}", "#8B5CF6"),
    ]

    for val, lbl, col in five_summary:
        ax1.axvline(val, color=col, lw=1.8, linestyle="--", zorder=4)
        ax1.text(val, -0.18, lbl, ha="center", va="top", fontsize=8.5, fontweight="bold", color=col,
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=col, lw=0.8))

    ax1.set_yticks([])
    ax1.set_xticks([])
    ax1.set_title("Розподіл індивідуальних оцінок за квартилями", fontsize=11, fontweight="bold", loc="left")

    # 2. Нижня панель: Box plot
    ax2.set_facecolor('#FFFFFF')
    ax2.set_xlim(58, 102)

    bp = ax2.boxplot(
        grades, vert=False, patch_artist=True,
        positions=[1], widths=0.5,
        boxprops=dict(facecolor="#DBEAFE", edgecolor="#1D4ED8", lw=2),
        medianprops=dict(color="#DC2626", lw=2.5),
        whiskerprops=dict(color="#1E3A8A", lw=1.8, linestyle="--"),
        capprops=dict(color="#1E3A8A", lw=2),
    )

    # Зв'язок IQR
    ax2.annotate(
        f"IQR = Q3 - Q1 = {q3 - q1:.1f} балів (центральні 50% даних)",
        xy=((q1 + q3) / 2, 1.35),
        ha="center", fontsize=9.5, fontweight="bold", color="#1D4ED8"
    )

    ax2.set_yticks([1])
    ax2.set_yticklabels(["Box Plot"], fontsize=10, fontweight="bold")
    ax2.set_xlabel("Бали студентів (за 100-бальною шкалою)", fontsize=11, fontweight="bold")
    ax2.grid(axis='x', alpha=0.3, linestyle="--")

    plt.tight_layout()
    save_fig(fig, "statistics-basics/variability", "04")


def generate_variability_range_vs_iqr():
    """
    05.png: Порівняння Range та IQR при появі аутлайера.
    Range змінюється на 800%, а IQR залишається незмінним (0% зміна).
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6.2), dpi=200, sharex=True)
    fig.patch.set_facecolor('#FFFFFF')

    fig.suptitle(
        "Стійкість до викидів: Розмах (Range) vs Міжквартильний розмах (IQR)",
        fontsize=14,
        fontweight="bold",
        color="#0F172A",
        y=0.98
    )

    data_clean = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    data_outlier = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 100])

    def plot_scenario(ax, data, title, is_outlier):
        ax.set_facecolor('#FFFFFF')
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        range_val = data.max() - data.min()

        # Підсвічування зони IQR
        ax.axvspan(q1, q3, color='#3B82F6', alpha=0.18, zorder=1)
        ax.text((q1 + q3) / 2, 0.45, f"IQR = {iqr:.1f}\n(центральні 50%)",
                ha="center", va="center", fontsize=9, fontweight="bold", color="#1D4ED8",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.2))

        # Стрілка Range
        ax.annotate(
            '', xy=(data.min(), 0.8), xytext=(data.max(), 0.8),
            arrowprops=dict(arrowstyle="<->", color="#DC2626" if is_outlier else "#059669", lw=2.2)
        )
        range_label = f"Range = {range_val:.0f} (збільшився на +800%!)" if is_outlier else f"Range = {range_val:.0f}"
        ax.text((data.min() + data.max()) / 2, 0.95, range_label,
                ha="center", fontsize=9.5, fontweight="bold", color="#DC2626" if is_outlier else "#059669")

        # Точки
        for val in data:
            if val == 100:
                ax.scatter(val, 0, s=180, color="#DC2626", edgecolor="#7F1D1D", lw=2, zorder=5, marker="X")
                ax.text(val, -0.3, "Аутлайер (100)", ha="center", fontsize=9, fontweight="bold", color="#DC2626")
            else:
                ax.scatter(val, 0, s=90, color="#2563EB", edgecolor="#1E293B", lw=1.2, zorder=4)

        ax.set_ylim(-0.5, 1.2)
        ax.set_yticks([])
        ax.set_title(title, fontsize=11.5, fontweight="bold", color="#1E293B", loc="left", pad=8)
        ax.grid(axis='x', alpha=0.3, linestyle="--")

    plot_scenario(ax1, data_clean, "1. Чисті дані (без викидів): [10 ... 20]", False)
    plot_scenario(ax2, data_outlier, "2. Дані з аутлайером: [10 ... 19, 100]", True)

    ax2.set_xlabel("Значення ознаки", fontsize=11, fontweight="bold")
    ax2.set_xlim(5, 105)
    ax2.set_xticks(range(10, 105, 10))

    # Висновок внизу
    fig.text(
        0.5, 0.02,
        "Висновок: IQR ігнорує крайні 25% з обох боків, тому на 100% захищений від екстремальних викидів (робастність).",
        ha="center", fontsize=10, fontweight="bold", color="#065F46",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor="#10B981", lw=1.2)
    )

    plt.subplots_adjust(bottom=0.15)
    save_fig(fig, "statistics-basics/variability", "05")


def generate_variability_tukey_boxplot():
    """
    06.png: Анатомія Box Plot та правило Тьюкі 1.5 IQR для виявлення аутлайерів.
    """
    fig, ax = plt.subplots(figsize=(12, 6.4), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Схема побудована на зарплатах із лекції
    q1 = 28.5
    median = 30.5
    q3 = 33.5
    iqr = q3 - q1  # 5.0
    lower_fence = q1 - 1.5 * iqr  # 21.0
    upper_fence = q3 + 1.5 * iqr  # 41.0
    whisker_low = 25.0
    whisker_high = 35.0

    ax.set_xlim(15, 65)
    ax.set_ylim(-1.5, 3.5)

    # 1. Зона нормальних значень
    ax.axvspan(lower_fence, upper_fence, color="#ECFDF5", alpha=0.6, zorder=1)
    ax.text((lower_fence + upper_fence) / 2, 3.0, "Зона типових значень (в межах парканів)",
            ha="center", fontsize=10, fontweight="bold", color="#047857")

    # Зона аутлайерів справа
    ax.axvspan(upper_fence, 65, color="#FEF2F2", alpha=0.6, zorder=1)
    ax.text(53, 3.0, "Зона аутлайерів\n($X > Q3 + 1.5\\times\\text{IQR}$)",
            ha="center", fontsize=9.5, fontweight="bold", color="#B91C1C")

    # 2. Паркани (Fences)
    ax.axvline(lower_fence, color="#DC2626", lw=1.8, linestyle=":", zorder=3)
    ax.text(lower_fence, -0.9, f"Нижній паркан\n$Q1 - 1.5\\times\\text{{IQR}}$\n= {lower_fence:.1f}",
            ha="center", fontsize=8.5, fontweight="bold", color="#B91C1C")

    ax.axvline(upper_fence, color="#DC2626", lw=1.8, linestyle=":", zorder=3)
    ax.text(upper_fence, -0.9, f"Верхній паркан\n$Q3 + 1.5\\times\\text{{IQR}}$\n= {upper_fence:.1f}",
            ha="center", fontsize=8.5, fontweight="bold", color="#B91C1C")

    # 3. Коробка (Box: Q1 to Q3)
    box_rect = patches.Rectangle(
        (q1, 0.5), iqr, 1.0,
        linewidth=2.2, edgecolor="#1D4ED8", facecolor="#DBEAFE", zorder=4
    )
    ax.add_patch(box_rect)

    # Медіана всередині коробки
    ax.plot([median, median], [0.5, 1.5], color="#DC2626", lw=3.0, zorder=5)

    # 4. Вуса (Whiskers)
    ax.plot([whisker_low, q1], [1.0, 1.0], color="#1E3A8A", lw=2, linestyle="-", zorder=3)
    ax.plot([q3, whisker_high], [1.0, 1.0], color="#1E3A8A", lw=2, linestyle="-", zorder=3)

    # Засічки на вусах
    ax.plot([whisker_low, whisker_low], [0.8, 1.2], color="#1E3A8A", lw=2, zorder=3)
    ax.plot([whisker_high, whisker_high], [0.8, 1.2], color="#1E3A8A", lw=2, zorder=3)

    # 5. Стрілки 1.5 x IQR
    ax.annotate('', xy=(lower_fence, 2.1), xytext=(q1, 2.1),
                arrowprops=dict(arrowstyle="<->", color="#DC2626", lw=1.6))
    ax.text((lower_fence + q1) / 2, 2.3, "$1.5 \\times \\text{IQR}$\n(7.5)", ha="center", fontsize=8, color="#DC2626", fontweight="bold")

    ax.annotate('', xy=(q3, 2.1), xytext=(upper_fence, 2.1),
                arrowprops=dict(arrowstyle="<->", color="#DC2626", lw=1.6))
    ax.text((q3 + upper_fence) / 2, 2.3, "$1.5 \\times \\text{IQR}$\n(7.5)", ha="center", fontsize=8, color="#DC2626", fontweight="bold")

    # Стрілка для IQR
    ax.annotate('', xy=(q1, 0.2), xytext=(q3, 0.2),
                arrowprops=dict(arrowstyle="<->", color="#1D4ED8", lw=2.0))
    ax.text((q1 + q3) / 2, -0.15, f"Міжквартильний розмах (IQR = {iqr:.1f})", ha="center", fontsize=9, fontweight="bold", color="#1D4ED8")

    # 6. Аутлайер (винесено умовну стрілку на 200)
    ax.scatter(58, 1.0, s=160, color="#DC2626", edgecolor="#7F1D1D", lw=2, marker="X", zorder=6)
    ax.annotate(
        "Аутлайер: 200 тис. грн\n(значно правіше 41.0)",
        xy=(58, 1.15),
        xytext=(52, 1.9),
        fontsize=9, fontweight="bold", color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#FEE2E2", edgecolor="#DC2626", lw=1.2),
        arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5)
    )

    # Підписи компонентів (рознесені за висотою, щоб уникнути накладання)
    ax.text(whisker_low, 1.35, f"Мін: {whisker_low:.0f}", ha="center", fontsize=8.5, color="#1E3A8A", fontweight="bold")
    ax.text(q1, 1.85, f"Q1 (25%)\n{q1:.1f}", ha="center", fontsize=8.5, color="#1D4ED8", fontweight="bold")
    ax.text(median, 1.60, f"Медіана\n{median:.1f}", ha="center", fontsize=8.5, color="#DC2626", fontweight="bold")
    ax.text(q3, 1.85, f"Q3 (75%)\n{q3:.1f}", ha="center", fontsize=8.5, color="#1D4ED8", fontweight="bold")
    ax.text(whisker_high, 1.35, f"Макс: {whisker_high:.0f}", ha="center", fontsize=8.5, color="#1E3A8A", fontweight="bold")

    ax.set_title("Анатомія Box Plot та правило Тьюкі $1.5 \\times \\text{IQR}$", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Зарплата (тис. грн)", fontsize=11, fontweight="bold")
    ax.set_yticks([])
    ax.set_xticks(range(15, 66, 5))
    ax.grid(axis='x', alpha=0.3, linestyle="--")

    plt.tight_layout()
    save_fig(fig, "statistics-basics/variability", "06")


# ==============================================================================
# 3. АВТОМАТИЧНА ГЕНЕРАЦІЯ З КОДІВ ЛЕКЦІЙ
# ==============================================================================
def run_all_extracted_plots():
    files_map = [
        ('content/16.ai-python/04.statistics-basics/01.random-variables.md', 'statistics-basics/random-variables', 2),
        ('content/16.ai-python/04.statistics-basics/02.central-tendency.md', 'statistics-basics/central-tendency', 1),
        ('content/16.ai-python/04.statistics-basics/04.distributions.md', 'statistics-basics/distributions', 1),
        ('content/16.ai-python/04.statistics-basics/05.correlation.md', 'statistics-basics/correlation', 1),
        ('content/16.ai-python/04.statistics-basics/06.outliers.md', 'statistics-basics/outliers', 1),
        ('content/16.ai-python/07.linear-regression-theory/05.practice.md', 'linear-regression-theory', 'practice-gd')
    ]

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for rel_path, out_sub, start_num in files_map:
        full_path = os.path.join(root_dir, rel_path)
        print(f"\nProcessing {rel_path}...")
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        in_code = False
        cur_code = []
        env = {'__name__': '__main__'}
        plot_num = start_num

        for line in lines:
            if line.startswith('```python'):
                in_code = True
                cur_code = []
            elif line.startswith('```') and in_code:
                in_code = False
                code_text = ''.join(cur_code)
                if 'plt.show()' in code_text:
                    if isinstance(plot_num, int):
                        name = f"{plot_num:02d}"
                        plot_num += 1
                    else:
                        name = f"{plot_num}"

                    env_cell = dict(env)
                    env_cell['plt'] = plt

                    def show_hook():
                        fig = plt.gcf()
                        save_fig(fig, out_sub, name)

                    plt.show = show_hook
                    try:
                        exec(code_text, env_cell)
                        env.update(env_cell)
                    except Exception as e:
                        print(f"ERROR generating {out_sub}/{name}: {e}", file=sys.stderr)
                else:
                    try:
                        exec(code_text, env)
                    except Exception:
                        pass
            elif in_code:
                cur_code.append(line)


if __name__ == "__main__":
    print("Step 1: Generating conceptual diagrams...")
    generate_random_variables_analogy()
    generate_central_tendency_salaries_outlier()
    generate_central_tendency_balance_beam()
    generate_central_tendency_skewness_trio()
    generate_central_tendency_housing_distribution()
    generate_variability_shooters()
    generate_variability_geometric_variance()
    generate_variability_three_levels()
    generate_variability_quartiles()
    generate_variability_range_vs_iqr()
    generate_variability_tukey_boxplot()

    print("\nStep 2: Generating all lecture code plots...")
    run_all_extracted_plots()
    print("\nAll images successfully generated!")

