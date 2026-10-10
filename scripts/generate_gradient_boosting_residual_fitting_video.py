import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.tree import DecisionTreeRegressor
import subprocess
import os

# Set seed for reproducibility
np.random.seed(42)

# Generate 1D regression dataset
n_samples = 65
X = np.sort(np.random.uniform(0.5, 9.5, n_samples))
y_true = np.sin(0.85 * X) * 2.2 + 0.7 * np.cos(1.8 * X) + 4.2
noise = np.random.normal(0, 0.4, n_samples)
y = y_true + noise

X_2d = X.reshape(-1, 1)
X_grid = np.linspace(0.2, 9.8, 300).reshape(-1, 1)
y_true_grid = np.sin(0.85 * X_grid.ravel()) * 2.2 + 0.7 * np.cos(1.8 * X_grid.ravel()) + 4.2

# Precompute sequential boosting with DecisionTreeRegressor (max_depth=2, lr=0.2)
learning_rate = 0.2
max_trees = 35

f0_val = np.mean(y)
F_train = np.full(n_samples, f0_val)
F_grid = np.full(len(X_grid), f0_val)

models = []
history_F_train = [F_train.copy()]
history_F_grid = [F_grid.copy()]
history_residuals = [(y - F_train).copy()]
history_tree_preds_grid = [np.zeros(len(X_grid))] # for m=0, no tree

for m in range(1, max_trees + 1):
    res = y - F_train
    tree = DecisionTreeRegressor(max_depth=2, random_state=42 + m)
    tree.fit(X_2d, res)
    models.append(tree)
    
    t_pred_train = tree.predict(X_2d)
    t_pred_grid = tree.predict(X_grid)
    
    F_train = F_train + learning_rate * t_pred_train
    F_grid = F_grid + learning_rate * t_pred_grid
    
    history_F_train.append(F_train.copy())
    history_F_grid.append(F_grid.copy())
    history_residuals.append((y - F_train).copy())
    history_tree_preds_grid.append(t_pred_grid.copy())

# Frame schedule for 110 frames
# frames 0..12: m=0 (Baseline)
# frames 13..27: m=1
# frames 28..42: m=2
# frames 43..55: m=3
# frames 56..67: m=5
# frames 68..78: m=8
# frames 79..89: m=14
# frames 90..100: m=22
# frames 101..110: m=35
m_schedule = []
for f in range(110):
    if f < 13:
        m_idx = 0
    elif f < 27:
        m_idx = 1
    elif f < 41:
        m_idx = 2
    elif f < 53:
        m_idx = 3
    elif f < 65:
        m_idx = 5
    elif f < 76:
        m_idx = 8
    elif f < 87:
        m_idx = 14
    elif f < 98:
        m_idx = 22
    else:
        m_idx = 35
    m_schedule.append(m_idx)

# Setup figure
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 0.95], height_ratios=[1.05, 0.95],
                      wspace=0.18, hspace=0.32, left=0.06, right=0.96, top=0.91, bottom=0.08)

ax_fit = fig.add_subplot(gs[:, 0])
ax_res = fig.add_subplot(gs[0, 1])
ax_info = fig.add_subplot(gs[1, 1])

for ax in [ax_fit, ax_res, ax_info]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=10.5)

ax_fit.grid(True, color='#1f2937', linestyle='--', alpha=0.6)
ax_res.grid(True, color='#1f2937', linestyle='--', alpha=0.6)
ax_info.set_xticks([])
ax_info.set_yticks([])

