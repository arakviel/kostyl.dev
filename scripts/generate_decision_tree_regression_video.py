import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from sklearn.tree import DecisionTreeRegressor
import subprocess
import os

# Set seed
np.random.seed(42)

# Generate non-linear 1D regression data
n_samples = 70
X = np.sort(np.random.uniform(0.5, 9.5, n_samples))
# Clean non-linear signal + Gaussian noise
y_true = np.sin(0.85 * X) * 2.2 + 0.8 * np.cos(1.8 * X) + 4.0
noise = np.random.normal(0, 0.45, n_samples)
y = y_true + noise

X_2d = X.reshape(-1, 1)
X_test = np.linspace(0.5, 9.5, 500).reshape(-1, 1)

# Sequence of depths and frames
# 120 frames total:
# 0..15: Depth 0 (mean only)
# 16..35: Depth 1 (2 steps)
# 36..55: Depth 2 (4 steps)
# 56..75: Depth 3 (8 steps)
# 76..95: Depth 5 (18 steps)
# 96..120: Depth 8 (Overfitting to noise)
depth_schedule = (
    [0] * 16 +
    [1] * 20 +
    [2] * 20 +
    [3] * 20 +
    [5] * 20 +
    [8] * 24
)

# Precompute models and predictions
models = {}
preds = {}
mses = {}

# Depth 0: baseline mean
mean_val = np.mean(y)
models[0] = None
preds[0] = np.full(500, mean_val)
mses[0] = np.mean((y - mean_val)**2)

for d in [1, 2, 3, 5, 8]:
    tree = DecisionTreeRegressor(max_depth=d, random_state=42)
    tree.fit(X_2d, y)
    models[d] = tree
    y_pred_grid = tree.predict(X_test)
    preds[d] = y_pred_grid
    mses[d] = np.mean((y - tree.predict(X_2d))**2)

# Setup figure
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 0.95], height_ratios=[1.0, 1.0],
                      wspace=0.18, hspace=0.32, left=0.06, right=0.96, top=0.90, bottom=0.08)

ax_fit = fig.add_subplot(gs[:, 0])
ax_mse = fig.add_subplot(gs[0, 1])
ax_info = fig.add_subplot(gs[1, 1])

for ax in [ax_fit, ax_mse, ax_info]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=11)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.5)

# ax_fit setup
ax_fit.set_xlim(0.2, 9.8)
ax_fit.set_ylim(0.5, 7.5)
ax_fit.set_xlabel('Числова ознака X (наприклад, температура, стаж або площа)', fontsize=13, color='#e5e7eb', labelpad=8)
ax_fit.set_ylabel('Цільова неперервна змінна y (прогноз)', fontsize=13, color='#e5e7eb', labelpad=8)
ax_fit.set_title('Регресійне дерево: Східчаста апроксимація функції (Piecewise Constant)', fontsize=14, fontweight='bold', color='#38bdf8', pad=12)

# True function line and points
ax_fit.plot(X_test.ravel(), np.sin(0.85 * X_test.ravel()) * 2.2 + 0.8 * np.cos(1.8 * X_test.ravel()) + 4.0,
            color='#64748b', linestyle='--', linewidth=2.0, alpha=0.7, label='Справжня залежність (True Signal)')
scatter_pts = ax_fit.scatter(X, y, color='#38bdf8', s=55, edgecolors='#0284c7', linewidths=1.2, alpha=0.9, zorder=5, label='Виміряні дані (зі спостережним шумом)')

step_line, = ax_fit.plot([], [], color='#10b981', linewidth=3.5, zorder=6, label='Прогноз дерева рішень ŷ')
ax_fit.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5, framealpha=0.95)

