import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

# Style configurations
plt.rcParams.update({
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
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

out_dir = 'public/images/ai-python/linear-regression'
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------
# 01.png: Realtor problem - Scatter plot with 3 candidate lines
# -------------------------------------------------------------
print("Generating 01.png...")
np.random.seed(42)
area = np.array([45, 50, 60, 55, 70, 65, 80, 75, 90, 85, 
                 100, 95, 110, 105, 120, 115, 130, 125, 140, 135])
price = 500 * area + np.random.normal(0, 3000, 20)

fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
ax.scatter(area, price, s=100, alpha=0.8, color="#2B6CB0", 
           edgecolor="#1A365D", linewidth=1.5, label="Продані квартири", zorder=4)

x_line = np.array([40, 145])
ax.plot(x_line, 600 * x_line - 5000, color='#E53E3E', linestyle='--', linewidth=2, alpha=0.8, label="Спроба 1: занадто крута")
ax.plot(x_line, 300 * x_line + 10000, color='#38A169', linestyle='--', linewidth=2, alpha=0.8, label="Спроба 2: занадто полога")
ax.plot(x_line, 500 * x_line, color='#ED8936', linewidth=3, label="Спроба 3: найкраща апроксимація")

ax.set_title("Залежність ціни квартири від площі", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Площа (м²)", fontsize=12)
ax.set_ylabel("Ціна ($)", fontsize=12)
ax.grid(True)
ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, '01.png'))
plt.close()

# -------------------------------------------------------------
# 02.png: Regression vs Classification
# -------------------------------------------------------------
print("Generating 02.png...")
np.random.seed(42)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=200)

x_reg = np.linspace(0, 10, 50)
y_reg = 2 * x_reg + 5 + np.random.normal(0, 2, 50)

