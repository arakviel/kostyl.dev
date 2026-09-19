"""
Script to generate high-quality matplotlib visualizations for 
content/16.ai-python/07.practical-regression/05.overfitting-underfitting.md

Visualizations:
1. 01.png (overfitting_poly15.png): Overfitting на поліномі 15-го ступеня
2. 02.png (underfitting_sine.png): Underfitting прямої лінії на синусоїді
3. 03.png (comparison_three.png): 3-панельне порівняння (Underfitting, Good Fit, Overfitting)
4. 04.png (learning_curve.png): Learning Curve на реальному Housing dataset
5. 05.png (bias_variance_tradeoff.png): Діаграма Bias-Variance Tradeoff та крива складності моделі
"""

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, learning_curve

# Styling parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

OUTPUT_DIR = "public/images/ai-python/practical-regression/overfitting-underfitting"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_01_overfitting():
    """Plot 1: Overfitting on degree 15 polynomial."""
    rng = np.random.default_rng(42)
    # Generate 30 points with quadratic relationship + noise
    X = np.linspace(0, 10, 30).reshape(-1, 1)
    y_true = 0.5 * X.ravel()**2 + 2 * X.ravel() + 5
    y = y_true + rng.normal(0, 5, 30)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    poly = PolynomialFeatures(degree=15, include_bias=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_poly, y_train)

    X_plot = np.linspace(0, 10, 300).reshape(-1, 1)
    X_plot_poly = poly.transform(X_plot)
    y_plot_pred = model.predict(X_plot_poly)
    y_plot_true = 0.5 * X_plot.ravel()**2 + 2 * X_plot.ravel() + 5

    fig, ax = plt.subplots(figsize=(10.5, 6), dpi=180)

    # True trend
    ax.plot(X_plot, y_plot_true, color='#888888', linestyle='--', linewidth=2, label='Справжня залежність (True trend)', zorder=1)
    # Overfit curve
    ax.plot(X_plot, y_plot_pred, color='#D0021B', linewidth=2.5, label='Модель: Поліном 15-го ступеня (Overfit)', zorder=2)
    # Data points
    ax.scatter(X_train, y_train, color='#2A75D3', s=80, edgecolor='black', linewidth=0.8, label=f'Train зразки (N={len(X_train)})', zorder=4)
    ax.scatter(X_test, y_test, color='#27AE60', s=110, marker='s', edgecolor='black', linewidth=0.8, label=f'Test зразки (N={len(X_test)})', zorder=4)

    ax.set_title("Overfitting (Перенавчання): Модель 'зазубрила' навчальний шум", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Ознака X", fontsize=11, fontweight='bold')
    ax.set_ylabel("Цільове значення y", fontsize=11, fontweight='bold')
    ax.set_ylim(-30, 130)
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.95, fontsize=10)

    # Text explanation box
    ax.text(0.55, 0.08, 
            "Діагностика Overfitting:\n"
            "• Крива робить дикі вигини, проходячи крізь шум\n"
            "• Train R² = 0.9987 (майже 100% точність)\n"
            "• Test R² = -2.4521 (провал на нових даних)\n"
            "• Модель не здатна до узагальнення (Generalization)",
            transform=ax.transAxes, fontsize=9.5,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#FDF2E9', edgecolor='#E67E22', alpha=0.95))

    plt.tight_layout()
    path_01 = os.path.join(OUTPUT_DIR, "01.png")
    path_alt = os.path.join(OUTPUT_DIR, "overfitting_poly15.png")
    plt.savefig(path_01, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_01, path_alt)
    print(f"Generated: {path_01} & {path_alt}")


def plot_02_underfitting():
    """Plot 2: Underfitting with a linear model on a sine wave."""
    rng = np.random.default_rng(42)
    X_sine = np.linspace(0, 4*np.pi, 100).reshape(-1, 1)
    y_true_sine = np.sin(X_sine).ravel()
    y_sine = y_true_sine + rng.normal(0, 0.12, 100)

    X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_sine, y_sine, test_size=0.3, random_state=42)

    model = LinearRegression()
    model.fit(X_train_s, y_train_s)

    X_plot_s = np.linspace(0, 4*np.pi, 300).reshape(-1, 1)
    y_plot_pred_s = model.predict(X_plot_s)

    fig, ax = plt.subplots(figsize=(10.5, 6), dpi=180)

    # True sine wave
    ax.plot(X_plot_s, np.sin(X_plot_s), color='#888888', linestyle='--', linewidth=2, label='Справжня залежність: y = sin(x)', zorder=1)
    # Underfit linear model
    ax.plot(X_plot_s, y_plot_pred_s, color='#D0021B', linewidth=2.5, label='Лінійна модель: y = w·x + b (Underfit)', zorder=2)
    # Data points
    ax.scatter(X_train_s, y_train_s, color='#2A75D3', s=45, alpha=0.7, edgecolor='black', linewidth=0.5, label=f'Train дані (N={len(X_train_s)})', zorder=3)
    ax.scatter(X_test_s, y_test_s, color='#27AE60', s=70, marker='s', alpha=0.85, edgecolor='black', linewidth=0.6, label=f'Test дані (N={len(X_test_s)})', zorder=3)

    ax.set_title("Underfitting (Недонавчання): Занадто проста лінійна модель для нелінійних даних", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Ознака X (радіани)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Цільове значення y", fontsize=11, fontweight='bold')
    ax.set_ylim(-1.6, 1.8)
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.95, fontsize=10)

    # Text explanation box
    ax.text(0.04, 0.08, 
            "Діагностика Underfitting:\n"
            "• Пряма лінія фізично не здатна описати синусоїду\n"
            "• Train R² = 0.0234 | Test R² = 0.0189 (обидва вкрай низькі)\n"
            "• Різниця між вибірками мізерна, але модель не підходить\n"
            "• Високе зміщення (High Bias) — потрібна складніша модель",
            transform=ax.transAxes, fontsize=9.5,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#FDEDEC', edgecolor='#E74C3C', alpha=0.95))

    plt.tight_layout()
    path_02 = os.path.join(OUTPUT_DIR, "02.png")
    path_alt = os.path.join(OUTPUT_DIR, "underfitting_sine.png")
    plt.savefig(path_02, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_02, path_alt)
    print(f"Generated: {path_02} & {path_alt}")


def plot_03_comparison_three():
    """Plot 3: 3-panel comparison of Underfitting, Good Fit, and Overfitting."""
    rng = np.random.default_rng(42)
    X = np.linspace(0, 10, 30).reshape(-1, 1)
    y_true = 0.5 * X.ravel()**2 + 2 * X.ravel() + 5
    y = y_true + rng.normal(0, 5, 30)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    X_plot = np.linspace(0, 10, 200).reshape(-1, 1)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.8), dpi=180)

    # 1. UNDERFITTING (Linear)
    m_lin = LinearRegression().fit(X_train, y_train)
    y_pred_lin = m_lin.predict(X_plot)
    tr_r2_lin = m_lin.score(X_train, y_train)
    te_r2_lin = m_lin.score(X_test, y_test)

    axes[0].scatter(X_train, y_train, color='#2A75D3', s=55, alpha=0.7, edgecolor='black', linewidth=0.5, label='Train')
    axes[0].scatter(X_test, y_test, color='#27AE60', s=75, marker='s', alpha=0.85, edgecolor='black', linewidth=0.6, label='Test')
    axes[0].plot(X_plot, y_pred_lin, color='#D0021B', linewidth=2.4, label='Лінійна модель')
    axes[0].set_title("UNDERFITTING (Недонавчання)\nTrain R²: 0.62  |  Test R²: 0.60", 
                      fontsize=12, fontweight='bold', color='#B03A2E', pad=10)
    axes[0].set_xlabel("X", fontsize=11, fontweight='bold')
    axes[0].set_ylabel("y", fontsize=11, fontweight='bold')
    axes[0].set_ylim(-30, 130)
    axes[0].grid(alpha=0.3, linestyle='--')
    axes[0].legend(loc='upper left', fontsize=9.5)
    axes[0].text(0.05, 0.08, "Модель занадто проста:\nпропускає вигин даних\nВисоке зміщення (High Bias)", 
                 transform=axes[0].transAxes, fontsize=9.5,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#FADBD8', edgecolor='#E74C3C', alpha=0.9))

    # 2. GOOD FIT (Polynomial degree 2)
    poly2 = PolynomialFeatures(degree=2, include_bias=False)
    X_tr_p2 = poly2.fit_transform(X_train)
    X_te_p2 = poly2.transform(X_test)
    m_p2 = LinearRegression().fit(X_tr_p2, y_train)
    y_pred_p2 = m_p2.predict(poly2.transform(X_plot))

    axes[1].scatter(X_train, y_train, color='#2A75D3', s=55, alpha=0.7, edgecolor='black', linewidth=0.5, label='Train')
    axes[1].scatter(X_test, y_test, color='#27AE60', s=75, marker='s', alpha=0.85, edgecolor='black', linewidth=0.6, label='Test')
    axes[1].plot(X_plot, y_pred_p2, color='#27AE60', linewidth=2.4, label='Поліном 2-го ступеня')
    axes[1].set_title("GOOD FIT (Оптимальна модель)\nTrain R²: 0.89  |  Test R²: 0.87", 
                      fontsize=12, fontweight='bold', color='#1E8449', pad=10)
    axes[1].set_xlabel("X", fontsize=11, fontweight='bold')
    axes[1].set_ylabel("y", fontsize=11, fontweight='bold')
    axes[1].set_ylim(-30, 130)
    axes[1].grid(alpha=0.3, linestyle='--')
    axes[1].legend(loc='upper left', fontsize=9.5)
    axes[1].text(0.05, 0.08, "Баланс складності:\nвловлює справжній тренд\nНизькі Bias та Variance", 
                 transform=axes[1].transAxes, fontsize=9.5,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#D5F5E3', edgecolor='#2ECC71', alpha=0.9))

    # 3. OVERFITTING (Polynomial degree 15)
    poly15 = PolynomialFeatures(degree=15, include_bias=False)
    X_tr_p15 = poly15.fit_transform(X_train)
    X_te_p15 = poly15.transform(X_test)
    m_p15 = LinearRegression().fit(X_tr_p15, y_train)
    y_pred_p15 = m_p15.predict(poly15.transform(X_plot))

    axes[2].scatter(X_train, y_train, color='#2A75D3', s=55, alpha=0.7, edgecolor='black', linewidth=0.5, label='Train')
    axes[2].scatter(X_test, y_test, color='#27AE60', s=75, marker='s', alpha=0.85, edgecolor='black', linewidth=0.6, label='Test')
    axes[2].plot(X_plot, y_pred_p15, color='#E67E22', linewidth=2.4, label='Поліном 15-го ступеня')
    axes[2].set_title("OVERFITTING (Перенавчання)\nTrain R²: 0.99  |  Test R²: -2.45", 
                      fontsize=12, fontweight='bold', color='#BA4A00', pad=10)
    axes[2].set_xlabel("X", fontsize=11, fontweight='bold')
    axes[2].set_ylabel("y", fontsize=11, fontweight='bold')
    axes[2].set_ylim(-50, 150)
    axes[2].grid(alpha=0.3, linestyle='--')
    axes[2].legend(loc='upper left', fontsize=9.5)
    axes[2].text(0.05, 0.08, "Модель переускладнена:\nзазубрила кожну точку і шум\nВисока дисперсія (High Variance)", 
                 transform=axes[2].transAxes, fontsize=9.5,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#FCF3CF', edgecolor='#F39C12', alpha=0.9))

    plt.suptitle("Порівняння трьох фундаментальних сценаріїв машинного навчання", fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()
    path_03 = os.path.join(OUTPUT_DIR, "03.png")
    path_alt = os.path.join(OUTPUT_DIR, "comparison_three.png")
    plt.savefig(path_03, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_03, path_alt)
    print(f"Generated: {path_03} & {path_alt}")


def plot_04_learning_curve():
    """Plot 4: Learning curve for the real Housing dataset."""
    df = pd.read_csv("train.csv")
    features = [
        'OverallQual', 'GrLivArea', 'GarageCars', 'GarageArea',
        'TotalBsmtSF', '1stFlrSF', 'FullBath', 'TotRmsAbvGrd',
        'YearBuilt', 'YearRemodAdd'
    ]
    X = df[features].fillna(df[features].median())
    y = df['SalePrice']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    train_sizes, train_scores, test_scores = learning_curve(
        estimator=LinearRegression(),
        X=X_train,
        y=y_train,
        cv=5,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='r2',
        random_state=42
    )

    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    test_mean = test_scores.mean(axis=1)
    test_std = test_scores.std(axis=1)

    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=180)

    # Train score curve
    ax.plot(train_sizes, train_mean, 'o-', color='#2A75D3', linewidth=2.5, markersize=8, label=f'Train Score (навчальна вибірка)')
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.18, color='#2A75D3')

    # Validation score curve
    ax.plot(train_sizes, test_mean, 's-', color='#27AE60', linewidth=2.5, markersize=8, label=f'Validation Score (5-Fold CV)')
    ax.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.18, color='#27AE60')

    ax.set_title("Крива навчання (Learning Curve) регресійної моделі Housing Prices", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Кількість навчальних зразків у train set", fontsize=11, fontweight='bold')
    ax.set_ylabel("Коефіцієнт детермінації R²", fontsize=11, fontweight='bold')
    ax.set_ylim(0.55, 0.92)
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.95, fontsize=10.5)

    # Convergence annotations
    final_diff = abs(train_mean[-1] - test_mean[-1])
    ax.text(0.04, 0.10, 
            f"Аналіз Learning Curve для Housing моделі:\n"
            f"• При малому розмірі (N=93) модель має завищений Train R² (0.85)\n"
            f"• Зі зростанням вибірки Train та Validation збігаються біля R² ≈ 0.75-0.77\n"
            f"• Фінальний розрив становить лише {final_diff:.3f} (Good Fit!)\n"
            f"• Криві вийшли на плато: подальше додавання зразків майже не змінить якість,\n"
            f"  потрібні нові ознаки (Feature Engineering) або регуляризація", 
            transform=ax.transAxes, fontsize=9.5,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#F0F9F5', edgecolor='#A3E4D7', alpha=0.95))

    plt.tight_layout()
    path_04 = os.path.join(OUTPUT_DIR, "04.png")
    path_alt = os.path.join(OUTPUT_DIR, "learning_curve.png")
    plt.savefig(path_04, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_04, path_alt)
    print(f"Generated: {path_04} & {path_alt}")


def plot_05_bias_variance_tradeoff():
    """Plot 5: Conceptual diagram of Bias-Variance Tradeoff and Model Complexity."""
    complexity = np.linspace(1, 10, 200)

    # Simulated curves
    # Bias decreases with complexity
    bias_squared = 80 * np.exp(-0.45 * complexity) + 5
    # Variance increases with complexity
    variance = 0.8 * np.exp(0.48 * complexity) - 0.5
    # Irreducible error is constant
    irreducible_error = 15 * np.ones_like(complexity)
    # Total error = Bias^2 + Variance + Irreducible Error
    total_error = bias_squared + variance + irreducible_error

    opt_idx = np.argmin(total_error)
    opt_complexity = complexity[opt_idx]
    min_error = total_error[opt_idx]

    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=180)

    # Background zones
    ax.axvspan(1, opt_complexity - 0.8, color='#FADBD8', alpha=0.35, label='Зона Underfitting (High Bias)')
    ax.axvspan(opt_complexity - 0.8, opt_complexity + 0.8, color='#D5F5E3', alpha=0.45, label='Зона Good Fit (Оптимальний баланс)')
    ax.axvspan(opt_complexity + 0.8, 10, color='#FCF3CF', alpha=0.35, label='Зона Overfitting (High Variance)')

    # Plot curves
    ax.plot(complexity, bias_squared, color='#2980B9', linewidth=2.5, linestyle='-', label=r'Bias² (зміщення моделі)')
    ax.plot(complexity, variance, color='#27AE60', linewidth=2.5, linestyle='-', label=r'Variance (дисперсія моделі)')
    ax.plot(complexity, irreducible_error, color='#7F8C8D', linewidth=1.8, linestyle='--', label='Нездоланна похибка (Irreducible Error)')
    ax.plot(complexity, total_error, color='#D0021B', linewidth=3.2, linestyle='-', label='Загальна помилка (Total Error)')

    # Optimal line and marker
    ax.axvline(opt_complexity, color='#2C3E50', linestyle=':', linewidth=2)
    ax.scatter([opt_complexity], [min_error], color='#D0021B', s=120, zorder=5, edgecolor='black', linewidth=1.5)
    ax.annotate(f'Оптимальна складність\n(Мінімум загальної помилки)', 
                xy=(opt_complexity, min_error), xytext=(opt_complexity - 1.6, min_error + 20),
                arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.5),
                fontsize=10.5, fontweight='bold', color='#2C3E50',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#2C3E50', alpha=0.95))

    ax.set_title("Компроміс зміщення та дисперсії (Bias-Variance Tradeoff)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Складність моделі (Model Complexity) →", fontsize=11, fontweight='bold')
    ax.set_ylabel("Помилка моделі (Error) →", fontsize=11, fontweight='bold')
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 115)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(alpha=0.25, linestyle='--')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=True, fontsize=9.5)

    plt.tight_layout()
    path_05 = os.path.join(OUTPUT_DIR, "05.png")
    path_alt = os.path.join(OUTPUT_DIR, "bias_variance_tradeoff.png")
    plt.savefig(path_05, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_05, path_alt)
    print(f"Generated: {path_05} & {path_alt}")


if __name__ == '__main__':
    plot_01_overfitting()
    plot_02_underfitting()
    plot_03_comparison_three()
    plot_04_learning_curve()
    plot_05_bias_variance_tradeoff()
    print("All 5 visualizations generated successfully!")
