import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    roc_curve, roc_auc_score,
    precision_recall_curve, average_precision_score,
    accuracy_score, precision_score, recall_score, f1_score
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Styling configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

out_dir = "public/images/ai-python/logistic-regression-classification/classification-metrics"
os.makedirs(out_dir, exist_ok=True)

# =============================================================================
# 1. 01-confusion-matrix-structure.png
# =============================================================================
def generate_confusion_matrix_structure():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')

    # Draw 2x2 grid
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.axis('off')

    # Cell coordinates:
    # Top-Left: TN (x=0, y=1)
    # Top-Right: FP (x=1, y=1)
    # Bottom-Left: FN (x=0, y=0)
    # Bottom-Right: TP (x=1, y=0)

    # Color boxes
    tn_box = plt.Rectangle((0, 1), 1, 1, facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=2.5, zorder=2)
    fp_box = plt.Rectangle((1, 1), 1, 1, facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=2.5, zorder=2)
    fn_box = plt.Rectangle((0, 0), 1, 1, facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=2.5, zorder=2)
    tp_box = plt.Rectangle((1, 0), 1, 1, facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=2.5, zorder=2)

    ax.add_patch(tn_box)
    ax.add_patch(fp_box)
    ax.add_patch(fn_box)
    ax.add_patch(tp_box)

    # Text in TN
    ax.text(0.5, 1.7, "True Negative (TN)", ha='center', va='center', fontsize=14, fontweight='bold', color='#15803D')
    ax.text(0.5, 1.45, "Факт: 0 (Здоровий)\nПрогноз: 0 (Здоровий)", ha='center', va='center', fontsize=10.5, color='#1E293B')
    ax.text(0.5, 1.2, "ПРАВИЛЬНО НЕГАТИВНИЙ", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#16A34A')

    # Text in FP
    ax.text(1.5, 1.7, "False Positive (FP)", ha='center', va='center', fontsize=14, fontweight='bold', color='#B91C1C')
    ax.text(1.5, 1.45, "Факт: 0 (Здоровий)\nПрогноз: 1 (Хворий)", ha='center', va='center', fontsize=10.5, color='#1E293B')
    ax.text(1.5, 1.2, "ПОМИЛКА I РОДУ (Хибна тривога)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#DC2626')

    # Text in FN
    ax.text(0.5, 0.7, "False Negative (FN)", ha='center', va='center', fontsize=14, fontweight='bold', color='#B91C1C')
    ax.text(0.5, 0.45, "Факт: 1 (Хворий)\nПрогноз: 0 (Здоровий)", ha='center', va='center', fontsize=10.5, color='#1E293B')
    ax.text(0.5, 0.2, "ПОМИЛКА II РОДУ (Пропуск цілі)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#DC2626')

    # Text in TP
    ax.text(1.5, 0.7, "True Positive (TP)", ha='center', va='center', fontsize=14, fontweight='bold', color='#15803D')
    ax.text(1.5, 0.45, "Факт: 1 (Хворий)\nПрогноз: 1 (Хворий)", ha='center', va='center', fontsize=10.5, color='#1E293B')
    ax.text(1.5, 0.2, "ПРАВИЛЬНО ПОЗИТИВНИЙ", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#16A34A')

    # Top Column Headers (Predicted)
    ax.text(0.5, 2.15, "Прогноз: Клас 0\n(Негативний)", ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')
    ax.text(1.5, 2.15, "Прогноз: Клас 1\n(Позитивний)", ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')
    ax.text(1.0, 2.4, "ПРОГНОЗ МОДЕЛІ (PREDICTED CLASS)", ha='center', va='center', fontsize=13, fontweight='bold', color='#2563EB')

    # Left Row Headers (Actual)
    ax.text(-0.25, 1.5, "Факт: Клас 0\n(Негативний)", ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A', rotation=90)
    ax.text(-0.25, 0.5, "Факт: Клас 1\n(Позитивний)", ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A', rotation=90)
    ax.text(-0.48, 1.0, "СПРАВЖНІЙ КЛАС (ACTUAL CLASS)", ha='center', va='center', fontsize=13, fontweight='bold', color='#2563EB', rotation=90)

    # Right Margin: Metrics Formulas
    ax.text(2.1, 1.5, "Specificity (TNR):\nTN / (TN + FP)", ha='left', va='center', fontsize=10.5, fontweight='bold', color='#475569',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F1F5F9', edgecolor='#CBD5E1'))
    ax.text(2.1, 0.5, "Recall (TPR / Повнота):\nTP / (TP + FN)", ha='left', va='center', fontsize=10.5, fontweight='bold', color='#15803D',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#DCFCE7', edgecolor='#86EFAC'))

    # Bottom Margin: Precision Formulas
    ax.text(0.5, -0.3, "Negative Predictive Value:\nTN / (TN + FN)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#475569',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F1F5F9', edgecolor='#CBD5E1'))
    ax.text(1.5, -0.3, "Precision (Точність):\nTP / (TP + FP)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#2563EB',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#DBEAFE', edgecolor='#93C5FD'))

    plt.title('АНАТОМІЯ МАТРИЦІ ПОМИЛОК (CONFUSION MATRIX)', fontsize=15, fontweight='bold', color='#0F172A', pad=25)
    plt.tight_layout()
    p = os.path.join(out_dir, "01-confusion-matrix-structure.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Збережено:", p)

# =============================================================================
# 2. 02-precision-recall-tradeoff.png
# =============================================================================
def generate_precision_recall_tradeoff():
    np.random.seed(42)
    # Generate realistic probability distributions
    n_neg = 300
    n_pos = 120
    probs_neg = np.random.beta(2, 6, n_neg)  # skewed towards 0
    probs_pos = np.random.beta(6, 3, n_pos)  # skewed towards 1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')

    # Subplot 1: Distribution of probabilities and moving threshold
    ax1.set_facecolor('#FFFFFF')
    ax1.hist(probs_neg, bins=30, alpha=0.6, color='#3B82F6', label='Клас 0 (Здорові / Негативні)', density=True)
    ax1.hist(probs_pos, bins=30, alpha=0.6, color='#EF4444', label='Клас 1 (Хворі / Позитивні)', density=True)

    # Mark 3 thresholds: Low (0.25), Balanced (0.50), High (0.75)
    ax1.axvline(0.25, color='#F59E0B', linestyle='--', linewidth=2.2, label='Низький поріг (T=0.25, Recall 97%)')
    ax1.axvline(0.50, color='#10B981', linestyle='-', linewidth=2.5, label='Стандартний поріг (T=0.50, Баланс)')
    ax1.axvline(0.75, color='#8B5CF6', linestyle='--', linewidth=2.2, label='Високий поріг (T=0.75, Precision 98%)')

    ax1.set_xlabel('Передбачена ймовірність P(клас 1)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Щільність розподілу', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_title('Розподіл ймовірностей та порогові межі', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax1.legend(loc='upper center', fontsize=8.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax1.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

    # Subplot 2: Precision & Recall vs Threshold
    ax2.set_facecolor('#FFFFFF')
    thresholds = np.linspace(0.05, 0.95, 100)
    precisions = []
    recalls = []
    f1s = []

    y_true = np.concatenate([np.zeros(n_neg), np.ones(n_pos)])
    all_probs = np.concatenate([probs_neg, probs_pos])

    for t in thresholds:
        y_pred = (all_probs >= t).astype(int)
        p = precision_score(y_true, y_pred, zero_division=0)
        r = recall_score(y_true, y_pred, zero_division=0)
        f = f1_score(y_true, y_pred, zero_division=0)
        precisions.append(p)
        recalls.append(r)
        f1s.append(f)

    ax2.plot(thresholds, precisions, color='#2563EB', linewidth=2.5, label='Precision (Точність)')
    ax2.plot(thresholds, recalls, color='#16A34A', linewidth=2.5, label='Recall (Повнота)')
    ax2.plot(thresholds, f1s, color='#F59E0B', linewidth=2.2, linestyle='-.', label='F1-Score (Гармонійне середнє)')

    # Optimal F1 intersection
    opt_idx = np.argmax(f1s)
    opt_t = thresholds[opt_idx]
    ax2.axvline(opt_t, color='#64748B', linestyle=':', linewidth=1.8, label=f'Оптимум F1 (T = {opt_t:.2f})')
    ax2.plot(opt_t, f1s[opt_idx], 'o', color='#F59E0B', markersize=9)

    ax2.set_xlabel('Поріг класифікації (Threshold)', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Значення метрики [0, 1]', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_title('Компроміс між Precision та Recall залежно від порогу', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax2.legend(loc='center left', fontsize=9, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax2.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

    plt.suptitle('ВЗАЄМОЗВ\'ЯЗОК PRECISION ТА RECALL (TRADE-OFF)', fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    p = os.path.join(out_dir, "02-precision-recall-tradeoff.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Збережено:", p)

# =============================================================================
# 3. 03-imbalanced-classes.png
# =============================================================================
def generate_imbalanced_classes():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')

    # Subplot 1: Imbalanced class ratio (Pie/Donut chart)
    ax1.set_facecolor('#FFFFFF')
    sizes = [95, 5]
    colors = ['#3B82F6', '#EF4444']
    explode = (0, 0.12)
    labels = ['Клас 0: Здорові / Легітимні транзакції (95%)', 'Клас 1: Хворі / Шахрайство (5%)']

    wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                                       autopct='%1.0f%%', startangle=45, pctdistance=0.75,
                                       textprops=dict(color='#0F172A', fontsize=10.5, fontweight='bold'),
                                       wedgeprops=dict(width=0.45, edgecolor='#CBD5E1', linewidth=1.5))

    for at in autotexts:
        at.set_fontsize(14)
        at.set_color('#FFFFFF')
        at.set_fontweight('bold')

    ax1.set_title('1. Розподіл незбалансованого датасету (95% проти 5%)', fontsize=12.5, fontweight='bold', color='#0F172A', pad=15)

    # Subplot 2: Comparison of Dummy Model vs Real ML Model
    ax2.set_facecolor('#FFFFFF')
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    dummy_scores = [0.95, 0.00, 0.00, 0.00]
    balanced_scores = [0.92, 0.78, 0.85, 0.81]

    x = np.arange(len(metrics_names))
    width = 0.35

    rects1 = ax2.bar(x - width/2, dummy_scores, width, label='Наївна модель ("Завжди клас 0")', color='#EF4444', alpha=0.85, edgecolor='#991B1B')
    rects2 = ax2.bar(x + width/2, balanced_scores, width, label='Збалансована ML модель', color='#10B981', alpha=0.85, edgecolor='#065F46')

    # Value labels on bars
    for r in rects1:
        h = r.get_height()
        ax2.annotate(f'{h:.0%}', xy=(r.get_x() + r.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#991B1B')

    for r in rects2:
        h = r.get_height()
        ax2.annotate(f'{h:.0%}', xy=(r.get_x() + r.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#065F46')

    ax2.set_ylabel('Значення показника', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_title('2. "Парадокс точності" (Accuracy Paradox)', fontsize=12.5, fontweight='bold', color='#0F172A', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics_names, fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 1.15)
    ax2.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax2.grid(axis='y', linestyle='--', alpha=0.3, color='#94A3B8')

    plt.suptitle('ПРОБЛЕМА НЕЗБАЛАНСОВАНИХ КЛАСІВ ТА ОМАНЛИВІСТЬ ACCURACY', fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    p = os.path.join(out_dir, "03-imbalanced-classes.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Збережено:", p)

# =============================================================================
# 4. 04-confusion-matrix-display.png (for confusion_matrix_example.ipynb)
# =============================================================================
def generate_confusion_matrix_display():
    # Matches the exact data from confusion_matrix_example.ipynb
    y_true = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])
    y_pred = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1])
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Здоровий (0)', 'Хворий (1)'])
    disp.plot(cmap='Blues', ax=ax, colorbar=False)

    plt.title('Confusion Matrix: Діагностика хвороби', fontsize=13.5, fontweight='bold', color='#0F172A', pad=15)
    plt.xlabel('Прогноз моделі', fontsize=11.5, fontweight='bold', color='#1E293B')
    plt.ylabel('Справжній діагноз', fontsize=11.5, fontweight='bold', color='#1E293B')
    plt.tight_layout()
    p = os.path.join(out_dir, "04-confusion-matrix-display.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Збережено:", p)

# =============================================================================
# 5. 05-roc-curve.png (for roc_curve_visualization.ipynb)
# =============================================================================
def generate_roc_curve():
    np.random.seed(42)
    # Generate data matching roc_curve_visualization.ipynb
    X, y = make_classification(n_samples=500, n_features=15, n_informative=10,
                               n_classes=2, weights=[0.6, 0.4], random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    y_probs = model.predict_proba(X_test)[:, 1]

    fpr, tpr, _ = roc_curve(y_test, y_probs)
    auc_score = roc_auc_score(y_test, y_probs)

    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')

    ax.plot(fpr, tpr, color='#2563EB', linewidth=2.8, label=f'Модель логістичної регресії (AUC = {auc_score:.3f})')
    ax.fill_between(fpr, tpr, color='#3B82F6', alpha=0.15)
    ax.plot([0, 1], [0, 1], 'k--', linewidth=2, alpha=0.7, label='Випадкова модель (AUC = 0.500)')
    ax.plot([0, 0, 1], [0, 1, 1], color='#10B981', linestyle=':', linewidth=2.2, alpha=0.8, label='Ідеальна модель (AUC = 1.000)')

    ax.set_xlabel('False Positive Rate (FPR = 1 - Specificity)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('True Positive Rate (TPR / Recall)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title(f'ROC-крива: Оцінка роздільної здатності класифікатора (AUC = {auc_score:.3f})', fontsize=13, fontweight='bold', color='#0F172A', pad=15)
    ax.legend(loc='lower right', fontsize=10, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.02])

    plt.tight_layout()
    p = os.path.join(out_dir, "05-roc-curve.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Збережено:", p)

# =============================================================================
# 6. 06-pr-vs-roc-imbalanced.png (for precision_recall_curve.ipynb)
# =============================================================================
def generate_pr_vs_roc_imbalanced():
    np.random.seed(42)
    # Generate imbalanced dataset (90% class 0, 10% class 1)
    X_imb, y_imb = make_classification(n_samples=1000, n_features=20, n_informative=12,
                                       n_classes=2, weights=[0.90, 0.10], random_state=42)
    X_train_imb, X_test_imb, y_train_imb, y_test_imb = train_test_split(
        X_imb, y_imb, test_size=0.3, random_state=42, stratify=y_imb
    )
    model_imb = LogisticRegression(random_state=42)
    model_imb.fit(X_train_imb, y_train_imb)
    y_probs_imb = model_imb.predict_proba(X_test_imb)[:, 1]

    fpr, tpr, _ = roc_curve(y_test_imb, y_probs_imb)
    roc_auc = roc_auc_score(y_test_imb, y_probs_imb)
    precision, recall, _ = precision_recall_curve(y_test_imb, y_probs_imb)
    avg_precision = average_precision_score(y_test_imb, y_probs_imb)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')

    # ROC curve
    axes[0].set_facecolor('#FFFFFF')
    axes[0].plot(fpr, tpr, color='#2563EB', linewidth=2.5, label=f'ROC-AUC = {roc_auc:.3f}')
    axes[0].plot([0, 1], [0, 1], 'k--', linewidth=1.8, alpha=0.6, label='Baseline (AUC = 0.500)')
    axes[0].set_xlabel('False Positive Rate (FPR)', fontsize=11, fontweight='bold', color='#1E293B')
    axes[0].set_ylabel('True Positive Rate (Recall)', fontsize=11, fontweight='bold', color='#1E293B')
    axes[0].set_title('1. ROC-крива (Оптимістична оцінка)', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    axes[0].legend(loc='lower right', fontsize=9.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    axes[0].grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

    # Precision-Recall curve
    axes[1].set_facecolor('#FFFFFF')
    axes[1].plot(recall, precision, color='#F59E0B', linewidth=2.5, label=f'PR-крива (AP = {avg_precision:.3f})')
    axes[1].axhline(y=(y_test_imb == 1).mean(), color='k', linestyle='--', linewidth=1.8, alpha=0.6,
                    label=f'Baseline (частка класу 1 = {(y_test_imb == 1).mean():.1%})')
    axes[1].set_xlabel('Recall (Повнота)', fontsize=11, fontweight='bold', color='#1E293B')
    axes[1].set_ylabel('Precision (Точність)', fontsize=11, fontweight='bold', color='#1E293B')
    axes[1].set_title('2. PR-крива (Реалістична оцінка на меншості)', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    axes[1].legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    axes[1].grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

    plt.suptitle('ПОРІВНЯННЯ ROC ТА PR-КРИВИХ ДЛЯ НЕЗБАЛАНСОВАНИХ ДАНИХ (10% МЕНШОСТІ)', fontsize=14, fontweight='bold', color='#0F172A', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    p = os.path.join(out_dir, "06-pr-vs-roc-imbalanced.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Збережено:", p)

# =============================================================================
# 7. 07-model-comparison-metrics.png (for model_comparison.ipynb)
# =============================================================================
def generate_model_comparison_metrics():
    # Load Breast Cancer data as in model_comparison.ipynb
    cancer = load_breast_cancer()
    X, y = cancer.data, cancer.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=5),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100)
    }

    results = []
    for name, m in models.items():
        if name == 'Logistic Regression':
            m.fit(X_train_s, y_train)
            yp = m.predict(X_test_s)
            yprob = m.predict_proba(X_test_s)[:, 1]
        else:
            m.fit(X_train, y_train)
            yp = m.predict(X_test)
            yprob = m.predict_proba(X_test)[:, 1]

        results.append({
            'Model': name,
            'Accuracy': accuracy_score(y_test, yp),
            'Precision': precision_score(y_test, yp),
            'Recall': recall_score(y_test, yp),
            'F1-Score': f1_score(y_test, yp),
            'ROC-AUC': roc_auc_score(y_test, yprob)
        })

    results_df = pd.DataFrame(results)

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')

    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
    x = np.arange(len(metrics))
    width = 0.25
    colors = ['#3B82F6', '#F59E0B', '#10B981']

    for i, (_, row) in enumerate(results_df.iterrows()):
        vals = [row[m] for m in metrics]
        rects = ax.bar(x + (i - 1) * width, vals, width, label=row['Model'], color=colors[i], alpha=0.88, edgecolor='#1E293B', linewidth=1.0)
        for r in rects:
            h = r.get_height()
            ax.annotate(f'{h:.3f}', xy=(r.get_x() + r.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1E293B')

    ax.set_xlabel('Метрики якості класифікації', fontsize=11.5, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Значення показника', fontsize=11.5, fontweight='bold', color='#1E293B')
    ax.set_title('Порівняння моделей класифікації на датасеті Breast Cancer', fontsize=13.5, fontweight='bold', color='#0F172A', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11, fontweight='bold')
    ax.legend(loc='lower left', fontsize=10, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.set_ylim([0.88, 1.03])
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='#94A3B8')

    plt.tight_layout()
    p = os.path.join(out_dir, "07-model-comparison-metrics.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Збережено:", p)

# =============================================================================
# 8. 08-task1-threshold-metrics.png (for solution_task_2.ipynb / Task 1)
# =============================================================================
def generate_task1_threshold_metrics():
    cancer = load_breast_cancer()
    X, y = cancer.data, cancer.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = LogisticRegression(random_state=42)
    model.fit(X_train_s, y_train)
    y_probs = model.predict_proba(X_test_s)[:, 1]

    thresholds = np.arange(0.1, 1.0, 0.1)
    results = []
    for t in thresholds:
        yp = (y_probs >= t).astype(int)
        results.append({
            'Threshold': t,
            'Precision': precision_score(y_test, yp, zero_division=0),
            'Recall': recall_score(y_test, yp, zero_division=0),
            'F1': f1_score(y_test, yp, zero_division=0)
        })
    df = pd.DataFrame(results)

    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')

    ax.plot(df['Threshold'], df['Precision'], marker='o', linewidth=2.5, markersize=7, label='Precision (Точність)', color='#3B82F6')
    ax.plot(df['Threshold'], df['Recall'], marker='s', linewidth=2.5, markersize=7, label='Recall (Повнота)', color='#10B981')
    ax.plot(df['Threshold'], df['F1'], marker='^', linewidth=2.5, markersize=7, label='F1-Score', color='#F59E0B')

    # Shaded medical sweet spot [0.1, 0.2]
    ax.axvspan(0.1, 0.2, color='#10B981', alpha=0.15, label='Оптимум для онкоскринінгу (Recall = 100%)')

    ax.set_xlabel('Поріг класифікації (Decision Threshold)', fontsize=11.5, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Значення метрики', fontsize=11.5, fontweight='bold', color='#1E293B')
    ax.set_title('Залежність метрик діагностики від порогу класифікації (Breast Cancer)', fontsize=13, fontweight='bold', color='#0F172A', pad=15)
    ax.legend(loc='lower left', fontsize=10, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax.set_ylim([0.80, 1.03])

    plt.tight_layout()
    p = os.path.join(out_dir, "08-task1-threshold-metrics.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Збережено:", p)

if __name__ == '__main__':
    print("Генерація графіків для 02.classification-metrics.md...")
    generate_confusion_matrix_structure()
    generate_precision_recall_tradeoff()
    generate_imbalanced_classes()
    generate_confusion_matrix_display()
    generate_roc_curve()
    generate_pr_vs_roc_imbalanced()
    generate_model_comparison_metrics()
    generate_task1_threshold_metrics()
    print("Усі 8 графіків успішно створено!")