ax1.scatter(x_reg, y_reg, alpha=0.7, s=60, color="#3182CE", edgecolor="#2B6CB0", label="Спостереження")
ax1.plot(x_reg, 2 * x_reg + 5, color='#E53E3E', linewidth=2.5, label="Лінія регресії (ŷ = 2x + 5)")
ax1.set_title("Регресія: передбачення неперервних значень", fontweight="bold", fontsize=12)
ax1.set_xlabel("Вхідна ознака X", fontsize=11)
ax1.set_ylabel("Вихід Y (неперервне число)", fontsize=11)
ax1.legend(loc="upper left", fontsize=9)
ax1.grid(True)
ax1.text(1.5, 20, "Y може бути будь-яким:\n14.3, 18.7, 21.2, ...", 
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEFCBF", edgecolor="#B7791F", alpha=0.9), fontsize=10)

x_class = np.random.randn(100, 2)
y_class = (x_class[:, 0] + x_class[:, 1] > 0).astype(int)
c_map = ['#E53E3E' if y == 0 else '#3182CE' for y in y_class]
ax2.scatter(x_class[:, 0], x_class[:, 1], c=c_map, alpha=0.7, s=60, edgecolor="#1A202C")
xx = np.linspace(-3, 3, 100)
ax2.plot(xx, -xx, color='#1A202C', linewidth=2.5, linestyle='-', label="Межа рішення")
ax2.set_title("Класифікація: передбачення дискретних класів", fontweight="bold", fontsize=12)
ax2.set_xlabel("Ознака X₁", fontsize=11)
ax2.set_ylabel("Ознака X₂", fontsize=11)
ax2.legend(["Межа класів", "Клас 0 (червоний)", "Клас 1 (синій)"], loc="upper right", fontsize=9)
ax2.grid(True)
ax2.text(-2.8, 2.0, "Y може належати лише\nдо класів: 0 або 1", 
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#BEE3F8", edgecolor="#2B6CB0", alpha=0.9), fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '02.png'))
plt.close()

# -------------------------------------------------------------
# 03.png: Linear equation parameters w and b
# -------------------------------------------------------------
print("Generating 03.png...")
x = np.linspace(0, 10, 100)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=200)

ax1.plot(x, 0.5*x + 5, label="w = 0.5 (пологий)", color="#319795", linewidth=2.5)
ax1.plot(x, 1.0*x + 5, label="w = 1.0 (помірний)", color="#3182CE", linewidth=2.5)
ax1.plot(x, 2.0*x + 5, label="w = 2.0 (крутий)", color="#DD6B20", linewidth=2.5)
ax1.set_title("Вплив ваги w (при фіксованому b = 5)", fontweight="bold", fontsize=12)
ax1.set_xlabel("X (площа квартири, м²)", fontsize=11)
ax1.set_ylabel("Y (ціна, тис. $)", fontsize=11)
ax1.legend(loc="upper left", fontsize=10)
ax1.grid(True)
ax1.text(1, 20, "w = кутовий коефіцієнт\n(зміна Y при ΔX = 1)", 
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEFCBF", edgecolor="#B7791F", alpha=0.9), fontsize=10)

ax2.plot(x, 1.0*x + 0, label="b = 0", color="#4A5568", linewidth=2.5)
ax2.plot(x, 1.0*x + 5, label="b = 5", color="#3182CE", linewidth=2.5)
ax2.plot(x, 1.0*x + 10, label="b = 10", color="#805AD5", linewidth=2.5)
ax2.set_title("Вплив зсуву b (при фіксованому w = 1.0)", fontweight="bold", fontsize=12)
ax2.set_xlabel("X (площа квартири, м²)", fontsize=11)
ax2.set_ylabel("Y (ціна, тис. $)", fontsize=11)
ax2.legend(loc="upper left", fontsize=10)
ax2.grid(True)
ax2.text(1, 16, "b = перетин з віссю Y\n(базова ціна при X = 0)", 
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#BEE3F8", edgecolor="#2B6CB0", alpha=0.9), fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '03.png'))
plt.close()

# -------------------------------------------------------------
# 04.png: District comparison
# -------------------------------------------------------------
print("Generating 04.png...")
area = np.linspace(30, 120, 100)
fig, ax = plt.subplots(figsize=(11, 6), dpi=200)

ax.plot(area, 600*area + 10000, label="Центр: ŷ = 600·x + 10 000", linewidth=2.5, color="#E53E3E")
ax.plot(area, 450*area + 5000, label="Середина: ŷ = 450·x + 5 000", linewidth=2.5, color="#3182CE")
ax.plot(area, 300*area + 2000, label="Околиця: ŷ = 300·x + 2 000", linewidth=2.5, color="#38A169")

ax.scatter([50, 50, 50], [600*50+10000, 450*50+5000, 300*50+2000], 
           s=160, color=["#E53E3E", "#3182CE", "#38A169"], edgecolor="black", linewidth=1.5, zorder=5)

ax.set_title("Ціноутворення в різних районах міста", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Площа квартири (м²)", fontsize=12)
ax.set_ylabel("Ціна ($)", fontsize=12)
ax.legend(fontsize=11, loc="upper left")
ax.grid(True)

ax.annotate("50 м² у центрі:\n$40 000", 
            xy=(50, 600*50+10000), xytext=(68, 42000),
            fontsize=10, fontweight="bold", color="#C53030",
            arrowprops=dict(arrowstyle="->", color="#C53030", lw=2))

ax.annotate("50 м² на околиці:\n$17 000", 
            xy=(50, 300*50+2000), xytext=(32, 8000),
            fontsize=10, fontweight="bold", color="#276749",
            arrowprops=dict(arrowstyle="->", color="#276749", lw=2))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '04.png'))
plt.close()

# -------------------------------------------------------------
# 05.png: Residuals visualization
# -------------------------------------------------------------
print("Generating 05.png...")
np.random.seed(42)
x_res = np.array([40, 50, 60, 70, 80, 90, 100])
y_true = 500 * x_res + np.random.normal(0, 2000, 7)
y_pred = 500 * x_res

fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
ax.plot(x_res, y_pred, color='#E53E3E', linewidth=2.5, label="Лінія регресії (передбачення ŷ = 500x)")
ax.scatter(x_res, y_true, s=120, alpha=0.9, color="#2B6CB0", 
           edgecolor="#1A365D", linewidth=1.8, label="Фактичні дані y", zorder=5)

for xi, yi_true, yi_pred in zip(x_res, y_true, y_pred):
    error = yi_true - yi_pred
    color = "#38A169" if abs(error) < 1500 else "#DD6B20"
    ax.plot([xi, xi], [yi_pred, yi_true], color=color, 
            linewidth=2, linestyle="--", alpha=0.85)
    ax.text(xi + 1.2, (yi_true + yi_pred)/2, f"{error:+.0f}$", 
            fontsize=9.5, fontweight="bold", color=color, va='center')

ax.set_title("Похибки передбачення: залишки (residuals = y − ŷ)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Площа (м²)", fontsize=12)
ax.set_ylabel("Ціна ($)", fontsize=12)
ax.legend(fontsize=11)
ax.grid(True)
ax.text(42, 51000, "Залишок = y_i − ŷ_i\n(довжина вертикального відрізка)", 
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEFCBF", edgecolor="#B7791F", alpha=0.9), fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '05.png'))
plt.close()

# -------------------------------------------------------------
# 06.png: R2 interpretation
# -------------------------------------------------------------
print("Generating 06.png...")
np.random.seed(42)
x_r2 = np.linspace(0, 10, 30)
fig, axes = plt.subplots(2, 2, figsize=(14, 9.5), dpi=200)
fig.suptitle("Що означає коефіцієнт детермінації R²?", fontsize=15, fontweight="bold", y=0.98)

# 1. R2 = 1.0
y_perf = 2 * x_r2 + 5
axes[0, 0].scatter(x_r2, y_perf, alpha=0.8, s=60, color="#38A169", edgecolor="#22543D")
axes[0, 0].plot(x_r2, y_perf, color='#E53E3E', linewidth=2.5)
axes[0, 0].set_title("R² = 1.00 (ідеальна модель)\nВсі точки точно на лінії", fontweight="bold", color="#22543D")
axes[0, 0].grid(True)

# 2. R2 ~ 0.90
y_good = 2 * x_r2 + 5 + np.random.normal(0, 1.2, 30)
r2_good = r2_score(y_good, 2*x_r2 + 5)
axes[0, 1].scatter(x_r2, y_good, alpha=0.8, s=60, color="#3182CE", edgecolor="#2A4365")
axes[0, 1].plot(x_r2, 2*x_r2 + 5, color='#E53E3E', linewidth=2.5)
axes[0, 1].set_title(f"R² = {r2_good:.2f} (дуже висока якість)\nМодель пояснює {r2_good*100:.0f}% дисперсії цілі", 
                     fontweight="bold", color="#2B6CB0")
axes[0, 1].grid(True)

# 3. R2 ~ 0.50
y_med = 2 * x_r2 + 5 + np.random.normal(0, 3.5, 30)
r2_med = r2_score(y_med, 2*x_r2 + 5)
axes[1, 0].scatter(x_r2, y_med, alpha=0.8, s=60, color="#DD6B20", edgecolor="#7B341E")
axes[1, 0].plot(x_r2, 2*x_r2 + 5, color='#E53E3E', linewidth=2.5)
axes[1, 0].set_title(f"R² = {r2_med:.2f} (помірний зв'язок)\nВисокий шум, значний розкид", 
                     fontweight="bold", color="#C05621")
axes[1, 0].grid(True)

# 4. R2 ~ 0
y_bad = np.random.normal(15, 5, 30)
r2_bad = r2_score(y_bad, 2*x_r2 + 5)
axes[1, 1].scatter(x_r2, y_bad, alpha=0.8, s=60, color="#E53E3E", edgecolor="#742A2A")
axes[1, 1].plot(x_r2, 2*x_r2 + 5, color='#E53E3E', linewidth=2.5)
axes[1, 1].axhline(y_bad.mean(), color="#805AD5", linestyle="--", linewidth=2, label="Базове середнє ȳ")
axes[1, 1].set_title(f"R² = {r2_bad:.2f} (непридатна модель)\nМодель не перевершує звичайне середнє", 
                     fontweight="bold", color="#9B2C2C")
axes[1, 1].legend()
axes[1, 1].grid(True)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '06.png'))
plt.close()

# -------------------------------------------------------------
# 07.png: Loss function parabola and regression lines
# -------------------------------------------------------------
print("Generating 07.png...")
x_data = np.array([1, 2, 3, 4, 5])
y_data = np.array([2, 4, 6, 8, 10])

w_vals = np.linspace(0, 4, 100)
losses = [np.mean((y_data - w * x_data) ** 2) for w in w_vals]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=200)

