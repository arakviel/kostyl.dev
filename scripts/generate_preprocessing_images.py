"""
Script to generate high-quality matplotlib visualizations for 
content/16.ai-python/07.practical-regression/03.data-preprocessing.md

Visualizations:
1. 01.png: Заповнення пропусків: LotFrontage (числова) та GarageType (категоріальна)
2. 02.png (also scaling_comparison.png): Порівняння оригінальних даних, MinMaxScaler та StandardScaler для GrLivArea
3. 03.png: Data Leakage: Порівняння правильного та неправильного масштабування Train/Test
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Styling parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

OUTPUT_DIR = "public/images/ai-python/practical-regression/data-preprocessing"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv("train.csv")


def plot_01_imputation():
    """Plot 1: Imputation for LotFrontage and GarageType."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # 1. LotFrontage (Linear feet of street connected to property)
    raw_frontage = df['LotFrontage'].dropna()
    median_val = raw_frontage.median()
    mean_val = raw_frontage.mean()
    imputed_frontage = df['LotFrontage'].fillna(median_val)
    
    # Plot histogram
    ax1.hist(raw_frontage, bins=35, color='#4A90E2', alpha=0.65, edgecolor='black', label='Відомі значення (1201 буд.)')
    # Imputed bar overlay
    ax1.hist([median_val] * 259, bins=1, range=(median_val-1.5, median_val+1.5), 
             color='#F5A623', edgecolor='black', linewidth=1.2, alpha=0.9,
             label=f'Заповнені медіаною (+259 буд. = {median_val:.0f})')
    
    ax1.axvline(median_val, color='#D0021B', linestyle='--', linewidth=2, label=f'Медіана: {median_val:.0f} фт (Median)')
    ax1.axvline(mean_val, color='#417505', linestyle=':', linewidth=2, label=f'Середнє: {mean_val:.1f} фт (Mean)')
    
    ax1.set_title("LotFrontage (довжина фасаду ділянки)\nЗаповнення числових пропусків медіаною", fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel("LotFrontage (лінійна довжина фасаду, фути)", fontsize=11)
    ax1.set_ylabel("Кількість будинків", fontsize=11)
    ax1.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 2. GarageType (Categorical)
    garage_counts = df['GarageType'].value_counts()
    categories = garage_counts.index.tolist()
    counts = garage_counts.values.tolist()
    
    # Ukrainian translation mapping
    cat_translations = {
        'Attchd': 'Attchd\n(Прибудований)',
        'Detchd': 'Detchd\n(Окремий)',
        'BuiltIn': 'BuiltIn\n(Вбудований)',
        'Basment': 'Basment\n(У підвалі)',
        'CarPort': 'CarPort\n(Навіс)',
        '2Types': '2Types\n(2 типи)'
    }
    x_labels = [cat_translations.get(c, c) for c in categories]
    
    colors = ['#50E3C2' if i == 0 else '#4A90E2' for i in range(len(categories))]
    bars = ax2.bar(range(len(categories)), counts, color=colors, edgecolor='black', linewidth=0.8, alpha=0.85)
    
    # Annotate counts
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f'{int(h)}',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9.5, fontweight='bold')
        
    ax2.set_xticks(range(len(categories)))
    ax2.set_xticklabels(x_labels, fontsize=9)
    ax2.set_title("GarageType (тип гаража)\nЗаповнення категоріальних пропусків модою", fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel("Категорія гаража", fontsize=11)
    ax2.set_ylabel("Кількість будинків", fontsize=11)
    
    # Add note on mode
    ax2.text(0.95, 0.82, f"Мода: Attchd (870 будинків)\n+81 пропуск заповнено 'Attchd'", 
             transform=ax2.transAxes, ha='right', va='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F8F5', edgecolor='#50E3C2', linewidth=1.2),
             fontsize=9.5)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "01.png")
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")


