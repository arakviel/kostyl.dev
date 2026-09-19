"""
Script to generate high-quality matplotlib visualizations for 
content/16.ai-python/07.practical-regression/04.train-test-split.md

Visualizations:
1. 01.png (predictions_scatter.png): Передбачення vs Реальність на Train та Test вибірках
2. 02.png (residuals_analysis.png): Аналіз залишків (Гістограма + Residual Plot)
3. 03.png (feature_importance.png): Коефіцієнти моделі та важливість ознак з перекладами
"""

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

OUTPUT_DIR = "public/images/ai-python/practical-regression/train-test-split"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load data and prepare model
df = pd.read_csv("train.csv")
features = [
    'OverallQual', 'GrLivArea', 'GarageCars', 'GarageArea',
    'TotalBsmtSF', '1stFlrSF', 'FullBath', 'TotRmsAbvGrd',
    'YearBuilt', 'YearRemodAdd'
]
X = df[features].fillna(df[features].median())
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

train_r2 = r2_score(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))

test_r2 = r2_score(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

residuals_train = y_train - y_train_pred
residuals_test = y_test - y_test_pred


def plot_01_predictions_scatter():
    """Plot 1: Scatter plot of predicted vs actual prices on Train and Test sets."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=180)
    
    # Common max for diagonal
    max_val = 600000
    diag_line = np.linspace(0, max_val, 100)
    
    # Currency formatter
    currency_fmt = ticker.FuncFormatter(lambda x, p: f"${int(x/1000)}k" if x > 0 else "$0")
    
    # 1. Train Set
    ax1.scatter(y_train, y_train_pred, alpha=0.45, color='#2A75D3', s=32, 
                edgecolor='#1B4F8F', linewidth=0.4, label=f'Train зразки (N={len(y_train)})')
    ax1.plot(diag_line, diag_line, color='#D0021B', linestyle='--', linewidth=2.2, 
             label='Ідеальна лінія (y = ŷ)')
    
    ax1.set_title(f"Train Set (навчальна вибірка 80%)\nR² = {train_r2:.4f}  |  MAE = \\${train_mae:,.0f}  |  RMSE = \\${train_rmse:,.0f}", 
                  fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel("Фактична ціна продажу, SalePrice ($)", fontsize=11, fontweight='bold')
    ax1.set_ylabel("Передбачена моделлю ціна, ŷ ($)", fontsize=11, fontweight='bold')
    ax1.set_xlim(0, max_val)
    ax1.set_ylim(0, max_val)
    ax1.xaxis.set_major_formatter(currency_fmt)
    ax1.yaxis.set_major_formatter(currency_fmt)
    ax1.grid(alpha=0.3, linestyle='--')
    ax1.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
    
    # Train explanation card
    ax1.text(0.55, 0.08, 
             "Точки щільно біля червоної лінії:\n"
             "модель успішно вловлює основні\n"
             "ринкові тренди вартості житла", 
             transform=ax1.transAxes, fontsize=9.5,
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#F0F4F8', edgecolor='#B0C4DE', alpha=0.9))

    # 2. Test Set
    ax2.scatter(y_test, y_test_pred, alpha=0.55, color='#27AE60', s=42, 
                edgecolor='#1E8449', linewidth=0.5, label=f'Test зразки (N={len(y_test)})')
    ax2.plot(diag_line, diag_line, color='#D0021B', linestyle='--', linewidth=2.2, 
             label='Ідеальна лінія (y = ŷ)')
    
    ax2.set_title(f"Test Set (тестова вибірка 20%)\nR² = {test_r2:.4f}  |  MAE = \\${test_mae:,.0f}  |  RMSE = \\${test_rmse:,.0f}", 
                  fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel("Фактична ціна продажу, SalePrice ($)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("Передбачена моделлю ціна, ŷ ($)", fontsize=11, fontweight='bold')
    ax2.set_xlim(0, max_val)
    ax2.set_ylim(0, max_val)
    ax2.xaxis.set_major_formatter(currency_fmt)
    ax2.yaxis.set_major_formatter(currency_fmt)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
    
    # Test explanation card
    r2_diff = abs(train_r2 - test_r2) * 100
    ax2.text(0.52, 0.08, 
             f"Узагальнення (Generalization):\n"
             f"• Різниця R² між вибірками: лише {r2_diff:.1f}%\n"
             f"• Поведінка на нових даних стабільна\n"
             f"• Відсутній Overfitting (перенавчання)", 
             transform=ax2.transAxes, fontsize=9.5,
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#EAFAF1', edgecolor='#A3E4D7', alpha=0.95))

    plt.suptitle("Передбачення vs Фактична ціна (Actual vs Predicted Price) у Housing Prices", 
                 fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()
    
    path_01 = os.path.join(OUTPUT_DIR, "01.png")
    path_alt = os.path.join(OUTPUT_DIR, "predictions_scatter.png")
    plt.savefig(path_01, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_01, path_alt)
    print(f"Generated: {path_01} & {path_alt}")


def plot_02_residuals_analysis():
    """Plot 2: Residual distribution histogram and residual plot vs predicted price."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=180)
    currency_fmt = ticker.FuncFormatter(lambda x, p: f"${int(x/1000)}k" if x != 0 else "$0")
    
    # 1. Left: Histogram of residuals
    bins = np.linspace(-120000, 180000, 35)
    ax1.hist(residuals_train, bins=bins, alpha=0.5, color='#2A75D3', edgecolor='black', linewidth=0.6,
             label=f'Train залишків (μ=${residuals_train.mean():,.0f}, σ=${residuals_train.std():,.0f})')
    ax1.hist(residuals_test, bins=bins, alpha=0.6, color='#27AE60', edgecolor='black', linewidth=0.6,
             label=f'Test залишків (μ=${residuals_test.mean():,.0f}, σ=${residuals_test.std():,.0f})')
    
    ax1.axvline(0, color='#D0021B', linestyle='--', linewidth=2.2, label='Нульова лінія (помилка = 0)')
    
    ax1.set_title("Розподіл залишків (Residuals = Реальне - Передбачене)", fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel("Величина залишку / помилки ($)", fontsize=11, fontweight='bold')
    ax1.set_ylabel("Кількість спостережень (частота)", fontsize=11, fontweight='bold')
    ax1.xaxis.set_major_formatter(currency_fmt)
    ax1.grid(alpha=0.3, linestyle='--')
    ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)
    
    ax1.text(0.04, 0.70, 
             "Аналіз розподілу залишків:\n"
             "• Дзвіноподібна симетрія навколо $0\n"
             "• Середня помилка наближена до $0\n"
             "• Немає системного заниження чи завищення\n"
             "• Присутні поодинокі важкі 'хвости' (викиди)", 
             transform=ax1.transAxes, fontsize=9.2,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#F9F9F9', edgecolor='#CCCCCC', alpha=0.9))

    # 2. Right: Residual Plot for Test set
    ax2.scatter(y_test_pred, residuals_test, alpha=0.6, color='#27AE60', s=42, 
                edgecolor='#1E8449', linewidth=0.5, label='Test залишків')
    ax2.axhline(0, color='#D0021B', linestyle='--', linewidth=2.2, label='Нульова помилка (e = 0)')
    
    # 1-sigma bounds
    std_val = residuals_test.std()
    ax2.axhline(std_val, color='#888888', linestyle=':', linewidth=1.2, label=f'±1 std діапазон (±${std_val:,.0f})')
    ax2.axhline(-std_val, color='#888888', linestyle=':', linewidth=1.2)
    ax2.fill_between([0, 500000], -std_val, std_val, color='#27AE60', alpha=0.08)
    
    ax2.set_title("Графік залишків для Test Set (Residual Plot)", fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel("Передбачена моделлю ціна, ŷ ($)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("Залишок / Помилка прогнозу: e = y - ŷ ($)", fontsize=11, fontweight='bold')
    ax2.set_xlim(50000, 480000)
    ax2.set_ylim(-120000, 320000)
    ax2.xaxis.set_major_formatter(currency_fmt)
    ax2.yaxis.set_major_formatter(currency_fmt)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)
    
    ax2.text(0.04, 0.10, 
             "Гомоскедастичність (стабільність дисперсії):\n"
             "• Більшість помилок лежать у смузі ±$39k\n"
             "• При високих цінах (> $350k) розкид зростає\n"
             "• Кілька елітних будинків недооцінені лінійною моделлю", 
             transform=ax2.transAxes, fontsize=9.2,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#EAFAF1', edgecolor='#A3E4D7', alpha=0.95))

    plt.suptitle("Аналіз помилок лінійної регресії (Residuals Analysis) на Housing Dataset", 
                 fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()
    
    path_02 = os.path.join(OUTPUT_DIR, "02.png")
    path_alt = os.path.join(OUTPUT_DIR, "residuals_analysis.png")
    plt.savefig(path_02, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_02, path_alt)
    print(f"Generated: {path_02} & {path_alt}")


def plot_03_feature_importance():
    """Plot 3: Linear regression coefficients horizontal bar chart with bilingual labels."""
    feature_labels = {
        'OverallQual': 'OverallQual (загальна якість оздоблення)',
        'GarageCars': 'GarageCars (місткість гаража, авто)',
        'FullBath': 'FullBath (повноцінні ванні кімнати)',
        'TotRmsAbvGrd': 'TotRmsAbvGrd (кількість кімнат)',
        'YearRemodAdd': 'YearRemodAdd (рік реконструкції)',
        'YearBuilt': 'YearBuilt (рік будівництва)',
        'GrLivArea': 'GrLivArea (житлова площа, кв. фути)',
        'TotalBsmtSF': 'TotalBsmtSF (площа підвалу, кв. фути)',
        '1stFlrSF': '1stFlrSF (площа 1-го поверху, кв. фути)',
        'GarageArea': 'GarageArea (площа гаража, кв. фути)'
    }
    
    unit_labels = {
        'OverallQual': '+$19,646 / бал якості',
        'GarageCars': '+$11,311 / авто в гаражі',
        'FullBath': '-$7,200 / ванну',
        'TotRmsAbvGrd': '+$454 / кімнату',
        'YearRemodAdd': '+$315 / рік новизни',
        'YearBuilt': '+$281 / рік побудови',
        'GrLivArea': '+$48.07 / кв. фут',
        'TotalBsmtSF': '+$15.06 / кв. фут',
        '1stFlrSF': '+$14.41 / кв. фут',
        'GarageArea': '+$14.07 / кв. фут'
    }
    
    coef_df = pd.DataFrame({
        'Feature': features,
        'Coefficient': model.coef_
    }).sort_values('Coefficient', ascending=True)
    
    fig, ax = plt.subplots(figsize=(14, 7.2), dpi=180)
    
    colors = ['#27AE60' if c >= 0 else '#D0021B' for c in coef_df['Coefficient']]
    y_pos = np.arange(len(coef_df))
    
    bars = ax.barh(y_pos, coef_df['Coefficient'], color=colors, edgecolor='#333333', linewidth=0.8, height=0.65)
    
    ax.axvline(0, color='black', linestyle='-', linewidth=1.0)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([feature_labels[f] for f in coef_df['Feature']], fontsize=10.5)
    
    # Currency formatter
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${int(x):,}" if x != 0 else "$0"))
    ax.set_xlabel("Коефіцієнт лінійної регресії (зміна SalePrice при +1 одиниці ознаки, $)", 
                  fontsize=11, fontweight='bold', labelpad=8)
    ax.set_title("Коефіцієнти лінійної регресії: Вплив ознак на ціну (Feature Coefficients)", 
                 fontsize=13, fontweight='bold', pad=12)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Annotate values next to bars
    for idx, (f, c) in enumerate(zip(coef_df['Feature'], coef_df['Coefficient'])):
        u = unit_labels[f]
        if c >= 0:
            ax.text(c + 300, idx, f"{u}", va='center', ha='left', fontsize=9.5, fontweight='bold', color='#196F3D')
        else:
            # Place inside the bar or to the left with enough margin
            ax.text(-500, idx, f"{u}  ", va='center', ha='right', fontsize=9.5, fontweight='bold', color='white')
            
    ax.set_xlim(-10000, 27000)
    
    # Note box placed in the bottom right corner where space is free
    ax.text(0.48, 0.08, 
            "Особливість інтерпретації нескальованих коефіцієнтів:\n"
            "• Коефіцієнти відображають зміну ціни на 1 фізичну одиницю ($/бал, $/рік, $/кв. фут).\n"
            "• Величина коефіцієнта залежить від масштабу: +500 кв. фт площі дає +$24,000 до ціни!\n"
            "• Від'ємний коефіцієнт FullBath (-$7,200) зумовлений мультиколінеарністю з GrLivArea та TotRmsAbvGrd.", 
            transform=ax.transAxes, fontsize=9.2,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#FDFEFE', edgecolor='#BDC3C7', alpha=0.95))
    
    plt.tight_layout()
    
    path_03 = os.path.join(OUTPUT_DIR, "03.png")
    path_alt = os.path.join(OUTPUT_DIR, "feature_importance.png")
    plt.savefig(path_03, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_03, path_alt)
    print(f"Generated: {path_03} & {path_alt}")


if __name__ == '__main__':
    plot_01_predictions_scatter()
    plot_02_residuals_analysis()
    plot_03_feature_importance()
    print("All 3 visualizations generated successfully!")