ax1.scatter(x_data, y_data, s=120, color="#E53E3E", edgecolor="black", linewidth=1.5, label="Дані (y = 2x)", zorder=5)
for w, color in zip([0.5, 1.0, 2.0, 3.0], ["#A0AEC0", "#DD6B20", "#38A169", "#805AD5"]):
    ax1.plot(x_data, w * x_data, linewidth=2, alpha=0.8, label=f"w = {w}")
ax1.set_title("Кандидати в лінії регресії (різні w)", fontweight="bold", fontsize=12)
ax1.set_xlabel("X", fontsize=11)
ax1.set_ylabel("Y", fontsize=11)
ax1.legend(loc="upper left")
ax1.grid(True)

ax2.plot(w_vals, losses, linewidth=2.8, color="#2B6CB0")
ax2.scatter([2.0], [0], s=200, color="#38A169", edgecolor="black", linewidth=2, zorder=5, label="w* = 2.0 (глобальний мінімум Loss=0)")
for w, color in zip([0.5, 1.0, 3.0], ["#A0AEC0", "#DD6B20", "#805AD5"]):
    loss_val = np.mean((y_data - w * x_data) ** 2)
    ax2.scatter([w], [loss_val], s=100, color=color, edgecolor="black", linewidth=1.5, zorder=4)
    ax2.annotate(f"w={w}\nMSE={loss_val:.1f}", xy=(w, loss_val), xytext=(w+0.25, loss_val+4),
                 fontsize=9, fontweight="bold", arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
ax2.set_title("Функція втрат L(w) = MSE", fontweight="bold", fontsize=12)
ax2.set_xlabel("Параметр w", fontsize=11)
ax2.set_ylabel("MSE (величина втрат)", fontsize=11)
ax2.legend(loc="upper center")
ax2.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '07.png'))
plt.close()

