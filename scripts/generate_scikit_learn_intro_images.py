#!/usr/bin/env python3
"""
Скрипт для генерації графіків для лекції:
content/16.ai-python/07.practical-regression/01.intro-scikit-learn.md

Зберігає графіки у:
public/images/ai-python/practical-regression/intro-scikit-learn/
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Налаштування стилю графіків
plt.rcParams.update({
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif'],
    'font.family': 'sans-serif',
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'savefig.facecolor': '#FFFFFF',
    'axes.edgecolor': '#D0D7DE',
    'axes.labelcolor': '#1F2328',
    'xtick.color': '#1F2328',
    'ytick.color': '#1F2328',
    'text.color': '#1F2328',
    'grid.color': '#E1E4E8',
    'grid.linestyle': '--',
    'grid.alpha': 0.7,
})

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "public", "images", "ai-python", "practical-regression", "intro-scikit-learn"
)
os.makedirs(BASE_DIR, exist_ok=True)

def generate_plot_1():
    """01.png: Перша модель scikit-learn: y = 2x"""
    print("Генерація 01.png...")
    # Дані
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([2, 4, 6, 8, 10])

    model = LinearRegression()
    model.fit(X, y)

    X_new = np.array([[6], [7]])
    predictions = model.predict(X_new)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)

    # Вихідні дані
    ax.scatter(X, y, color='dodgerblue', s=120, label='Вихідні дані', zorder=3, edgecolor='black')

    # Лінія регресії
    X_line = np.linspace(0, 8, 100).reshape(-1, 1)
    y_line = model.predict(X_line)
    ax.plot(X_line, y_line, color='crimson', linewidth=2.5, label='Лінія регресії', zorder=2)

    # Передбачення для нових точок
    ax.scatter(X_new, predictions, color='limegreen', s=180, marker='*', 
               label='Передбачення', zorder=4, edgecolor='black')

    # Оформлення
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Перша модель scikit-learn: y = 2x', fontsize=14, fontweight='bold', pad=12)
    ax.legend(fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 16)
    plt.tight_layout()

    output_path = os.path.join(BASE_DIR, '01.png')
    fig.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Збережено: {output_path}")

def generate_plot_2():
    """02.png: Зріст vs Вага (R² = 1.0000)"""
    print("Генерація 02.png...")
    heights = np.array([[150], [160], [165], [170], [175], 
                        [180], [185], [190], [195], [200]])  # см
    weights = np.array([50, 58, 62, 68, 73, 78, 83, 88, 93, 98])  # кг

    model = LinearRegression()
    model.fit(heights, weights)

    new_height = np.array([[172]])
    predicted_weight = model.predict(new_height)
    r2 = model.score(heights, weights)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)

    # Вихідні дані
    ax.scatter(heights, weights, color='dodgerblue', s=120, 
               label='Вихідні дані', zorder=3, edgecolor='black')

    # Лінія регресії
    heights_line = np.linspace(145, 205, 100).reshape(-1, 1)
    weights_line = model.predict(heights_line)
    ax.plot(heights_line, weights_line, color='crimson', linewidth=2.5, 
            label='Лінія регресії', zorder=2)

    # Нове передбачення
    ax.scatter(new_height, predicted_weight, color='limegreen', s=200, marker='*',
               label=f'Передбачення ({new_height[0][0]} см → {predicted_weight[0]:.1f} кг)',
               zorder=4, edgecolor='black')

    # Оформлення
    ax.set_xlabel('Зріст (см)', fontsize=12)
    ax.set_ylabel('Вага (кг)', fontsize=12)
    ax.set_title(f'Зріст vs Вага (R² = {r2:.4f})', fontsize=14, fontweight='bold', pad=12)
    ax.legend(fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    output_path = os.path.join(BASE_DIR, '02.png')
    fig.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Збережено: {output_path}")

if __name__ == '__main__':
    generate_plot_1()
    generate_plot_2()
    print("Всі графіки успішно згенеровано!")
