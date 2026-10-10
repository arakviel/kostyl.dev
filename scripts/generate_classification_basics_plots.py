import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures

# Configure plotting aesthetics
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

out_dir = "public/images/ai-python/logistic-regression-classification/classification-basics"
os.makedirs(out_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. 01-types-of-classification.png: Binary vs Multiclass vs Multilabel
# -----------------------------------------------------------------------------
def generate_types_of_classification():
    np.random.seed(42)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5), dpi=300)

    # Subplot 1: Binary (2 classes)
    c0 = np.random.randn(25, 2) * 0.7 + np.array([1.8, 1.8])
    c1 = np.random.randn(25, 2) * 0.7 + np.array([4.2, 4.2])
    ax1.scatter(c0[:, 0], c0[:, 1], color='#3B82F6', s=60, edgecolors='#1E293B', linewidths=1.0, label='Клас 0 (Спам)')
    ax1.scatter(c1[:, 0], c1[:, 1], color='#EF4444', s=60, edgecolors='#1E293B', linewidths=1.0, label='Клас 1 (Не спам)')
    x_b = np.linspace(0.5, 5.5, 50)
    ax1.plot(x_b, 6.0 - x_b, color='#10B981', linewidth=2.5, linestyle='--', label='Розділова межа')
    ax1.set_title('1. Бінарна класифікація\n(Лише 2 взаємовиключні класи)', fontsize=12, fontweight='bold', color='#0F172A', pad=10)
    ax1.set_xlabel('Ознака 1', fontsize=10.5, color='#1E293B')
    ax1.set_ylabel('Ознака 2', fontsize=10.5, color='#1E293B')
    ax1.legend(loc='lower left', fontsize=9, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax1.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')

    # Subplot 2: Multiclass (3 classes)
    m0 = np.random.randn(20, 2) * 0.6 + np.array([1.8, 4.2])
    m1 = np.random.randn(20, 2) * 0.6 + np.array([4.5, 4.2])
    m2 = np.random.randn(20, 2) * 0.6 + np.array([3.1, 1.6])
    ax2.scatter(m0[:, 0], m0[:, 1], color='#3B82F6', s=60, edgecolors='#1E293B', linewidths=1.0, label='Клас 0 (Кіт)')
    ax2.scatter(m1[:, 0], m1[:, 1], color='#EF4444', s=60, edgecolors='#1E293B', linewidths=1.0, label='Клас 1 (Собака)')
    ax2.scatter(m2[:, 0], m2[:, 1], color='#F59E0B', s=60, edgecolors='#1E293B', linewidths=1.0, label='Клас 2 (Пташка)')
    ax2.plot([3.1, 3.1], [2.8, 5.5], color='#64748B', linestyle=':', linewidth=2)
    ax2.plot([0.5, 3.1], [2.8, 2.8], color='#64748B', linestyle=':', linewidth=2)
    ax2.plot([3.1, 5.5], [2.8, 2.8], color='#64748B', linestyle=':', linewidth=2)
    ax2.set_title('2. Багатокласова (Multiclass)\n(3+ взаємовиключні класи: 1 об\'єкт = 1 клас)', fontsize=12, fontweight='bold', color='#0F172A', pad=10)
    ax2.set_xlabel('Ознака 1', fontsize=10.5, color='#1E293B')
    ax2.legend(loc='lower left', fontsize=9, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax2.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')

    # Subplot 3: Multilabel (multiple labels per sample)
    np.random.seed(101)
    pts = np.random.uniform(1.0, 5.0, (15, 2))
    ax3.scatter(pts[:, 0], pts[:, 1], color='#F8FAFC', edgecolors='#0F172A', s=180, linewidths=1.5, zorder=2)
    # Give some points blue center (Tech tag)
    tech_idx = [0, 1, 3, 4, 7, 8, 11]
    ax3.scatter(pts[tech_idx, 0], pts[tech_idx, 1], color='#3B82F6', s=70, label='Тег: Технології', zorder=3)
    # Give some points red ring/cross (Finance tag)
    fin_idx = [2, 3, 5, 8, 9, 11, 13]
    ax3.scatter(pts[fin_idx, 0], pts[fin_idx, 1], facecolors='none', edgecolors='#EF4444', s=130, linewidths=2.5, label='Тег: Фінанси', zorder=4)
    # Give some points amber plus (AI tag)
    ai_idx = [0, 3, 6, 8, 12, 14]
    ax3.scatter(pts[ai_idx, 0], pts[ai_idx, 1], marker='+', color='#D97706', s=100, linewidths=2.5, label='Тег: Штучний інтелект', zorder=5)

    ax3.set_title('3. Мультилейбл (Multilabel)\n(1 об\'єкт може мати ОДНОЧАСНО кілька тегів)', fontsize=12, fontweight='bold', color='#0F172A', pad=10)
    ax3.set_xlabel('Ознака 1', fontsize=10.5, color='#1E293B')
    ax3.legend(loc='lower left', fontsize=8.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax3.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')

    for ax in [ax1, ax2, ax3]:
        ax.set_facecolor('#FFFFFF')
        ax.set_xlim(0.5, 5.8)
        ax.set_ylim(0.5, 5.8)

    plt.tight_layout()
    path = os.path.join(out_dir, "01-types-of-classification.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

# -----------------------------------------------------------------------------
# 2. 02-regression-vs-classification.png: Regression vs Classification
# -----------------------------------------------------------------------------
def generate_regression_vs_classification():
    np.random.seed(42)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8), dpi=300)

    # Regression: continuous curve
    x_reg = np.linspace(1, 10, 35)
    y_reg = 2.5 * x_reg + 15 + np.random.normal(0, 3.2, 35)
    ax1.scatter(x_reg, y_reg, color='#3B82F6', s=60, edgecolors='#1E293B', linewidths=1.0, alpha=0.9, label='Спостереження (ціна житла)')
    x_line = np.linspace(0.5, 10.5, 100)
    ax1.plot(x_line, 2.5 * x_line + 15, color='#DC2626', linewidth=2.8, label='Неперервна лінія: ŷ = wx + b')
    ax1.set_title('РЕГРЕСІЯ: Прогноз неперервної числової величини', fontsize=12.5, fontweight='bold', color='#0F172A', pad=12)
    ax1.set_xlabel('Площа приміщення (м²)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Ціна нерухомості (тис. $)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.legend(loc='upper left', fontsize=10, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax1.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax1.text(0.05, 0.06, '• Цільова змінна: y ∈ ℝ (будь-яке неперервне число)\n• Помилка: різниця відстаней MSE = (y - ŷ)²',
             transform=ax1.transAxes, fontsize=9.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#F59E0B', alpha=0.9))

    # Classification: discrete categories
    hours = np.array([1, 1.8, 2.3, 2.9, 3.4, 4.0, 4.6, 5.5, 6.2, 6.8, 7.3, 8.1, 8.9, 9.8])
    passed = np.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1])
    
    # Fit logistic regression
    clf = LogisticRegression()
    clf.fit(hours.reshape(-1, 1), passed)
    x_clf = np.linspace(0.5, 10.5, 200).reshape(-1, 1)
    probs = clf.predict_proba(x_clf)[:, 1]

    ax2.scatter(hours[passed == 0], passed[passed == 0], color='#EF4444', marker='s', s=70, edgecolors='#1E293B', linewidths=1.2, label='Клас 0: Не склав іспит')
    ax2.scatter(hours[passed == 1], passed[passed == 1], color='#10B981', marker='o', s=70, edgecolors='#1E293B', linewidths=1.2, label='Клас 1: Склав іспит')
    ax2.plot(x_clf, probs, color='#2563EB', linewidth=2.8, label='Сигмоїдна ймовірність: P(y=1|x)')
    ax2.axhline(0.5, color='#F59E0B', linestyle='--', linewidth=2.0, label='Поріг рішення: T = 0.5')
    
    # Decision boundary x where prob == 0.5
    boundary_x = -clf.intercept_[0] / clf.coef_[0][0]
    ax2.axvline(boundary_x, color='#10B981', linestyle=':', linewidth=2.0)
    ax2.text(boundary_x + 0.15, 0.2, f'Розділова межа\nx ≈ {boundary_x:.1f} год', fontsize=9.5, fontweight='bold', color='#047857')

    ax2.set_title('КЛАСИФІКАЦІЯ: Прогноз дискретної категорії', fontsize=12.5, fontweight='bold', color='#0F172A', pad=12)
    ax2.set_xlabel('Години підготовки до іспиту (год)', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Ймовірність належності до класу 1', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.legend(loc='center left', fontsize=9.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax2.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax2.set_ylim(-0.08, 1.08)
    ax2.text(0.05, 0.65, '• Цільова змінна: y ∈ {0, 1} (дискретні класи)\n• Рішення: дискретний вибір за порогом ймовірності',
             transform=ax2.transAxes, fontsize=9.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#DCFCE7', edgecolor='#10B981', alpha=0.9))

    plt.tight_layout()
    path = os.path.join(out_dir, "02-regression-vs-classification.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

# -----------------------------------------------------------------------------
# 3. 03-outlier-sensitivity.png: Outlier sensitivity Linear vs Logistic
# -----------------------------------------------------------------------------
def generate_outlier_sensitivity():
    # Base data
    X_base = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
    y_base = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

    # Outlier at x=28, y=1
    X_outlier = np.append(X_base, [[28]], axis=0)
    y_outlier = np.append(y_base, [1])

    # Linear models
    lin_clean = LinearRegression().fit(X_base, y_base)
    lin_out = LinearRegression().fit(X_outlier, y_outlier)

    # Logistic models
    log_clean = LogisticRegression().fit(X_base, y_base)
    log_out = LogisticRegression().fit(X_outlier, y_outlier)

    x_dense = np.linspace(0, 30, 300).reshape(-1, 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8), dpi=300)

    # Subplot 1: Linear Regression
    ax1.scatter(X_base[y_base == 0], y_base[y_base == 0], color='#EF4444', s=65, label='Клас 0', zorder=4)
    ax1.scatter(X_base[y_base == 1], y_base[y_base == 1], color='#10B981', s=65, label='Клас 1', zorder=4)
    ax1.scatter([28], [1], color='#D97706', s=120, marker='*', edgecolors='#0F172A', label='Екстремальний викид (x=28, y=1)', zorder=5)

    ax1.plot(x_dense, lin_clean.predict(x_dense), color='#10B981', linewidth=2.2, linestyle='--', label='Лінійна регресія (без викиду)')
    ax1.plot(x_dense, lin_out.predict(x_dense), color='#DC2626', linewidth=2.8, label='Лінійна регресія (З ВИКИДОМ)')
    ax1.axhline(0.5, color='#64748B', linestyle=':', label='Поріг класифікації 0.5')

    # Find thresholds
    t_clean = (0.5 - lin_clean.intercept_) / lin_clean.coef_[0]
    t_out = (0.5 - lin_out.intercept_) / lin_out.coef_[0]
    ax1.axvline(t_clean, color='#10B981', linestyle=':', linewidth=1.8)
    ax1.axvline(t_out, color='#DC2626', linestyle=':', linewidth=1.8)

    ax1.set_title('Лінійна регресія: катастрофічна чутливість до викиду', fontsize=12, fontweight='bold', color='#DC2626', pad=12)
    ax1.set_xlabel('Ознака X', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Прогноз ŷ', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylim(-0.25, 1.35)
    ax1.set_xlim(0, 30)
    ax1.legend(loc='upper left', fontsize=8.8, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax1.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax1.text(0.04, 0.05, f'• Поріг без викиду: x = {t_clean:.1f}\n• Зсув через викид: x = {t_out:.1f}!\nУвага: половина точок класу 1 класифікується невірно!',
             transform=ax1.transAxes, fontsize=9.2, bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEE2E2', edgecolor='#DC2626', alpha=0.9))

    # Subplot 2: Logistic Regression
    ax2.scatter(X_base[y_base == 0], y_base[y_base == 0], color='#EF4444', s=65, label='Клас 0', zorder=4)
    ax2.scatter(X_base[y_base == 1], y_base[y_base == 1], color='#10B981', s=65, label='Клас 1', zorder=4)
    ax2.scatter([28], [1], color='#D97706', s=120, marker='*', edgecolors='#0F172A', label='Екстремальний викид (x=28, y=1)', zorder=5)

    ax2.plot(x_dense, log_clean.predict_proba(x_dense)[:, 1], color='#10B981', linewidth=2.2, linestyle='--', label='Логістична (без викиду)')
    ax2.plot(x_dense, log_out.predict_proba(x_dense)[:, 1], color='#2563EB', linewidth=2.8, label='Логістична (З ВИКИДОМ)')
    ax2.axhline(0.5, color='#64748B', linestyle=':', label='Поріг класифікації 0.5')

    t_log_clean = -log_clean.intercept_[0] / log_clean.coef_[0][0]
    t_log_out = -log_out.intercept_[0] / log_out.coef_[0][0]
    ax2.axvline(t_log_clean, color='#10B981', linestyle=':', linewidth=1.8)
    ax2.axvline(t_log_out, color='#2563EB', linestyle=':', linewidth=1.8)

    ax2.set_title('Логістична регресія: висока стійкість до викиду', fontsize=12, fontweight='bold', color='#16A34A', pad=12)
    ax2.set_xlabel('Ознака X', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Ймовірність P(y=1 | x)', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylim(-0.08, 1.12)
    ax2.set_xlim(0, 30)
    ax2.legend(loc='center right', fontsize=8.8, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax2.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax2.text(0.04, 0.05, f'• Поріг без викиду: x = {t_log_clean:.1f}\n• Поріг з викидом: x = {t_log_out:.1f}\nВисновок: сигмоїда наситилася біля 1.0, межа стабільна!',
             transform=ax2.transAxes, fontsize=9.2, bbox=dict(boxstyle='round,pad=0.5', facecolor='#DCFCE7', edgecolor='#16A34A', alpha=0.9))

    plt.tight_layout()
    path = os.path.join(out_dir, "03-outlier-sensitivity.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

# -----------------------------------------------------------------------------
# 4. 05-decision-boundary.png: 2D Decision Boundary (Exams data)
# -----------------------------------------------------------------------------
def generate_decision_boundary_2d():
    # Data from decision_boundary_2d.ipynb in the textbook
    X_train = np.array([
        [45, 85], [55, 70], [60, 90], [65, 75], [70, 88],
        [75, 92], [80, 85], [85, 95], [30, 50], [40, 60],
        [50, 65], [35, 55], [42, 68]
    ])
    y_train = np.array([0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0])

    model = LogisticRegression()
    model.fit(X_train, y_train)

    w1, w2 = model.coef_[0]
    b = model.intercept_[0]

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

    # Meshgrid for probability background
    xx, yy = np.meshgrid(np.linspace(20, 95, 300), np.linspace(35, 105, 300))
    grid_pts = np.c_[xx.ravel(), yy.ravel()]
    probs = model.predict_proba(grid_pts)[:, 1].reshape(xx.shape)

    # Filled contour regions
    contour = ax.contourf(xx, yy, probs, levels=np.linspace(0, 1, 11), cmap='RdYlGn', alpha=0.35)
    cbar = fig.colorbar(contour, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Передбачена ймовірність P(Прийнято | x)', fontsize=10.5, fontweight='bold', color='#1E293B')

    # Decision boundary line where P = 0.5 (w1*x1 + w2*x2 + b = 0)
    x1_line = np.linspace(25, 90, 100)
    x2_line = -(w1 * x1_line + b) / w2
    ax.plot(x1_line, x2_line, color='#2563EB', linewidth=3.0, linestyle='--', label=f'Розділова межа (P = 0.5): x2 = {-w1/w2:.2f}·x1 + {-b/w2:.1f}')

    # Scatter points
    ax.scatter(X_train[y_train == 0, 0], X_train[y_train == 0, 1],
               c='#EF4444', marker='x', s=110, linewidths=2.5, label='Клас 0: Не прийнято (0)', zorder=5)
    ax.scatter(X_train[y_train == 1, 0], X_train[y_train == 1, 1],
               c='#10B981', marker='o', s=110, edgecolors='#0F172A', linewidths=1.5, label='Клас 1: Прийнято (1)', zorder=5)

    ax.set_title('Лінійна розділова межа логістичної регресії у 2D просторі', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax.set_xlabel('Іспит 1 (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Іспит 2 (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_xlim(25, 92)
    ax.set_ylim(40, 102)
    ax.legend(loc='lower left', fontsize=10, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')

    plt.tight_layout()
    path = os.path.join(out_dir, "05-decision-boundary.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

# -----------------------------------------------------------------------------
# 5. 06-linearly-nonseparable.png: XOR Problem & Non-linear Boundary
# -----------------------------------------------------------------------------
def generate_linearly_nonseparable():
    # XOR dataset
    X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_xor = np.array([0, 1, 1, 0])

    # Add surrounding synthetic points to form nice 2D XOR clusters
    np.random.seed(42)
    cluster_0_a = np.random.randn(20, 2) * 0.15 + np.array([0.15, 0.15])
    cluster_0_b = np.random.randn(20, 2) * 0.15 + np.array([0.85, 0.85])
    cluster_1_a = np.random.randn(20, 2) * 0.15 + np.array([0.15, 0.85])
    cluster_1_b = np.random.randn(20, 2) * 0.15 + np.array([0.85, 0.15])

    X_full = np.vstack([cluster_0_a, cluster_0_b, cluster_1_a, cluster_1_b])
    y_full = np.hstack([np.zeros(40), np.ones(40)])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8), dpi=300)

    # Subplot 1: Linear failure
    ax1.scatter(X_full[y_full == 0, 0], X_full[y_full == 0, 1], color='#EF4444', s=60, edgecolors='#1E293B', label='Клас 0', zorder=4)
    ax1.scatter(X_full[y_full == 1, 0], X_full[y_full == 1, 1], color='#3B82F6', s=60, edgecolors='#1E293B', label='Клас 1', zorder=4)
    # A linear boundary attempt
    x_line = np.linspace(-0.2, 1.2, 50)
    ax1.plot(x_line, 1.0 - x_line, color='#DC2626', linewidth=2.5, linestyle='--', label='Спроба прямої межі (Точність: 50%)')
    ax1.set_title('Звичайна лінійна модель на XOR-даних\n(Жодна пряма лінія не розділить класи)', fontsize=12, fontweight='bold', color='#DC2626', pad=10)
    ax1.set_xlabel('Ознака x1', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Ознака x2', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax1.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')

    # Subplot 2: Non-linear boundary with polynomial features
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly.fit_transform(X_full)
    model_poly = LogisticRegression()
    model_poly.fit(X_poly, y_full)

    xx, yy = np.meshgrid(np.linspace(-0.2, 1.2, 250), np.linspace(-0.2, 1.2, 250))
    grid_poly = poly.transform(np.c_[xx.ravel(), yy.ravel()])
    zz = model_poly.predict_proba(grid_poly)[:, 1].reshape(xx.shape)

    ax2.contourf(xx, yy, zz, levels=[0, 0.5, 1], colors=['#FEE2E2', '#DBEAFE'], alpha=0.45)
    ax2.contour(xx, yy, zz, levels=[0.5], colors=['#10B981'], linewidths=[3.0], linestyles=['--'])

    ax2.scatter(X_full[y_full == 0, 0], X_full[y_full == 0, 1], color='#EF4444', s=60, edgecolors='#1E293B', label='Клас 0', zorder=4)
    ax2.scatter(X_full[y_full == 1, 0], X_full[y_full == 1, 1], color='#3B82F6', s=60, edgecolors='#1E293B', label='Клас 1', zorder=4)
    ax2.plot([], [], color='#10B981', linewidth=2.5, linestyle='--', label='Нелінійна межа (Точність: 100%)')

    ax2.set_title('Модель із поліноміальними ознаками (x1·x2)\n(Крива межа ідеально розділяє простір)', fontsize=12, fontweight='bold', color='#16A34A', pad=10)
    ax2.set_xlabel('Ознака x1', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Ознака x2', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax2.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')

    for ax in [ax1, ax2]:
        ax.set_xlim(-0.15, 1.15)
        ax.set_ylim(-0.15, 1.15)

    plt.tight_layout()
    path = os.path.join(out_dir, "06-linearly-nonseparable.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

# -----------------------------------------------------------------------------
# 6. 07-one-vs-rest.png: One-vs-Rest Multiclass Strategy
# -----------------------------------------------------------------------------
def generate_one_vs_rest():
    np.random.seed(42)
    cA = np.random.randn(20, 2) * 0.45 + np.array([2.0, 4.2])
    cB = np.random.randn(20, 2) * 0.45 + np.array([4.2, 4.2])
    cC = np.random.randn(20, 2) * 0.45 + np.array([3.1, 1.8])

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5), dpi=300)

    # 1. Class A vs Rest
    ax1.scatter(cA[:, 0], cA[:, 1], color='#3B82F6', s=70, edgecolors='#1E293B', linewidths=1.2, label='Клас A (Позитивний)')
    ax1.scatter(cB[:, 0], cB[:, 1], color='#94A3B8', s=45, alpha=0.7, label='Клас B (Решта)')
    ax1.scatter(cC[:, 0], cC[:, 1], color='#94A3B8', s=45, alpha=0.7, label='Клас C (Решта)')
    x_line = np.linspace(1.0, 4.5, 50)
    ax1.plot(x_line, 1.2 * x_line + 0.8, color='#3B82F6', linewidth=2.8, linestyle='--', label='Межа Класифікатора 1')
    ax1.set_title('Класифікатор 1:\nКлас A проти [B + C]', fontsize=11.5, fontweight='bold', color='#1E293B', pad=10)

    # 2. Class B vs Rest
    ax2.scatter(cA[:, 0], cA[:, 1], color='#94A3B8', s=45, alpha=0.7, label='Клас A (Решта)')
    ax2.scatter(cB[:, 0], cB[:, 1], color='#EF4444', s=70, edgecolors='#1E293B', linewidths=1.2, label='Клас B (Позитивний)')
    ax2.scatter(cC[:, 0], cC[:, 1], color='#94A3B8', s=45, alpha=0.7, label='Клас C (Решта)')
    x_line = np.linspace(2.5, 5.2, 50)
    ax2.plot(x_line, -1.2 * x_line + 7.6, color='#EF4444', linewidth=2.8, linestyle='--', label='Межа Класифікатора 2')
    ax2.set_title('Класифікатор 2:\nКлас B проти [A + C]', fontsize=11.5, fontweight='bold', color='#1E293B', pad=10)

    # 3. Class C vs Rest
    ax3.scatter(cA[:, 0], cA[:, 1], color='#94A3B8', s=45, alpha=0.7, label='Клас A (Решта)')
    ax3.scatter(cB[:, 0], cB[:, 1], color='#94A3B8', s=45, alpha=0.7, label='Клас B (Решта)')
    ax3.scatter(cC[:, 0], cC[:, 1], color='#10B981', s=70, edgecolors='#1E293B', linewidths=1.2, label='Клас C (Позитивний)')
    x_line = np.linspace(1.0, 5.2, 50)
    ax3.plot(x_line, np.full_like(x_line, 2.9), color='#10B981', linewidth=2.8, linestyle='--', label='Межа Класифікатора 3')
    ax3.set_title('Класифікатор 3:\nКлас C проти [A + B]', fontsize=11.5, fontweight='bold', color='#1E293B', pad=10)

    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(0.8, 5.4)
        ax.set_ylim(0.8, 5.4)
        ax.set_xlabel('Ознака 1', fontsize=10.5, color='#1E293B')
        ax.set_ylabel('Ознака 2', fontsize=10.5, color='#1E293B')
        ax.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
        ax.legend(loc='lower left', fontsize=8.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

    fig.suptitle('Стратегія One-vs-Rest (OvR): Розбиття задачі з 3 класів на 3 незалежні бінарні класифікатори',
                 fontsize=13, fontweight='bold', color='#0F172A', y=1.02)
    plt.tight_layout()
    path = os.path.join(out_dir, "07-one-vs-rest.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

# -----------------------------------------------------------------------------
# 7. 08-threshold-accuracy.png: Task 2 Threshold vs Accuracy
# -----------------------------------------------------------------------------
def generate_threshold_accuracy():
    thresholds = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    accuracies = np.array([0.9298, 0.9649, 0.9766, 0.9766, 0.9766, 0.9766, 0.9649, 0.9532, 0.8830])

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.plot(thresholds, accuracies, marker='o', linewidth=2.5, markersize=8, color='#2563EB', label='Точність моделі (Accuracy)')
    
    max_acc = accuracies.max()
    ax.axhline(y=max_acc, color='#10B981', linestyle='--', linewidth=2.0, label=f'Максимальна точність: {max_acc:.3f} (97.7%)')

    # Highlight optimal plateau
    ax.axvspan(0.3, 0.6, color='#DCFCE7', alpha=0.4, label='Оптимальне плато порогів: [0.3 – 0.6]')
    ax.scatter([0.5], [max_acc], color='#D97706', s=120, zorder=5, edgecolors='#0F172A', linewidths=1.5, label='Стандартний поріг: T = 0.5')

    ax.set_xlabel('Поріг прийняття рішень (Decision Threshold)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Точність класифікації (Accuracy)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Залежність точності класифікації від порогу (Breast Cancer Dataset)', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax.set_ylim(0.85, 1.00)
    ax.set_xlim(0.05, 0.95)
    ax.legend(loc='lower center', fontsize=9.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

    plt.tight_layout()
    path = os.path.join(out_dir, "08-threshold-accuracy.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

# -----------------------------------------------------------------------------
# 8. 05-weights-impact.png: Вплив ваг (w) на нахил та орієнтацію межі
# -----------------------------------------------------------------------------
def generate_weights_impact():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=300)

    x = np.linspace(0, 100, 300)
    y = np.linspace(0, 100, 300)
    X, Y = np.meshgrid(x, y)

    # Subplot 1: w = [1, 1], b = -100
    Z1 = X + Y - 100
    ax1.contourf(X, Y, Z1 >= 0, levels=[-0.5, 0.5, 1.5], colors=['#FEE2E2', '#DCFCE7'], alpha=0.6)
    
    x1_line = np.linspace(0, 100, 100)
    x2_line1 = -x1_line + 100
    valid1 = (x2_line1 >= 0) & (x2_line1 <= 100)
    ax1.plot(x1_line[valid1], x2_line1[valid1], color='#2563EB', linewidth=3.2,
             label=r'Розділова межа: $x_1 + x_2 = 100$ ($k = -1$)')

    ax1.annotate('', xy=(68, 68), xytext=(50, 50),
                 arrowprops=dict(facecolor='#1E3A8A', edgecolor='#1E3A8A', width=2.5, headwidth=9, headlength=10))
    ax1.text(69, 69, r'$\mathbf{w} = [1, 1]$' + '\n' + r'(вектор ваг $\perp$ межі)',
             fontsize=10.5, fontweight='bold', color='#1E3A8A', va='bottom', ha='left')

    ax1.scatter([40, 70], [70, 40], color='#10B981', s=100, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax1.text(42, 72, r'$A(40, 70) \to \hat{y}=1$', fontsize=9.5, fontweight='bold', color='#065F46')
    ax1.text(72, 42, r'$B(70, 40) \to \hat{y}=1$', fontsize=9.5, fontweight='bold', color='#065F46')

    ax1.scatter([30], [40], color='#EF4444', s=100, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax1.text(32, 38, r'$C(30, 40) \to \hat{y}=0$', fontsize=9.5, fontweight='bold', color='#991B1B')

    ax1.text(75, 85, 'Клас 1: Прийнято\n($x_1 + x_2 > 100$)', fontsize=11, fontweight='bold',
             color='#166534', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#86EFAC', alpha=0.9))
    ax1.text(25, 20, 'Клас 0: Не прийнято\n($x_1 + x_2 < 100$)', fontsize=11, fontweight='bold',
             color='#991B1B', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#FCA5A5', alpha=0.9))

    ax1.text(0.04, 0.05,
             "• Рівноважні ваги: $w_1 = w_2 = 1$\n• Кут нахилу: 45° ($k = -1$)\n• Внесок $x_1$ та $x_2$ однаковий\n• +10 балів за $x_1$ = +10 балів за $x_2$",
             transform=ax1.transAxes, fontsize=10, verticalalignment='bottom',
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC', edgecolor='#CBD5E1', alpha=0.98))

    ax1.set_title('Приклад 1: Рівноважні ваги\n$w = [1, 1], \\quad b = -100$', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax1.set_xlabel('Іспит 1: $x_1$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Іспит 2: $x_2$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax1.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    # Subplot 2: w = [3, 1], b = -100
    Z2 = 3 * X + Y - 100
    ax2.contourf(X, Y, Z2 >= 0, levels=[-0.5, 0.5, 1.5], colors=['#FEE2E2', '#DCFCE7'], alpha=0.6)

    ax2.plot(x1_line[valid1], x2_line1[valid1], color='#94A3B8', linewidth=2.0, linestyle='--',
             label=r'Стара межа ($w = [1, 1]$)')

    x2_line2 = -3 * x1_line + 100
    valid2 = (x2_line2 >= 0) & (x2_line2 <= 100)
    ax2.plot(x1_line[valid2], x2_line2[valid2], color='#7C3AED', linewidth=3.2,
             label=r'Нова межа: $3x_1 + x_2 = 100$ ($k = -3$)')

    norm_w = np.sqrt(3**2 + 1**2)
    dx = (3 / norm_w) * 22
    dy = (1 / norm_w) * 22
    ax2.annotate('', xy=(25 + dx, 25 + dy), xytext=(25, 25),
                 arrowprops=dict(facecolor='#5B21B6', edgecolor='#5B21B6', width=2.5, headwidth=9, headlength=10))
    ax2.text(25 + dx + 2, 25 + dy, r'$\mathbf{w} = [3, 1]$' + '\n' + r'(повернутий ближче до $x_1$)',
             fontsize=10.5, fontweight='bold', color='#5B21B6', va='center', ha='left')

    ax2.annotate('Поворот межі\nпри $w_1 = 3$', xy=(18, 55), xytext=(35, 75),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.25", color='#7C3AED', lw=2.2),
                 fontsize=10.5, fontweight='bold', color='#7C3AED', ha='center',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F3FF', edgecolor='#DDD6FE', alpha=0.9))

    ax2.scatter([20], [80], color='#10B981', s=100, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax2.text(23, 82, r'$D(20, 80) \to \hat{y}=1$' + '\n(завдяки високому $x_1$)', fontsize=9, fontweight='bold', color='#065F46')

    ax2.scatter([15], [45], color='#EF4444', s=100, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax2.text(17, 41, r'$E(15, 45) \to \hat{y}=0$', fontsize=9, fontweight='bold', color='#991B1B')

    ax2.text(0.48, 0.05,
             "• $x_1$ у 3 рази важливіший за $x_2$\n• Крутіший нахил ($k = -3$)\n• Невеликий ріст $x_1$ різко змінює клас\n• Для компенсації потрібен утричі більший $x_2$",
             transform=ax2.transAxes, fontsize=10, verticalalignment='bottom', zorder=10,
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFFFFF', edgecolor='#CBD5E1', alpha=1.0))

    ax2.set_title('Приклад 2: $x_1$ важливіший за $x_2$\n$w = [3, 1], \\quad b = -100$', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax2.set_xlabel('Іспит 1: $x_1$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Іспит 2: $x_2$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax2.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    plt.tight_layout()
    path = os.path.join(out_dir, "05-weights-impact.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

# -----------------------------------------------------------------------------
# 9. 05-bias-impact.png: Вплив зміщення (bias b) на паралельний зсув межі
# -----------------------------------------------------------------------------
def generate_bias_impact():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=300)

    x1 = np.linspace(0, 140, 200)

    lines_info = [
        (-80, '#10B981', 'b = -80 (м\'який поріг: x1 + x2 ≥ 80)', '--'),
        (-100, '#2563EB', 'b = -100 (базовий поріг: x1 + x2 ≥ 100)', '-'),
        (-120, '#EF4444', 'b = -120 (суворий поріг: x1 + x2 ≥ 120)', '-.')
    ]

    for b_val, col, lbl, style in lines_info:
        x2 = -x1 - b_val
        valid = (x2 >= 0) & (x2 <= 140)
        ax1.plot(x1[valid], x2[valid], color=col, linewidth=3.0, linestyle=style, label=lbl)

    ax1.annotate('', xy=(100, 50), xytext=(85, 35),
                 arrowprops=dict(facecolor='#1E293B', edgecolor='#1E293B', width=2.5, headwidth=9, headlength=10))
    ax1.text(102, 52, r'$\mathbf{w} = [1, 1]$' + '\n' + r'(однаковий вектор для всіх 3-х меж)',
             fontsize=10.0, fontweight='bold', color='#1E293B', va='bottom', ha='left')

    ax1.annotate('', xy=(50, 50), xytext=(26, 26),
                 arrowprops=dict(arrowstyle="<->", color='#475569', lw=2.4))
    ax1.text(20, 36, 'Паралельний зсув\n(кут не змінюється)', fontsize=9.0, fontweight='bold',
             color='#334155', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8FAFC', edgecolor='#CBD5E1', alpha=0.95))

    ax1.scatter([35], [55], color='#D97706', s=130, edgecolors='#0F172A', linewidths=1.8, zorder=6)
    ax1.annotate('Студент А (35, 55)\nСума = 90 балів:\n[+] b = -80  => Прийнято\n[-] b = -100 => Відхилено',
                 xy=(35, 55), xytext=(12, 85),
                 arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.8),
                 fontsize=9.0, fontweight='bold', color='#B45309',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#FEF3C7', edgecolor='#FCD34D', alpha=0.95))

    ax1.scatter([70], [40], color='#2563EB', s=130, edgecolors='#0F172A', linewidths=1.8, zorder=6)
    ax1.annotate('Студент Б (70, 40)\nСума = 110 балів:\n[+] b = -100 => Прийнято\n[-] b = -120 => Відхилено',
                 xy=(70, 40), xytext=(85, 12),
                 arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8),
                 fontsize=9.0, fontweight='bold', color='#1D4ED8',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#EFF6FF', edgecolor='#BFDBFE', alpha=0.95))

    ax1.set_title('Паралельний зсув межі у 2D просторі ознак\n$w = [1, 1], \\quad b \\in \\{-80, -100, -120\\}$',
                  fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax1.set_xlabel('Іспит 1: $x_1$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Іспит 2: $x_2$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_xlim(0, 135)
    ax1.set_ylim(0, 135)
    ax1.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax1.legend(loc='upper right', fontsize=9.0, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    # Subplot 2: 1D розріз сигмоїди P(y=1)
    S = np.linspace(50, 150, 300)

    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    scale = 0.1
    p_80 = sigmoid(scale * (S - 80))
    p_100 = sigmoid(scale * (S - 100))
    p_120 = sigmoid(scale * (S - 120))

    ax2.plot(S, p_80, color='#10B981', linewidth=2.8, linestyle='--', label=r'$b = -80$: поріг $S = 80$')
    ax2.plot(S, p_100, color='#2563EB', linewidth=3.2, linestyle='-', label=r'$b = -100$: поріг $S = 100$')
    ax2.plot(S, p_120, color='#EF4444', linewidth=2.8, linestyle='-.', label=r'$b = -120$: поріг $S = 120$')

    ax2.axhline(0.5, color='#64748B', linestyle=':', linewidth=1.5, label='Поріг рішення P = 0.5')

    ax2.scatter([80, 100, 120], [0.5, 0.5, 0.5], color=['#10B981', '#2563EB', '#EF4444'],
                s=110, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax2.text(80, 0.53, '80 балів', color='#065F46', fontsize=9.5, fontweight='bold', ha='center')
    ax2.text(100, 0.53, '100 балів', color='#1D4ED8', fontsize=9.5, fontweight='bold', ha='center')
    ax2.text(120, 0.53, '120 балів', color='#991B1B', fontsize=9.5, fontweight='bold', ha='center')

    ax2.annotate('', xy=(122, 0.22), xytext=(78, 0.22),
                 arrowprops=dict(arrowstyle="->", color='#1E293B', lw=2.2))
    ax2.text(100, 0.25, 'Зменшення b (суворіший відбір)\nзміщує криву праворуч',
             fontsize=9.5, fontweight='bold', color='#1E293B', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8FAFC', edgecolor='#CBD5E1', alpha=0.95))

    p_stu_a_80 = sigmoid(scale * (90 - 80))
    p_stu_a_100 = sigmoid(scale * (90 - 100))
    ax2.scatter([90, 90], [p_stu_a_80, p_stu_a_100], color='#D97706', s=80, zorder=6)
    ax2.plot([90, 90], [p_stu_a_100, p_stu_a_80], color='#D97706', linestyle=':', lw=2)
    ax2.annotate('Студент А (Сума S=90):\n• P = 73% при b = -80\n• P = 27% при b = -100',
                 xy=(90, p_stu_a_80), xytext=(55, 0.75),
                 arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.8),
                 fontsize=9.0, fontweight='bold', color='#B45309',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF3C7', edgecolor='#FCD34D', alpha=0.95))

    ax2.set_title('Зсув кривої ймовірності $P(y=1) = \\sigma(S + b)$\nзалежно від сумарного балу $S = x_1 + x_2$',
                  fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax2.set_xlabel('Сумарний бал: $S = x_1 + x_2$', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Ймовірність зарахування $P(y=1)$', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_xlim(50, 150)
    ax2.set_ylim(-0.02, 1.05)
    ax2.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax2.legend(loc='lower right', fontsize=9.0, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    plt.tight_layout()
    path = os.path.join(out_dir, "05-bias-impact.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)

if __name__ == '__main__':
    generate_types_of_classification()
    generate_regression_vs_classification()
    generate_outlier_sensitivity()
    generate_decision_boundary_2d()
    generate_linearly_nonseparable()
    generate_one_vs_rest()
    generate_threshold_accuracy()
    generate_weights_impact()
    generate_bias_impact()
    print("All classification basics images generated successfully!")