# ax_fit setup
ax_fit.set_xlim(0.2, 9.8)
ax_fit.set_ylim(0.5, 7.6)
ax_fit.set_xlabel('Ознака X', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax_fit.set_ylabel('Цільова змінна y', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax_fit.set_title('Прогноз ансамблю: F_m(x) = F_{m-1}(x) + η · h_m(x)', fontsize=14, fontweight='bold', color='#38bdf8', pad=12)

ax_fit.plot(X_grid.ravel(), y_true_grid, color='#64748b', linestyle='--', linewidth=2.0, alpha=0.7, label='Справжній сигнал (True y)')
ax_fit.scatter(X, y, color='#38bdf8', s=50, edgecolors='#0284c7', linewidths=1.2, alpha=0.85, zorder=4, label='Дані (y_train)')

line_f0 = ax_fit.axhline(f0_val, color='#9ca3af', linestyle=':', linewidth=1.8, alpha=0.5, label=f'Baseline F_0 = {f0_val:.2f}')
line_pred, = ax_fit.plot([], [], color='#10b981', linewidth=3.2, zorder=6, label='Ансамбль F_m(x)')
ax_fit.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

badge_fit = ax_fit.text(
    0.04, 0.05, '', transform=ax_fit.transAxes,
    fontsize=11.5, color='#e5e7eb',
    bbox=dict(boxstyle='round,pad=0.6', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    zorder=10
)

# ax_res setup
ax_res.set_xlim(0.2, 9.8)
ax_res.set_ylim(-3.2, 3.2)
ax_res.set_xlabel('Ознака X', fontsize=11.5, color='#e5e7eb', labelpad=6)
ax_res.set_ylabel('Залишки r_i = y_i - F(x_i)', fontsize=11.5, color='#e5e7eb', labelpad=6)
ax_res.set_title('Навчання слабкого дерева на залишках помилок r_i', fontsize=13, fontweight='bold', color='#facc15', pad=10)
ax_res.axhline(0, color='#6b7280', linestyle='-', linewidth=1.2, alpha=0.8)

# ax_info setup
info_text = ax_info.text(
    0.05, 0.90, '', transform=ax_info.transAxes,
    fontsize=11.5, color='#e5e7eb', verticalalignment='top',
    family='monospace', linespacing=1.4
)

def init():
    line_pred.set_data([], [])
    badge_fit.set_text('')
    info_text.set_text('')
    return [line_pred, badge_fit, info_text]

def update(frame):
    m = m_schedule[frame]
    
    # 1. Update ensemble prediction line
    F_curr_grid = history_F_grid[m]
    line_pred.set_data(X_grid.ravel(), F_curr_grid)
    
    F_curr_train = history_F_train[m]
    mse = np.mean((y - F_curr_train) ** 2)
    mae = np.mean(np.abs(y - F_curr_train))
    
    badge_fit.set_text(
        f"🌲 Ітерація бустингу: m = {m}\n"
        f"📉 Train MSE: {mse:.4f}  |  MAE: {mae:.4f}\n"
        f"⚡ Крок оновлення: η = {learning_rate}"
    )
    
    # 2. Update residuals axis
    ax_res.cla()
    ax_res.set_facecolor('#111827')
    for spine in ax_res.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax_res.tick_params(colors='#9ca3af', labelsize=10.5)
    ax_res.grid(True, color='#1f2937', linestyle='--', alpha=0.6)
    ax_res.set_xlim(0.2, 9.8)
    ax_res.set_ylim(-3.0, 3.0)
    ax_res.set_xlabel('Ознака X', fontsize=11.5, color='#e5e7eb', labelpad=6)
    ax_res.set_ylabel('Залишки r_i = y_i - F_m(x_i)', fontsize=11.5, color='#e5e7eb', labelpad=6)
    ax_res.set_title(f'Поточні залишки помилок (ітерація m={m})', fontsize=13, fontweight='bold', color='#facc15', pad=10)
    ax_res.axhline(0, color='#6b7280', linestyle='-', linewidth=1.2, alpha=0.8)
    
    curr_res = history_residuals[m]
    
    # Draw stems for residuals
    for xi, ri in zip(X, curr_res):
        c = '#ef4444' if ri > 0 else '#38bdf8'
        ax_res.plot([xi, xi], [0, ri], color=c, alpha=0.5, linewidth=1.3)
    
    ax_res.scatter(X, curr_res, c=np.where(curr_res > 0, '#f87171', '#38bdf8'), s=42, edgecolors='#1f2937', zorder=5)
    
    # Draw next tree approximation if m < max_trees
    if m < max_trees:
        tree_idx = m + 1
        t_pred = history_tree_preds_grid[tree_idx] if tree_idx < len(history_tree_preds_grid) else np.zeros(len(X_grid))
        ax_res.plot(X_grid.ravel(), t_pred, color='#facc15', linewidth=2.5, linestyle='--',
                    label=f'Слабке дерево h_{tree_idx}(x) [max_depth=2]')
        ax_res.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=9.5)
    
    # 3. Info diagnostic card
    res_std = np.std(curr_res)
    if m == 0:
        stage_desc = (
            "• Крок 0 (Baseline):\n"
            "  Початковий прогноз дорівнює просто середньому значенню (y_bar).\n"
            "  Залишки r_i величезні й повторюють повну форму вихідних даних.\n"
            "  Наступне дерево h_1(x) навчиться передбачати саме ці залишки!"
        )
    elif m <= 2:
        stage_desc = (
            f"• Крок {m} (Груба форма):\n"
            "  Дерево підхопило головний підйом і спуск синусоїди.\n"
            "  Оновлюємо: F_m(x) = F_{m-1}(x) + 0.2 · h_m(x).\n"
            "  Амплітуда залишків помітно впала з ±2.5 до ±1.3."
        )
    elif m <= 8:
        stage_desc = (
            f"• Крок {m} (Виправлення локальних помилок):\n"
            "  Кожне нове дерево фокусується лише на ділянках, де модель помилилася.\n"
            "  Форма ансамблю згладжується і все точніше повторює справжній сигнал.\n"
            "  Залишки починають коливатися близько до нуля."
        )
    else:
        stage_desc = (
            f"• Крок {m} (Тонка підгонка):\n"
            "  Залишки майже перетворилися на випадковий білий шум.\n"
            "  Ансамбль стабільно утримує правильну криву без диких сплесків.\n"
            "  Темп η=0.2 захищає від різких рухів окремих дерев."
        )
        
    info_text.set_text(
        f"📊 ПОСЛІДОВНЕ ВИПРАВЛЕННЯ ЗАЛИШКІВ\n"
        f"---------------------------------------------------\n"
        f"{stage_desc}\n\n"
        f"📌 Статистика залишків: Mean = {np.mean(curr_res):+.4f} | Std = {res_std:.4f}\n"
        f"💡 Формула: F_{m}(x) = F_0(x) + η·h_1(x) + ... + η·h_{m}(x)"
    )
    
    return [line_pred, badge_fit, info_text]

ani = animation.FuncAnimation(fig, update, frames=110, init_func=init, interval=80)

out_dir = 'public/videos/ai-python/gradient-boosting/gradient-boosting-xgboost'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'gradient_boosting_residual_fitting.mp4')
output_webm = os.path.join(out_dir, 'gradient_boosting_residual_fitting.webm')
output_gif = os.path.join(out_dir, 'gradient_boosting_residual_fitting.gif')
poster_png = os.path.join(out_dir, 'gradient_boosting_residual_fitting_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно створено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:05', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео gradient_boosting_residual_fitting успішно згенеровано!")
