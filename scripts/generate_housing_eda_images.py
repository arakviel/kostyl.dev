#!/usr/bin/env python3
"""
Скрипт для генерації всіх 6 графіків для лекції:
content/16.ai-python/07.practical-regression/02.housing-dataset-eda.md

Додано українські переклади назв ознак у дужках для максимальної навчальної зрозумілості.
Зберігає графіки у:
public/images/ai-python/practical-regression/housing-dataset-eda/
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Налаштування стилю
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
    "public", "images", "ai-python", "practical-regression", "housing-dataset-eda"
)
os.makedirs(BASE_DIR, exist_ok=True)

CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data", "train.csv"
)

FEATURE_TRANSLATIONS = {
    'PoolQC': 'PoolQC (Якість басейну)',
    'MiscFeature': 'MiscFeature (Додаткові зручності)',
    'Alley': 'Alley (Тип провулка)',
    'Fence': 'Fence (Огорожа)',
    'MasVnrType': 'MasVnrType (Тип облицювання)',
    'FireplaceQu': 'FireplaceQu (Якість каміна)',
    'LotFrontage': 'LotFrontage (Фасад ділянки)',
    'GarageType': 'GarageType (Тип гаража)',
    'GarageYrBlt': 'GarageYrBlt (Рік гаража)',
    'GarageFinish': 'GarageFinish (Оздоблення гаража)',
    'GarageQual': 'GarageQual (Якість гаража)',
    'GarageCond': 'GarageCond (Стан гаража)',
    'BsmtFinType2': 'BsmtFinType2 (Тип оздобл. підвалу 2)',
    'BsmtExposure': 'BsmtExposure (Освітленість підвалу)',
    'BsmtFinType1': 'BsmtFinType1 (Тип оздобл. підвалу 1)',
    'BsmtCond': 'BsmtCond (Стан підвалу)',
    'BsmtQual': 'BsmtQual (Якість підвалу)',
    'MasVnrArea': 'MasVnrArea (Площа облицювання)',
    'Electrical': 'Electrical (Електрика)',
    'OverallQual': 'OverallQual (Загальна якість)',
    'GrLivArea': 'GrLivArea (Житлова площа)',
    'GarageCars': 'GarageCars (Місткість гаража, авто)',
    'GarageArea': 'GarageArea (Площа гаража)',
    'TotalBsmtSF': 'TotalBsmtSF (Площа підвалу)',
    '1stFlrSF': '1stFlrSF (Площа 1-го поверху)',
    'FullBath': 'FullBath (Повноцінні ванні)',
    'TotRmsAbvGrd': 'TotRmsAbvGrd (Кімнати над землею)',
    'YearBuilt': 'YearBuilt (Рік побудови)',
    'YearRemodAdd': 'YearRemodAdd (Рік реконструкції)',
    'Fireplaces': 'Fireplaces (Каміни)',
    'BsmtFinSF1': 'BsmtFinSF1 (Площа 1-го оздобл. підвалу)',
    'LotArea': 'LotArea (Площа ділянки)',
    'SalePrice': 'SalePrice (Ціна продажу)',
}

def tr(feature_name: str) -> str:
    """Повертає назву ознаки з перекладом у дужках."""
    return FEATURE_TRANSLATIONS.get(feature_name, feature_name)

def load_data():
    if not os.path.exists(CSV_PATH):
        url = "https://raw.githubusercontent.com/manavkapadnis/House-prices-Advanced-regression-techniques/master/train.csv"
        print(f"Завантаження датасету з {url}...")
        df = pd.read_csv(url)
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        df.to_csv(CSV_PATH, index=False)
        return df
    return pd.read_csv(CSV_PATH)

def generate_plot_1(df):
    """01.png: Топ-19 стовпців з пропусками з перекладами"""
    print("Генерація 01.png (пропуски з перекладами)...")
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    missing_percent = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Стовпець': [tr(col) for col in missing.index],
        'Відсоток': missing_percent.values
    })

    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=200)
    ax.barh(range(len(missing_df)), missing_df['Відсоток'], color='coral', edgecolor='black', alpha=0.85)
    ax.set_yticks(range(len(missing_df)))
    ax.set_yticklabels(missing_df['Стовпець'], fontsize=10)
    ax.set_xlabel('Відсоток пропусків (%)', fontsize=12)
    ax.set_title('Топ-19 стовпців з пропусками (пропущені значення в датасеті)', fontsize=14, fontweight='bold', pad=12)
    ax.axvline(50, color='red', linestyle='--', linewidth=2, label='50% поріг для видалення/обробки')
    ax.legend(fontsize=11, loc='lower right', framealpha=0.95)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()

    out_path = os.path.join(BASE_DIR, '01.png')
    fig.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Збережено: {out_path}")

def generate_plot_2(df):
    """02.png: Розподіл цін на будинки (гістограма + boxplot)"""
    print("Генерація 02.png (розподіл цін)...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=200)

    # Гістограма
    ax1.hist(df['SalePrice'], bins=50, color='skyblue', edgecolor='black', alpha=0.75)
    mean_val = df['SalePrice'].mean()
    median_val = df['SalePrice'].median()
    ax1.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                label=f'Середня ціна: ${mean_val:,.0f}')
    ax1.axvline(median_val, color='green', linestyle='--', linewidth=2,
                label=f'Медіанна ціна: ${median_val:,.0f}')
    ax1.set_xlabel('Ціна будинку SalePrice ($)', fontsize=11)
    ax1.set_ylabel('Кількість будинків', fontsize=11)
    ax1.set_title('Розподіл цін SalePrice (правостороння асиметрія)', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10, framealpha=0.95)
    ax1.grid(alpha=0.3, linestyle='--')

    # Box plot
    ax2.boxplot(df['SalePrice'], orientation='horizontal', patch_artist=True,
                boxprops=dict(facecolor='lightgreen', alpha=0.7),
                medianprops=dict(color='red', linewidth=2))
    ax2.set_xlabel('Ціна будинку SalePrice ($)', fontsize=11)
    ax2.set_yticks([1])
    ax2.set_yticklabels(['SalePrice\n(Ціна продажу)'], fontsize=10)
    ax2.set_title('Box Plot — виявлення екстремальних викидів (> $500k)', fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.3, linestyle='--')

    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, '02.png')
    fig.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Збережено: {out_path}")

def generate_plot_3(df):
    """03.png: Топ-10 ознак за кореляцією з ціною з перекладами"""
    print("Генерація 03.png (кореляція з ціною з перекладами)...")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    correlations = df[numeric_cols].corr()['SalePrice'].sort_values(ascending=False)
    top_corr = correlations[1:11]  # без SalePrice

    labels = [tr(col) for col in top_corr.index]

    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=200)
    colors = ['forestgreen' if x > 0.6 else 'orange' for x in top_corr.values]
    ax.barh(range(len(top_corr)), top_corr.values, color=colors, edgecolor='black', alpha=0.85)
    ax.set_yticks(range(len(top_corr)))
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel('Коефіцієнт лінійної кореляції Пірсона з SalePrice', fontsize=12)
    ax.set_title('Топ-10 ознак за кореляцією з ціною будинку', fontsize=14, fontweight='bold', pad=12)
    ax.axvline(0.5, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Поріг сильного зв\'язку (0.5)')
    ax.invert_yaxis()
    ax.legend(fontsize=10, loc='lower right', framealpha=0.95)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()

    out_path = os.path.join(BASE_DIR, '03.png')
    fig.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Збережено: {out_path}")

def generate_plot_4(df):
    """04.png: Кореляційна матриця топ-15 ознак з перекладами"""
    print("Генерація 04.png (heatmap з перекладами)...")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    correlations = df[numeric_cols].corr()['SalePrice'].sort_values(ascending=False)
    top_features = correlations[1:16].index.tolist() + ['SalePrice']
    corr_matrix = df[top_features].corr()

    # Компактні підписи для теплової карти
    SHORT_LABELS = {
        'OverallQual': 'OverallQual (Якість)',
        'GrLivArea': 'GrLivArea (Житл. площа)',
        'GarageCars': 'GarageCars (Гараж, авто)',
        'GarageArea': 'GarageArea (Площа гаража)',
        'TotalBsmtSF': 'TotalBsmtSF (Площа підвалу)',
        '1stFlrSF': '1stFlrSF (1-й поверх)',
        'FullBath': 'FullBath (Ванні)',
        'TotRmsAbvGrd': 'TotRmsAbvGrd (Кімнати)',
        'YearBuilt': 'YearBuilt (Рік побудови)',
        'YearRemodAdd': 'YearRemodAdd (Рік реконстр.)',
        'GarageYrBlt': 'GarageYrBlt (Рік гаража)',
        'MasVnrArea': 'MasVnrArea (Облицювання)',
        'Fireplaces': 'Fireplaces (Каміни)',
        'BsmtFinSF1': 'BsmtFinSF1 (Оздобл. підвал)',
        'LotFrontage': 'LotFrontage (Фасад ділянки)',
        'SalePrice': 'SalePrice (Ціна продажу)',
    }
    display_labels = [SHORT_LABELS.get(col, col) for col in top_features]

    fig, ax = plt.subplots(figsize=(15.5, 13.5), dpi=200)
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
        vmin=-1, vmax=1,
        xticklabels=display_labels,
        yticklabels=display_labels,
        annot_kws={"size": 10},
        ax=ax
    )
    ax.set_title('Кореляційна матриця топ-15 ознак (виявлення мультиколінеарності)', fontsize=15, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()

    out_path = os.path.join(BASE_DIR, '04.png')
    fig.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Збережено: {out_path}")

def generate_plot_5(df):
    """05.png: Scatter Plots Топ-4 ознаки vs Ціна з перекладами"""
    print("Генерація 05.png (scatter plots з перекладами)...")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    correlations = df[numeric_cols].corr()['SalePrice'].sort_values(ascending=False)
    
    features_info = [
        ('OverallQual', 'Загальна якість (шкала 1-10)'),
        ('GrLivArea', 'Житлова площа над землею (кв. фути)'),
        ('GarageCars', 'Місткість гаража (кількість авто)'),
        ('TotalBsmtSF', 'Загальна площа підвалу (кв. фути)')
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10.5), dpi=200)
    axes = axes.flatten()

    for i, (col, desc) in enumerate(features_info):
        axes[i].scatter(df[col], df['SalePrice'], alpha=0.5, color='dodgerblue', edgecolor='black', s=32)
        axes[i].set_xlabel(f'{col} — {desc}', fontsize=11)
        axes[i].set_ylabel('SalePrice — Ціна будинку ($)', fontsize=11)
        axes[i].set_title(f'{col} ({desc.split("(")[0].strip()}) vs Ціна (corr={correlations[col]:.3f})', 
                          fontsize=12, fontweight='bold')
        axes[i].grid(alpha=0.3, linestyle='--')

    plt.suptitle('Scatter Plots: Топ-4 ознаки vs Ціна будинку', fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()

    out_path = os.path.join(BASE_DIR, '05.png')
    fig.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Збережено: {out_path}")

def generate_plot_6(df):
    """06.png: Box Plots для виявлення викидів з перекладами"""
    print("Генерація 06.png (box plots з перекладами)...")
    features_info = [
        ('GrLivArea', 'Житлова площа', 'Площа (кв. фути)'),
        ('TotalBsmtSF', 'Площа підвалу', 'Площа (кв. фути)'),
        ('LotArea', 'Площа ділянки', 'Площа (кв. фути)'),
        ('SalePrice', 'Ціна продажу', 'Ціна ($)')
    ]

    fig, axes = plt.subplots(1, 4, figsize=(16, 4.5), dpi=200)

    for i, (col, ua_name, y_unit) in enumerate(features_info):
        axes[i].boxplot(df[col].dropna(), patch_artist=True,
                        boxprops=dict(facecolor='lightyellow', alpha=0.7),
                        medianprops=dict(color='red', linewidth=2),
                        whiskerprops=dict(linewidth=1.5),
                        capprops=dict(linewidth=1.5))
        axes[i].set_ylabel(y_unit, fontsize=11)
        axes[i].set_title(f'{col}\n({ua_name})', fontsize=12, fontweight='bold')
        axes[i].set_xticks([1])
        axes[i].set_xticklabels([col], fontsize=10)
        axes[i].grid(axis='y', alpha=0.3, linestyle='--')

    plt.suptitle('Box Plots — виявлення екстремальних викидів у ключових ознаках', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    out_path = os.path.join(BASE_DIR, '06.png')
    fig.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Збережено: {out_path}")

if __name__ == '__main__':
    df = load_data()
    print(f"Дані завантажено: {df.shape[0]} рядків × {df.shape[1]} стовпців")
    generate_plot_1(df)
    generate_plot_2(df)
    generate_plot_3(df)
    generate_plot_4(df)
    generate_plot_5(df)
    generate_plot_6(df)
    print("Всі 6 зображень з українськими перекладами успішно згенеровано!")