# -------------------------------------------------------------
# 08.png: Gradient descent trajectory
# -------------------------------------------------------------
print("Generating 08.png...")
w_vals = np.linspace(-1, 6, 100)
loss_vals = (w_vals - 2)**2
traj_w = [5.5, 4.8, 4.0, 3.3, 2.8, 2.4, 2.1, 2.0]
traj_l = [(w - 2)**2 for w in traj_w]

fig, ax = plt.subplots(figsize=(11, 6.5), dpi=200)
ax.plot(w_vals, loss_vals, linewidth=3, color="#2B6CB0", label="Функція втрат L(w) = (w − 2)²")
ax.plot(traj_w, traj_l, 'o-', color='#E53E3E', linewidth=2, markersize=8, label="Траєкторія градієнтного спуску", zorder=5)

ax.scatter([traj_w[0]], [traj_l[0]], s=280, color="#E53E3E", edgecolor="black", linewidth=2, zorder=6, marker="*", label="Старт: w = 5.5")
ax.scatter([traj_w[-1]], [traj_l[-1]], s=280, color="#38A169", edgecolor="black", linewidth=2, zorder=6, marker="*", label="Мінімум: w* = 2.0")

for i in range(len(traj_w) - 1):
    ax.annotate("", xy=(traj_w[i+1], traj_l[i+1]), xytext=(traj_w[i], traj_l[i]),
                arrowprops=dict(arrowstyle="->", lw=2, color="#C53030"))

