"""
Generate all visualizations for Module 08: Polynomial Regression & Regularization
- 01.nonlinear-patterns (01-08)
- 02.regularization-methods (01-05)
- 03.housing-prices-practice (01-03)
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV

# Set global styles
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 1.0

base_dir = 'public/images/ai-python/polynomial-regression'
dir_01 = os.path.join(base_dir, 'nonlinear-patterns')
dir_02 = os.path.join(base_dir, 'regularization-methods')
dir_03 = os.path.join(base_dir, 'housing-prices-practice')

os.makedirs(dir_01, exist_ok=True)
os.makedirs(dir_02, exist_ok=True)
os.makedirs(dir_03, exist_ok=True)

rng = np.random.default_rng(42)

# ==============================================================================
# SECTION 1: 01.nonlinear-patterns
# ==============================================================================
print("Generating images for 01.nonlinear-patterns...")

# Common data for 01: experience vs salary
exp = np.linspace(0, 10, 100)
sal = 30000 + 5000 * exp + 800 * exp**2 + rng.normal(0, 5000, 100)
X_exp = exp.reshape(-1, 1)

# 01_01: Scatter Experience vs Salary
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.scatter(exp, sal, color='#2A75D3', alpha=0.75, s=55, edgecolors='black', linewidths=0.6, label='Реальні дані (спостереження)')
ax.set_xlabel('Досвід роботи (роки)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_ylabel('Річна зарплата ($)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_title('Залежність зарплати від досвіду роботи (параболічний тренд)', fontsize=14, fontweight='bold', pad=12)
ax.grid(alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(dir_01, '01.png'), bbox_inches='tight')
plt.close()

# 01_02: Linear regression failure
lr_model = LinearRegression()
lr_model.fit(X_exp, sal)
sal_pred_linear = lr_model.predict(X_exp)
r2_linear = r2_score(sal, sal_pred_linear)

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.scatter(exp, sal, color='#2A75D3', alpha=0.7, s=50, edgecolors='black', linewidths=0.5, label='Реальні дані')
ax.plot(exp, sal_pred_linear, color='#D0021B', linewidth=2.5, label=f'Лінійна регресія (R² = {r2_linear:.2f})')
ax.set_xlabel('Досвід роботи (роки)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_ylabel('Річна зарплата ($)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_title('Лінійна регресія: недонавчання для нелінійних даних', fontsize=14, fontweight='bold', pad=12)
ax.legend(fontsize=11, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(dir_01, '02.png'), bbox_inches='tight')
plt.close()

# 01_03: 4 polynomial degrees comparison (1, 2, 3, 5)
degrees = [1, 2, 3, 5]
colors = ['#D0021B', '#27AE60', '#E67E22', '#8E44AD']
X_exp_line = np.linspace(0, 10, 300).reshape(-1, 1)

fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
for idx, (deg, col) in enumerate(zip(degrees, colors)):
    ax = axes[idx // 2, idx % 2]
    pipe = Pipeline([
        ('poly', PolynomialFeatures(degree=deg)),
        ('reg', LinearRegression())
    ])
    pipe.fit(X_exp, sal)
    y_line = pipe.predict(X_exp_line)
    r2_deg = r2_score(sal, pipe.predict(X_exp))
    
    ax.scatter(exp, sal, color='#2A75D3', alpha=0.55, s=35, edgecolors='black', linewidths=0.4)
    ax.plot(X_exp_line, y_line, color=col, linewidth=2.5, label=f'Ступінь {deg} (R² = {r2_deg:.4f})')
    ax.set_xlabel('Досвід (роки)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Зарплата ($)', fontsize=11, fontweight='bold')
    ax.set_title(f'Поліном ступеня {deg}', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(alpha=0.3, linestyle='--')

plt.suptitle('Порівняння апроксимації поліномами різного ступеня', fontsize=15, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(os.path.join(dir_01, '03.png'), bbox_inches='tight')
plt.close()

# Train/test split for experience/salary
X_tr, X_te, y_tr, y_te = train_test_split(X_exp, sal, test_size=0.3, random_state=42)

# 01_04: Overfitting degree 15
pipe_15 = Pipeline([
    ('poly', PolynomialFeatures(degree=15)),
    ('scaler', StandardScaler()),
    ('reg', LinearRegression())
])
pipe_15.fit(X_tr, y_tr)
r2_tr_15 = pipe_15.score(X_tr, y_tr)
r2_te_15 = pipe_15.score(X_te, y_te)

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.scatter(X_tr, y_tr, color='#2A75D3', s=55, alpha=0.8, edgecolors='black', label=f'Train зразки ({len(X_tr)})')
ax.scatter(X_te, y_te, color='#F39C12', s=55, alpha=0.8, edgecolors='black', label=f'Test зразки ({len(X_te)})')
ax.plot(X_exp_line, pipe_15.predict(X_exp_line), color='#D0021B', linewidth=2.5, 
        label=f'Поліном 15-го ступеня\n(R² train = {r2_tr_15:.4f}, test = {r2_te_15:.4f})')
ax.set_ylim(20000, 145000)
ax.set_xlabel('Досвід роботи (роки)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_ylabel('Зарплата ($)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_title('Катастрофічне перенавчання (Overfitting): ступінь 15', fontsize=14, fontweight='bold', pad=12)
ax.legend(fontsize=11, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(dir_01, '04.png'), bbox_inches='tight')
plt.close()

# 01_05: Train vs Test R2 curve
deg_range = range(1, 16)
tr_scores = []
te_scores = []

for d in deg_range:
    m = Pipeline([
        ('poly', PolynomialFeatures(degree=d)),
        ('scaler', StandardScaler()),
        ('reg', LinearRegression())
    ])
    m.fit(X_tr, y_tr)
    tr_scores.append(m.score(X_tr, y_tr))
    te_scores.append(m.score(X_te, y_te))

fig, ax = plt.subplots(figsize=(10.5, 6), dpi=300)
ax.plot(deg_range, tr_scores, marker='o', linewidth=2.5, label='Train R² (навчальна вибірка)', color='#2A75D3')
ax.plot(deg_range, te_scores, marker='s', linewidth=2.5, label='Test R² (відкладена вибірка)', color='#E67E22')
ax.axvline(x=2, color='#27AE60', linestyle='--', linewidth=2, label='Оптимальний ступінь = 2 (Sweet Spot)')
ax.set_xlabel('Ступінь полінома (Degree)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_ylabel('Коефіцієнт детермінації R²', fontsize=12, fontweight='bold', labelpad=8)
ax.set_title('Критерій вибору складності: Train R² проти Test R²', fontsize=14, fontweight='bold', pad=12)
ax.set_ylim(0.75, 1.02)
ax.legend(fontsize=11, loc='lower left')
ax.grid(alpha=0.35, linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(dir_01, '05.png'), bbox_inches='tight')
plt.close()

# 01_06: Quadratic synthetic example (1, 2, 3)
rng_q = np.random.default_rng(123)
X_q = np.linspace(-5, 5, 80).reshape(-1, 1)
y_q = 100 + 20*X_q.ravel() + 5*X_q.ravel()**2 + rng_q.normal(0, 15, 80)
X_q_line = np.linspace(-5, 5, 200).reshape(-1, 1)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=300)
for i, d in enumerate([1, 2, 3], 0):
    ax = axes[i]
    p = Pipeline([('poly', PolynomialFeatures(degree=d)), ('scaler', StandardScaler()), ('reg', LinearRegression())])
    p.fit(X_q, y_q)
    r2_val = r2_score(y_q, p.predict(X_q))
    ax.scatter(X_q, y_q, color='#2A75D3', alpha=0.55, s=28, edgecolors='black', linewidths=0.5)
    ax.plot(X_q_line, p.predict(X_q_line), color='#D0021B', linewidth=2.5, label=f'Ступінь {d} (R² = {r2_val:.3f})')
    ax.set_title(f'Ступінь {d}', fontsize=12, fontweight='bold')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, linestyle='--')
plt.suptitle('Квадратична функція: y = 100 + 20x + 5x² + шум', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(os.path.join(dir_01, '06.png'), bbox_inches='tight')
plt.close()

# 01_07: Cubic synthetic example (1, 2, 3, 4)
rng_c = np.random.default_rng(456)
X_c = np.linspace(-3, 3, 80).reshape(-1, 1)
y_c = 50 - 10*X_c.ravel() + 3*X_c.ravel()**2 + 2*X_c.ravel()**3 + rng_c.normal(0, 10, 80)
X_c_line = np.linspace(-3, 3, 200).reshape(-1, 1)

fig, axes = plt.subplots(1, 4, figsize=(16, 4.5), dpi=300)
for i, d in enumerate([1, 2, 3, 4], 0):
    ax = axes[i]
    p = Pipeline([('poly', PolynomialFeatures(degree=d)), ('scaler', StandardScaler()), ('reg', LinearRegression())])
    p.fit(X_c, y_c)
    r2_val = r2_score(y_c, p.predict(X_c))
    ax.scatter(X_c, y_c, color='#2A75D3', alpha=0.55, s=25, edgecolors='black', linewidths=0.5)
    ax.plot(X_c_line, p.predict(X_c_line), color='#27AE60' if d == 3 else '#D0021B', linewidth=2.5, label=f'Ступінь {d} (R² = {r2_val:.3f})')
    ax.set_title(f'Ступінь {d}' + (' (Оптимум)' if d == 3 else ''), fontsize=12, fontweight='bold', color='#1E8449' if d == 3 else 'black')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9.5)
    ax.grid(alpha=0.3, linestyle='--')
plt.suptitle('Кубічна функція: y = 50 - 10x + 3x² + 2x³ + шум', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(os.path.join(dir_01, '07.png'), bbox_inches='tight')
plt.close()

# 01_08: Sinusoidal synthetic example (1, 3, 5, 7)
rng_s = np.random.default_rng(789)
X_s = np.linspace(0, 2*np.pi, 100).reshape(-1, 1)
y_s = np.sin(X_s.ravel()) * 10 + rng_s.normal(0, 0.5, 100)
X_s_line = np.linspace(0, 2*np.pi, 300).reshape(-1, 1)

fig, axes = plt.subplots(1, 4, figsize=(16, 4.5), dpi=300)
for i, d in enumerate([1, 3, 5, 7], 0):
    ax = axes[i]
    p = Pipeline([('poly', PolynomialFeatures(degree=d)), ('scaler', StandardScaler()), ('reg', LinearRegression())])
    p.fit(X_s, y_s)
    r2_val = r2_score(y_s, p.predict(X_s))
    ax.scatter(X_s, y_s, color='#2A75D3', alpha=0.5, s=20, edgecolors='black', linewidths=0.4)
    ax.plot(X_s_line, p.predict(X_s_line), color='#8E44AD' if d >= 5 else '#D0021B', linewidth=2.5, label=f'Ступінь {d} (R² = {r2_val:.3f})')
    ax.set_title(f'Ступінь {d}', fontsize=12, fontweight='bold')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.set_ylim(-13, 13)
    ax.legend(fontsize=9.5)
    ax.grid(alpha=0.3, linestyle='--')
plt.suptitle('Синусоїдальна функція: y = 10·sin(x) + шум', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(os.path.join(dir_01, '08.png'), bbox_inches='tight')
plt.close()
print("01.nonlinear-patterns images completed!")

# ==============================================================================
# SECTION 2: 02.regularization-methods
# ==============================================================================
print("Generating images for 02.regularization-methods...")

rng_reg = np.random.default_rng(42)
X_r = np.linspace(0, 10, 100).reshape(-1, 1)
y_r = 30 + 5*X_r.ravel() + 2*X_r.ravel()**2 + rng_reg.normal(0, 10, 100)
X_r_tr, X_r_te, y_r_tr, y_r_te = train_test_split(X_r, y_r, test_size=0.3, random_state=42)
X_r_line = np.linspace(0, 10, 300).reshape(-1, 1)

# 02_01: Ridge with different alphas (5 subplots)
alphas_ridge = [0, 0.1, 1, 10, 100]
fig, axes = plt.subplots(1, 5, figsize=(20, 4.5), dpi=300)
for i, a in enumerate(alphas_ridge):
    ax = axes[i]
    if a == 0:
        p = Pipeline([('poly', PolynomialFeatures(degree=10)), ('scaler', StandardScaler()), ('reg', LinearRegression())])
        title_str = 'α = 0 (OLS)'
    else:
        p = Pipeline([('poly', PolynomialFeatures(degree=10)), ('scaler', StandardScaler()), ('reg', Ridge(alpha=a))])
        title_str = f'Ridge (α = {a})'
    p.fit(X_r_tr, y_r_tr)
    r2_tr = p.score(X_r_tr, y_r_tr)
    r2_te = p.score(X_r_te, y_r_te)
    
    ax.scatter(X_r_tr, y_r_tr, color='#2A75D3', alpha=0.5, s=25, edgecolors='black', linewidths=0.4, label='Train')
    ax.scatter(X_r_te, y_r_te, color='#E67E22', alpha=0.5, s=25, edgecolors='black', linewidths=0.4, label='Test')
    ax.plot(X_r_line, p.predict(X_r_line), color='#D0021B' if a == 0 else ('#27AE60' if a == 10 else '#2A75D3'), linewidth=2.5)
    ax.set_title(f"{title_str}\nTrain R²={r2_tr:.3f} | Test R²={r2_te:.3f}", fontsize=10.5, fontweight='bold')
    ax.set_ylim(0, 260)
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.grid(alpha=0.3, linestyle='--')
    if i == 0:
        ax.legend(fontsize=9, loc='upper left')

plt.suptitle('Вплив гіперпараметра регуляризації α на згладжування полінома 10-го ступеня', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(os.path.join(dir_02, '01.png'), bbox_inches='tight')
plt.close()

# 02_02: Model coefficients (Linear vs Ridge vs Lasso) - Sparsity
rng_sparse = np.random.default_rng(42)
n_samples, n_features = 100, 50
X_sp = rng_sparse.normal(0, 1, (n_samples, n_features))
# Only first 8 features are real
true_weights = np.zeros(n_features)
true_weights[:8] = [10, -8, 6, -5, 4, -3, 2, -1]
y_sp = X_sp @ true_weights + rng_sparse.normal(0, 1.5, n_samples)
scaler_sp = StandardScaler()
X_sp = scaler_sp.fit_transform(X_sp)

lr_sp = LinearRegression().fit(X_sp, y_sp)
ridge_sp = Ridge(alpha=10).fit(X_sp, y_sp)
lasso_sp = Lasso(alpha=0.8).fit(X_sp, y_sp)

fig, axes = plt.subplots(1, 3, figsize=(17, 5), dpi=300)
models_sp = [('LinearRegression (OLS)', lr_sp.coef_, '#D0021B'),
             ('Ridge (L2, α=10)', ridge_sp.coef_, '#2A75D3'),
             ('Lasso (L1, α=0.8)', lasso_sp.coef_, '#27AE60')]

for idx, (name, coefs, col) in enumerate(models_sp):
    ax = axes[idx]
    nonzero = np.sum(np.abs(coefs) > 1e-4)
    bar_colors = [col if abs(c) > 1e-4 else '#CCCCCC' for c in coefs]
    ax.bar(range(len(coefs)), coefs, color=bar_colors, edgecolor='black', linewidth=0.4, width=0.8)
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_title(f"{name}\nНенульових коефіцієнтів: {nonzero} з {len(coefs)}", fontsize=12, fontweight='bold')
    ax.set_xlabel('Індекс ознаки (0–49)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Значення ваги (w)', fontsize=11, fontweight='bold')
    ax.set_ylim(-12, 12)
    ax.grid(alpha=0.3, axis='y', linestyle='--')

plt.suptitle('Порівняння ваг моделей: Lasso обнуляє шумові змінні (L1 Sparsity)', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(os.path.join(dir_02, '02.png'), bbox_inches='tight')
plt.close()

# 02_03: R2 vs Alpha curves for Ridge and Lasso
alphas_curve = np.logspace(-3, 2, 50)
X_sp_tr, X_sp_te, y_sp_tr, y_sp_te = train_test_split(X_sp, y_sp, test_size=0.3, random_state=42)
r2_ridge_te = [Ridge(alpha=a).fit(X_sp_tr, y_sp_tr).score(X_sp_te, y_sp_te) for a in alphas_curve]
r2_lasso_te = [Lasso(alpha=a, max_iter=2000).fit(X_sp_tr, y_sp_tr).score(X_sp_te, y_sp_te) for a in alphas_curve]

fig, ax = plt.subplots(figsize=(10.5, 6), dpi=300)
ax.plot(alphas_curve, r2_ridge_te, color='#2A75D3', linewidth=2.5, label='Ridge (L2) Test R²')
ax.plot(alphas_curve, r2_lasso_te, color='#27AE60', linewidth=2.5, label='Lasso (L1) Test R²')
ax.set_xscale('log')
ax.set_xlabel('Сила регуляризації α (логарифмічна шкала)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_ylabel('Коефіцієнт детермінації R² на тесті', fontsize=12, fontweight='bold', labelpad=8)
ax.set_title('Залежність Test R² від параметра α для Ridge та Lasso', fontsize=14, fontweight='bold', pad=12)
ax.axvline(alphas_curve[np.argmax(r2_lasso_te)], color='#27AE60', linestyle='--', alpha=0.7, label=f'Оптимум Lasso (α = {alphas_curve[np.argmax(r2_lasso_te)]:.3f})')
ax.axvline(alphas_curve[np.argmax(r2_ridge_te)], color='#2A75D3', linestyle='--', alpha=0.7, label=f'Оптимум Ridge (α = {alphas_curve[np.argmax(r2_ridge_te)]:.3f})')
ax.legend(fontsize=10.5, loc='lower left')
ax.grid(alpha=0.35, which='both', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(dir_02, '03.png'), bbox_inches='tight')
plt.close()

# 02_04: Polynomial 15 fit comparison: Linear vs Ridge vs Lasso
poly_deg = 15
pipe_ols = Pipeline([('p', PolynomialFeatures(degree=poly_deg)), ('s', StandardScaler()), ('r', LinearRegression())]).fit(X_r_tr, y_r_tr)
pipe_rid = Pipeline([('p', PolynomialFeatures(degree=poly_deg)), ('s', StandardScaler()), ('r', Ridge(alpha=10))]).fit(X_r_tr, y_r_tr)
pipe_las = Pipeline([('p', PolynomialFeatures(degree=poly_deg)), ('s', StandardScaler()), ('r', Lasso(alpha=0.5, max_iter=3000))]).fit(X_r_tr, y_r_tr)

fig, axes = plt.subplots(1, 3, figsize=(17, 5), dpi=300)
comp_models = [('LinearRegression (Overfit)', pipe_ols, '#D0021B'),
               ('Ridge (α=10, L2)', pipe_rid, '#2A75D3'),
               ('Lasso (α=0.5, L1)', pipe_las, '#27AE60')]

for i, (name, p, col) in enumerate(comp_models):
    ax = axes[i]
    r2_te = p.score(X_r_te, y_r_te)
    ax.scatter(X_r_tr, y_r_tr, color='#2A75D3', alpha=0.5, s=25, edgecolors='black', linewidths=0.4, label='Train')
    ax.scatter(X_r_te, y_r_te, color='#E67E22', alpha=0.5, s=25, edgecolors='black', linewidths=0.4, label='Test')
    ax.plot(X_r_line, p.predict(X_r_line), color=col, linewidth=2.5, label=f'Модель (Test R²={r2_te:.3f})')
    ax.set_ylim(0, 260)
    ax.set_title(name, fontsize=12, fontweight='bold')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(alpha=0.3, linestyle='--')

plt.suptitle('Поліном 15-го ступеня: приборкання перенавчання методами регуляризації', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(os.path.join(dir_02, '04.png'), bbox_inches='tight')
plt.close()

# 02_05: Feature selection: True weights vs Lasso vs Ridge (first 15 features)
fig, ax = plt.subplots(figsize=(12, 5.5), dpi=300)
x_idx = np.arange(15)
width = 0.25

ax.bar(x_idx - width, true_weights[:15], width=width, label='Справжні ваги (Ground Truth)', color='#333333', edgecolor='black')
ax.bar(x_idx, lasso_sp.coef_[:15], width=width, label='Оцінки Lasso (L1)', color='#27AE60', edgecolor='black')
ax.bar(x_idx + width, ridge_sp.coef_[:15], width=width, label='Оцінки Ridge (L2)', color='#2A75D3', edgecolor='black')

ax.set_xticks(x_idx)
ax.set_xticklabels([f'x_{i}' for i in range(15)])
ax.set_xlabel('Ознаки (перші 8 — інформативні, решта — шум)', fontsize=11, fontweight='bold', labelpad=8)
ax.set_ylabel('Значення коефіцієнта', fontsize=11, fontweight='bold', labelpad=8)
ax.set_title('Відбір ознак: Lasso точно занулює шум (x_8...x_14), тоді як Ridge залишає малі ваги', fontsize=13, fontweight='bold', pad=12)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.legend(fontsize=11)
ax.grid(alpha=0.3, axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(dir_02, '05.png'), bbox_inches='tight')
plt.close()
print("02.regularization-methods images completed!")

# ==============================================================================
# SECTION 3: 03.housing-prices-practice
# ==============================================================================
print("Generating images for 03.housing-prices-practice...")
from sklearn.datasets import fetch_california_housing

cal_data = fetch_california_housing(as_frame=True)
df_cal = cal_data.frame
df_cal['MedHouseVal'] = cal_data.target

# 03_01: Correlation with MedHouseVal
corr_vals = df_cal.corr()['MedHouseVal'].sort_values()
corr_vals = corr_vals.drop('MedHouseVal')

ukr_feature_names = {
    'MedInc': 'MedInc (медіанний дохід)',
    'AveRooms': 'AveRooms (середня к-ть кімнат)',
    'HouseAge': 'HouseAge (вік будинку)',
    'AveBedrms': 'AveBedrms (к-ть спалень)',
    'Population': 'Population (населення кварталу)',
    'AveOccup': 'AveOccup (заселеність родини)',
    'Latitude': 'Latitude (географічна широта)',
    'Longitude': 'Longitude (географічна довгота)'
}

fig, ax = plt.subplots(figsize=(10.5, 6), dpi=300)
colors_corr = ['#D0021B' if v < 0 else '#2A75D3' for v in corr_vals.values]
bars = ax.barh([ukr_feature_names.get(k, k) for k in corr_vals.index], corr_vals.values, color=colors_corr, edgecolor='black', linewidth=0.5, height=0.6)
ax.axvline(0, color='black', linewidth=0.9, linestyle='--')
ax.set_xlabel('Коефіцієнт кореляції Пірсона з MedHouseVal', fontsize=11, fontweight='bold', labelpad=8)
ax.set_title('Кореляція ознак California Housing із медіанною ціною житла', fontsize=13, fontweight='bold', pad=12)
ax.set_xlim(-0.25, 0.8)
ax.grid(axis='x', alpha=0.35, linestyle='--')

for bar, val in zip(bars, corr_vals.values):
    offset = 0.015 if val >= 0 else -0.015
    ha = 'left' if val >= 0 else 'right'
    ax.text(val + offset, bar.get_y() + bar.get_height()/2, f'{val:+.3f}', ha=ha, va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(dir_03, '01.png'), bbox_inches='tight')
plt.close()

# 03_02: Ridge GridSearchCV Validation curve on top-5 features
sel_cols = ['MedInc', 'AveRooms', 'HouseAge', 'Latitude', 'Longitude']
X_sub = df_cal[sel_cols]
y_target = df_cal['MedHouseVal']

X_c_tr, X_c_te, y_c_tr, y_c_te = train_test_split(X_sub, y_target, test_size=0.2, random_state=42)

pipe_ridge_search = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('scaler', StandardScaler()),
    ('regressor', Ridge())
])

alphas_test_c = [0.1, 0.5, 1, 5, 10, 50, 100]
grid_ridge = GridSearchCV(pipe_ridge_search, {'regressor__alpha': alphas_test_c}, cv=5, scoring='r2', n_jobs=-1)
grid_ridge.fit(X_c_tr, y_c_tr)

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
ax.plot(alphas_test_c, grid_ridge.cv_results_['mean_test_score'], marker='o', linewidth=2.5, markersize=8, color='#2A75D3', label='Середній CV R² (5-Fold)')
ax.axvline(x=10, color='#D0021B', linestyle='--', linewidth=2, label='Оптимальний α = 10 (R² = 0.6445)')
ax.scatter([10], [grid_ridge.best_score_], color='#D0021B', s=120, zorder=5, edgecolor='black')
ax.set_xscale('log')
ax.set_xlabel('Параметр регуляризації α (логарифмічна шкала)', fontsize=11, fontweight='bold', labelpad=8)
ax.set_ylabel('Коефіцієнт R² (5-Fold CV)', fontsize=11, fontweight='bold', labelpad=8)
ax.set_title('Підбір оптимального α для поліноміальної Ridge-регресії (degree=2)', fontsize=13, fontweight='bold', pad=12)
ax.legend(fontsize=11)
ax.grid(alpha=0.35, which='both', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(dir_03, '02.png'), bbox_inches='tight')
plt.close()

# 03_03: Diagnostic plots (Predicted vs Actual, Residuals, Feature importance)
best_ridge_pipe = grid_ridge.best_estimator_
y_pred_te = best_ridge_pipe.predict(X_c_te)
residuals = y_c_te - y_pred_te

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)

# Subplot 1: Predicted vs Actual
axes[0].scatter(y_c_te, y_pred_te, color='#2A75D3', alpha=0.3, s=20, edgecolors='none')
axes[0].plot([0, 5], [0, 5], color='#D0021B', linestyle='--', linewidth=2, label='Ідеальний прогноз (y = ŷ)')
axes[0].set_xlabel('Фактична ціна MedHouseVal ($100k)', fontsize=11, fontweight='bold')
axes[0].set_ylabel('Передбачена ціна ($100k)', fontsize=11, fontweight='bold')
axes[0].set_title(f'Predicted vs Actual\n(R² = {r2_score(y_c_te, y_pred_te):.4f})', fontsize=12, fontweight='bold')
axes[0].legend(fontsize=10)
axes[0].grid(alpha=0.3, linestyle='--')
axes[0].set_xlim(0, 5.2)
axes[0].set_ylim(0, 5.2)

# Subplot 2: Residuals vs Predicted
axes[1].scatter(y_pred_te, residuals, color='#8E44AD', alpha=0.3, s=20, edgecolors='none')
axes[1].axhline(0, color='#D0021B', linestyle='--', linewidth=2)
axes[1].set_xlabel('Передбачена ціна ($100k)', fontsize=11, fontweight='bold')
axes[1].set_ylabel('Залишки (Residuals: y - ŷ)', fontsize=11, fontweight='bold')
axes[1].set_title(f'Графік залишків\n(MAE = {mean_absolute_error(y_c_te, y_pred_te):.4f})', fontsize=12, fontweight='bold')
axes[1].grid(alpha=0.3, linestyle='--')

# Subplot 3: Feature importance
poly_step = best_ridge_pipe.named_steps['poly']
ridge_step = best_ridge_pipe.named_steps['regressor']
poly_feat_names = poly_step.get_feature_names_out(sel_cols)
coef_df = pd.DataFrame({'feature': poly_feat_names, 'coef': ridge_step.coef_})
coef_df['abs_coef'] = coef_df['coef'].abs()
top_coefs = coef_df.sort_values('abs_coef', ascending=True).tail(8)

axes[2].barh(top_coefs['feature'], top_coefs['coef'], color='#27AE60', edgecolor='black', linewidth=0.5, height=0.6)
axes[2].axvline(0, color='black', linewidth=0.8, linestyle='--')
axes[2].set_xlabel('Вага коефіцієнта (Standardized)', fontsize=11, fontweight='bold')
axes[2].set_title('Топ-8 найвпливовіших поліноміальних ознак', fontsize=12, fontweight='bold')
axes[2].grid(axis='x', alpha=0.35, linestyle='--')

plt.suptitle('Виробнича діагностика поліноміальної Ridge-моделі (California Housing)', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(os.path.join(dir_03, '03.png'), bbox_inches='tight')
plt.close()
print("03.housing-prices-practice images completed!")
print("ALL 16 IMAGES GENERATED SUCCESSFULLY!")
