import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.tree import DecisionTreeRegressor
import subprocess
import os

np.random.seed(42)

# Generate dataset with strong non-linear signal + noise
n_samples = 75
X = np.sort(np.random.uniform(0.5, 9.5, n_samples))
y_true = np.sin(0.85 * X) * 2.2 + 0.8 * np.cos(1.8 * X) + 4.0
noise = np.random.normal(0, 0.55, n_samples)
y = y_true + noise

# 65% Train, 35% Validation
val_indices = np.random.choice(n_samples, size=int(0.35 * n_samples), replace=False)
train_mask = np.ones(n_samples, dtype=bool)
train_mask[val_indices] = False

X_train, y_train = X[train_mask].reshape(-1, 1), y[train_mask]
X_val, y_val = X[~train_mask].reshape(-1, 1), y[~train_mask]

X_grid = np.linspace(0.3, 9.7, 300).reshape(-1, 1)
y_true_grid = np.sin(0.85 * X_grid.ravel()) * 2.2 + 0.8 * np.cos(1.8 * X_grid.ravel()) + 4.0

max_trees = 80
learning_rate = 0.25 # slightly aggressive to clearly induce overfitting past best tree
patience = 10

# Precompute boosting models and train/val error
f0 = np.mean(y_train)
F_tr = np.full(len(X_train), f0)
F_vl = np.full(len(X_val), f0)
F_gr = np.full(len(X_grid), f0)

history_preds_grid = [F_gr.copy()]
history_train_mse = [np.mean((y_train - F_tr)**2)]
history_val_mse = [np.mean((y_val - F_vl)**2)]

best_val_mse = history_val_mse[0]
best_m = 0
early_stop_triggered_at = None

trees = []

for m in range(1, max_trees + 1):
    res = y_train - F_tr
    tree = DecisionTreeRegressor(max_depth=3, random_state=42 + m)
    tree.fit(X_train, res)
    trees.append(tree)
    
    F_tr += learning_rate * tree.predict(X_train)
    F_vl += learning_rate * tree.predict(X_val)
    F_gr += learning_rate * tree.predict(X_grid)
    
    tr_mse = np.mean((y_train - F_tr)**2)
    vl_mse = np.mean((y_val - F_vl)**2)
    
    history_preds_grid.append(F_gr.copy())
    history_train_mse.append(tr_mse)
    history_val_mse.append(vl_mse)
    
    if vl_mse < best_val_mse:
        best_val_mse = vl_mse
        best_m = m
    elif early_stop_triggered_at is None and (m - best_m) >= patience:
        early_stop_triggered_at = m

# Animation frames: 110 frames
# 0..12: m=0 (Baseline)
# 13..55: m=1..best_m (convergence to optimum)
# 56..80: m=best_m..early_stop_triggered_at (patience counter filling up, trigger at 80)
# 81..110: show early stopped model locked at best_m vs what overfit would look like!
m_schedule = []
for f in range(110):
    if f < 12:
        m = 0
    elif f <= 55:
        p = (f - 12) / 43.0
        m = int(1 + (best_m - 1) * p)
    elif f <= 80:
        p = (f - 55) / 25.0
        m = int(best_m + (early_stop_triggered_at - best_m) * p)
    else:
        # Later phase: keep m progressing to show overfitting trajectory on error plot
        p = (f - 80) / 30.0
        m = int(early_stop_triggered_at + (max_trees - early_stop_triggered_at) * p)
    m_schedule.append(min(max_trees, m))

# Setup figure
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 0.95], height_ratios=[1.0, 1.0],
                      wspace=0.18, hspace=0.32, left=0.06, right=0.96, top=0.91, bottom=0.08)

ax_fit = fig.add_subplot(gs[:, 0])
ax_loss = fig.add_subplot(gs[0, 1])
ax_info = fig.add_subplot(gs[1, 1])

for ax in [ax_fit, ax_loss, ax_info]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=10.5)

ax_fit.grid(True, color='#1f2937', linestyle='--', alpha=0.6)
ax_loss.grid(True, color='#1f2937', linestyle='--', alpha=0.6)
ax_info.set_xticks([])
ax_info.set_yticks([])