ax.set_title("Градієнтний спуск: рух у напрямку антиградієнта", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Параметр w", fontsize=12)
ax.set_ylabel("Втрати L(w)", fontsize=12)
ax.legend(fontsize=11)
ax.grid(True)

ax.text(3.8, 8.5, "Кроки оптимізації:\n1. Випадкова ініціалізація\n2. Обчислення градієнта ∂L/∂w\n3. Крок w = w − α·(∂L/∂w)\n4. Зупинка в точці мінімуму", 
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#FEFCBF", edgecolor="#B7791F", alpha=0.9), fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '08.png'))
plt.close()

# -------------------------------------------------------------
# 09.png: Local vs Global minima
# -------------------------------------------------------------
print("Generating 09.png...")
x_nonconv = np.linspace(-10, 10, 500)
y_nonconv = 0.2 * x_nonconv**2 + 5 * np.sin(x_nonconv) + 20

fig, ax = plt.subplots(figsize=(11, 6), dpi=200)
ax.plot(x_nonconv, y_nonconv, linewidth=2.8, color="#2B6CB0")

glob_idx = np.argmin(y_nonconv)
ax.scatter([x_nonconv[glob_idx]], [y_nonconv[glob_idx]], s=280, color="#38A169", 
           edgecolor="black", linewidth=2, zorder=6, marker="*", label="Глобальний мінімум (найкращий розв'язок)")

local_x = [-6.4, 3.3]
local_y = [0.2 * lx**2 + 5 * np.sin(lx) + 20 for lx in local_x]
ax.scatter(local_x, local_y, s=140, color="#DD6B20", edgecolor="black", linewidth=1.5, zorder=5, label="Локальні мінімуми")

ax.set_title("Локальні та глобальний мінімуми складної функції втрат", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Параметр моделі w", fontsize=12)
ax.set_ylabel("Втрати L(w)", fontsize=12)
ax.legend(fontsize=11, loc="upper right")
ax.grid(True)

ax.text(-9.5, 34, "Почавши тут, градієнтний спуск\nможе «застрягти» в локальній ямі!", 
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEFCBF", edgecolor="#B7791F", alpha=0.9), fontsize=10)
ax.annotate("", xy=(-6.4, 25), xytext=(-8.0, 33),
            arrowprops=dict(arrowstyle="->", lw=2, color="#E53E3E"))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '09.png'))
plt.close()

# -------------------------------------------------------------
# 10.png: Learning rate impact
# -------------------------------------------------------------
print("Generating 10.png...")
w_vals = np.linspace(-2, 6, 100)
loss_vals = (w_vals - 2)**2

fig, axes = plt.subplots(1, 3, figsize=(16, 5.2), dpi=200)
fig.suptitle("Вплив темпу навчання (Learning Rate α) на збіжність", fontsize=15, fontweight="bold", y=0.98)

# 1. Too small
ax = axes[0]
ax.plot(w_vals, loss_vals, linewidth=2, color="#2B6CB0")
traj_small = [5.5]
for _ in range(30):
    w_curr = traj_small[-1]
    traj_small.append(w_curr - 0.05 * 2 * (w_curr - 2))
traj_l_small = [(w - 2)**2 for w in traj_small]
ax.plot(traj_small, traj_l_small, 'o-', color='#DD6B20', linewidth=1.5, markersize=4)
ax.set_title("α = 0.05 (занадто малий)\nПовільна збіжність, сотні кроків", fontweight="bold", color="#C05621", fontsize=11)
ax.set_xlabel("w")
ax.set_ylabel("L(w)")
ax.grid(True)

# 2. Optimal
ax = axes[1]
ax.plot(w_vals, loss_vals, linewidth=2, color="#2B6CB0")
traj_opt = [5.5]
for _ in range(8):
    w_curr = traj_opt[-1]
    traj_opt.append(w_curr - 0.5 * 2 * (w_curr - 2))
traj_l_opt = [(w - 2)**2 for w in traj_opt]
ax.plot(traj_opt, traj_l_opt, 'o-', color='#38A169', linewidth=2, markersize=8)
ax.set_title("α = 0.5 (оптимальний)\nШвидка, стабільна збіжність до мінімуму", fontweight="bold", color="#22543D", fontsize=11)
ax.set_xlabel("w")
ax.set_ylabel("L(w)")
ax.grid(True)

# 3. Too large
ax = axes[2]
ax.plot(w_vals, loss_vals, linewidth=2, color="#2B6CB0")
traj_large = [5.5, -0.4, 7.4, -3.2, 10.2]
traj_l_large = [(w - 2)**2 for w in traj_large]
ax.plot(traj_large, traj_l_large, 'o-', color='#E53E3E', linewidth=2, markersize=8)
ax.set_title("α = 1.2 (занадто великий)\nПерестрибування мінімуму, дивергенція", fontweight="bold", color="#9B2C2C", fontsize=11)
ax.set_xlabel("w")
ax.set_ylabel("L(w)")
ax.set_ylim(0, 80)
ax.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '10.png'))
plt.close()