card_fit = ax_fit.text(
    0.04, 0.04, '', transform=ax_fit.transAxes,
    fontsize=12, color='#e5e7eb', verticalalignment='bottom',
    bbox=dict(boxstyle='round,pad=0.7', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    zorder=10
)

# ax_mse setup
all_depth_keys = [0, 1, 2, 3, 5, 8]
depth_labels = ['d=0\n(База)', 'd=1', 'd=2', 'd=3', 'd=5', 'd=8\n(Шум)']
mse_vals = [mses[d] for d in all_depth_keys]

ax_mse.set_xlim(-0.6, 5.6)
ax_mse.set_ylim(0, 3.2)
ax_mse.set_xticks(range(6))
ax_mse.set_xticklabels(depth_labels, color='#9ca3af', fontsize=11)
ax_mse.set_ylabel('Помилка MSE (Дисперсія залишків)', fontsize=12, color='#e5e7eb', labelpad=6)
ax_mse.set_title('Зниження MSE: Кожне розбиття мінімізує сумарну дисперсію', fontsize=13, fontweight='bold', color='#fbbf24', pad=10)

bars = ax_mse.bar(range(6), [0]*6, color='#fbbf24', edgecolor='#d97706', linewidth=1.5, width=0.55, alpha=0.4)
bars_highlight = ax_mse.bar(range(6), [0]*6, color='#10b981', edgecolor='#059669', linewidth=2.0, width=0.55)

bar_labels = [
    ax_mse.text(i, 0.1, '', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#ffffff')
    for i in range(6)
]

# ax_info setup: conceptual guide
ax_info.set_xlim(0, 1)
ax_info.set_ylim(0, 1)
ax_info.axis('off')

info_text = ax_info.text(
    0.05, 0.95, '',
    fontsize=12, color='#e5e7eb', verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.8', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    linespacing=1.45
)

fig.suptitle('Анімація регресійного дерева: Як розбиття на прямокутні сходинки наближає криву',
             fontsize=17, fontweight='bold', color='#ffffff', y=0.97)

def init():
    step_line.set_data([], [])
    return [step_line]

def update(frame):
    d = depth_schedule[frame]
    pred_y = preds[d]
    cur_mse = mses[d]
    
    step_line.set_data(X_test.ravel(), pred_y)
    
    # Color logic
    if d == 0:
        step_line.set_color('#9ca3af')
        n_leaves = 1
        status_note = "Базовий рівень: прогноз дорівнює просто середньому значенню ȳ."
        border_col = '#9ca3af'
    elif d == 1:
        step_line.set_color('#38bdf8')
        n_leaves = 2
        status_note = "Глибина 1 (Stump): 1 поріг розділив вісь на 2 плоскі сходинки."
        border_col = '#38bdf8'
    elif d == 2:
        step_line.set_color('#34d399')
        n_leaves = 4
        status_note = "Глибина 2: 3 пороги створили 4 сегменти, наближаючи вершину."
        border_col = '#34d399'
    elif d == 3:
        step_line.set_color('#10b981')
        n_leaves = 8
        status_note = "Глибина 3: Збалансована модель, чітко повторює форму хвилі."
        border_col = '#10b981'
    elif d == 5:
        step_line.set_color('#fbbf24')
        n_leaves = 18
        status_note = "Глибина 5: Дерево починає реагувати на локальні флуктуації."
        border_col = '#fbbf24'
    else:
        step_line.set_color('#f43f5e')
        n_leaves = 42
        status_note = "Глибина 8 (Перенавчання): сходинки підлаштовуються під кожну шумну точку!"
        border_col = '#f43f5e'
        
    card_fit.set_text(
        f"• Глибина дерева: max_depth = {d}\n"
        f"  Кількість листків: {n_leaves} сегментів\n"
        f"  Помилка MSE: {cur_mse:.3f}\n"
        f"  {status_note}"
    )
    card_fit.get_bbox_patch().set_edgecolor(border_col)
    
    # Update bars
    idx = all_depth_keys.index(d)
    for i in range(6):
        bars[i].set_height(mse_vals[i])
        bar_labels[i].set_position((i, mse_vals[i] + 0.06))
        bar_labels[i].set_text(f"{mse_vals[i]:.2f}")
        if i == idx:
            bars_highlight[i].set_height(mse_vals[i])
            bars_highlight[i].set_color(border_col)
            bars[i].set_alpha(0.0)
        else:
            bars_highlight[i].set_height(0)
            bars[i].set_alpha(0.35)
            
    info_text.set_text(
        f"📋 Механізм регресії в листку:\n\n"
        f"1. Прогноз у кожному листку — це просте середнє значення:\n"
        f"   ŷ_leaf = (1 / N) · Σ y_i  для всіх точок у цьому сегменті.\n\n"
        f"2. Чому сходинки горизонтальні?\n"
        f"   Дерево не проводить похилих ліній, як лінійна регресія.\n"
        f"   Уся область між двома порогами отримує однакову константу.\n\n"
        f"3. Критерій розбиття (Split Criteria):\n"
        f"   Обирається поріг s, який максимізує зменшення дисперсії:\n"
        f"   ΔMSE = MSE(вузол) - [ (N_L/N)·MSE_L + (N_R/N)·MSE_R ]"
    )
    info_text.get_bbox_patch().set_edgecolor(border_col)
    
    return [step_line, card_fit, info_text]

ani = animation.FuncAnimation(fig, update, frames=120, init_func=init, interval=83)

out_dir = 'public/videos/ai-python/decision-trees-random-forest/decision-trees'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'decision_tree_regression_step_approximation.mp4')
output_webm = os.path.join(out_dir, 'decision_tree_regression_step_approximation.webm')
output_gif = os.path.join(out_dir, 'decision_tree_regression_step_approximation.gif')
poster_png = os.path.join(out_dir, 'decision_tree_regression_step_approximation_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно створено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:06', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео decision_tree_regression_step_approximation успішно згенеровано!")
