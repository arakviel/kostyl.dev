"""
Script to generate high-quality matplotlib visualizations for 
content/16.ai-python/07.practical-regression/06.cross-validation.md

Visualizations:
1. 01.png (01_price_distribution.png): Порівняння розподілу цін у найкращому та найгіршому split
2. 02.png (02_kfold_scheme.png): Інфографічна схема K-Fold Cross-Validation (k=5)
3. 03.png (02_boxplot_models.png / 03_boxplot_models.png): Box Plot порівняння 5 моделей через 5-Fold CV
4. 04.png (04_stratified_kfold.png): Схема порівняння Regular K-Fold vs Stratified K-Fold для класифікації
5. 05.png (05_cv_workflow.png): Повний інженерний workflow: Train/Validation/Test Split + Cross-Validation
"""

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.model_selection import train_test_split, cross_validate, KFold, StratifiedKFold
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_classification

# Styling parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

OUTPUT_DIR = "public/images/ai-python/practical-regression/cross-validation"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_01_price_distribution():
    """Plot 1: Price distribution comparison for best vs worst train/test split."""
    df = pd.read_csv('train.csv')
    features = [
        'OverallQual', 'GrLivArea', 'GarageCars', 'GarageArea',
        'TotalBsmtSF', '1stFlrSF', 'FullBath', 'TotRmsAbvGrd',
        'YearBuilt', 'YearRemodAdd'
    ]
    X = df[features].fillna(df[features].median())
    y = df['SalePrice']

    # Seed 6 (Best in tutorial, R² = 0.8256)
    X_tr6, X_te6, y_tr6, y_te6 = train_test_split(X, y, test_size=0.2, random_state=6)
    # Seed 7 (Worst in tutorial, R² = 0.7534)
    X_tr7, X_te7, y_tr7, y_te7 = train_test_split(X, y, test_size=0.2, random_state=7)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8), dpi=180)

    # Best Split (seed=6)
    axes[0].hist(y_tr6, bins=30, alpha=0.6, label=f'Train (80%, N={len(y_tr6)})', color='#2A75D3', edgecolor='black', linewidth=0.5)
    axes[0].hist(y_te6, bins=15, alpha=0.75, label=f'Test (20%, N={len(y_te6)})', color='#27AE60', edgecolor='black', linewidth=0.6)
    axes[0].axvline(y_tr6.mean(), color='#1B4F72', linestyle='--', linewidth=2.2, label=f'Train mean: ${y_tr6.mean():,.0f}')
    axes[0].axvline(y_te6.mean(), color='#145A32', linestyle='-', linewidth=2.2, label=f'Test mean: ${y_te6.mean():,.0f}')
    axes[0].set_xlabel('SalePrice (Ціна продажу, $)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Кількість будинків (Частота)', fontsize=11, fontweight='bold')
    axes[0].set_title('Найкращий split (seed=6, R² = 0.8256)\nВдалий збіг розподілів вибірок', fontsize=12, fontweight='bold', color='#1E8449', pad=10)
    axes[0].legend(fontsize=9.5, framealpha=0.95)
    axes[0].grid(alpha=0.3, linestyle='--')
    axes[0].set_xlim(0, 600000)
    axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda val, loc: f'${int(val/1000)}k'))
    axes[0].text(0.48, 0.42, 
                 f"Різниця середніх: ${abs(y_tr6.mean() - y_te6.mean()):,.0f}\n"
                 f"• Тестовий набір гарно повторює\n  форму навчального розподілу\n"
                 f"• Модель отримує завищену оцінку R²", 
                 transform=axes[0].transAxes, fontsize=9.5,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#EAFAF1', edgecolor='#2ECC71', alpha=0.95))

    # Worst Split (seed=7)
    axes[1].hist(y_tr7, bins=30, alpha=0.6, label=f'Train (80%, N={len(y_tr7)})', color='#2A75D3', edgecolor='black', linewidth=0.5)
    axes[1].hist(y_te7, bins=15, alpha=0.75, label=f'Test (20%, N={len(y_te7)})', color='#E67E22', edgecolor='black', linewidth=0.6)
    axes[1].axvline(y_tr7.mean(), color='#1B4F72', linestyle='--', linewidth=2.2, label=f'Train mean: ${y_tr7.mean():,.0f}')
    axes[1].axvline(y_te7.mean(), color='#B03A2E', linestyle='-', linewidth=2.2, label=f'Test mean: ${y_te7.mean():,.0f}')
    axes[1].set_xlabel('SalePrice (Ціна продажу, $)', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Кількість будинків (Частота)', fontsize=11, fontweight='bold')
    axes[1].set_title('Найгірший split (seed=7, R² = 0.7534)\nНезбалансований зсув у вибірках', fontsize=12, fontweight='bold', color='#B03A2E', pad=10)
    axes[1].legend(fontsize=9.5, framealpha=0.95)
    axes[1].grid(alpha=0.3, linestyle='--')
    axes[1].set_xlim(0, 600000)
    axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda val, loc: f'${int(val/1000)}k'))
    axes[1].text(0.48, 0.42, 
                 f"Різниця середніх: ${abs(y_tr7.mean() - y_te7.mean()):,.0f}\n"
                 f"• У test потрапило більше дорогих об'єктів\n"
                 f"• Розрив у якості: 7.22 процентних пункти\n"
                 f"• Оцінка залежить від випадковості split", 
                 transform=axes[1].transAxes, fontsize=9.5,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#FDEDEC', edgecolor='#E74C3C', alpha=0.95))

    plt.suptitle("Проблема одного train/test split: розкид оцінки якості моделі", fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()

    path_01 = os.path.join(OUTPUT_DIR, "01.png")
    path_alt = os.path.join(OUTPUT_DIR, "01_price_distribution.png")
    plt.savefig(path_01, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_01, path_alt)
    print(f"Generated: {path_01} & {path_alt}")


def plot_02_kfold_scheme():
    """Plot 2: Diagram of 5-Fold Cross-Validation scheme."""
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=180)

    n_folds = 5
    block_width = 1.6
    block_height = 0.55
    spacing_x = 0.15
    spacing_y = 0.85
    start_x = 1.8
    start_y = 4.0

    scores = [0.7821, 0.7654, 0.7912, 0.7534, 0.7789]

    # Draw Header
    ax.text(start_x + 2.5 * (block_width + spacing_x) - 0.5, start_y + 1.1, 
            "Повний датасет (100% даних, розбитий на 5 рівних блоків по 20%)", 
            ha='center', fontsize=12, fontweight='bold', color='#2C3E50')

    # Draw Fold blocks for each iteration
    for i in range(n_folds):
        y_pos = start_y - i * spacing_y
        iter_num = i + 1

        # Label for iteration
        ax.text(start_x - 0.3, y_pos + block_height/2, f"Ітерація {iter_num}:", 
                ha='right', va='center', fontsize=11, fontweight='bold', color='#333333')

        for f in range(n_folds):
            x_pos = start_x + f * (block_width + spacing_x)
            is_test = (f == i)

            color = '#27AE60' if is_test else '#2A75D3'
            label_text = "TEST (20%)" if is_test else "TRAIN"

            rect = patches.FancyBboxPatch(
                (x_pos, y_pos), block_width, block_height,
                boxstyle="round,pad=0.04,rounding_size=0.08",
                facecolor=color, edgecolor='#1B4F72' if not is_test else '#145A32',
                linewidth=1.2, alpha=0.9
            )
            ax.add_patch(rect)
            ax.text(x_pos + block_width/2, y_pos + block_height/2, label_text, 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)

        # Arrow and Fold Score
        arrow_start_x = start_x + n_folds * (block_width + spacing_x) + 0.1
        ax.annotate('', xy=(arrow_start_x + 0.6, y_pos + block_height/2), 
                    xytext=(arrow_start_x, y_pos + block_height/2),
                    arrowprops=dict(arrowstyle="->", color='#555555', lw=1.5))
        
        ax.text(arrow_start_x + 0.7, y_pos + block_height/2, f"Fold {iter_num} R² = {scores[i]:.4f}", 
                ha='left', va='center', fontsize=10.5, fontweight='bold', color='#2C3E50',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#F4F6F7', edgecolor='#BDC3C7', alpha=0.9))

    # Summary box at bottom
    mean_val = np.mean(scores)
    std_val = np.std(scores)
    summary_text = (
        f"Усереднення результатів 5-Fold Cross-Validation:\n"
        f"• Середнє R² = {mean_val:.4f}  |  Std = {std_val:.4f}  |  95% ДІ = [{mean_val-2*std_val:.4f}, {mean_val+2*std_val:.4f}]\n"
        f"• Кожен зразок потрапляє у TEST рівно 1 раз і у TRAIN 4 рази (100% використання вибірки)"
    )
    ax.text(start_x + 2.5 * (block_width + spacing_x) - 0.5, start_y - n_folds * spacing_y + 0.15,
            summary_text, ha='center', va='top', fontsize=10.5,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#E8F8F5', edgecolor='#1ABC9C', alpha=0.95))

    ax.set_xlim(0, 13.2)
    ax.set_ylim(start_y - n_folds * spacing_y - 0.8, start_y + 1.6)
    ax.axis('off')
    plt.title("Схема 5-Fold Cross-Validation: усунення випадковості одного розбиття", 
              fontsize=13, fontweight='bold', pad=10)
    plt.tight_layout()

    path_02 = os.path.join(OUTPUT_DIR, "02.png")
    path_alt = os.path.join(OUTPUT_DIR, "02_kfold_scheme.png")
    plt.savefig(path_02, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_02, path_alt)
    print(f"Generated: {path_02} & {path_alt}")


def plot_03_boxplot_models():
    """Plot 3: Box plot comparing multiple models evaluated via 5-Fold CV."""
    df = pd.read_csv('train.csv')
    features = [
        'OverallQual', 'GrLivArea', 'GarageCars', 'GarageArea',
        'TotalBsmtSF', '1stFlrSF', 'FullBath', 'TotRmsAbvGrd',
        'YearBuilt', 'YearRemodAdd'
    ]
    X = df[features].fillna(df[features].median())
    y = df['SalePrice']

    models = {
        'LinearRegression': LinearRegression(),
        'Ridge (α=1.0)': Ridge(alpha=1.0),
        'Ridge (α=10.0)': Ridge(alpha=10.0),
        'DecisionTree': DecisionTreeRegressor(max_depth=8, random_state=42),
        'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    }

    # Collect CV scores
    scores_data = {}
    for name, model in models.items():
        res = cross_validate(model, X, y, cv=5, scoring='r2', n_jobs=-1)
        scores_data[name] = res['test_score']

    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=180)

    colors = ['#2A75D3', '#5DADE2', '#48C9B0', '#E67E22', '#27AE60']

    # Draw boxplot
    bp = ax.boxplot(
        list(scores_data.values()),
        tick_labels=list(scores_data.keys()),
        patch_artist=True,
        widths=0.55,
        whiskerprops=dict(color='#2C3E50', linewidth=1.4),
        capprops=dict(color='#2C3E50', linewidth=1.4),
        medianprops=dict(color='#D0021B', linewidth=2.2),
        flierprops=dict(marker='o', markerfacecolor='#D0021B', markersize=6, markeredgecolor='black')
    )

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
        patch.set_edgecolor('#2C3E50')
        patch.set_linewidth(1.3)

    # Overlay individual fold points with jitter
    rng = np.random.default_rng(42)
    means = []
    for idx, (name, vals) in enumerate(scores_data.items(), 1):
        jitter = rng.normal(0, 0.04, size=len(vals))
        ax.scatter(np.full_like(vals, idx) + jitter, vals, color='#1B4F72', alpha=0.75, s=40, zorder=5, edgecolor='black', linewidth=0.5)
        means.append(vals.mean())

    # Line of means
    ax.plot(range(1, len(means) + 1), means, 's--', color='#1E8449', linewidth=2.2, markersize=8, 
            label='Середнє значення R² по 5 fold\'ам', zorder=6)

    # Print mean value above each box
    for idx, (m, vals) in enumerate(zip(means, scores_data.values()), 1):
        ax.text(idx, max(vals) + 0.012, f"R²={m:.3f}\n±{vals.std():.3f}", 
                ha='center', fontsize=9, fontweight='bold', color='#2C3E50')

    ax.set_ylabel('Коефіцієнт детермінації R²', fontsize=11.5, fontweight='bold')
    ax.set_title('Об\'єктивне порівняння стабільності та якості моделей (5-Fold Cross-Validation)', 
                 fontsize=13, fontweight='bold', pad=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0.60, 0.93)
    ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.95, fontsize=10)

    # Summary Annotation
    ax.text(0.53, 0.05,
            "Висновки з Box Plot:\n"
            "• RandomForest має найвищу якість (R² ≈ 0.83-0.85) та найменшу дисперсію\n"
            "• Ridge та LinearRegression показують ідентичні результати (L2 не покращує якість)\n"
            "• DecisionTree має найбільшу дисперсію по fold'ам (чутливе до вибірки)",
            transform=ax.transAxes, fontsize=9.5,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F9EBEA', edgecolor='#E74C3C', alpha=0.95))

    plt.xticks(fontsize=10.5, fontweight='bold')
    plt.tight_layout()

    path_03 = os.path.join(OUTPUT_DIR, "03.png")
    path_alt1 = os.path.join(OUTPUT_DIR, "02_boxplot_models.png")
    path_alt2 = os.path.join(OUTPUT_DIR, "03_boxplot_models.png")
    plt.savefig(path_03, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_03, path_alt1)
    shutil.copyfile(path_03, path_alt2)
    print(f"Generated: {path_03}, {path_alt1} & {path_alt2}")


def plot_04_stratified_kfold():
    """Plot 4: Comparison of Regular K-Fold vs Stratified K-Fold for imbalanced classification."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), dpi=180)

    folds = ['Fold 1', 'Fold 2', 'Fold 3', 'Fold 4', 'Fold 5']
    # Example values from tutorial
    regular_c1 = [12.5, 9.0, 8.5, 11.0, 9.0]
    regular_c0 = [100 - x for x in regular_c1]

    stratified_c1 = [10.0, 10.0, 10.0, 10.0, 10.0]
    stratified_c0 = [90.0, 90.0, 90.0, 90.0, 90.0]

    y_pos = np.arange(len(folds))

    # 1. Regular K-Fold
    axes[0].barh(y_pos, regular_c0, color='#2A75D3', alpha=0.7, edgecolor='black', label='Клас 0 (Мажоритарний, ~90%)')
    axes[0].barh(y_pos, regular_c1, left=regular_c0, color='#E74C3C', alpha=0.85, edgecolor='black', label='Клас 1 (Міноритарний, ~10%)')
    axes[0].axvline(90, color='#C0392B', linestyle='--', linewidth=2, label='Цільова межа (90% / 10%)')
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels(folds, fontsize=10.5, fontweight='bold')
    axes[0].set_xlabel('Відсоток зразків у тестовому fold\'і (%)', fontsize=11, fontweight='bold')
    axes[0].set_title('Звичайний K-Fold (Випадковий розкид)\nНерівномірна частка рідкісного класу', fontsize=12, fontweight='bold', color='#B03A2E', pad=10)
    axes[0].set_xlim(0, 100)
    axes[0].grid(axis='x', alpha=0.3, linestyle='--')
    axes[0].legend(loc='lower left', fontsize=9, framealpha=0.95)

    for idx, c1 in enumerate(regular_c1):
        axes[0].text(94, idx, f"{c1:.1f}%", va='center', ha='center', color='white', fontweight='bold', fontsize=9)

    # 2. Stratified K-Fold
    axes[1].barh(y_pos, stratified_c0, color='#2A75D3', alpha=0.7, edgecolor='black', label='Клас 0 (90.0%)')
    axes[1].barh(y_pos, stratified_c1, left=stratified_c0, color='#27AE60', alpha=0.85, edgecolor='black', label='Клас 1 (10.0%)')
    axes[1].axvline(90, color='#1E8449', linestyle='--', linewidth=2, label='Ідеальна межа (90% / 10%)')
    axes[1].set_yticks(y_pos)
    axes[1].set_yticklabels(folds, fontsize=10.5, fontweight='bold')
    axes[1].set_xlabel('Відсоток зразків у тестовому fold\'і (%)', fontsize=11, fontweight='bold')
    axes[1].set_title('Stratified K-Fold (Збереження пропорції)\nСуворе збереження 10% у кожному fold\'і', fontsize=12, fontweight='bold', color='#1E8449', pad=10)
    axes[1].set_xlim(0, 100)
    axes[1].grid(axis='x', alpha=0.3, linestyle='--')
    axes[1].legend(loc='lower left', fontsize=9, framealpha=0.95)

    for idx, c1 in enumerate(stratified_c1):
        axes[1].text(95, idx, f"{c1:.1f}%", va='center', ha='center', color='white', fontweight='bold', fontsize=9)

    plt.suptitle("Чому класифікація потребує Stratified K-Fold: захист від спотворення класів", fontsize=13.5, fontweight='bold', y=0.99)
    plt.tight_layout()

    path_04 = os.path.join(OUTPUT_DIR, "04.png")
    path_alt = os.path.join(OUTPUT_DIR, "04_stratified_kfold.png")
    plt.savefig(path_04, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_04, path_alt)
    print(f"Generated: {path_04} & {path_alt}")


def plot_05_cv_workflow():
    """Plot 5: Clean visual flowchart of the proper ML validation workflow."""
    fig, ax = plt.subplots(figsize=(12.5, 6.8), dpi=180)

    # Box coordinates and sizes
    # 1. Dataset Box
    ax.text(6.25, 6.2, "Повний вихідний набір даних (100%)", ha='center', va='center',
            fontsize=12, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#2C3E50', edgecolor='#1A252F', lw=1.5))

    # Split Arrows
    ax.annotate('', xy=(3.5, 5.0), xytext=(5.5, 5.9),
                arrowprops=dict(arrowstyle="->", color='#34495E', lw=2))
    ax.annotate('', xy=(9.0, 5.0), xytext=(7.0, 5.9),
                arrowprops=dict(arrowstyle="->", color='#34495E', lw=2))

    # 2. Train Set Box (80%)
    ax.text(3.5, 4.6, "Навчальний набір (Train Set: 80%)\nВикористовується для досліджень та тюнінгу", 
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1B4F72',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#EBF5FB', edgecolor='#2980B9', lw=1.5))

    # 3. Holdout Test Box (20%)
    ax.text(9.0, 4.6, "Контрольний набір (Hold-out Test: 20%)\nІЗОЛЬОВАНИЙ ДО САМОГО ФІНАЛУ!", 
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#78281F',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FDEDEC', edgecolor='#E74C3C', lw=1.5))

    # 4. CV loop box on Train Set
    ax.annotate('', xy=(3.5, 3.4), xytext=(3.5, 4.0),
                arrowprops=dict(arrowstyle="->", color='#2980B9', lw=2))

    ax.text(3.5, 2.9, "5-Fold Cross-Validation\n(Порівняння алгоритмів + GridSearch)", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#196F3D',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F8F5', edgecolor='#27AE60', lw=1.5))

    # 5. Best Model selection
    ax.annotate('', xy=(3.5, 1.9), xytext=(3.5, 2.3),
                arrowprops=dict(arrowstyle="->", color='#27AE60', lw=2))

    ax.text(3.5, 1.4, "Вибір найкращої моделі\nта повторне навчання на ВСІХ 80%", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#512E5F',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4ECF7', edgecolor='#8E44AD', lw=1.5))

    # 6. Final Evaluation Arrow from Best Model + Test Set
    ax.annotate('', xy=(6.25, 0.45), xytext=(4.9, 1.3),
                arrowprops=dict(arrowstyle="->", color='#8E44AD', lw=2.2))
    ax.annotate('', xy=(6.25, 0.45), xytext=(8.5, 4.0),
                arrowprops=dict(arrowstyle="->", color='#E74C3C', lw=2.2, linestyle='--'))

    ax.text(6.25, 0.25, "ФІНАЛЬНА ОЦІНКА НА HOLDOUT TEST (Один-єдиний раз перед production!)\nЗахист від Data Leakage та оптимістичного зміщення", 
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#196F3D', edgecolor='#145A32', lw=1.8))

    ax.set_xlim(0.5, 12.0)
    ax.set_ylim(-0.2, 6.8)
    ax.axis('off')
    plt.title("Правильний Data Science Workflow: Розбиття вибірки та роль крос-валідації", 
              fontsize=13.5, fontweight='bold', pad=10)
    plt.tight_layout()

    path_05 = os.path.join(OUTPUT_DIR, "05.png")
    path_alt = os.path.join(OUTPUT_DIR, "05_cv_workflow.png")
    plt.savefig(path_05, dpi=180, bbox_inches='tight')
    plt.close()
    shutil.copyfile(path_05, path_alt)
    print(f"Generated: {path_05} & {path_alt}")


if __name__ == '__main__':
    plot_01_price_distribution()
    plot_02_kfold_scheme()
    plot_03_boxplot_models()
    plot_04_stratified_kfold()
    plot_05_cv_workflow()
    print("All 5 cross-validation visualizations successfully created!")