# -------------------------------------------------------------
# 11.png: Initial synthetic dataset
# -------------------------------------------------------------
print("Generating 11.png...")
np.random.seed(42)
X_syn = 2 * np.random.rand(100, 1)
y_syn = 4 + 3 * X_syn + np.random.randn(100, 1)

fig, ax = plt.subplots(figsize=(9, 5.5), dpi=200)
ax.scatter(X_syn, y_syn, alpha=0.75, s=60, color="#3182CE", edgecolor="#2A4365")
ax.set_title("Згенерований синтетичний датасет для навчання регресії", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Вхідна ознака X", fontsize=11)
ax.set_ylabel("Цільове значення y (справжня залежність y = 4 + 3x + шум)", fontsize=11)
ax.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, '11.png'))
plt.close()

# -------------------------------------------------------------
# 12.png: Training result from scratch
# -------------------------------------------------------------
print("Generating 12.png...")
w = np.random.randn()
b = np.random.randn()
lr = 0.1
epochs = 100
loss_hist = []

for epoch in range(epochs):
    y_p = w * X_syn + b
    loss = np.mean((y_syn - y_p) ** 2)
    loss_hist.append(loss)
    grad_w = -2 * np.mean(X_syn * (y_syn - y_p))
    grad_b = -2 * np.mean(y_syn - y_p)
    w = w - lr * grad_w
    b = b - lr * grad_b

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=200)

ax1.scatter(X_syn, y_syn, alpha=0.75, s=50, color="#3182CE", edgecolor="#2A4365", label="Спостереження")
ax1.plot(X_syn, w * X_syn + b, color="#E53E3E", linewidth=2.8, label=f"Лінія: ŷ = {w:.2f}x + {b:.2f}")
ax1.set_title("Результат навчання моделі «з нуля»", fontweight="bold", fontsize=12)
ax1.set_xlabel("X", fontsize=11)
ax1.set_ylabel("y", fontsize=11)
ax1.legend(loc="upper left", fontsize=10)
ax1.grid(True)

ax2.plot(range(1, epochs + 1), loss_hist, linewidth=2.8, color="#1A365D")
ax2.set_title("Збіжність градієнтного спуску (крива втрат)", fontweight="bold", fontsize=12)
ax2.set_xlabel("Епоха (Epoch)", fontsize=11)
ax2.set_ylabel("MSE Loss", fontsize=11)
ax2.grid(True)
ax2.annotate(f"Фінальний Loss: {loss_hist[-1]:.3f}", xy=(100, loss_hist[-1]), 
             xytext=(60, loss_hist[-1] + 2),
             fontsize=10, fontweight="bold", color="#1A365D",
             arrowprops=dict(arrowstyle="->", color="#1A365D", lw=1.5))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '12.png'))
plt.close()

