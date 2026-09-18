import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("public/images/ai-python/linear-regression-theory/multiple-regression", exist_ok=True)
os.makedirs("public/images/ai-python/linear-regression-theory/quality-metrics", exist_ok=True)
os.makedirs("public/images/ai-python/linear-regression-theory/gradient-descent", exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Feature Scaling Contours (Multiple Regression)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Unscaled (Elongated Ellipse)
w1 = np.linspace(-5, 5, 200)
w2 = np.linspace(-1, 1, 200)
W1, W2 = np.meshgrid(w1, w2)
Z_unscaled = 0.2 * (W1 - 0.5)**2 + 10.0 * (W2 - 0.1)**2

ax1.contour(W1, W2, Z_unscaled, levels=15, cmap='Blues_r', alpha=0.8)
# Zigzag path
path_w1 = [-4.5, -4.0, -3.2, -2.8, -1.8, -1.2, -0.4, 0.0, 0.3, 0.5]
path_w2 = [ 0.8, -0.7,  0.6, -0.5,  0.4, -0.3,  0.2, -0.1, 0.05, 0.1]
ax1.plot(path_w1, path_w2, 'r-o', linewidth=2, markersize=5, label='Траєкторія GD (зигзаг)')
ax1.plot(0.5, 0.1, 'g*', markersize=16, label='Оптимум (w*)')
ax1.set_title("Без масштабування (Unscaled Features)\nВидовжена ущелина втрат, повільна збіжність", fontsize=12, fontweight='bold', pad=10)
ax1.set_xlabel("Вага w₁ (ознака з великим масштабом, напр. площа м²)", fontsize=10)
ax1.set_ylabel("Вага w₂ (малий масштаб, напр. кімнати)", fontsize=10)
ax1.legend(loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.4)

# Right: Scaled (Z-score, Spherical/Circular contours)
w_s1 = np.linspace(-3, 3, 200)
w_s2 = np.linspace(-3, 3, 200)
WS1, WS2 = np.meshgrid(w_s1, w_s2)
Z_scaled = (WS1 - 0.5)**2 + (WS2 - 0.5)**2

ax2.contour(WS1, WS2, Z_scaled, levels=15, cmap='Blues_r', alpha=0.8)
# Direct path
path_s1 = [-2.5, -1.5, -0.7, 0.0, 0.35, 0.5]
path_s2 = [-2.5, -1.5, -0.7, 0.0, 0.35, 0.5]
ax2.plot(path_s1, path_s2, 'g-o', linewidth=2.5, markersize=6, label='Траєкторія GD (прямий спуск)')
ax2.plot(0.5, 0.5, 'r*', markersize=16, label='Оптимум (w*)')
ax2.set_title("З нормалізацією StandardScaler (Z-Score)\nКонцентричні кола, швидкий і прямий рух", fontsize=12, fontweight='bold', pad=10)
ax2.set_xlabel("Нормалізована вага w₁ (scaled)", fontsize=10)
ax2.set_ylabel("Нормалізована вага w₂ (scaled)", fontsize=10)
ax2.legend(loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig("public/images/ai-python/linear-regression-theory/multiple-regression/04-feature-scaling-contours.png", dpi=200)
plt.close()
print("Generated 04-feature-scaling-contours.png")

# 2. Outlier impact on MAE vs MSE (Quality Metrics)
fig, ax = plt.subplots(figsize=(10, 6))
np.random.seed(42)
x = np.linspace(30, 100, 20)
y_true = 500 * x + np.random.normal(0, 3000, 20)

# Outlier: 1 huge luxury penthouse or typo (e.g. area 95 m^2, price 140,000$ instead of 50,000$)
x_with_outlier = np.append(x, [95])
y_with_outlier = np.append(y_true, [140000])

# Fit MSE (least squares)
coef_clean = np.polyfit(x, y_true, 1)
coef_mse = np.polyfit(x_with_outlier, y_with_outlier, 1)

# Fit MAE approximation (using LAD / robust slope)
# In MAE, outlier doesn't distort line significantly:
x_grid = np.linspace(25, 105, 100)
line_clean = coef_clean[0] * x_grid + coef_clean[1]
line_mse = coef_mse[0] * x_grid + coef_mse[1]

ax.scatter(x, y_true, s=70, color='#3182CE', edgecolor='#1A365D', alpha=0.85, label='Звичайні спостереження (типове житло)', zorder=4)
ax.scatter([95], [140000], s=220, color='#E53E3E', edgecolor='black', linewidth=2, label='Аномальний викид (Outlier / елітний пентхаус)', zorder=6)

ax.plot(x_grid, line_mse, 'r--', linewidth=2.5, label=f'Лінія під MSE втрати (перекошена через 1 викид)', zorder=5)
ax.plot(x_grid, line_clean, 'g-', linewidth=2.5, label=f'Лінія під MAE втрати (стійка до викидів / Robust)', zorder=5)

ax.annotate("Викид різко тягне лінію MSE вгору,\nпогіршуючи прогноз для 95% даних!", 
            xy=(95, 140000), xytext=(45, 120000),
            fontsize=11, fontweight='bold', color='#E53E3E',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF5F5", edgecolor="#E53E3E", lw=1.5),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color="#E53E3E", lw=2))

ax.set_title("Стійкість до викидів: порівняння чутливості MSE та MAE", fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel("Площа (м²)", fontsize=11)
ax.set_ylabel("Ціна ($)", fontsize=11)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig("public/images/ai-python/linear-regression-theory/quality-metrics/03-outlier-impact-mae-mse.png", dpi=200)
plt.close()
print("Generated 03-outlier-impact-mae-mse.png")

# 3. Batch GD vs SGD vs Mini-batch GD (Gradient Descent)
fig, ax = plt.subplots(figsize=(10, 7))

w1_range = np.linspace(-3, 3, 200)
w2_range = np.linspace(-3, 3, 200)
W1, W2 = np.meshgrid(w1_range, w2_range)
Z = 0.5 * (W1 - 0.2)**2 + (W2 - 0.2)**2

ax.contour(W1, W2, Z, levels=12, cmap='viridis', alpha=0.6)

# Batch GD (Smooth, exact)
batch_x = [-2.8, -2.0, -1.2, -0.5, 0.0, 0.15, 0.2]
batch_y = [-2.8, -1.8, -0.9, -0.2, 0.1, 0.18, 0.2]
ax.plot(batch_x, batch_y, color='#3182CE', linewidth=3, marker='o', markersize=5, label='Batch GD (стабільний, плавний рух)')

# SGD (Stochastic - high noise, zigzag)
np.random.seed(10)
sgd_x = [-2.8]
sgd_y = [-2.8]
curr_x, curr_y = -2.8, -2.8
for _ in range(16):
    step_x = 0.22 * (0.2 - curr_x) + np.random.normal(0, 0.45)
    step_y = 0.22 * (0.2 - curr_y) + np.random.normal(0, 0.45)
    curr_x += step_x
    curr_y += step_y
    sgd_x.append(curr_x)
    sgd_y.append(curr_y)
sgd_x.append(0.2)
sgd_y.append(0.2)
ax.plot(sgd_x, sgd_y, color='#E53E3E', linewidth=1.5, linestyle='-', marker='x', markersize=6, alpha=0.85, label='Stochastic GD / SGD (шумний, хаотичний)')

# Mini-batch GD (Balanced, moderate noise)
np.random.seed(25)
mb_x = [-2.8]
mb_y = [-2.8]
curr_x, curr_y = -2.8, -2.8
for _ in range(9):
    step_x = 0.35 * (0.2 - curr_x) + np.random.normal(0, 0.18)
    step_y = 0.35 * (0.2 - curr_y) + np.random.normal(0, 0.18)
    curr_x += step_x
    curr_y += step_y
    mb_x.append(curr_x)
    mb_y.append(curr_y)
mb_x.append(0.2)
mb_y.append(0.2)
ax.plot(mb_x, mb_y, color='#38A169', linewidth=2.5, marker='s', markersize=5, label='Mini-batch GD (золота середина, баланс)')

ax.plot(0.2, 0.2, 'y*', markersize=18, markeredgecolor='black', label='Глобальний мінімум (w*)', zorder=10)

ax.set_title("Порівняння траєкторій оптимізації: Batch vs SGD vs Mini-batch", fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel("Параметр w₁", fontsize=11)
ax.set_ylabel("Параметр w₂", fontsize=11)
ax.legend(loc='lower right', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.35)

plt.tight_layout()
plt.savefig("public/images/ai-python/linear-regression-theory/gradient-descent/08-gd-variants-trajectories.png", dpi=200)
plt.close()
print("Generated 08-gd-variants-trajectories.png")
