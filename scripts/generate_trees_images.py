import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing, load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestRegressor

# Output directories
dir_dt = "public/images/ai-python/decision-trees-random-forest/decision-trees"
dir_rf = "public/images/ai-python/decision-trees-random-forest/random-forest"
os.makedirs(dir_dt, exist_ok=True)
os.makedirs(dir_rf, exist_ok=True)

# Set common aesthetic style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# ==========================================
# 1. Decision Trees: California Housing Tree (01.png)
# ==========================================
print("Generating decision-trees/01.png...")
cal_housing = fetch_california_housing(as_frame=True)
X_cal = cal_housing.data
y_cal = cal_housing.target
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_cal, y_cal, test_size=0.2, random_state=42
)

model_small = DecisionTreeRegressor(max_depth=3, random_state=42)
model_small.fit(X_train_c, y_train_c)

fig, ax = plt.subplots(figsize=(20, 10), facecolor='white', dpi=300)
plot_tree(
    model_small,
    feature_names=X_cal.columns,
    filled=True,
    rounded=True,
    fontsize=11,
    ax=ax,
    precision=2
)
ax.set_title('Дерево рішень для регресії (California Housing, max_depth=3)', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(dir_dt, "01.png"), dpi=300)
plt.close()

# ==========================================
# 2. Decision Trees: Validation curve max_depth (02.png)
# ==========================================
print("Generating decision-trees/02.png...")
depths_range = list(range(1, 21))
train_scores = []
test_scores = []

for depth in depths_range:
    model = DecisionTreeRegressor(max_depth=depth, random_state=42)
    model.fit(X_train_c, y_train_c)
    train_scores.append(model.score(X_train_c, y_train_c))
    test_scores.append(model.score(X_test_c, y_test_c))

optimal_depth = depths_range[np.argmax(test_scores)]

plt.figure(figsize=(10, 6), facecolor='white', dpi=300)
plt.plot(depths_range, train_scores, marker='o', linewidth=2.2, label='R² train (навчальна)', color='#1976D2', markersize=6)
plt.plot(depths_range, test_scores, marker='s', linewidth=2.2, label='R² test (тестова)', color='#F57C00', markersize=6)
plt.axvline(x=optimal_depth, color='#388E3C', linestyle='--', linewidth=2, alpha=0.85, 
            label=f'Оптимальна глибина (max_depth={optimal_depth})')

# Annotate overfitting zone
plt.axvspan(optimal_depth + 1, 20, color='#FFCDD2', alpha=0.3, label='Зона перенавчання (Overfitting)')

plt.xlabel('Максимальна глибина дерева (max_depth)', fontsize=12, labelpad=8)
plt.ylabel('Коефіцієнт детермінації R²', fontsize=12, labelpad=8)
plt.title('Вплив максимальної глибини дерева (max_depth) на якість моделі', fontsize=14, fontweight='bold', pad=12)
plt.xticks(depths_range)
plt.legend(fontsize=10.5, loc='center right', framealpha=0.95)
plt.grid(True, linestyle='--', alpha=0.35)
plt.tight_layout()
plt.savefig(os.path.join(dir_dt, "02.png"), dpi=300)
plt.close()

# ==========================================
# 3. Decision Trees: Iris Classification Tree (03.png)
# ==========================================
print("Generating decision-trees/03.png...")
iris = load_iris(as_frame=True)
X_iris = iris.data
y_iris = iris.target
X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(
    X_iris, y_iris, test_size=0.3, random_state=42
)

clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train_i, y_train_i)

fig, ax = plt.subplots(figsize=(18, 9), facecolor='white', dpi=300)
plot_tree(
    clf,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True,
    fontsize=11,
    ax=ax,
    precision=2
)
ax.set_title('Дерево рішень для класифікації (Iris Dataset, max_depth=3)', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(dir_dt, "03.png"), dpi=300)
plt.close()

# ==========================================
# 4. Random Forest: n_estimators vs R² & Time (01.png)
# ==========================================
print("Generating random-forest/01.png...")
n_trees_range = [10, 50, 100, 200, 500]
rf_train_scores = []
rf_test_scores = []
rf_train_times = []