# -------------------------------------------------------------
# 13.png: Multiple Regression Diagnostics (Actual vs Predicted & Residuals)
# -------------------------------------------------------------
print("Generating 13.png...")
np.random.seed(42)
n_samples = 200
X_multi = np.column_stack([
    np.random.uniform(30, 150, n_samples),
    np.random.randint(1, 5, n_samples),
    np.random.randint(1, 20, n_samples)
])
y_multi = 500 * X_multi[:, 0] + 5000 * X_multi[:, 1] + 300 * X_multi[:, 2] + np.random.normal(0, 5000, n_samples)

lr_model = LinearRegression()
lr_model.fit(X_multi, y_multi)
y_multi_pred = lr_model.predict(X_multi)
residuals = y_multi - y_multi_pred

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=200)

ax1.scatter(y_multi, y_multi_pred, alpha=0.75, s=55, color="#3182CE", edgecolor="#1A365D")
min_val, max_val = min(y_multi.min(), y_multi_pred.min()), max(y_multi.max(), y_multi_pred.max())
ax1.plot([min_val, max_val], [min_val, max_val], color="#E53E3E", linestyle="--", linewidth=2.5, label="Ідеальний збіг (y = ŷ)")
ax1.set_title(f"Фактичні vs Передбачені ціни (R² = {r2_score(y_multi, y_multi_pred):.3f})", fontweight="bold", fontsize=12)
ax1.set_xlabel("Фактична ціна ($)", fontsize=11)
ax1.set_ylabel("Передбачена ціна ($)", fontsize=11)
ax1.legend(loc="upper left")
ax1.grid(True)

ax2.hist(residuals, bins=25, color="#4FD1C5", edgecolor="#234E52", alpha=0.85, density=True)
from scipy.stats import norm
mu_res, std_res = norm.fit(residuals)
x_norm = np.linspace(residuals.min(), residuals.max(), 100)
ax2.plot(x_norm, norm.pdf(x_norm, mu_res, std_res), color="#E53E3E", linewidth=2.5, label=f"Normal fit (μ={mu_res:.0f}, σ={std_res:.0f})")
ax2.set_title("Розподіл залишків (Residuals Distribution)", fontweight="bold", fontsize=12)
ax2.set_xlabel("Залишок e = y − ŷ ($)", fontsize=11)
ax2.set_ylabel("Щільність", fontsize=11)
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '13.png'))
plt.close()

# -------------------------------------------------------------
# 14.png: 3D Regression Plane Visualization
# -------------------------------------------------------------
print("Generating 14.png...")
np.random.seed(42)
n_pts = 60
x1_3d = np.random.uniform(30, 120, n_pts)
x2_3d = np.random.randint(1, 6, n_pts)
y_3d = 500 * x1_3d + 6000 * x2_3d + np.random.normal(0, 4000, n_pts)

fig = plt.figure(figsize=(10, 7), dpi=200)
ax3d = fig.add_subplot(111, projection='3d')

# Plane grid
x1_grid, x2_grid = np.meshgrid(np.linspace(30, 120, 20), np.linspace(1, 5, 20))
y_grid = 500 * x1_grid + 6000 * x2_grid

surf = ax3d.plot_surface(x1_grid, x2_grid, y_grid, alpha=0.35, cmap='coolwarm', edgecolor='none')
ax3d.scatter(x1_3d, x2_3d, y_3d, color='#E53E3E', s=50, edgecolor='black', depthshade=True, label="Спостереження квартир")

ax3d.set_title("Геометрична інтерпретація: регресійна площина у 3D просторі", fontsize=13, fontweight="bold", pad=15)
ax3d.set_xlabel("Площа (м²)", fontsize=10, labelpad=8)
ax3d.set_ylabel("Кімнати", fontsize=10, labelpad=8)
ax3d.set_zlabel("Ціна ($)", fontsize=10, labelpad=8)
ax3d.view_init(elev=20, azim=130)
ax3d.legend(loc="upper left")

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '14.png'))
plt.close()

print("All 14 images generated successfully!")
