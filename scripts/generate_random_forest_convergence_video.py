import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.ensemble import RandomForestRegressor
import subprocess
import os

# Set seed
np.random.seed(42)

# Generate 1D non-linear regression dataset
n_samples = 80
X = np.sort(np.random.uniform(0.5, 9.5, n_samples))
y_true = np.sin(0.85 * X) * 2.2 + 0.8 * np.cos(1.8 * X) + 4.0
noise = np.random.normal(0, 0.45, n_samples)
y = y_true + noise

# Train / Test split
test_mask = np.random.rand(n_samples) < 0.3
X_train, y_train = X[~test_mask].reshape(-1, 1), y[~test_mask]
X_test_pts, y_test_pts = X[test_mask].reshape(-1, 1), y[test_mask]

X_grid = np.linspace(0.5, 9.5, 300).reshape(-1, 1)

# Sequence of forest sizes T for 120 frames
# Smooth progression:
# 1..15: 1 tree (jagged baseline)
# 16..75: 2 -> 35 trees (steep convergence)
# 76..100: 36 -> 80 trees (fine stabilization)
# 101..120: 80 -> 120 trees (plateau / saturation)
t_schedule = []
for frame in range(120):
    if frame < 15:
        t = 1
    elif frame < 75:
        p = (frame - 15) / 60.0
        t = int(1 + 34 * (p ** 1.3))
    elif frame < 100:
        p = (frame - 75) / 25.0
        t = int(35 + 45 * p)
    else:
        p = (frame - 100) / 20.0
        t = int(80 + 40 * p)
    t_schedule.append(max(1, t))

# Pre-train forests for unique sizes to make animation fast
unique_ts = sorted(list(set(t_schedule)))
forest_preds = {}
train_mses = {}
test_mses = {}
oob_mses = {}

for t in unique_ts:
    rf = RandomForestRegressor(n_estimators=t, oob_score=(t > 15), random_state=42)
    rf.fit(X_train, y_train)
    forest_preds[t] = rf.predict(X_grid)
    train_mses[t] = np.mean((y_train - rf.predict(X_train))**2)
    test_mses[t] = np.mean((y_test_pts - rf.predict(X_test_pts))**2)
    oob_mses[t] = (1.0 - rf.oob_score_) * np.var(y_train) if (t > 15 and hasattr(rf, 'oob_score_')) else test_mses[t] * 1.05

# Setup plot
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 0.95], height_ratios=[1.0, 1.0],
                      wspace=0.18, hspace=0.32, left=0.06, right=0.96, top=0.90, bottom=0.08)

ax_fit = fig.add_subplot(gs[:, 0])
ax_curve = fig.add_subplot(gs[0, 1])
ax_diag = fig.add_subplot(gs[1, 1])

for ax in [ax_fit, ax_curve, ax_diag]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=10.5)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.5)

