import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.tree import DecisionTreeRegressor
import subprocess
import os

np.random.seed(42)

# Generate dataset with train and test points
n_samples = 70
X = np.sort(np.random.uniform(0.5, 9.5, n_samples))
y_true = np.sin(0.9 * X) * 2.3 + 0.6 * np.cos(2.0 * X) + 4.0
noise = np.random.normal(0, 0.45, n_samples)
y = y_true + noise

# 70% Train, 30% Test split
test_indices = np.random.choice(n_samples, size=int(0.3 * n_samples), replace=False)
train_mask = np.ones(n_samples, dtype=bool)
train_mask[test_indices] = False

X_train, y_train = X[train_mask].reshape(-1, 1), y[train_mask]
X_test, y_test = X[~train_mask].reshape(-1, 1), y[~train_mask]

X_grid = np.linspace(0.3, 9.7, 300).reshape(-1, 1)
y_true_grid = np.sin(0.9 * X_grid.ravel()) * 2.3 + 0.6 * np.cos(2.0 * X_grid.ravel()) + 4.0

rates = [0.03, 0.15, 0.90]
rate_labels = ['η = 0.03 (Малий темп)', 'η = 0.15 (Оптимальний)', 'η = 0.90 (Агресивний)']
rate_colors = ['#f59e0b', '#10b981', '#f43f5e']

max_trees = 60

# Precompute boosting for all 3 learning rates
history_preds = {lr: [] for lr in rates}
history_train_mse = {lr: [] for lr in rates}
history_test_mse = {lr: [] for lr in rates}

for lr in rates:
    f0 = np.mean(y_train)
    F_tr = np.full(len(X_train), f0)
    F_te = np.full(len(X_test), f0)
    F_gr = np.full(len(X_grid), f0)
    
    history_preds[lr].append(F_gr.copy())
    history_train_mse[lr].append(np.mean((y_train - F_tr)**2))
    history_test_mse[lr].append(np.mean((y_test - F_te)**2))
    
    for m in range(1, max_trees + 1):
        res = y_train - F_tr
        tree = DecisionTreeRegressor(max_depth=3, random_state=100 + m)
        tree.fit(X_train, res)
        
        F_tr += lr * tree.predict(X_train)
        F_te += lr * tree.predict(X_test)
        F_gr += lr * tree.predict(X_grid)
        
        history_preds[lr].append(F_gr.copy())
        history_train_mse[lr].append(np.mean((y_train - F_tr)**2))
        history_test_mse[lr].append(np.mean((y_test - F_te)**2))

# 110 animation frames mapping to tree count m in [0..60]
# Gradual pacing:
# 0..15: m=0 (Baseline)
# 16..45: m=1..10
# 46..80: m=11..35
# 81..110: m=36..60
m_schedule = []
for f in range(110):
    if f < 15:
        m = 0
    elif f < 45:
        p = (f - 15) / 30.0
        m = int(1 + 9 * p)
    elif f < 80:
        p = (f - 45) / 35.0
        m = int(10 + 25 * p)
    else:
        p = (f - 80) / 30.0
        m = int(35 + 25 * p)
    m_schedule.append(min(max_trees, m))

# Setup figure
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 0.95], height_ratios=[1.0, 1.0],
                      wspace=0.18, hspace=0.32, left=0.06, right=0.96, top=0.91, bottom=0.08)

ax_fit = fig.add_subplot(gs[:, 0])
ax_curve = fig.add_subplot(gs[0, 1])
ax_card = fig.add_subplot(gs[1, 1])

for ax in [ax_fit, ax_curve, ax_card]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=10.5)

ax_fit.grid(True, color='#1f2937', linestyle='--', alpha=0.6)
ax_curve.grid(True, color='#1f2937', linestyle='--', alpha=0.6)
ax_card.set_xticks([])
ax_card.set_yticks([])

