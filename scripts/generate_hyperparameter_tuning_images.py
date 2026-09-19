"""
Generate visualizations for content/16.ai-python/07.practical-regression/07.hyperparameter-tuning.md
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs('public/images/ai-python/practical-regression/hyperparameter-tuning', exist_ok=True)
output_dir = 'public/images/ai-python/practical-regression/hyperparameter-tuning'

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 1.0

# -------------------------------------------------------------
# 1. Grid Search: Alpha vs R^2 for Ridge Regression
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 6), dpi=300)

alphas = np.array([0.01, 0.1, 1.0, 10.0, 50.0, 100.0, 500.0, 1000.0])
mean_scores = np.array([0.7738, 0.7740, 0.7741, 0.7742, 0.7735, 0.7728, 0.7420, 0.7102])
std_scores = np.array([0.0142, 0.0141, 0.0140, 0.0141, 0.0139, 0.0138, 0.0185, 0.0234])

ax.plot(alphas, mean_scores, 'o-', color='#2A75D3', linewidth=2.5, markersize=8, label='Середній CV R² (5-Fold)', zorder=4)
ax.fill_between(alphas, mean_scores - std_scores, mean_scores + std_scores, alpha=0.18, color='#2A75D3', label='Діапазон розкиду (±1σ)', zorder=2)

# Optimal alpha marker
opt_alpha = 10.0
opt_score = 0.7742
ax.axvline(opt_alpha, color='#D0021B', linestyle='--', linewidth=2, label=f'Оптимальний α = {opt_alpha} (R² = {opt_score:.4f})', zorder=3)
ax.scatter([opt_alpha], [opt_score], color='#D0021B', s=120, zorder=5, edgecolor='black')

ax.set_xscale('log')
ax.set_xlabel('Гіперпараметр регуляризації α (логарифмічна шкала)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_ylabel('Усереднений коефіцієнт R² (5-Fold CV)', fontsize=12, fontweight='bold', labelpad=8)
ax.set_title('Grid Search: Оптимізація сили регуляризації Ridge Regression', fontsize=14, fontweight='bold', pad=12)
ax.set_ylim(0.68, 0.81)

# Annotations
ax.annotate('Зона слабкої регуляризації\n(ризик перенавчання)', xy=(0.05, 0.774), xytext=(0.02, 0.72),
            arrowprops=dict(facecolor='#4A90E2', arrowstyle='->', lw=1.5),
            fontsize=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0F4F8', edgecolor='#B0C4DE'))

ax.annotate('Зона надмірної регуляризації\n(Underfitting / High Bias)', xy=(600, 0.72), xytext=(120, 0.695),
            arrowprops=dict(facecolor='#D0021B', arrowstyle='->', lw=1.5),
            fontsize=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF0F0', edgecolor='#FFB0B0'))

ax.legend(fontsize=11, loc='lower left', framealpha=0.95)
ax.grid(True, which='both', linestyle='--', alpha=0.35)
plt.tight_layout()

p1_a = os.path.join(output_dir, '01.png')
p1_b = os.path.join(output_dir, '01_gridsearch_alpha.png')
plt.savefig(p1_a, bbox_inches='tight')
plt.savefig(p1_b, bbox_inches='tight')
plt.close()
print("Saved 01.png")

# -------------------------------------------------------------
# 2. Grid Search vs Random Search (Bergstra & Bengio diagram)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), dpi=300)

rng = np.random.default_rng(42)

# Grid Search (5x5 = 25 evaluations)
x_grid = np.linspace(0.1, 0.9, 5)
y_grid = np.linspace(0.1, 0.9, 5)
X_g, Y_g = np.meshgrid(x_grid, y_grid)
ax1.scatter(X_g.ravel(), Y_g.ravel(), color='#2A75D3', s=70, edgecolor='black', zorder=3)

# Highlight projections on Important Parameter (X axis)
for x in x_grid:
    ax1.axvline(x, color='#4A90E2', linestyle=':', alpha=0.5)

ax1.set_title('Grid Search (25 обчислень)\nТільки 5 унікальних значень важливого параметра', fontsize=12, fontweight='bold', pad=10)
ax1.set_xlabel('Важливий гіперпараметр (Important)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Малозначущий параметр (Unimportant)', fontsize=11, fontweight='bold')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.grid(alpha=0.25, linestyle='--')

# Random Search (25 evaluations)
x_rand = rng.uniform(0.05, 0.95, 25)
y_rand = rng.uniform(0.05, 0.95, 25)
ax2.scatter(x_rand, y_rand, color='#27AE60', s=70, edgecolor='black', zorder=3)

for x in x_rand:
    ax2.axvline(x, color='#27AE60', linestyle=':', alpha=0.35)

ax2.set_title('Random Search (25 обчислень)\n25 різних унікальних значень важливого параметра!', fontsize=12, fontweight='bold', pad=10, color='#1E8449')
ax2.set_xlabel('Важливий гіперпараметр (Important)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Малозначущий параметр (Unimportant)', fontsize=11, fontweight='bold')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.grid(alpha=0.25, linestyle='--')

fig.suptitle('Порівняння ефективності дослідження простору параметрів: Grid vs Random Search', fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout()

p2_a = os.path.join(output_dir, '02.png')
p2_b = os.path.join(output_dir, '02_grid_vs_random.png')
plt.savefig(p2_a, bbox_inches='tight')
plt.savefig(p2_b, bbox_inches='tight')
plt.close()
print("Saved 02.png")

# -------------------------------------------------------------
# 3. Model Progression / Final Results
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=300)

model_names = [
    'Baseline Linear\n(без обробки)',
    'Ridge (GridSearch)\n(α=10.0, CV=5)',
    'Decision Tree\n(Tuned, depth=10)',
    'Random Forest\n(Baseline, 100 trees)',
    'Random Forest Final\n(Tuned, Pipeline + CV)'
]
r2_scores = [0.7616, 0.7742, 0.7634, 0.8512, 0.8734]
colors = ['#BDC3C7', '#3498DB', '#E67E22', '#2ECC71', '#1B5E20']

bars = ax.barh(model_names, r2_scores, color=colors, edgecolor='black', height=0.6, zorder=3)
ax.set_xlabel('Коефіцієнт детермінації R² на валідації/тесті', fontsize=12, fontweight='bold', labelpad=8)
ax.set_title('Еволюція точності моделей Housing Prices через Hyperparameter Tuning', fontsize=14, fontweight='bold', pad=12)
ax.set_xlim(0.70, 0.92)
ax.grid(axis='x', linestyle='--', alpha=0.35, zorder=1)

for bar, score in zip(bars, r2_scores):
    width = bar.get_width()
    ax.text(width + 0.004, bar.get_y() + bar.get_height()/2, f'R² = {score:.4f}',
            ha='left', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
p3_a = os.path.join(output_dir, '03.png')
p3_b = os.path.join(output_dir, '03_model_progression.png')
plt.savefig(p3_a, bbox_inches='tight')
plt.savefig(p3_b, bbox_inches='tight')
plt.close()
print("Saved 03.png")

# -------------------------------------------------------------
# 4. Decision Tree Hyperparameter Heatmap (max_depth vs min_samples_split)
# -------------------------------------------------------------
import seaborn as sns

depths = ['3', '5', '7', '10', '15']
splits = ['2', '5', '10', '20']
heatmap_data = np.array([
    [0.6090, 0.6682, 0.7214, 0.6597, 0.6579],
    [0.6090, 0.6680, 0.7119, 0.6699, 0.6698],
    [0.6090, 0.6711, 0.7170, 0.7147, 0.6769],
    [0.6090, 0.7307, 0.7426, 0.7111, 0.7110]
])

fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
sns.heatmap(
    heatmap_data, 
    annot=True, 
    fmt='.4f', 
    cmap='Blues', 
    xticklabels=depths, 
    yticklabels=splits,
    cbar_kws={'label': 'Усереднений CV R² (5-Fold)'},
    linewidths=1.5,
    linecolor='white',
    ax=ax
)

# Highlight best combination (depth=7, split=20 or depth=10, split=5 depending on leaf)
ax.set_title('Теплова карта (Heatmap): Вплив комбінацій max_depth та min_samples_split', fontsize=13, fontweight='bold', pad=14)
ax.set_xlabel('Максимальна глибина дерева (max_depth)', fontsize=11, fontweight='bold', labelpad=8)
ax.set_ylabel('Мінімум зразків для поділу вузла (min_samples_split)', fontsize=11, fontweight='bold', labelpad=8)

plt.tight_layout()
p4_a = os.path.join(output_dir, '04.png')
p4_b = os.path.join(output_dir, '04_tree_heatmap.png')
plt.savefig(p4_a, bbox_inches='tight')
plt.savefig(p4_b, bbox_inches='tight')
plt.close()
print("Saved 04.png")