# ax_fit setup
ax_fit.set_xlim(0.2, 9.8)
ax_fit.set_ylim(0.5, 7.6)
ax_fit.set_xlabel('Ознака X', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax_fit.set_ylabel('Цільова змінна y', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax_fit.set_title('Early Stopping: Запобігання перенавчанню ансамблю дерев', fontsize=14, fontweight='bold', color='#38bdf8', pad=12)

ax_fit.plot(X_grid.ravel(), y_true_grid, color='#64748b', linestyle='--', linewidth=2.0, alpha=0.7, label='Справжній сигнал (True y)')
ax_fit.scatter(X_train, y_train, color='#38bdf8', s=48, edgecolors='#0284c7', alpha=0.85, label='Train точки')
ax_fit.scatter(X_val, y_val, facecolors='none', edgecolors='#facc15', marker='D', s=55, linewidths=1.8, label='Validation точки')

line_curr, = ax_fit.plot([], [], color='#f43f5e', linewidth=2.4, linestyle=':', alpha=0.8, label='Поточна модель (m)')
line_best, = ax_fit.plot([], [], color='#10b981', linewidth=3.4, label=f'Найкраща модель (m*={best_m})')

ax_fit.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

badge_fit = ax_fit.text(
    0.04, 0.05, '', transform=ax_fit.transAxes,
    fontsize=11.5, color='#e5e7eb',
    bbox=dict(boxstyle='round,pad=0.6', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    zorder=10
)

# ax_loss setup
ax_loss.set_xlim(0, max_trees)
ax_loss.set_ylim(0.05, 1.8)
ax_loss.set_xlabel('Кількість дерев (ітерації m)', fontsize=11.5, color='#e5e7eb', labelpad=6)
ax_loss.set_ylabel('Mean Squared Error (MSE)', fontsize=11.5, color='#e5e7eb', labelpad=6)
ax_loss.set_title('Криві Train Loss vs Validation Loss', fontsize=13, fontweight='bold', color='#38bdf8', pad=10)

line_tr, = ax_loss.plot([], [], color='#38bdf8', linewidth=2.2, linestyle='--', label='Train Loss (падає монотонно)')
line_vl, = ax_loss.plot([], [], color='#facc15', linewidth=2.4, label='Validation Loss (U-подібна крива)')
dot_vl, = ax_loss.plot([], [], marker='o', markersize=7, color='#facc15')
star_best, = ax_loss.plot([], [], marker='*', markersize=14, color='#10b981', label=f'Мінімум Val Loss (m*={best_m})')

ax_loss.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=9.5)

# ax_info setup
info_text = ax_info.text(
    0.05, 0.90, '', transform=ax_info.transAxes,
    fontsize=11.5, color='#e5e7eb', verticalalignment='top',
    family='monospace', linespacing=1.35
)

def init():
    line_curr.set_data([], [])
    line_best.set_data([], [])
    line_tr.set_data([], [])
    line_vl.set_data([], [])
    dot_vl.set_data([], [])
    star_best.set_data([], [])
    badge_fit.set_text('')
    info_text.set_text('')
    return [line_curr, line_best, line_tr, line_vl, dot_vl, star_best, badge_fit, info_text]

def update(frame):
    m = m_schedule[frame]
    is_stopped = (frame >= 80)
    
    # 1. Update fit view
    # If not stopped, current curve is active; if stopped, best curve is locked as primary!
    line_curr.set_data(X_grid.ravel(), history_preds_grid[m])
    
    if m >= best_m:
        line_best.set_data(X_grid.ravel(), history_preds_grid[best_m])
    else:
        line_best.set_data([], [])
        
    curr_tr = history_train_mse[m]
    curr_vl = history_val_mse[m]
    
    # 2. Update loss curve
    x_range = np.arange(m + 1)
    line_tr.set_data(x_range, history_train_mse[:m + 1])
    line_vl.set_data(x_range, history_val_mse[:m + 1])
    dot_vl.set_data([m], [curr_vl])
    
    if m >= best_m:
        star_best.set_data([best_m], [best_val_mse])
    else:
        star_best.set_data([], [])
        
    # 3. Status logic
    rounds_since_best = max(0, m - best_m)
    patience_filled = min(patience, rounds_since_best)
    bar = '█' * patience_filled + '░' * (patience - patience_filled)
    
    if not is_stopped:
        if m < best_m:
            status_badge = "🟢 Покращення валідаційної помилки"
            card_status = (
                f"• Стадія 1 (Активне навчання, m={m}):\n"
                f"  Обидві помилки (Train та Val) синхронно зменшуються.\n"
                f"  Модель вивчає спільну форму закономірності даних."
            )
        elif m == best_m:
            status_badge = "⭐ Знайдено глобальний оптимум Val Loss!"
            card_status = (
                f"• Найкраща точка (m*={best_m}):\n"
                f"  Мінімальний Val MSE = {best_val_mse:.4f}!\n"
                f"  Зберігаємо чекпоінт найкращих ваг моделі."
            )
        else:
            status_badge = f"🟡 Очікування покращення ({patience_filled}/{patience})"
            card_status = (
                f"• Стадія 2 (Ризик перенавчання, m={m}):\n"
                f"  Train Loss продовжує падати ({curr_tr:.4f}), але Val Loss зростає ({curr_vl:.4f})!\n"
                f"  Лічильник patience: [{bar}] {patience_filled}/{patience} раундів без покращення."
            )
    else:
        status_badge = f"🛑 Early Stopping Спрацював! Зафіксовано m*={best_m}"
        card_status = (
            f"• Стадія 3 (Зупинка та відкат до чекпоінта):\n"
            f"  10 раундів поспіль якість на валідації не зростала!\n"
            f"  Алгоритм автоматично повернув стан моделі до ітерації m*={best_m}.\n"
            f"  Червона пунктирна лінія показує, яке перенавчання сталося б без зупинки!"
        )

    badge_fit.set_text(
        f"🌲 Дерево: m = {m} | Краще: m* = {best_m}\n"
        f"📉 Train MSE: {curr_tr:.4f} | Val MSE: {curr_vl:.4f}\n"
        f"{status_badge}"
    )

    info_text.set_text(
        f"📊 ТЕЛЕМЕТРІЯ РАННЬОЇ ЗУПИНКИ (EARLY STOPPING)\n"
        f"---------------------------------------------------\n"
        f"{card_status}\n\n"
        f"💡 Переваги Early Stopping у продакшені:\n"
        f"1. Захист від перенавчання (гарантовано обирає мінімум Val Loss).\n"
        f"2. Економія обчислювальних ресурсів і часу (не потрібно тренувати всі 100+ дерев)."
    )

    return [line_curr, line_best, line_tr, line_vl, dot_vl, star_best, badge_fit, info_text]

ani = animation.FuncAnimation(fig, update, frames=110, init_func=init, interval=80)

out_dir = 'public/videos/ai-python/gradient-boosting/gradient-boosting-xgboost'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'gradient_boosting_early_stopping.mp4')
output_webm = os.path.join(out_dir, 'gradient_boosting_early_stopping.webm')
output_gif = os.path.join(out_dir, 'gradient_boosting_early_stopping.gif')
poster_png = os.path.join(out_dir, 'gradient_boosting_early_stopping_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно створено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:07', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео gradient_boosting_early_stopping успішно згенеровано!")