# ax_fit setup
ax_fit.set_xlim(0.2, 9.8)
ax_fit.set_ylim(0.5, 7.6)
ax_fit.set_xlabel('Ознака X', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax_fit.set_ylabel('Цільова змінна y', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax_fit.set_title('Вплив темпу навчання η (Learning Rate) на форму моделі', fontsize=14, fontweight='bold', color='#38bdf8', pad=12)

ax_fit.plot(X_grid.ravel(), y_true_grid, color='#64748b', linestyle='--', linewidth=2.0, alpha=0.7, label='Справжній сигнал (True y)')
ax_fit.scatter(X_train, y_train, color='#38bdf8', s=48, edgecolors='#0284c7', alpha=0.85, label='Train точки')
ax_fit.scatter(X_test, y_test, facecolors='none', edgecolors='#facc15', marker='^', s=65, linewidths=1.8, label='Test точки')

lines_pred = []
for lr, col, lbl in zip(rates, rate_colors, rate_labels):
    ln, = ax_fit.plot([], [], color=col, linewidth=2.8, alpha=0.95, label=lbl)
    lines_pred.append(ln)

ax_fit.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

badge_fit = ax_fit.text(
    0.04, 0.05, '', transform=ax_fit.transAxes,
    fontsize=11.5, color='#e5e7eb',
    bbox=dict(boxstyle='round,pad=0.6', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    zorder=10
)

# ax_curve setup: Test MSE vs Trees
ax_curve.set_xlim(0, max_trees)
ax_curve.set_ylim(0.1, 2.5)
ax_curve.set_xlabel('Кількість дерев (m)', fontsize=11.5, color='#e5e7eb', labelpad=6)
ax_curve.set_ylabel('Test MSE (Похибка узагальнення)', fontsize=11.5, color='#e5e7eb', labelpad=6)
ax_curve.set_title('Динаміка Test MSE для трьох значень η', fontsize=13, fontweight='bold', color='#38bdf8', pad=10)

lines_test = []
dots_test = []
for lr, col, lbl in zip(rates, rate_colors, rate_labels):
    ln, = ax_curve.plot([], [], color=col, linewidth=2.2, label=f'Test MSE ({lbl.split()[0]})')
    dt, = ax_curve.plot([], [], marker='o', markersize=7, color=col)
    lines_test.append(ln)
    dots_test.append(dt)

ax_curve.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=9.5)

# ax_card setup
card_text = ax_card.text(
    0.05, 0.90, '', transform=ax_card.transAxes,
    fontsize=11.5, color='#e5e7eb', verticalalignment='top',
    family='monospace', linespacing=1.35
)

def init():
    for ln in lines_pred:
        ln.set_data([], [])
    for ln in lines_test:
        ln.set_data([], [])
    for dt in dots_test:
        dt.set_data([], [])
    badge_fit.set_text('')
    card_text.set_text('')
    return lines_pred + lines_test + dots_test + [badge_fit, card_text]

def update(frame):
    m = m_schedule[frame]
    
    # Update predictions
    for i, lr in enumerate(rates):
        lines_pred[i].set_data(X_grid.ravel(), history_preds[lr][m])
        
        # update test curves up to m
        x_vals = np.arange(m + 1)
        y_vals = history_test_mse[lr][:m + 1]
        lines_test[i].set_data(x_vals, y_vals)
        dots_test[i].set_data([m], [history_test_mse[lr][m]])
        
    te_003 = history_test_mse[0.03][m]
    te_015 = history_test_mse[0.15][m]
    te_090 = history_test_mse[0.90][m]
    
    badge_fit.set_text(
        f"🌲 Поточна кількість дерев: m = {m} / {max_trees}\n"
        f"• η=0.03 Test MSE: {te_003:.4f}\n"
        f"• η=0.15 Test MSE: {te_015:.4f}\n"
        f"• η=0.90 Test MSE: {te_090:.4f}"
    )
    
    if m <= 5:
        phase = (
            "• Стадія 1 (Перші 5 дерев):\n"
            "  - η=0.90 різко кидається наздоганяти дані й відразу будує ламану лінію.\n"
            "  - η=0.15 робить акуратні, зважені кроки в напрямку форми сигналу.\n"
            "  - η=0.03 ледь зрушив із місця (сильне недонавчання на старті)."
        )
    elif m <= 25:
        phase = (
            "• Стадія 2 (Середній етап, m ~ 15-25):\n"
            "  - η=0.15 досягає ідеального балансу: мінімальний Test MSE, плавна крива!\n"
            "  - η=0.90 починає підлаштовуватися під шум окремих train-точок.\n"
            "  - η=0.03 повільно, але стабільно покращує прогноз."
        )
    else:
        phase = (
            "• Стадія 3 (Пізній етап, m > 35):\n"
            "  - η=0.90 ПЕРЕНАВЧАЄТЬСЯ: Test MSE росте, модель звивається навколо викидів!\n"
            "  - η=0.15 стабільно утримує лідерство і найменшу помилку узагальнення.\n"
            "  - η=0.03 плавно наближається до оптимуму, потребуючи більше дерев."
        )
        
    card_text.set_text(
        f"📊 ІНЖЕНЕРНИЙ ВИСНОВОК: ПРАВИЛО ТЕМПУ НАВЧАННЯ\n"
        f"---------------------------------------------------\n"
        f"{phase}\n\n"
        f"💡 Практичне правило Data Science:\n"
        f"Зменшуйте learning_rate (наприклад, 0.05–0.1) та пропорційно збільшуйте\n"
        f"n_estimators. Це завжди дає вищу точність, ніж великий η з малим числом дерев!"
    )
    
    return lines_pred + lines_test + dots_test + [badge_fit, card_text]

ani = animation.FuncAnimation(fig, update, frames=110, init_func=init, interval=80)

out_dir = 'public/videos/ai-python/gradient-boosting/gradient-boosting-xgboost'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'gradient_boosting_learning_rate.mp4')
output_webm = os.path.join(out_dir, 'gradient_boosting_learning_rate.webm')
output_gif = os.path.join(out_dir, 'gradient_boosting_learning_rate.gif')
poster_png = os.path.join(out_dir, 'gradient_boosting_learning_rate_poster.png')

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

print("Відео gradient_boosting_learning_rate успішно згенеровано!")
