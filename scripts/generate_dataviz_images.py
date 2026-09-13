#!/usr/bin/env python3
"""
Скрипт для генерації всіх графіків та візуалізацій для модуля 16.ai-python/05.data-visualization.
Зберігає зображення у public/images/ai-python/data-visualization/<section>/<number>.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec

# Налаштування стилю та шрифтів для коректного відображення кирилиці
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = False

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "images", "ai-python", "data-visualization")

def save_fig(fig, section, name, dpi=160):
    folder = os.path.join(BASE_DIR, section)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{name}.png")
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Generated: {filepath}")

# ==========================================
# 0. INDEX
# ==========================================
def generate_index():
    print("Generating index images...")
    # 01.png: Порівняння таблиці та графіка
    np.random.seed(42)
    hours = np.arange(1000)
    temperature = 20 + 5 * np.sin(hours * 2 * np.pi / 24) + np.random.normal(0, 1, 1000)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    ax1.text(0.05, 0.5, f"Дані:\n{temperature[:100].round(1).tolist()[:20]}...", 
             fontsize=9, wrap=True, family="monospace", va="center")
    ax1.set_title("Таблиця з числами (перші 100 значень)", fontsize=12, fontweight="bold")
    ax1.axis("off")

    ax2.plot(hours[:240], temperature[:240], color="#2563eb", linewidth=1.2, alpha=0.85)
    ax2.set_title("Графік (перші 10 днів — одразу видно добовий патерн!)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Години", fontsize=10)
    ax2.set_ylabel("Температура (°C)", fontsize=10)
    ax2.grid(alpha=0.3, linestyle="--")

    plt.tight_layout()
    save_fig(fig, "index", "01")


# ==========================================
# 1. MATPLOTLIB BASICS
# ==========================================
def generate_basics():
    print("Generating matplotlib-basics images...")
    
    # 01.png: Анатомія matplotlib
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y, label="sin(x)", color="#2563eb", linewidth=2.5)
    ax.set_title("Структура matplotlib (Анатомія об'єктів)", fontsize=15, fontweight="bold")
    ax.set_xlabel("Вісь X (незалежна змінна)", fontsize=11)
    ax.set_ylabel("Вісь Y (залежна змінна)", fontsize=11)
    ax.legend(loc="upper right", framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle="--")

    ax.annotate("Title (заголовок)", xy=(5, 0.8), xytext=(6.5, 0.9),
                fontsize=10, color="crimson", weight="bold",
                arrowprops=dict(arrowstyle="->", color="crimson", lw=1.5))
    ax.annotate("Legend\n(легенда)", xy=(9.5, 0.9), xytext=(7.8, 0.6),
                fontsize=10, color="forestgreen", weight="bold",
                arrowprops=dict(arrowstyle="->", color="forestgreen", lw=1.5))
    ax.annotate("Plot\n(графік)", xy=(3, 0.1), xytext=(1.2, -0.5),
                fontsize=10, color="indigo", weight="bold",
                arrowprops=dict(arrowstyle="->", color="indigo", lw=1.5))
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "01")

    # 02.png: Підхід 1 pyplot
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x = np.linspace(-5, 5, 100)
    y = x ** 2
    ax.plot(x, y, color="#0284c7", linewidth=2)
    ax.set_title("Парабола y = x² (Підхід pyplot)", fontsize=13, fontweight="bold")
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("y", fontsize=11)
    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "02")

    # 03.png: Підхід 2 OOP API
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x = np.linspace(-5, 5, 100)
    y = x ** 2
    ax.plot(x, y, color="purple", linewidth=2.5)
    ax.set_title("Парабола y = x² (Підхід OOP API)", fontsize=13, fontweight="bold")
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("y", fontsize=11)
    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "03")

    # 04.png: Порівняння pyplot та OOP
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    x = np.linspace(0, 2 * np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    ax1.plot(x, y1, label="sin(x)", color="#2563eb", linewidth=2)
    ax1.plot(x, y2, label="cos(x)", color="#dc2626", linewidth=2)
    ax1.set_title("Підхід pyplot", fontsize=12, fontweight="bold")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(x, y1, label="sin(x)", color="#2563eb", linewidth=2)
    ax2.plot(x, y2, label="cos(x)", color="#dc2626", linewidth=2)
    ax2.set_title("Підхід OOP API", fontsize=12, fontweight="bold")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "04")

    # 05.png: Температура протягом тижня
    days = np.arange(1, 8)
    temperature = [18, 22, 25, 23, 20, 19, 21]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(days, temperature, marker="o", linestyle="-", color="orangered", 
            linewidth=2.5, markersize=8, label="Температура")
    ax.set_title("Температура протягом тижня", fontsize=14, fontweight="bold")
    ax.set_xlabel("День тижня", fontsize=11)
    ax.set_ylabel("Температура (°C)", fontsize=11)
    ax.set_xticks(days)
    ax.set_xticklabels(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"])
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "05")

    # 06.png: Динаміка продажів трьох продуктів
    months = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер"]
    product_a = [120, 150, 180, 170, 200, 220]
    product_b = [80, 95, 110, 105, 130, 140]
    product_c = [200, 190, 185, 180, 175, 170]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(months, product_a, marker="o", label="Продукт A", linewidth=2.2, color="#3b82f6")
    ax.plot(months, product_b, marker="s", label="Продукт B", linewidth=2.2, color="#10b981")
    ax.plot(months, product_c, marker="^", label="Продукт C", linewidth=2.2, color="#f59e0b")
    ax.set_title("Динаміка продажів за півроку", fontsize=14, fontweight="bold")
    ax.set_xlabel("Місяць", fontsize=11)
    ax.set_ylabel("Обсяг продажів (тис. грн)", fontsize=11)
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "06")

    # 07.png: Графік з кастомними заголовками
    x = np.linspace(0, 10, 100)
    y = np.exp(-x/5) * np.sin(2*x)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x, y, color="darkblue", linewidth=2.5)
    ax.set_title("Загасаюча синусоїда", fontsize=15, fontweight="bold", color="darkred", pad=15)
    ax.set_xlabel("Час (секунди)", fontsize=12, fontstyle="italic")
    ax.set_ylabel("Амплітуда", fontsize=12, fontstyle="italic")
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)
    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "07")

    # 08.png: Три варіанти сітки
    x = np.linspace(0, 4 * np.pi, 100)
    y = np.sin(x)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4))
    ax1.plot(x, y, color="#2563eb", linewidth=2)
    ax1.set_title("Без сітки", fontweight="bold")

    ax2.plot(x, y, color="#2563eb", linewidth=2)
    ax2.grid(True)
    ax2.set_title("Сітка за замовчуванням", fontweight="bold")

    ax3.plot(x, y, color="#2563eb", linewidth=2)
    ax3.grid(True, alpha=0.3, linestyle="--", linewidth=1.2, color="gray")
    ax3.set_title("Кастомна сітка", fontweight="bold")
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "08")

    # 09.png: Графік з легендою
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x, np.sin(x), label="sin(x)", linewidth=2, color="#2563eb")
    ax.plot(x, np.cos(x), label="cos(x)", linewidth=2, color="#dc2626")
    ax.plot(x, np.sin(x) * np.cos(x), label="sin(x)·cos(x)", linewidth=2, linestyle="--", color="#059669")
    ax.set_title("Тригонометричні функції", fontsize=14, fontweight="bold")
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("y", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=10, frameon=True, shadow=True, fancybox=True)
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "09")

    # 10.png: Різні способи задання кольорів
    x = np.linspace(0, 5, 50)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x, x + 0, color="red", label="Назва кольору: 'red'", linewidth=2)
    ax.plot(x, x + 1, color="r", label="Короткий код: 'r'", linewidth=2)
    ax.plot(x, x + 2, color="#FF6B35", label="HEX: '#FF6B35'", linewidth=2)
    ax.plot(x, x + 3, color=(0.2, 0.4, 0.8), label="RGB tuple: (0.2, 0.4, 0.8)", linewidth=2)
    ax.plot(x, x + 4, color="C4", label="Колір з палітри: 'C4'", linewidth=2)
    ax.set_title("Способи задання кольорів", fontsize=14, fontweight="bold")
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("y", fontsize=11)
    ax.legend(loc="upper left", fontsize=9.5)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "10")

    # 11.png: Порівняння розмірів фігур
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
    ax1.plot(x, y, color="#2563eb")
    ax1.set_title("4x3 дюйми (замала)", fontsize=10, fontweight="bold")
    ax1.set_xlabel("x", fontsize=8)
    ax1.set_ylabel("y", fontsize=8)

    ax2.plot(x, y, color="#059669")
    ax2.set_title("8x6 дюймів (оптимально)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("x", fontsize=10)
    ax2.set_ylabel("y", fontsize=10)

    ax3.plot(x, y, color="#d97706")
    ax3.set_title("12x9 дюймів (презентація)", fontsize=14, fontweight="bold")
    ax3.set_xlabel("x", fontsize=12)
    ax3.set_ylabel("y", fontsize=12)
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "11")

    # 12.png: Синусоїда для звіту (savefig)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, y, linewidth=2.5, color="#2563eb")
    ax.set_title("Синусоїда для звіту (savefig demo)", fontsize=13, fontweight="bold")
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("sin(x)", fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "matplotlib-basics", "12")


# ==========================================
# 2. DISTRIBUTIONS
# ==========================================
def generate_distributions():
    print("Generating distributions images...")
    np.random.seed(42)

    # 01.png: Порівняння: таблиця vs гістограма
    heights = np.random.normal(loc=170, scale=10, size=500)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.text(0.05, 0.5, f"Перші 50 значень:\n{heights[:50].round(1)}", 
             fontsize=8, family="monospace", verticalalignment="center")
    ax1.set_title("Дані у вигляді чисел\n(неможливо зрозуміти структуру)", 
                  fontsize=12, fontweight="bold")
    ax1.axis("off")

    ax2.hist(heights, bins=30, color="steelblue", edgecolor="black", alpha=0.75)
    ax2.axvline(heights.mean(), color="red", linestyle="--", linewidth=2, 
                label=f"Середнє: {heights.mean():.1f} см")
    ax2.axvline(np.median(heights), color="green", linestyle="--", linewidth=2,
                label=f"Медіана: {np.median(heights):.1f} см")
    ax2.set_title("Гістограма розподілу зросту\n(структура видна одразу)", 
                  fontsize=12, fontweight="bold")
    ax2.set_xlabel("Зріст (см)", fontsize=11)
    ax2.set_ylabel("Кількість пацієнтів", fontsize=11)
    ax2.legend()
    ax2.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "01")

    # 02.png: Гістограма балів на іспиті
    np.random.seed(123)
    scores = np.random.normal(loc=70, scale=15, size=200)
    scores = np.clip(scores, 0, 100)
    fig, ax = plt.subplots(figsize=(9, 5))
    counts, bins, patches = ax.hist(scores, bins=20, color="coral", 
                                     edgecolor="black", alpha=0.75)
    ax.set_title("Розподіл балів на іспиті (200 студентів)", 
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Бали (0–100)", fontsize=11)
    ax.set_ylabel("Кількість студентів", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "02")

    # 03.png: Анатомія гістограми з анотаціями
    np.random.seed(42)
    data = np.random.normal(50, 10, 300)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    counts, bins, patches = ax.hist(data, bins=15, color="skyblue", 
                                     edgecolor="navy", alpha=0.75, linewidth=1.5)
    ax.set_title("Анатомія гістограми", fontsize=14, fontweight="bold")
    ax.set_xlabel("Значення змінної", fontsize=11)
    ax.set_ylabel("Частота (кількість спостережень)", fontsize=11)

    ax.annotate("Bin (інтервал):\nусі значення 40–45\nпотрапляють у цей стовпець", 
                xy=(42.5, counts[5]), xytext=(22, counts.max()*0.8),
                fontsize=9.5, color="darkred", weight="bold",
                arrowprops=dict(arrowstyle="->", color="darkred", lw=2),
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#fef08a", alpha=0.9))

    ax.annotate("Висота стовпця =\nкількість значень\nу цьому інтервалі", 
                xy=(55, counts[9]), xytext=(68, counts.max()*0.65),
                fontsize=9.5, color="darkblue", weight="bold",
                arrowprops=dict(arrowstyle="->", color="darkblue", lw=2),
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#bfdbfe", alpha=0.9))
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "03")

    # 04.png: Порівняння різної кількості bins
    np.random.seed(42)
    data_exp = np.random.exponential(scale=2, size=500)
    fig, axes = plt.subplots(2, 3, figsize=(14, 7.5))
    fig.suptitle("Той самий датасет з різною кількістю bins", fontsize=14, fontweight="bold")
    bin_counts = [5, 10, 20, 30, 50, 100]
    for ax, b in zip(axes.flat, bin_counts):
        ax.hist(data_exp, bins=b, color="#3b82f6", edgecolor="black", alpha=0.7)
        ax.set_title(f"bins = {b}", fontweight="bold", fontsize=11)
        ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "04")

    # 05.png: Автоматичні методи вибору bins
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Автоматичні алгоритми вибору bins у matplotlib", fontsize=14, fontweight="bold")
    methods = [("sturges", "Правило Стерджеса (sturges)"), 
               ("scott", "Правило Скотта (scott)"), 
               ("fd", "Правило Фрідмана-Діакона (fd)"), 
               ("auto", "Автоматичний вибір (auto — рекомендовано)")]
    for ax, (m, label) in zip(axes.flat, methods):
        counts, b, _ = ax.hist(data_exp, bins=m, color="#10b981", edgecolor="black", alpha=0.7)
        ax.set_title(f"{label} [отримано {len(b)-1} bins]", fontsize=10.5, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "05")

    # 06.png: Типові форми розподілів
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle("Типові форми розподілів та їх значення", fontsize=15, fontweight="bold")

    data_normal = np.random.normal(50, 10, 1000)
    axes[0, 0].hist(data_normal, bins=30, color="steelblue", edgecolor="black", alpha=0.7)
    axes[0, 0].set_title("Нормальний (Gaussian)\nЗріст людей, IQ, помилки вимірювань", fontsize=10, fontweight="bold")
    axes[0, 0].axvline(np.mean(data_normal), color="red", linestyle="--", label="Середнє")
    axes[0, 0].legend()

    data_right_skew = np.random.exponential(2, 1000)
    axes[0, 1].hist(data_right_skew, bins=30, color="coral", edgecolor="black", alpha=0.7)
    axes[0, 1].set_title("Правий перекіс (Right-skewed)\nДоходи населення, ціни нерухомості", fontsize=10, fontweight="bold")
    axes[0, 1].axvline(np.median(data_right_skew), color="green", linestyle="--", label="Медіана")
    axes[0, 1].legend()

    data_left_skew = 100 - np.random.exponential(2, 1000)
    axes[0, 2].hist(data_left_skew, bins=30, color="gold", edgecolor="black", alpha=0.7)
    axes[0, 2].set_title("Лівий перекіс (Left-skewed)\nВік виходу на пенсію, тривалість життя", fontsize=10, fontweight="bold")
    axes[0, 2].axvline(np.median(data_left_skew), color="green", linestyle="--", label="Медіана")
    axes[0, 2].legend()

    data_uniform = np.random.uniform(0, 100, 1000)
    axes[1, 0].hist(data_uniform, bins=30, color="mediumpurple", edgecolor="black", alpha=0.7)
    axes[1, 0].set_title("Рівномірний (Uniform)\nКидок грального кубика, випадкові числа", fontsize=10, fontweight="bold")

    data_bimodal = np.concatenate([np.random.normal(30, 5, 500), np.random.normal(70, 8, 500)])
    axes[1, 1].hist(data_bimodal, bins=30, color="teal", edgecolor="black", alpha=0.7)
    axes[1, 1].set_title("Бімодальний (дві вершини)\nДві змішані популяції (напр. чоловіки/жінки)", fontsize=10, fontweight="bold")

    data_exp2 = np.random.exponential(1, 1000)
    axes[1, 2].hist(data_exp2, bins=30, color="salmon", edgecolor="black", alpha=0.7)
    axes[1, 2].set_title("Експоненційний (Exponential)\nЧас між дзвінками, термін служби ламп", fontsize=10, fontweight="bold")

    for ax in axes.flat:
        ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "06")

    # 07.png: Детальна анатомія box plot
    np.random.seed(42)
    data_bp = np.random.normal(100, 15, 100)
    data_bp = np.append(data_bp, [150, 155, 45, 40])
    fig, ax = plt.subplots(figsize=(8, 9))
    bp = ax.boxplot(data_bp, vert=True, patch_artist=True, widths=0.45,
                    boxprops=dict(facecolor="#bfdbfe", edgecolor="navy", linewidth=2),
                    medianprops=dict(color="red", linewidth=3),
                    whiskerprops=dict(color="navy", linewidth=2),
                    capprops=dict(color="navy", linewidth=2),
                    flierprops=dict(marker="o", markerfacecolor="red", markersize=8, markeredgecolor="darkred"))

    q1, median, q3 = np.percentile(data_bp, [25, 50, 75])
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    ax.annotate("Викиди (outliers)\nзначення > Q3 + 1.5·IQR", xy=(1, 150), xytext=(1.35, 150),
                fontsize=9.5, color="darkred", weight="bold",
                arrowprops=dict(arrowstyle="->", color="darkred", lw=1.8))
    ax.annotate(f"Максимум (без викидів)\n≈ {upper_fence:.1f}", xy=(1, upper_fence), xytext=(1.35, upper_fence+3),
                fontsize=9.5, color="navy", weight="bold",
                arrowprops=dict(arrowstyle="->", color="navy"))
    ax.annotate(f"Q3 (75% даних нижче)\n≈ {q3:.1f}", xy=(1, q3), xytext=(1.35, q3),
                fontsize=9.5, color="darkblue", weight="bold",
                arrowprops=dict(arrowstyle="->", color="darkblue"))
    ax.annotate(f"Медіана (Q2, 50%)\n≈ {median:.1f}", xy=(1, median), xytext=(0.35, median+8),
                fontsize=10.5, color="red", weight="bold",
                arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.annotate(f"Q1 (25% даних нижче)\n≈ {q1:.1f}", xy=(1, q1), xytext=(1.35, q1-5),
                fontsize=9.5, color="darkblue", weight="bold",
                arrowprops=dict(arrowstyle="->", color="darkblue"))
    ax.annotate(f"Мінімум (без викидів)\n≈ {lower_fence:.1f}", xy=(1, lower_fence), xytext=(1.35, lower_fence-8),
                fontsize=9.5, color="navy", weight="bold",
                arrowprops=dict(arrowstyle="->", color="navy"))
    ax.annotate(f"IQR = Q3 - Q1\n= {iqr:.1f}", xy=(1.12, (q1+q3)/2), xytext=(0.4, (q1+q3)/2-12),
                fontsize=10, color="darkgreen", weight="bold",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#bbf7d0", alpha=0.85))

    ax.set_title("Анатомія Box Plot", fontsize=14, fontweight="bold")
    ax.set_ylabel("Значення", fontsize=11)
    ax.set_xlim(0.3, 1.9)
    ax.set_xticks([])
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "07")

    # 08.png: Порівняння трьох груп
    group_a = np.random.normal(75, 10, 80)
    group_b = np.random.normal(85, 7, 80)
    group_c = np.random.normal(65, 15, 80)
    data_groups = [group_a, group_b, group_c]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bp = ax.boxplot(data_groups, tick_labels=["Група A", "Група B", "Група C"],
                    patch_artist=True, notch=True, showmeans=True,
                    boxprops=dict(facecolor="skyblue", edgecolor="navy", linewidth=1.5),
                    medianprops=dict(color="red", linewidth=2),
                    meanprops=dict(marker="D", markerfacecolor="green", markersize=8),
                    whiskerprops=dict(linestyle="--", linewidth=1.5),
                    flierprops=dict(marker="o", markerfacecolor="orange", markersize=6, alpha=0.5))
    ax.set_title("Порівняння балів трьох груп студентів", fontsize=14, fontweight="bold")
    ax.set_ylabel("Бали (0–100)", fontsize=11)
    ax.set_xlabel("Група", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    custom_lines = [Line2D([0], [0], color="red", linewidth=2),
                    Line2D([0], [0], marker="D", color="w", markerfacecolor="green", markersize=8)]
    ax.legend(custom_lines, ["Медіана", "Середнє"], loc="lower right")
    plt.tight_layout()
    save_fig(fig, "distributions", "08")

    # 09.png: Параметри boxplot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.boxplot([group_a, group_b], tick_labels=["Стандартний", "З виїмкою (notch)"],
                patch_artist=True, notch=True,
                boxprops=dict(facecolor="#fef08a", edgecolor="#854d0e"))
    ax1.set_title("Параметр notch=True (довірчий інтервал)", fontweight="bold")
    ax1.grid(axis="y", alpha=0.3)

    ax2.boxplot([group_a, group_b], tick_labels=["A", "B"], vert=False, patch_artist=True,
                boxprops=dict(facecolor="#fed7aa", edgecolor="#9a3412"))
    ax2.set_title("Параметр vert=False (горизонтальний)", fontweight="bold")
    ax2.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "09")

    # 10.png: Горизонтальні box plots
    cities = ["Київ", "Львів", "Одеса", "Харків", "Дніпро", "Запоріжжя"]
    salaries = [np.random.normal(800, 150, 100),
                np.random.normal(650, 120, 100),
                np.random.normal(700, 140, 100),
                np.random.normal(720, 130, 100),
                np.random.normal(680, 110, 100),
                np.random.normal(640, 100, 100)]
    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(salaries, tick_labels=cities, vert=False, patch_artist=True,
                    boxprops=dict(facecolor="lightcoral", alpha=0.75),
                    medianprops=dict(color="darkred", linewidth=2))
    ax.set_title("Розподіл зарплат у містах України", fontsize=14, fontweight="bold")
    ax.set_xlabel("Зарплата (USD)", fontsize=11)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "10")

    # 11.png: Комбінована візуалізація
    data_gamma = np.random.gamma(2, 2, 500)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                                    gridspec_kw={'height_ratios': [3, 1]})
    ax1.hist(data_gamma, bins=30, color="mediumseagreen", edgecolor="black", alpha=0.75)
    ax1.set_title("Розподіл часу відповіді сервера (мс)", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Частота", fontsize=11)
    ax1.grid(axis="y", alpha=0.3)

    ax2.boxplot(data_gamma, vert=False, patch_artist=True,
                boxprops=dict(facecolor="lightgreen", edgecolor="darkgreen"),
                medianprops=dict(color="red", linewidth=2),
                flierprops=dict(marker="o", markerfacecolor="red", markersize=5, alpha=0.6))
    ax2.set_xlabel("Час відповіді (мс)", fontsize=11)
    ax2.set_yticks([])
    ax2.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "distributions", "11")


# ==========================================
# 3. RELATIONSHIPS
# ==========================================
def generate_relationships():
    print("Generating relationships images...")
    np.random.seed(42)

    # 01.png: Scatter plot площа vs ціна
    area = np.random.uniform(30, 150, 100)
    price = 500 * area + np.random.normal(0, 8000, 100) + 15000
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.scatter(area, price, color="#3b82f6", alpha=0.7, edgecolors="black", s=60)
    ax.set_title("Залежність ціни квартири від площі", fontsize=14, fontweight="bold")
    ax.set_xlabel("Площа (м²)", fontsize=11)
    ax.set_ylabel("Ціна ($)", fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "01")

    # 02.png: Базовий scatter plot
    heights = np.random.normal(170, 10, 80)
    weights = 0.7 * heights - 45 + np.random.normal(0, 5, 80)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(heights, weights, color="#10b981", edgecolors="black", s=50, alpha=0.75)
    ax.set_title("Зріст та вага людини", fontsize=13, fontweight="bold")
    ax.set_xlabel("Зріст (см)", fontsize=11)
    ax.set_ylabel("Вага (кг)", fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "02")

    # 03.png: Демонстрація параметрів scatter
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    ax1.scatter(heights, weights, s=120, c="#f59e0b", alpha=0.5, marker="^", edgecolor="black", linewidth=1.5)
    ax1.set_title("Кастомні маркери (трикутники s=120, alpha=0.5)", fontweight="bold")
    ax1.grid(True, alpha=0.3)

    ax2.scatter(heights, weights, s=weights, c=heights, cmap="coolwarm", edgecolor="black", linewidth=0.5)
    ax2.set_title("Колір за зростом, розмір за вагою", fontweight="bold")
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "03")

    # 04.png: Чотири типи кореляцій
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Типи кореляцій та їх візуалізація", fontsize=15, fontweight="bold")

    x1 = np.linspace(0, 10, 100)
    y1 = 2 * x1 + 3 + np.random.normal(0, 1, 100)
    r1 = np.corrcoef(x1, y1)[0, 1]
    axes[0, 0].scatter(x1, y1, alpha=0.6, color="green", s=50)
    axes[0, 0].set_title(f"Сильна позитивна кореляція (r = {r1:.2f})", fontsize=11, fontweight="bold", color="darkgreen")

    x2 = np.linspace(0, 10, 100)
    y2 = 0.5 * x2 + 3 + np.random.normal(0, 3, 100)
    r2 = np.corrcoef(x2, y2)[0, 1]
    axes[0, 1].scatter(x2, y2, alpha=0.6, color="lightgreen", s=50, edgecolors="black")
    axes[0, 1].set_title(f"Слабка позитивна кореляція (r = {r2:.2f})", fontsize=11, fontweight="bold")

    x3 = np.linspace(0, 10, 100)
    y3 = -2 * x3 + 20 + np.random.normal(0, 1.5, 100)
    r3 = np.corrcoef(x3, y3)[0, 1]
    axes[1, 0].scatter(x3, y3, alpha=0.6, color="crimson", s=50)
    axes[1, 0].set_title(f"Негативна кореляція (r = {r3:.2f})", fontsize=11, fontweight="bold", color="darkred")

    x4 = np.random.uniform(0, 10, 100)
    y4 = np.random.uniform(0, 10, 100)
    r4 = np.corrcoef(x4, y4)[0, 1]
    axes[1, 1].scatter(x4, y4, alpha=0.6, color="gray", s=50)
    axes[1, 1].set_title(f"Відсутня кореляція (r = {r4:.2f})", fontsize=11, fontweight="bold")

    for ax in axes.flat:
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "04")

    # 05.png: Лінійні vs нелінійні залежності
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.2))
    x = np.linspace(-3, 3, 100)

    # Парабола
    y_quad = x**2 + np.random.normal(0, 0.5, 100)
    r_quad = np.corrcoef(x, y_quad)[0, 1]
    ax1.scatter(x, y_quad, color="#6366f1", alpha=0.7)
    ax1.set_title(f"Параболічна: y = x²\n(r = {r_quad:.2f} — оманливо!)", fontweight="bold", fontsize=10.5)

    # Синусоїда
    x_sin = np.linspace(0, 4*np.pi, 100)
    y_sin = np.sin(x_sin) + np.random.normal(0, 0.1, 100)
    ax2.scatter(x_sin, y_sin, color="#ec4899", alpha=0.7)
    ax2.set_title("Синусоїдальна: y = sin(x)\n(сильний зв'язок, r ≈ 0)", fontweight="bold", fontsize=10.5)

    # Експонента
    x_exp = np.linspace(0, 3, 100)
    y_exp = np.exp(x_exp) + np.random.normal(0, 1, 100)
    ax3.scatter(x_exp, y_exp, color="#f59e0b", alpha=0.7)
    ax3.set_title("Експоненційна: y = eˣ\n(нелінійне зростання)", fontweight="bold", fontsize=10.5)

    for ax in (ax1, ax2, ax3):
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "05")

    # 06.png: Scatter з лінією тренду
    x_trend = np.linspace(10, 50, 80)
    y_trend = 2.5 * x_trend + 10 + np.random.normal(0, 15, 80)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(x_trend, y_trend, color="#3b82f6", alpha=0.7, edgecolors="black", label="Дані спостережень")

    # Лінія тренду через polyfit
    z = np.polyfit(x_trend, y_trend, 1)
    p = np.poly1d(z)
    ax.plot(x_trend, p(x_trend), "r--", linewidth=2.5, label=f"Тренд: y = {z[0]:.2f}x + {z[1]:.1f}")
    ax.set_title("Scatter plot з лінією тренду", fontsize=14, fontweight="bold")
    ax.set_xlabel("X", fontsize=11)
    ax.set_ylabel("Y", fontsize=11)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "06")

    # 07.png: Порівняння лінійної та нелінійної ліній регресії
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    ax1.scatter(x_trend, y_trend, color="#0284c7", alpha=0.6)
    ax1.plot(x_trend, p(x_trend), color="red", linewidth=2, label="Лінійний тренд (deg=1)")
    ax1.set_title("Лінійна регресія (NumPy polyfit)", fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Поліноміальний тренд для нелінійних даних
    x_curve = np.linspace(0, 5, 80)
    y_curve = 2 * (x_curve**2) - 3*x_curve + 5 + np.random.normal(0, 2, 80)
    z_curve = np.polyfit(x_curve, y_curve, 2)
    p_curve = np.poly1d(z_curve)
    ax2.scatter(x_curve, y_curve, color="#10b981", alpha=0.6)
    ax2.plot(x_curve, p_curve(x_curve), color="darkgreen", linewidth=2, label="Поліном 2-го степеня (deg=2)")
    ax2.set_title("Нелінійна регресія (polyfit deg=2)", fontweight="bold")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "07")

    # 08.png: Кольорове кодування районів
    n = 150
    area = np.random.uniform(30, 120, n)
    district = np.random.choice([0, 1, 2], n, p=[0.4, 0.3, 0.3])
    price_per_sqm = np.array([400, 600, 500])
    price = price_per_sqm[district] * area + np.random.normal(0, 5000, n)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    colors = ["#FF6B6B", "#4ECDC4", "#95E1D3"]
    district_names = ["Схід", "Центр", "Захід"]
    for i, (color, name) in enumerate(zip(colors, district_names)):
        mask = district == i
        ax.scatter(area[mask], price[mask], c=color, s=80, alpha=0.8, 
                   edgecolor="black", linewidth=0.5, label=name)
    ax.set_title("Ціна квартир: площа vs район", fontsize=14, fontweight="bold")
    ax.set_xlabel("Площа (м²)", fontsize=11)
    ax.set_ylabel("Ціна ($)", fontsize=11)
    ax.legend(title="Район")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "08")

    # 09.png: Scatter з кодуванням розміром
    fig, ax = plt.subplots(figsize=(10, 5.5))
    rooms = np.random.randint(1, 5, n)
    sc = ax.scatter(area, price, s=rooms*40, c=price, cmap="viridis", alpha=0.75, edgecolor="black", linewidth=0.5)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Ціна ($)", fontsize=10)
    ax.set_title("Площа vs Ціна (розмір = к-ть кімнат, колір = ціна)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Площа (м²)", fontsize=11)
    ax.set_ylabel("Ціна ($)", fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "relationships", "09")

    # 10.png: Демонстрація колірних карт (colormaps)
    fig, axes = plt.subplots(5, 1, figsize=(10, 5))
    cmaps = ["viridis", "plasma", "Blues", "coolwarm", "tab10"]
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    for ax, cmap in zip(axes, cmaps):
        ax.imshow(gradient, aspect="auto", cmap=cmap)
        ax.set_title(f"Колірна карта: '{cmap}'", fontsize=10, loc="left", fontweight="bold")
        ax.set_axis_off()
    plt.tight_layout()
    save_fig(fig, "relationships", "10")

    # 11.png: Scatter Matrix
    n_mat = 200
    df_mat = pd.DataFrame({
        "Зріст (см)": np.random.normal(170, 10, n_mat),
        "Вага (кг)": np.random.normal(70, 15, n_mat),
        "Вік (роки)": np.random.uniform(18, 65, n_mat),
        "Дохід ($)": np.random.lognormal(10, 0.5, n_mat)
    })
    df_mat["Вага (кг)"] = 0.4 * df_mat["Зріст (см)"] + np.random.normal(0, 8, n_mat)

    from pandas.plotting import scatter_matrix
    fig, axes = plt.subplots(4, 4, figsize=(12, 12))
    scatter_matrix(df_mat, ax=axes, alpha=0.6, diagonal="hist", color="#2563eb",
                   hist_kwds={"bins": 20, "edgecolor": "black", "color": "#60a5fa"})
    plt.suptitle("Scatter Matrix: всі пари змінних", fontsize=15, fontweight="bold", y=0.995)
    plt.tight_layout()
    save_fig(fig, "relationships", "11")

    # 12.png: Heatmap кореляційної матриці
    fig, ax = plt.subplots(figsize=(7, 5.5))
    corr = df_mat.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax, cbar_kws={'label': 'Коефіцієнт кореляції'})
    ax.set_title("Кореляційна матриця (Seaborn Heatmap)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    save_fig(fig, "relationships", "12")


# ==========================================
# 4. CATEGORICAL
# ==========================================
def generate_categorical():
    print("Generating categorical images...")
    np.random.seed(42)

    # 01.png: Групові bar charts для продажів
    categories = ["Електроніка", "Одяг", "Продукти", "Книги"]
    q1 = [150, 120, 200, 80]
    q2 = [180, 140, 210, 75]
    x = np.arange(len(categories))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width/2, q1, width, label="Q1 (I квартал)", color="#3b82f6", edgecolor="black")
    ax.bar(x + width/2, q2, width, label="Q2 (II квартал)", color="#10b981", edgecolor="black")
    ax.set_title("Порівняння продажів за кварталами", fontsize=14, fontweight="bold")
    ax.set_ylabel("Обсяг продажів (тис. грн)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10.5)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "categorical", "01")

    # 02.png: Вертикальні bar charts
    languages = ["Python", "JavaScript", "Java", "C#", "C++"]
    popularity = [28, 22, 17, 13, 9]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(languages, popularity, color="#6366f1", edgecolor="black", alpha=0.85)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.6, f"{h}%", ha="center", va="bottom", fontweight="bold")
    ax.set_title("Популярність мов програмування", fontsize=14, fontweight="bold")
    ax.set_ylabel("Частка (%)", fontsize=11)
    ax.set_ylim(0, 33)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "categorical", "02")

    # 03.png: Підписи над стовпцями детально
    fig, ax = plt.subplots(figsize=(8, 4.5))
    items = ["Проєкт A", "Проєкт B", "Проєкт C"]
    vals = [42.5, 78.1, 55.3]
    bars = ax.bar(items, vals, color=["#38bdf8", "#818cf8", "#c084fc"], edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.2, f"{h:.1f}", ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_title("Автоматичні підписи над вершинами стовпців", fontsize=13, fontweight="bold")
    ax.set_ylim(0, 95)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "categorical", "03")

    # 04.png: Горизонтальні bar charts
    departments = [
        "Технічна підтримка",
        "Відділ продажів",
        "Бухгалтерія",
        "HR (кадри)",
        "IT (розробка)",
        "Маркетинг"
    ]
    response_time = [2.5, 4.0, 8.5, 6.0, 3.0, 5.5]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(departments, response_time, color="#f59e0b", edgecolor="black", alpha=0.85)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.15, bar.get_y() + bar.get_height()/2, f"{w} год", va="center", fontweight="bold")
    ax.set_title("Середній час відповіді відділів", fontsize=13, fontweight="bold")
    ax.set_xlabel("Години", fontsize=11)
    ax.set_xlim(0, 10)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "categorical", "04")

    # 05.png: Групові bar charts
    fig, ax = plt.subplots(figsize=(10, 5))
    channels = ["Сайт", "Мобільний додаток", "Партнери"]
    q1_c = [350, 420, 180]
    q2_c = [390, 480, 210]
    q3_c = [410, 530, 200]
    x_c = np.arange(len(channels))
    w_c = 0.25
    ax.bar(x_c - w_c, q1_c, w_c, label="Q1", color="#3b82f6", edgecolor="black")
    ax.bar(x_c, q2_c, w_c, label="Q2", color="#10b981", edgecolor="black")
    ax.bar(x_c + w_c, q3_c, w_c, label="Q3", color="#f97316", edgecolor="black")
    ax.set_xticks(x_c)
    ax.set_xticklabels(channels, fontsize=11)
    ax.set_title("Динаміка залучення клієнтів за каналами", fontsize=14, fontweight="bold")
    ax.set_ylabel("Кількість нових клієнтів", fontsize=11)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "categorical", "05")

    # 06.png: Stacked bar charts
    fig, ax = plt.subplots(figsize=(9, 5))
    months = ["Січ", "Лют", "Бер", "Кві"]
    desktop = np.array([45, 50, 48, 52])
    mobile = np.array([35, 38, 42, 40])
    tablet = np.array([10, 12, 10, 8])
    ax.bar(months, desktop, label="Desktop", color="#3b82f6", edgecolor="black")
    ax.bar(months, mobile, bottom=desktop, label="Mobile", color="#10b981", edgecolor="black")
    ax.bar(months, tablet, bottom=desktop+mobile, label="Tablet", color="#fbbf24", edgecolor="black")
    ax.set_title("Частка пристроїв відвідувачів (Stacked Bar Chart)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Трафік (тис. сесій)", fontsize=11)
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "categorical", "06")

    # 07.png: Pie chart з витягнутим сектором
    sizes = [40, 25, 20, 15]
    labels = ["Desktop (40%)", "Mobile (25%)", "Tablet (20%)", "Other (15%)"]
    explode = (0.08, 0, 0, 0)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
           shadow=True, startangle=140, colors=["#3b82f6", "#10b981", "#fbbf24", "#94a3b8"])
    ax.set_title("Розподіл часток користувачів (Pie Chart)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    save_fig(fig, "categorical", "07")

    # 08.png: Порівняння pie vs bar
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    shares = [22, 21, 20, 19, 18]
    cats = ["A", "B", "C", "D", "E"]
    ax1.pie(shares, labels=cats, autopct='%1.0f%%', colors=plt.cm.Pastel1.colors)
    ax1.set_title("Pie chart: чи легко знайти найбільший?", fontweight="bold")

    bars = ax2.bar(cats, shares, color="#3b82f6", edgecolor="black")
    ax2.set_title("Bar chart: різниця одразу очевидна!", fontweight="bold")
    ax2.set_ylim(0, 25)
    ax2.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "categorical", "08")

    # 09.png: Ефект сортування
    cats_unsorted = ["Продукт E", "Продукт A", "Продукт D", "Продукт B", "Продукт C"]
    vals_unsorted = [15, 85, 30, 60, 45]
    sorted_pairs = sorted(zip(vals_unsorted, cats_unsorted), reverse=True)
    vals_sorted = [v for v, c in sorted_pairs]
    cats_sorted = [c for v, c in sorted_pairs]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
    ax1.bar(cats_unsorted, vals_unsorted, color="#94a3b8", edgecolor="black")
    ax1.set_title("Невпорядковані категорії (важко порівнювати)", fontweight="bold")
    ax1.tick_params(axis='x', rotation=15)
    ax1.grid(axis="y", alpha=0.3)

    ax2.bar(cats_sorted, vals_sorted, color="#059669", edgecolor="black")
    ax2.set_title("Відсортовані за спаданням (ідеально сприймається)", fontweight="bold")
    ax2.tick_params(axis='x', rotation=15)
    ax2.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "categorical", "09")


# ==========================================
# 5. SUBPLOTS & STYLING
# ==========================================
def generate_subplots_styling():
    print("Generating subplots-styling images...")
    np.random.seed(42)

    # 01.png: Квартальний дашборд з 4 графіків
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Квартальний дашборд показників бізнесу", fontsize=15, fontweight="bold")

    # 1. Line plot
    months = ["Січ", "Лют", "Бер"]
    rev = [120, 145, 160]
    axes[0, 0].plot(months, rev, marker="o", color="#2563eb", linewidth=2.5)
    axes[0, 0].set_title("Динаміка виручки (тис. $)", fontweight="bold")
    axes[0, 0].grid(True, alpha=0.3)

    # 2. Bar chart
    products = ["SaaS", "Консалтинг", "Підтримка"]
    sales = [310, 140, 95]
    axes[0, 1].bar(products, sales, color="#10b981", edgecolor="black")
    axes[0, 1].set_title("Продажі за напрямками", fontweight="bold")
    axes[0, 1].grid(axis="y", alpha=0.3)

    # 3. Histogram
    n_cust = np.random.normal(45, 12, 200)
    axes[1, 0].hist(n_cust, bins=15, color="#f59e0b", edgecolor="black", alpha=0.8)
    axes[1, 0].set_title("Розподіл віку користувачів", fontweight="bold")
    axes[1, 0].grid(axis="y", alpha=0.3)

    # 4. Scatter plot
    adv = np.random.uniform(5, 30, 50)
    roi = adv * 3.2 + np.random.normal(0, 10, 50)
    axes[1, 1].scatter(adv, roi, color="#8b5cf6", alpha=0.7, edgecolor="black")
    axes[1, 1].set_title("Витрати на маркетинг vs Прибуток", fontweight="bold")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig, "subplots-styling", "01")

    # 02.png: Сітка 2x2
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for i, ax in enumerate(axes.flat, 1):
        ax.plot([0, 1], [0, i], linewidth=2)
        ax.set_title(f"Subplot {i} (axes[{ (i-1)//2 }, { (i-1)%2 }])", fontweight="bold")
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "subplots-styling", "02")

    # 03.png: Параметри plt.subplots
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), sharey=True)
    fig.suptitle("Демонстрація sharey=True (спільна вісь Y)", fontsize=13, fontweight="bold")
    for i, ax in enumerate(axes, 1):
        ax.bar(["X", "Y"], [i*10, i*15], color=f"C{i}")
        ax.set_title(f"Категорія {i}")
        ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "subplots-styling", "03")

    # 04.png: Три різні конфігурації subplots (композиція 1x3, 3x1, 2x3)
    fig = plt.figure(figsize=(14, 9))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1.2])

    # Верхня ліва: 1 ряд, 3 стовпчики (в мініатюрі)
    ax_top = fig.add_subplot(gs[0, :])
    ax_top.set_title("Конфігурація 1: один рядок (1×3)", fontweight="bold")
    ax_top.axis("off")
    # Sub-axes
    sub_gs = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=gs[0, :])
    for i in range(3):
        ax_sub = fig.add_subplot(sub_gs[0, i])
        ax_sub.plot(np.sin(np.linspace(0, 5, 20) + i))
        ax_sub.set_title(f"ax[{i}]")

    # Нижня ліва: 3 рядки 1 стовпець
    sub_gs_vert = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[1, 0])
    for i in range(3):
        ax_sub = fig.add_subplot(sub_gs_vert[i, 0])
        ax_sub.bar(["A", "B"], [2+i, 4+i], color=f"C{i}")
        ax_sub.set_title(f"Рядок {i+1}", fontsize=9)

    # Нижня права: 2x3 сітка
    sub_gs_grid = gridspec.GridSpecFromSubplotSpec(2, 3, subplot_spec=gs[1, 1])
    for r in range(2):
        for c in range(3):
            ax_sub = fig.add_subplot(sub_gs_grid[r, c])
            ax_sub.scatter([1], [1], s=50)
            ax_sub.set_title(f"[{r},{c}]", fontsize=8)
            ax_sub.set_xticks([])
            ax_sub.set_yticks([])

    plt.tight_layout()
    save_fig(fig, "subplots-styling", "04")

    # 05.png: GridSpec асиметрична композиція
    fig = plt.figure(figsize=(12, 7))
    gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1])
    ax_main = fig.add_subplot(gs[:, 0])  # займає весь лівий стовпець
    ax_top_right = fig.add_subplot(gs[0, 1])
    ax_bot_right = fig.add_subplot(gs[1, 1])

    t = np.linspace(0, 10, 100)
    ax_main.plot(t, np.sin(t), color="#2563eb", linewidth=2.5)
    ax_main.set_title("Головний графік (GridSpec[:, 0])", fontweight="bold")
    ax_main.grid(True, alpha=0.3)

    ax_top_right.hist(np.random.normal(0, 1, 100), color="#10b981", edgecolor="black")
    ax_top_right.set_title("Додатковий 1 (GridSpec[0, 1])", fontweight="bold")

    ax_bot_right.scatter(np.random.rand(30), np.random.rand(30), color="#f59e0b")
    ax_bot_right.set_title("Додатковий 2 (GridSpec[1, 1])", fontweight="bold")

    plt.tight_layout()
    save_fig(fig, "subplots-styling", "05")

    # 06.png: Графіки зі спільною віссю X
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    t = np.linspace(0, 10, 100)
    ax1.plot(t, np.sin(t), color="#2563eb", linewidth=2)
    ax1.set_title("Спільна вісь X (sharex=True)", fontsize=13, fontweight="bold")
    ax1.set_ylabel("Амплітуда 1")
    ax1.grid(True, alpha=0.3)

    ax2.plot(t, np.cos(t), color="#dc2626", linewidth=2)
    ax2.set_xlabel("Час (секунди)", fontsize=11)
    ax2.set_ylabel("Амплітуда 2")
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "subplots-styling", "06")

    # 07.png: Порівняння 4 стилів
    styles = ["default", "seaborn-v0_8-darkgrid", "ggplot", "bmh"]
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("Порівняння стилів matplotlib", fontsize=15, fontweight="bold")
    x = np.linspace(0, 10, 100)
    for ax, style in zip(axes.flat, styles):
        with plt.style.context(style):
            ax.plot(x, np.sin(x), label="sin(x)", linewidth=2)
            ax.plot(x, np.cos(x), label="cos(x)", linewidth=2)
            ax.set_title(f"Стиль: {style}", fontweight="bold")
            ax.legend()
            ax.grid(True)
    plt.tight_layout()
    save_fig(fig, "subplots-styling", "07")

    # 08.png: Порівняння кольорових палітр
    categories = ["A", "B", "C", "D", "E"]
    values = [23, 45, 56, 78, 32]
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle("Кольорові палітри для категорій", fontsize=15, fontweight="bold")

    axes[0, 0].bar(categories, values, color=[f"C{i}" for i in range(5)], edgecolor="black")
    axes[0, 0].set_title("Default (C0–C9)", fontweight="bold")

    colors_tab10 = plt.cm.tab10(np.linspace(0, 1, 5))
    axes[0, 1].bar(categories, values, color=colors_tab10, edgecolor="black")
    axes[0, 1].set_title("Tab10 (рекомендовано)", fontweight="bold")

    colors_viridis = plt.cm.viridis(np.linspace(0, 1, 5))
    axes[0, 2].bar(categories, values, color=colors_viridis, edgecolor="black")
    axes[0, 2].set_title("Viridis", fontweight="bold")

    colors_pastel = plt.cm.Pastel1(np.linspace(0, 1, 5))
    axes[1, 0].bar(categories, values, color=colors_pastel, edgecolor="black")
    axes[1, 0].set_title("Pastel1", fontweight="bold")

    colors_set3 = plt.cm.Set3(np.linspace(0, 1, 5))
    axes[1, 1].bar(categories, values, color=colors_set3, edgecolor="black")
    axes[1, 1].set_title("Set3", fontweight="bold")

    custom_colors = ["#FF6B6B", "#4ECDC4", "#95E1D3", "#FFD93D", "#C7CEEA"]
    axes[1, 2].bar(categories, values, color=custom_colors, edgecolor="black")
    axes[1, 2].set_title("Кастомна (HEX)", fontweight="bold")

    for ax in axes.flat:
        ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "subplots-styling", "08")

    # 09.png: Графік з анотаціями
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(x, y, linewidth=2.5, color="#2563eb", label="Сигнал")
    ax.annotate("Локальний максимум", xy=(np.pi/2, 1), xytext=(np.pi/2 + 1, 0.8),
                arrowprops=dict(facecolor="crimson", shrink=0.05, width=1.5, headwidth=8),
                fontsize=10.5, fontweight="bold", color="crimson")
    ax.annotate("Локальний мінімум", xy=(3*np.pi/2, -1), xytext=(3*np.pi/2 + 0.8, -0.7),
                arrowprops=dict(facecolor="darkgreen", shrink=0.05, width=1.5, headwidth=8),
                fontsize=10.5, fontweight="bold", color="darkgreen")
    ax.set_title("Графік з розширеними анотаціями", fontsize=14, fontweight="bold")
    ax.set_xlabel("X", fontsize=11)
    ax.set_ylabel("Y", fontsize=11)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "subplots-styling", "09")

    # 10.png: Демонстрація ліній та зон
    fig, ax = plt.subplots(figsize=(10, 5.5))
    t = np.linspace(0, 24, 100)
    temp = 18 + 7 * np.sin((t - 9) * np.pi / 12)
    ax.plot(t, temp, color="#0284c7", linewidth=2.5, label="Температура")
    ax.axhline(22, color="crimson", linestyle="--", linewidth=1.5, label="Поріг комфорту (22°C)")
    ax.axvline(14, color="darkorange", linestyle=":", linewidth=2, label="Пік сонячної активності")
    ax.axhspan(20, 25, alpha=0.15, color="green", label="Зона оптимуму (20–25°C)")
    ax.axvspan(12, 16, alpha=0.1, color="orange", label="Обідній період")
    ax.set_title("Демонстрація axhline, axvline, axhspan, axvspan", fontsize=13, fontweight="bold")
    ax.set_xlabel("Години доби", fontsize=11)
    ax.set_ylabel("Температура (°C)", fontsize=11)
    ax.legend(loc="lower left", fontsize=9.5)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "subplots-styling", "10")

if __name__ == "__main__":
    print(f"Target directory: {BASE_DIR}")
    generate_index()
    generate_basics()
    generate_distributions()
    generate_relationships()
    generate_categorical()
    generate_subplots_styling()
    print("All visual diagrams have been successfully generated!")
