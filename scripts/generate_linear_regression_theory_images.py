#!/usr/bin/env python3
"""
Скрипт для генерації всіх графіків та візуалізацій для модуля:
content/16.ai-python/07.linear-regression-theory

Зберігає графіки у:
public/images/ai-python/linear-regression-theory/<section>/<01|02|...>.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Налаштування стилю та шрифтів
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.facecolor'] = '#FFFFFF'
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['savefig.facecolor'] = '#FFFFFF'
plt.rcParams['axes.edgecolor'] = '#D0D7DE'
plt.rcParams['axes.labelcolor'] = '#1F2328'
plt.rcParams['xtick.color'] = '#1F2328'
plt.rcParams['ytick.color'] = '#1F2328'
plt.rcParams['text.color'] = '#1F2328'
plt.rcParams['grid.color'] = '#E1E4E8'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "public", "images", "ai-python", "linear-regression-theory"
)

def save_fig(fig, section: str, name: str, dpi: int = 200):
    folder = os.path.join(BASE_DIR, section)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{name}.png")
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Generated: {filepath}")

# ==========================================
# 01. REGRESSION TASK
# ==========================================
def generate_regression_task():
    print("Generating regression-task images...")

    # 01.png: Scatter plot площа vs ціна
    np.random.seed(42)
    area = np.array([45, 50, 60, 55, 70, 65, 80, 75, 90, 85,
                     100, 95, 110, 105, 120, 115, 130, 125, 140, 135])
    price = 500 * area + np.random.normal(0, 3000, 20)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(area, price, s=100, alpha=0.7, color="steelblue",
               edgecolor="navy", linewidth=1.5, label="Продані квартири")
    ax.set_title("Залежність ціни квартири від площі", fontsize=14, fontweight="bold")
    ax.set_xlabel("Площа (м²)", fontsize=12)
    ax.set_ylabel("Ціна ($)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    plt.tight_layout()
    save_fig(fig, "regression-task", "01")

    # 02.png: Порівняння трьох варіантів моделі
    x_line = np.array([40, 145])
    model_1 = {"w": 600, "b": -5000, "label": "Модель 1 (занадто крута)"}
    model_2 = {"w": 300, "b": 10000, "label": "Модель 2 (занадто плоска)"}
    model_3 = {"w": 500, "b": 0, "label": "Модель 3 (оптимальна)"}

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(area, price, s=100, alpha=0.7, color="steelblue",
               edgecolor="navy", linewidth=1.5, label="Реальні дані", zorder=3)
    ax.plot(x_line, model_1["w"] * x_line + model_1["b"], 
            'r--', linewidth=2, alpha=0.6, label=model_1["label"])
    ax.plot(x_line, model_2["w"] * x_line + model_2["b"], 
            'g--', linewidth=2, alpha=0.6, label=model_2["label"])
    ax.plot(x_line, model_3["w"] * x_line + model_3["b"], 
            'orange', linewidth=3, label=model_3["label"], zorder=2)
    ax.set_title("Порівняння трьох варіантів моделі", fontsize=14, fontweight="bold")
    ax.set_xlabel("Площа (м²)", fontsize=12)
    ax.set_ylabel("Ціна ($)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=10)
    ax.set_ylim(15000, 75000)
    plt.tight_layout()
    save_fig(fig, "regression-task", "02")

    # 03.png: Обмеження лінійної регресії (нелінійні дані)
    np.random.seed(123)
    x = np.linspace(0, 10, 50)
    y = 2 * x**2 - 5 * x + 10 + np.random.normal(0, 10, 50)

    w = np.polyfit(x, y, 1)[0]
    b = np.polyfit(x, y, 1)[1]
    y_pred_linear = w * x + b

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, s=80, alpha=0.6, color="steelblue", label="Реальні дані")
    ax.plot(x, y_pred_linear, 'r-', linewidth=2, label=f"Лінійна модель (y = {w:.1f}x + {b:.1f})")
    ax.plot(x, 2 * x**2 - 5 * x + 10, 'g--', linewidth=2, label="Справжня залежність (квадратична)")
    ax.set_title("Обмеження лінійної регресії: нелінійні дані", fontsize=14, fontweight="bold")
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "regression-task", "03")

# ==========================================
# 03. GRADIENT DESCENT
# ==========================================
def generate_gradient_descent():
    print("Generating gradient-descent images...")

    # 01.png: Графік функції втрат L(w) 1D
    np.random.seed(42)
    x = np.array([1, 2, 3, 4, 5])
    y = 2 * x + np.random.normal(0, 0.5, 5)

    def loss_function(w):
        predictions = w * x
        return np.mean((y - predictions) ** 2)

    w_values = np.linspace(0, 4, 100)
    losses = [loss_function(w) for w in w_values]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(w_values, losses, linewidth=3, color='steelblue', label='L(w) = MSE')
    ax.axvline(x=2, color='red', linestyle='--', linewidth=2, label='Оптимальне w ≈ 2')

    min_idx = np.argmin(losses)
    ax.plot(w_values[min_idx], losses[min_idx], 'ro', markersize=12, 
            label=f'Мінімум: w={w_values[min_idx]:.2f}')

    ax.set_title('Функція втрат L(w) для лінійної регресії', fontsize=14, fontweight='bold')
    ax.set_xlabel('Параметр w', fontsize=12)
    ax.set_ylabel('MSE (втрати)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    plt.tight_layout()
    save_fig(fig, "gradient-descent", "01")

    # 02.png: Вплив learning rate на збіжність
    def gradient_descent(x, y, lr, epochs=50):
        w = 0.1
        history = [w]
        for _ in range(epochs):
            y_pred = w * x
            dw = -2 * np.mean(x * (y - y_pred))
            w = w - lr * dw
            history.append(w)
        return np.array(history)

    lr_small = 0.01
    lr_optimal = 0.1
    lr_large = 0.5

    history_small = gradient_descent(x, y, lr_small)
    history_optimal = gradient_descent(x, y, lr_optimal)
    history_large = gradient_descent(x, y, lr_large)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(history_small, linewidth=2, label=f'α = {lr_small} (занадто малий)', marker='o', markersize=4)
    ax.plot(history_optimal, linewidth=2, label=f'α = {lr_optimal} (оптимальний)', marker='s', markersize=4)
    ax.plot(history_large, linewidth=2, label=f'α = {lr_large} (занадто великий)', marker='^', markersize=4)
    ax.axhline(y=2.0, color='red', linestyle='--', linewidth=2, label='Справжнє w ≈ 2.0')

    ax.set_title('Вплив Learning Rate на збіжність', fontsize=14, fontweight='bold')
    ax.set_xlabel('Епоха', fontsize=12)
    ax.set_ylabel('Значення параметра w', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "gradient-descent", "02")

    # 03.png: Результати градієнтного спуску (крива навчання + фінальна пряма)
    np.random.seed(42)
    area = np.array([45, 50, 60, 55, 70, 65, 80, 75, 90, 85,
                     100, 95, 110, 105, 120, 115, 130, 125, 140, 135])
    price = 500 * area + np.random.normal(0, 3000, 20)

    x_mean, x_std = area.mean(), area.std()
    x_norm = (area - x_mean) / x_std

    def gradient_descent_full(x, y, learning_rate=0.1, epochs=1000):
        n = len(x)
        w, b = 0.0, 0.0
        loss_history = []
        for epoch in range(epochs):
            y_pred = w * x + b
            loss = np.mean((y - y_pred) ** 2)
            loss_history.append(loss)
            dw = -(2/n) * np.sum(x * (y - y_pred))
            db = -(2/n) * np.sum(y - y_pred)
            w = w - learning_rate * dw
            b = b - learning_rate * db
        return w, b, loss_history

    w_final, b_final, loss_history = gradient_descent_full(x_norm, price, learning_rate=0.1, epochs=1000)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(loss_history, linewidth=2, color='steelblue')
    ax1.set_title('Крива навчання (Loss по епохах)', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Епоха', fontsize=11)
    ax1.set_ylabel('MSE Loss', fontsize=11)
    ax1.grid(True, alpha=0.3)

    y_pred_final = w_final * x_norm + b_final
    ax2.scatter(area, price, s=80, alpha=0.6, color='steelblue', label='Реальні дані')
    ax2.plot(area, y_pred_final, 'r-', linewidth=2, label=f'Модель (w={w_final:.0f}, b={b_final:.0f})')
    ax2.set_title('Результат навчання', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Площа (м²)', fontsize=11)
    ax2.set_ylabel('Ціна ($)', fontsize=11)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "gradient-descent", "03")

# ==========================================
# 04. MULTIPLE REGRESSION
# ==========================================
def generate_multiple_regression():
    print("Generating multiple-regression images...")

    # 01.png: Feature Importance
    w_final = np.array([14679.68, 8820.52, 586.57, -14690.19])
    feature_names = ['Area', 'Rooms', 'Floor', 'Metro Distance']
    weights = np.abs(w_final)
    sorted_idx = np.argsort(weights)[::-1]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(weights)), weights[sorted_idx], color='steelblue', edgecolor='navy')
    ax.set_yticks(range(len(weights)))
    ax.set_yticklabels([feature_names[i] for i in sorted_idx])
    ax.set_xlabel('Абсолютне значення ваги', fontsize=12)
    ax.set_title('Важливість ознак (Feature Importance)', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "multiple-regression", "01")

# ==========================================
# 05. PRACTICE
# ==========================================
def generate_practice():
    print("Generating practice images...")

    # 01.png: Крива навчання градієнтного спуску та навчена модель
    def gradient_descent_simple(x, y, lr=0.0001, epochs=1000):
        w, b = 0.0, 0.0
        n = len(x)
        loss_history = []
        for _ in range(epochs):
            y_pred = w * x + b
            loss = np.mean((y - y_pred) ** 2)
            loss_history.append(loss)
            dw = -(2/n) * np.sum(x * (y - y_pred))
            db = -(2/n) * np.sum(y - y_pred)
            w -= lr * dw
            b -= lr * db
        return w, b, loss_history

    np.random.seed(42)
    X = np.array([50, 60, 70, 80, 90, 100])
    y = 500 * X + 10000 + np.random.normal(0, 2000, len(X))

    w_final, b_final, losses = gradient_descent_simple(X, y, lr=0.0001, epochs=1000)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(losses, linewidth=2, color='steelblue')
    ax1.set_title('Крива навчання', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Епоха', fontsize=11)
    ax1.set_ylabel('MSE Loss', fontsize=11)
    ax1.grid(True, alpha=0.3)

    ax2.scatter(X, y, label='Дані', s=100, color='steelblue', edgecolor='navy')
    ax2.plot(X, w_final * X + b_final, 'r-', linewidth=2, label=f'ŷ = {w_final:.0f}x + {b_final:.0f}')
    ax2.set_title('Навчена модель', fontsize=13, fontweight='bold')
    ax2.set_xlabel('X', fontsize=11)
    ax2.set_ylabel('y', fontsize=11)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, "practice", "01")

if __name__ == "__main__":
    generate_regression_task()
    generate_gradient_descent()
    generate_multiple_regression()
    generate_practice()
    print("All 8 images generated successfully!")