for n in n_trees_range:
    start = time.time()
    rf_model = RandomForestRegressor(n_estimators=n, max_depth=10, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_c, y_train_c)
    rf_train_times.append(time.time() - start)
    rf_train_scores.append(rf_model.score(X_train_c, y_train_c))
    rf_test_scores.append(rf_model.score(X_test_c, y_test_c))

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white', dpi=300)

# 4.1 R² vs n_estimators
axes[0].plot(n_trees_range, rf_train_scores, marker='o', linewidth=2.2, label='R² train', color='#1976D2', markersize=6)
axes[0].plot(n_trees_range, rf_test_scores, marker='s', linewidth=2.2, label='R² test', color='#F57C00', markersize=6)
axes[0].axvline(100, color='#388E3C', linestyle='--', linewidth=1.8, alpha=0.8, label='Оптимальний баланс (n=100)')
axes[0].set_xlabel('Кількість дерев (n_estimators)', fontsize=11, labelpad=8)
axes[0].set_ylabel('Коефіцієнт детермінації R²', fontsize=11, labelpad=8)
axes[0].set_title('Точність прогнозу залежно від кількості дерев', fontsize=12, fontweight='bold', pad=10)
axes[0].legend(fontsize=10, framealpha=0.95)
axes[0].grid(True, linestyle='--', alpha=0.35)

# 4.2 Time vs n_estimators
axes[1].plot(n_trees_range, rf_train_times, marker='o', linewidth=2.2, color='#388E3C', markersize=6)
axes[1].set_xlabel('Кількість дерев (n_estimators)', fontsize=11, labelpad=8)
axes[1].set_ylabel('Час навчання (секунди)', fontsize=11, labelpad=8)
axes[1].set_title('Час навчання моделі (лінійне зростання)', fontsize=12, fontweight='bold', pad=10)
axes[1].grid(True, linestyle='--', alpha=0.35)

plt.tight_layout()
plt.savefig(os.path.join(dir_rf, "01.png"), dpi=300)
plt.close()

# ==========================================
# 5. Random Forest: Feature Importance (02.png)
# ==========================================
print("Generating random-forest/02.png...")
model_rf = RandomForestRegressor(n_estimators=100, max_depth=10, max_features='sqrt', random_state=42, n_jobs=-1)
model_rf.fit(X_train_c, y_train_c)

importances = model_rf.feature_importances_
feature_translations = {
    'MedInc': 'MedInc (медіанний дохід жителів)',
    'Latitude': 'Latitude (географічна широта)',
    'Longitude': 'Longitude (географічна довгота)',
    'AveRooms': 'AveRooms (середня к-сть кімнат)',
    'Population': 'Population (населення кварталу)',
    'HouseAge': 'HouseAge (вік будинку, роки)',
    'AveBedrms': 'AveBedrms (середня к-сть спалень)',
    'AveOccup': 'AveOccup (середня заселеність)'
}

importance_df = pd.DataFrame({
    'Feature': [feature_translations.get(col, col) for col in X_cal.columns],
    'Importance': importances
}).sort_values('Importance', ascending=True)

plt.figure(figsize=(10, 6), facecolor='white', dpi=300)
bars = plt.barh(importance_df['Feature'], importance_df['Importance'], color='#4682B4', edgecolor='#222222', linewidth=0.7, alpha=0.85)

# Add value labels to bars
for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.008, bar.get_y() + bar.get_height()/2, f"{w*100:.1f}%", 
             va='center', ha='left', fontsize=10, fontweight='bold', color='#333333')

plt.xlabel('Відносна важливість ознаки (Gini Importance)', fontsize=12, labelpad=8)
plt.ylabel('Ознаки датасету California Housing', fontsize=12, labelpad=8)
plt.title('Важливість ознак (Feature Importance) у моделі Random Forest', fontsize=14, fontweight='bold', pad=12)
plt.xlim(0, max(importances) * 1.15)
plt.grid(True, linestyle='--', alpha=0.35, axis='x')
plt.tight_layout()
plt.savefig(os.path.join(dir_rf, "02.png"), dpi=300)
plt.close()

print("All 5 images generated successfully!")
