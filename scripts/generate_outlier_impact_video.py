import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import minimize
import subprocess

np.random.seed(42)

# 1. Генерація даних (типові точки)
n_inliers = 22
x_in = np.linspace(0.5, 4.5, n_inliers)
true_w, true_b = 1.5, 2.0
noise = np.random.normal(0, 0.45, n_inliers)
y_in = true_w * x_in + true_b + noise

# 2. Анімація викиду: викид знаходиться на x = 4.2 і піднімається від y=8.5 до y=28.0
outlier_x = 4.2
n_frames = 50
outlier_y_vals = np.linspace(8.5, 28.0, n_frames)

# Зберігаємо історію параметрів
mse_w_hist, mse_b_hist = [], []
mae_w_hist, mae_b_hist = [], []

for y_out in outlier_y_vals:
    x_all = np.append(x_in, outlier_x)
    y_all = np.append(y_in, y_out)
    
    # MSE (Least Squares)
    w_mse, b_mse = np.polyfit(x_all, y_all, 1)
    mse_w_hist.append(w_mse)
    mse_b_hist.append(b_mse)
    
    # MAE (Least Absolute Deviations)
    def loss_mae(params):
        return np.sum(np.abs(y_all - (params[0] * x_all + params[1])))
    
    res = minimize(loss_mae, x0=[true_w, true_b], method='Nelder-Mead')
    mae_w_hist.append(res.x[0])
    mae_b_hist.append(res.x[1])

# Пауза в кінці
pause = 15
total_frames = n_frames + pause

# 3. Налаштування візуалізації
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1], wspace=0.25, left=0.07, right=0.95, top=0.86, bottom=0.1)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

for ax in [ax1, ax2]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
    ax.tick_params(colors='#9ca3af', labelsize=11)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.6)

fig.suptitle("Вплив викидів (Outliers) на моделі: Робастність MAE проти вразливості MSE", 
             fontsize=18, fontweight='bold', color='#f3f4f6', y=0.95)

# Лівий графік (Дані та 2 прямі)
ax1.scatter(x_in, y_in, color='#38bdf8', s=65, alpha=0.9, edgecolors='#0284c7', linewidth=1.5, zorder=3, label='Типові квартири (Inliers)')
outlier_scatter = ax1.scatter([], [], color='#fbbf24', s=160, marker='D', edgecolors='#ef4444', linewidth=2.5, zorder=6, label='Аномальний викид (Outlier)')

line_mae, = ax1.plot([], [], color='#10b981', linewidth=3.2, linestyle='-', zorder=4, label='Модель за MAE (стійка)')
line_mse, = ax1.plot([], [], color='#f43f5e', linewidth=3.2, linestyle='-', zorder=5, label='Модель за MSE (перекошується)')

x_plot = np.linspace(0, 5, 100)
ax1.set_xlim(-0.2, 5.2)
ax1.set_ylim(0, 31)
ax1.set_xlabel('Площа або ознака (x)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Ціна або цільова змінна (y)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_title('Простір даних: зміщення ліній під дією викиду', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

# Правий графік (Зміна кута нахилу w від викиду)
ax2.plot(outlier_y_vals, [true_w]*n_frames, color='#64748b', linestyle=':', linewidth=2, label=f'Справжній нахил w={true_w:.1f}')
mae_w_line, = ax2.plot([], [], color='#10b981', linewidth=2.8, label='Нахил w (MAE-модель)')
mse_w_line, = ax2.plot([], [], color='#f43f5e', linewidth=2.8, label='Нахил w (MSE-модель)')

mae_curr_pt, = ax2.plot([], [], marker='o', color='#10b981', markeredgecolor='#ffffff', markersize=9)
mse_curr_pt, = ax2.plot([], [], marker='o', color='#f43f5e', markeredgecolor='#ffffff', markersize=9)

ax2.set_xlim(outlier_y_vals[0] - 1, outlier_y_vals[-1] + 1)
ax2.set_ylim(1.0, 5.5)
ax2.set_xlabel('Значення аномального викиду (Y викиду)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Коефіцієнт нахилу моделі (w)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_title('Деформація параметра w: стійкість vs перекіс', fontsize=14, fontweight='bold', color='#fbbf24', pad=10)
ax2.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

status_box = ax1.text(0.04, 0.55, '', transform=ax1.transAxes, 
                      fontsize=11.5, family='monospace', color='#f9fafb',
                      bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))

def init():
    line_mae.set_data([], [])
    line_mse.set_data([], [])
    outlier_scatter.set_offsets(np.empty((0, 2)))
    mae_w_line.set_data([], [])
    mse_w_line.set_data([], [])
    mae_curr_pt.set_data([], [])
    mse_curr_pt.set_data([], [])
    status_box.set_text('')
    return [line_mae, line_mse, outlier_scatter, mae_w_line, mse_w_line, mae_curr_pt, mse_curr_pt, status_box]

def update(frame):
    idx = min(frame, n_frames - 1)
    
    y_out = outlier_y_vals[idx]
    w_m, b_m = mae_w_hist[idx], mae_b_hist[idx]
    w_s, b_s = mse_w_hist[idx], mse_b_hist[idx]
    
    # Оновлення ліній
    line_mae.set_data(x_plot, w_m * x_plot + b_m)
    line_mse.set_data(x_plot, w_s * x_plot + b_s)
    outlier_scatter.set_offsets([[outlier_x, y_out]])
    
    # Оновлення графіків параметрів
    mae_w_line.set_data(outlier_y_vals[:idx+1], mae_w_hist[:idx+1])
    mse_w_line.set_data(outlier_y_vals[:idx+1], mse_w_hist[:idx+1])
    mae_curr_pt.set_data([y_out], [w_m])
    mse_curr_pt.set_data([y_out], [w_s])
    
    status_box.set_text(
        f"Аномалія Y: {y_out:.1f}\n"
        f"MAE w:     {w_m:.3f} (майже без змін)\n"
        f"MSE w:     {w_s:.3f} (перекіс на +{(w_s - true_w):.2f})"
    )
    
    return [line_mae, line_mse, outlier_scatter, mae_w_line, mse_w_line, mae_curr_pt, mse_curr_pt, status_box]

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=130)

output_mp4 = 'public/videos/ai-python/linear-regression-theory/quality-metrics/outlier_impact_mse_vs_mae.mp4'
output_webm = 'public/videos/ai-python/linear-regression-theory/quality-metrics/outlier_impact_mse_vs_mae.webm'
output_gif = 'public/videos/ai-python/linear-regression-theory/quality-metrics/outlier_impact_mse_vs_mae.gif'
poster_png = 'public/videos/ai-python/linear-regression-theory/quality-metrics/outlier_poster.png'

print("Збереження MP4...")
ani.save(output_mp4, writer='ffmpeg', fps=10, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:03', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео успішно створено!")
