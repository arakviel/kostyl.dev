import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.linear_model import LinearRegression, LogisticRegression
import subprocess

# Set font and style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

# -----------------------------------------------------------------------------
# Base Dataset: Normal Class 0 and Class 1, plus 1 moving outlier
# -----------------------------------------------------------------------------
np.random.seed(42)
n_c0 = 12
n_c1 = 12

x_c0 = np.linspace(10, 26, n_c0)
y_c0 = np.zeros(n_c0)

x_c1_base = np.linspace(34, 50, n_c1)
y_c1_base = np.ones(n_c1)

# Animation frames: 90 frames
# outlier moves from x=50 to x=125, then pauses
n_frames = 90
outlier_positions = np.concatenate([
    np.full(12, 50.0),                          # initial pause
    np.linspace(50.0, 120.0, 58),               # moving outlier
    np.full(20, 120.0)                          # end pause
])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.2), dpi=100)
fig.patch.set_facecolor('#F8FAFC')

# Line grids & x limits
x_eval = np.linspace(5, 125, 400)

def setup_ax(ax, title):
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(5, 125)
    ax.set_ylim(-0.25, 1.25)
    ax.axhline(0.0, color='#94A3B8', linestyle=':', linewidth=1.0, alpha=0.7)
    ax.axhline(1.0, color='#94A3B8', linestyle=':', linewidth=1.0, alpha=0.7)
    ax.axhline(0.5, color='#F59E0B', linestyle='--', linewidth=1.5, alpha=0.8, label='Поріг P = 0.5')
    ax.set_xlabel('Ознака X (наприклад, вік або сума)', fontsize=11, color='#1E293B', fontweight='bold')
    ax.set_ylabel('Прогноз y / Ймовірність P(y=1)', fontsize=11, color='#1E293B', fontweight='bold')
    ax.set_title(title, fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

setup_ax(ax1, '1. Лінійна регресія (Вразлива до викидів)')
setup_ax(ax2, '2. Логістична регресія (Стійка до викидів)')

# Scatter artists
scatter_c0_1 = ax1.scatter(x_c0, y_c0, color='#3B82F6', s=70, edgecolors='#1E293B', zorder=4, label='Клас 0 (y=0)')
scatter_c1_1 = ax1.scatter(x_c1_base, y_c1_base, color='#10B981', s=70, edgecolors='#1E293B', zorder=4, label='Клас 1 (y=1)')
outlier_dot_1 = ax1.scatter([50], [1], color='#EF4444', s=150, marker='*', edgecolors='#0F172A', linewidths=1.5, zorder=6, label='Викид (Outlier)')

scatter_c0_2 = ax2.scatter(x_c0, y_c0, color='#3B82F6', s=70, edgecolors='#1E293B', zorder=4, label='Клас 0 (y=0)')
scatter_c1_2 = ax2.scatter(x_c1_base, y_c1_base, color='#10B981', s=70, edgecolors='#1E293B', zorder=4, label='Клас 1 (y=1)')
outlier_dot_2 = ax2.scatter([50], [1], color='#EF4444', s=150, marker='*', edgecolors='#0F172A', linewidths=1.5, zorder=6, label='Викид (Outlier)')

# Dynamic lines
line_lin, = ax1.plot([], [], color='#EF4444', linewidth=2.8, label='Лінійна пряма')
thresh_lin_line = ax1.axvline(30, color='#DC2626', linestyle='-.', linewidth=2.0, alpha=0.9, label='Розділова межа')

line_log, = ax2.plot([], [], color='#3B82F6', linewidth=2.8, label='Сигмоїдна крива σ(z)')
thresh_log_line = ax2.axvline(30, color='#2563EB', linestyle='-.', linewidth=2.0, alpha=0.9, label='Розділова межа')

# Badges and metrics text
text_lin = ax1.text(0.04, 0.94, '', transform=ax1.transAxes, fontsize=10,
                    verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF2F2', edgecolor='#FCA5A5', alpha=0.95))

text_log = ax2.text(0.04, 0.94, '', transform=ax2.transAxes, fontsize=10,
                    verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0FDF4', edgecolor='#86EFAC', alpha=0.95))

# Shaded misclassification region on ax1
import matplotlib.patches as mpatches
error_span = mpatches.Rectangle((30, -0.25), 0, 1.5, color='#F87171', alpha=0.25, label='Зона помилкових прогнозів')
ax1.add_patch(error_span)

ax1.legend(loc='lower right', fontsize=8.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
ax2.legend(loc='lower right', fontsize=8.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

plt.tight_layout(rect=[0, 0.05, 1, 0.96])

fig.suptitle('ВПЛИВ ВИКИДУ НА ЛІНІЙНУ ТА ЛОГІСТИЧНУ РЕГРЕСІЮ',
             fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)

def init():
    line_lin.set_data([], [])
    line_log.set_data([], [])
    text_lin.set_text('')
    text_log.set_text('')
    return [line_lin, line_log, text_lin, text_log]

def update(frame):
    outlier_x = outlier_positions[frame]
    
    # Update outlier dots
    outlier_dot_1.set_offsets([[outlier_x, 1.0]])
    outlier_dot_2.set_offsets([[outlier_x, 1.0]])
    
    # Combined dataset with outlier
    X_curr = np.concatenate([x_c0, x_c1_base, [outlier_x]]).reshape(-1, 1)
    y_curr = np.concatenate([y_c0, y_c1_base, [1.0]])
    
    # 1. Fit Linear Regression
    lin_model = LinearRegression()
    lin_model.fit(X_curr, y_curr)
    y_lin_pred = lin_model.predict(x_eval.reshape(-1, 1))
    line_lin.set_data(x_eval, y_lin_pred)
    
    # Threshold where y_pred = 0.5: 0.5 = w * x + b => x = (0.5 - b) / w
    w_lin = lin_model.coef_[0]
    b_lin = lin_model.intercept_
    if abs(w_lin) > 1e-5:
        x_thresh_lin = (0.5 - b_lin) / w_lin
    else:
        x_thresh_lin = 30.0
    
    thresh_lin_line.set_xdata([x_thresh_lin, x_thresh_lin])
    
    # Misclassified points in Class 1 due to threshold shift
    misclassified_c1 = np.sum(x_c1_base < x_thresh_lin)
    
    # Update error span
    if x_thresh_lin > 30.0:
        error_span.set_x(30.0)
        error_span.set_width(x_thresh_lin - 30.0)
        error_span.set_visible(True)
    else:
        error_span.set_visible(False)
        
    text_lin.set_text(
        f"Викид: X = {outlier_x:.1f}\n"
        f"Рівняння: y = {w_lin:.4f}·X + ({b_lin:.2f})\n"
        f"Поріг (y=0.5): X = {x_thresh_lin:.1f}\n"
        f"Помилково класифіковано: {misclassified_c1} з 12 об'єктів!\n"
        f"Статус: Пряма нахилилася до викиду"
    )
    
    # 2. Fit Logistic Regression
    log_model = LogisticRegression(solver='lbfgs', C=1.0)
    log_model.fit(X_curr, y_curr)
    y_log_prob = log_model.predict_proba(x_eval.reshape(-1, 1))[:, 1]
    line_log.set_data(x_eval, y_log_prob)
    
    w_log = log_model.coef_[0][0]
    b_log = log_model.intercept_[0]
    x_thresh_log = -b_log / w_log if abs(w_log) > 1e-5 else 30.0
    thresh_log_line.set_xdata([x_thresh_log, x_thresh_log])
    
    text_log.set_text(
        f"Викид: X = {outlier_x:.1f}\n"
        f"Рівняння: z = {w_log:.4f}·X + ({b_log:.2f})\n"
        f"Поріг (P=0.5): X = {x_thresh_log:.1f}\n"
        f"Помилково класифіковано: 0 об'єктів (100% точно)\n"
        f"Статус: Сигмоїда наситилася, межа стабільна"
    )
    
    return [line_lin, line_log, outlier_dot_1, outlier_dot_2, thresh_lin_line, thresh_log_line, text_lin, text_log]

ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=80)

out_dir = 'public/videos/ai-python/logistic-regression-classification/classification-basics'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'linear_vs_logistic_outlier_dynamics.mp4')
output_webm = os.path.join(out_dir, 'linear_vs_logistic_outlier_dynamics.webm')
output_gif = os.path.join(out_dir, 'linear_vs_logistic_outlier_dynamics.gif')
poster_png = os.path.join(out_dir, 'linear_vs_logistic_outlier_dynamics_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно створено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:04', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео linear_vs_logistic_outlier_dynamics успішно завершено!")