# ax_fit setup
ax_fit.set_xlim(0.2, 9.8)
ax_fit.set_ylim(0.5, 7.5)
ax_fit.set_xlabel('Числова ознака X', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax_fit.set_ylabel('Цільова неперервна змінна y', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax_fit.set_title('Згладжування прогнозу Random Forest при зростанні n_estimators', fontsize=14, fontweight='bold', color='#38bdf8', pad=12)

ax_fit.plot(X_grid.ravel(), np.sin(0.85 * X_grid.ravel()) * 2.2 + 0.8 * np.cos(1.8 * X_grid.ravel()) + 4.0,
            color='#64748b', linestyle='--', linewidth=2.0, alpha=0.7, label='Справжній сигнал (True function)')
ax_fit.scatter(X_train, y_train, color='#38bdf8', s=55, edgecolors='#0284c7', linewidths=1.2, alpha=0.85, label='Train точки')
ax_fit.scatter(X_test_pts, y_test_pts, facecolors='none', edgecolors='#facc15', s=70, linewidths=1.8, marker='^', label='Test точки')

pred_line, = ax_fit.plot([], [], color='#10b981', linewidth=3.2, zorder=6, label='Прогноз лісу (середнє Т дерев)')
ax_fit.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

card_fit = ax_fit.text(
    0.04, 0.04, '', transform=ax_fit.transAxes,
    fontsize=11.5, color='#e5e7eb', verticalalignment='bottom',
    bbox=dict(boxstyle='round,pad=0.7', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    zorder=10
)

# ax_curve setup: Error vs n_estimators
ax_curve.set_xlim(0, 125)
ax_curve.set_ylim(0.10, 0.95)
ax_curve.set_xlabel('Кількість дерев (n_estimators)', fontsize=12, color='#e5e7eb', labelpad=6)
ax_curve.set_ylabel('Середньоквадратична помилка (MSE)', fontsize=12, color='#e5e7eb', labelpad=6)
ax_curve.set_title('Крива збіжності: Швидке падіння та насичення (Plateau)', fontsize=13, fontweight='bold', color='#fbbf24', pad=10)

# Precalculate curves for full range
eval_ts = sorted(unique_ts)
eval_train = [train_mses[t] for t in eval_ts]
eval_test = [test_mses[t] for t in eval_ts]

ax_curve.plot(eval_ts, eval_train, color='#38bdf8', linewidth=2.2, linestyle='--', label='Train MSE')
ax_curve.plot(eval_ts, eval_test, color='#f43f5e', linewidth=2.8, label='Test MSE (виходить на плато)')
ax_curve.axvline(50, color='#10b981', linestyle=':', linewidth=1.8, label='Зона насичення (T ≥ 50)')
ax_curve.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=9.5)

dot_train, = ax_curve.plot([], [], marker='o', markersize=8, color='#38bdf8', markeredgecolor='#ffffff', markeredgewidth=1.5)
dot_test, = ax_curve.plot([], [], marker='s', markersize=8, color='#f43f5e', markeredgecolor='#ffffff', markeredgewidth=1.5)

# ax_diag setup
ax_diag.set_xlim(0, 1)
ax_diag.set_ylim(0, 1)
ax_diag.axis('off')

diag_text = ax_diag.text(
    0.05, 0.95, '',
    fontsize=11.5, color='#e5e7eb', verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.8', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    linespacing=1.45
)

fig.suptitle('Анімація збіжності Random Forest: Чому додавання дерев не викликає перенавчання',
             fontsize=17, fontweight='bold', color='#ffffff', y=0.97)

def init():
    pred_line.set_data([], [])
    dot_train.set_data([], [])
    dot_test.set_data([], [])
    return [pred_line, dot_train, dot_test]

def update(frame):
    t = t_schedule[frame]
    y_pred = forest_preds[t]
    tr_mse = train_mses[t]
    te_mse = test_mses[t]
    
    pred_line.set_data(X_grid.ravel(), y_pred)
    dot_train.set_data([t], [tr_mse])
    dot_test.set_data([t], [te_mse])
    
    if t == 1:
        status_note = "Одиночне дерево: ламана лінія, висока дисперсія."
        border_col = '#f43f5e'
        diag_box = (
            "• Початковий стан: T = 1 дерево\n"
            "• Прогноз грубий та кутастий, залежить від випадкових стрибків\n"
            "• Помилка на тесті максимальна"
        )
    elif t < 25:
        status_note = "Швидке усереднення: перші дерева компенсують помилки одне одного."
        border_col = '#fbbf24'
        diag_box = (
            f"• Фаза активного навчання: T = {t} дерев\n"
            "• Помилка Test стрімко падає зі швидкістю ~ 1 / √T\n"
            "• Згладжуються випадкові виступи окремих листків"
        )
    elif t < 60:
        status_note = "Оптимальний ансамбль: плавна, точна крива без перенавчання."
        border_col = '#10b981'
        diag_box = (
            f"• Зона стабілізації: T = {t} дерев\n"
            "• Крива прогнозу майже повністю збігається зі справжнім сигналом\n"
            "• Помилка Test досягла свого мінімуму"
        )
    else:
        status_note = "Насичення (Plateau): подальше додавання дерев не змінює результат."
        border_col = '#38bdf8'
        diag_box = (
            f"• Ефект насичення: T = {t} дерев\n"
            "• Test MSE залишається ідеально пласкою (не росте!)\n"
            "• Фундаментальне правило: ліс НЕ перенавчається від зростання T,\n"
            "  але після 100 дерев ви лише даремно витрачаєте час процесора."
        )
        
    card_fit.set_text(
        f"• Кількість дерев: n_estimators = {t}\n"
        f"  Помилка Train MSE: {tr_mse:.3f} | Test MSE: {te_mse:.3f}\n"
        f"  {status_note}"
    )
    card_fit.get_bbox_patch().set_edgecolor(border_col)
    
    diag_text.set_text(
        f"• Інженерний аналіз збіжності:\n\n"
        f"{diag_box}\n\n"
        f"💡 Практичний висновок для продакшену:\n"
        f"Значення n_estimators=100 є стандартом за замовчуванням у scikit-learn,\n"
        f"оскільки забезпечує 99% максимальної точності без зайвих витрат пам'яті."
    )
    diag_text.get_bbox_patch().set_edgecolor(border_col)
    
    return [pred_line, dot_train, dot_test, card_fit, diag_text]

ani = animation.FuncAnimation(fig, update, frames=120, init_func=init, interval=83)

out_dir = 'public/videos/ai-python/decision-trees-random-forest/random-forest'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'random_forest_convergence.mp4')
output_webm = os.path.join(out_dir, 'random_forest_convergence.webm')
output_gif = os.path.join(out_dir, 'random_forest_convergence.gif')
poster_png = os.path.join(out_dir, 'random_forest_convergence_poster.png')

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

print("Відео random_forest_convergence успішно згенеровано!")