def plot_02_scaling_comparison():
    """Plot 2: Original vs MinMaxScaler vs StandardScaler for GrLivArea."""
    feature = df[['GrLivArea']].values
    
    # MinMaxScaler
    min_val, max_val = feature.min(), feature.max()
    data_minmax = (feature - min_val) / (max_val - min_val)
    
    # StandardScaler
    mean_val, std_val = feature.mean(), feature.std()
    data_standard = (feature - mean_val) / std_val
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
    
    # 1. Original
    axes[0].hist(feature, bins=35, color='#4A90E2', edgecolor='black', alpha=0.75)
    axes[0].set_title('Оригінальні дані\nGrLivArea (житлова площа)', fontsize=12, fontweight='bold', pad=10)
    axes[0].set_xlabel('Площа (кв. фути)', fontsize=11)
    axes[0].set_ylabel('Кількість будинків (Частота)', fontsize=11)
    axes[0].axvline(mean_val, color='#D0021B', linestyle='--', linewidth=2, label=f'Середнє: {mean_val:.0f} фт²')
    axes[0].axvline(float(np.median(feature)), color='#417505', linestyle=':', linewidth=2, label=f'Медіана: {float(np.median(feature)):.0f} фт²')
    axes[0].legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    axes[0].grid(alpha=0.3, linestyle='--')
    
    # 2. MinMaxScaler
    axes[1].hist(data_minmax, bins=35, color='#7ED321', edgecolor='black', alpha=0.75)
    axes[1].set_title('MinMaxScaler (Нормалізація)\nДіапазон [0, 1]', fontsize=12, fontweight='bold', pad=10)
    axes[1].set_xlabel('Масштабована площа [0, 1]', fontsize=11)
    axes[1].set_ylabel('Кількість будинків (Частота)', fontsize=11)
    axes[1].axvline(data_minmax.mean(), color='#D0021B', linestyle='--', linewidth=2, label=f'Середнє: {data_minmax.mean():.2f}')
    axes[1].legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    axes[1].grid(alpha=0.3, linestyle='--')
    
    # 3. StandardScaler
    axes[2].hist(data_standard, bins=35, color='#FF6B6B', edgecolor='black', alpha=0.75)
    axes[2].set_title('StandardScaler (Стандартизація)\nЦентр μ = 0, дисперсія σ = 1', fontsize=12, fontweight='bold', pad=10)
    axes[2].set_xlabel('Стандартизована площа (z-score)', fontsize=11)
    axes[2].set_ylabel('Кількість будинків (Частота)', fontsize=11)
    axes[2].axvline(0, color='#D0021B', linestyle='--', linewidth=2, label='Середнє: 0.00')
    axes[2].axvline(1, color='#333333', linestyle=':', linewidth=1.5, label='+1 σ (станд. відхилення)')
    axes[2].axvline(-1, color='#333333', linestyle=':', linewidth=1.5, label='-1 σ')
    axes[2].legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    axes[2].grid(alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    path1 = os.path.join(OUTPUT_DIR, "02.png")
    path2 = os.path.join(OUTPUT_DIR, "scaling_comparison.png")
    plt.savefig(path1, dpi=200, bbox_inches='tight')
    plt.savefig(path2, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path1} and {path2}")


def plot_03_data_leakage():
    """Plot 3: Data leakage visualization (Correct vs Incorrect Scaling)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    rng = np.random.default_rng(42)
    train_raw = rng.normal(loc=50, scale=10, size=160)
    # Test set has shifted mean / outliers
    test_raw = np.concatenate([rng.normal(loc=65, scale=12, size=35), [110, 115]])
    
    # 1. INCORRECT: Fit on all data
    all_raw = np.concatenate([train_raw, test_raw])
    mean_all = all_raw.mean()
    std_all = all_raw.std()
    
    train_bad = (train_raw - mean_all) / std_all
    test_bad = (test_raw - mean_all) / std_all
    
    ax1.hist(train_bad, bins=20, color='#4A90E2', alpha=0.6, edgecolor='black', label='Train вибірка (80%)')
    ax1.hist(test_bad, bins=15, color='#D0021B', alpha=0.6, edgecolor='black', label='Test вибірка (20%)')
    ax1.axvline(0, color='black', linestyle='--', linewidth=1.5, label=f'Спільне середнє = 0')
    ax1.set_title("НЕПРАВИЛЬНО: Data Leakage (Fit на всіх даних)\nІнформація з Test потрапляє в Train під час масштабування", 
                  fontsize=11.5, fontweight='bold', color='#B00020', pad=10)
    ax1.set_xlabel("Масштабоване значення", fontsize=11)
    ax1.set_ylabel("Частота", fontsize=11)
    ax1.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)
    ax1.grid(alpha=0.3, linestyle='--')
    
    # 2. CORRECT: Fit ONLY on train data
    mean_train = train_raw.mean()
    std_train = train_raw.std()
    
    train_good = (train_raw - mean_train) / std_train
    test_good = (test_raw - mean_train) / std_train
    
    ax2.hist(train_good, bins=20, color='#4A90E2', alpha=0.6, edgecolor='black', label='Train вибірка (Fit тут: μ=0, σ=1)')
    ax2.hist(test_good, bins=15, color='#7ED321', alpha=0.7, edgecolor='black', label='Test вибірка (Лише Transform)')
    ax2.axvline(0, color='#4A90E2', linestyle='--', linewidth=1.8, label=f'Train середнє = 0.0')
    ax2.axvline(test_good.mean(), color='#7ED321', linestyle=':', linewidth=2, label=f'Test середнє = {test_good.mean():.2f}')
    
    ax2.set_title("ПРАВИЛЬНО: Fit тільки на Train, Transform для Train і Test\nПовна ізоляція тестових даних від процесу навчання", 
                  fontsize=11.5, fontweight='bold', color='#1B5E20', pad=10)
    ax2.set_xlabel("Масштабоване значення (параметри з Train)", fontsize=11)
    ax2.set_ylabel("Частота", fontsize=11)
    ax2.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)
    ax2.grid(alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "03.png")
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")


if __name__ == '__main__':
    plot_01_imputation()
    plot_02_scaling_comparison()
    plot_03_data_leakage()
    print("All preprocessing images successfully generated!")
