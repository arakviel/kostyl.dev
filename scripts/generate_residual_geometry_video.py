import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import subprocess
import os

np.random.seed(42)

# Small clean dataset to clearly display squares
x = np.array([1.0, 2.0, 3.2, 4.5, 6.0, 7.5, 9.0])
w_line, b_line = 1.2, 2.0
# Add controlled noise, with point 4 having larger deviation (outlier-like)
y = np.array([3.4, 4.2, 6.4, 6.0, 9.8, 10.2, 13.8])

# Predictions and residuals
y_pred = w_line * x + b_line
residuals = y - y_pred
abs_res = np.abs(residuals)
sq_res = residuals ** 2

mae = np.mean(abs_res)
mse = np.mean(sq_res)
rmse = np.sqrt(mse)

# Phases:
# 1. Residual lines intro (0-25)
# 2. Squares expanding (26-55)
# 3. Square root & RMSE conversion (56-85)
frames_p1 = 25
frames_p2 = 30
frames_p3 = 30
total_frames = frames_p1 + frames_p2 + frames_p3

fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0], wspace=0.25, left=0.07, right=0.95, top=0.86, bottom=0.1)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

for ax in [ax1, ax2]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
    ax.tick_params(colors='#9ca3af', labelsize=11)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.6)

fig.suptitle("Геометрія метрик регресії: MAE (довжина) vs MSE (площа) vs RMSE (сторона)", 
             fontsize=18, fontweight='bold', color='#f3f4f6', y=0.95)

# Left Subplot: Data, Line, Residuals and Squares
ax1.scatter(x, y, color='#38bdf8', s=80, edgecolors='#0284c7', linewidth=2, zorder=5, label='Фактичні спостереження (y)')
x_line = np.linspace(0, 10.5, 100)
ax1.plot(x_line, w_line * x_line + b_line, color='#10b981', linewidth=3, zorder=4, label='Модель регресії: ŷ = w·x + b')

res_lines = [ax1.plot([], [], color='#fbbf24', linewidth=2.8, linestyle='-', zorder=6)[0] for _ in range(len(x))]
sq_patches = [patches.Rectangle((0, 0), 0, 0, facecolor='#f43f5e', edgecolor='#fda4af', alpha=0.4, linewidth=1.5, zorder=3) for _ in range(len(x))]
for p in sq_patches:
    ax1.add_patch(p)

ax1.set_xlim(0, 11)
ax1.set_ylim(0, 16)
ax1.set_xlabel('Ознака x', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Цільова змінна y', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax1.set_title('Простір помилок: перехід від 1D відрізка до 2D площі', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

status_box = ax1.text(0.04, 0.65, '', transform=ax1.transAxes,
                      fontsize=11.5, family='sans-serif', fontweight='bold', color='#f3f4f6',
                      bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.92))

# Right Subplot: Metrics Summary Dashboard
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')

ax2.text(5, 9.2, "Анатомія одиниць вимірювання", ha='center', va='center',
         fontsize=15, fontweight='bold', color='#fbbf24')

# Card 1: MAE
ax2.add_patch(plt.Rectangle((0.5, 6.2), 9.0, 2.3, facecolor='#1f2937', edgecolor='#fbbf24', linewidth=1.5))
ax2.text(1.0, 7.9, "1. MAE (Mean Absolute Error)", fontsize=13, fontweight='bold', color='#fbbf24')
ax2.text(1.0, 7.2, f"Формула:  (1/n) · Σ |y_i - ŷ_i|  =  {mae:.2f} $", fontsize=11.5, family='monospace', color='#f3f4f6')
ax2.text(1.0, 6.6, "Геометрія:  СЕРЕДНЯ ДОВЖИНА лінійних відрізків (1D, $)", fontsize=10.5, color='#9ca3af')

# Card 2: MSE
ax2.add_patch(plt.Rectangle((0.5, 3.4), 9.0, 2.3, facecolor='#1f2937', edgecolor='#f43f5e', linewidth=1.5))
ax2.text(1.0, 5.1, "2. MSE (Mean Squared Error)", fontsize=13, fontweight='bold', color='#f43f5e')
ax2.text(1.0, 4.4, f"Формула:  (1/n) · Σ (y_i - ŷ_i)²  =  {mse:.2f} $²", fontsize=11.5, family='monospace', color='#f3f4f6')
ax2.text(1.0, 3.8, "Геометрія:  СЕРЕДНЯ ПЛОЩА фізичних квадратів (2D, $²)", fontsize=10.5, color='#9ca3af')

# Card 3: RMSE
ax2.add_patch(plt.Rectangle((0.5, 0.6), 9.0, 2.3, facecolor='#1f2937', edgecolor='#38bdf8', linewidth=1.5))
ax2.text(1.0, 2.3, "3. RMSE (Root Mean Squared Error)", fontsize=13, fontweight='bold', color='#38bdf8')
ax2.text(1.0, 1.6, f"Формула:  √MSE  =  √{mse:.2f}  =  {rmse:.2f} $", fontsize=11.5, family='monospace', color='#f3f4f6')
ax2.text(1.0, 1.0, "Геометрія:  ДОВЖИНА СТОРОНИ усередненого квадрата ($)", fontsize=10.5, color='#9ca3af')

def init():
    for rl in res_lines:
        rl.set_data([], [])
    for p in sq_patches:
        p.set_width(0)
        p.set_height(0)
    status_box.set_text('')
    return res_lines + sq_patches + [status_box]

def update(frame):
    if frame < frames_p1:
        # Phase 1: draw vertical segments
        progress = frame / frames_p1
        for i in range(len(x)):
            y_curr = y_pred[i] + (y[i] - y_pred[i]) * progress
            res_lines[i].set_data([x[i], x[i]], [y_pred[i], y_curr])
            sq_patches[i].set_width(0)
            sq_patches[i].set_height(0)
        status_box.set_text(
            "📏 Фаза 1: Залишки як лінійні відрізки\n"
            "• Відстань між фактом та лінією моделі\n"
            f"• Середня довжина: MAE = {mae:.2f} $"
        )
        status_box.get_bbox_patch().set_edgecolor('#fbbf24')
        
    elif frame < frames_p1 + frames_p2:
        # Phase 2: expand squares
        progress = (frame - frames_p1) / frames_p2
        for i in range(len(x)):
            res_lines[i].set_data([x[i], x[i]], [y_pred[i], y[i]])
            side = abs_res[i] * progress
            y_base = min(y[i], y_pred[i])
            sq_patches[i].set_xy((x[i], y_base))
            sq_patches[i].set_width(side * 0.45) # scaled width for coordinate system
            sq_patches[i].set_height(side)
            
        status_box.set_text(
            "📐 Фаза 2: Квадрати помилок (MSE)\n"
            "• Кожен відрізок розгортається у площу (ei)²\n"
            "• Великі помилки гіперболізуються!\n"
            f"• Сумарна середня площа: MSE = {mse:.2f} $²"
        )
        status_box.get_bbox_patch().set_edgecolor('#f43f5e')
        
    else:
        # Phase 3: square root to RMSE
        for i in range(len(x)):
            res_lines[i].set_data([x[i], x[i]], [y_pred[i], y[i]])
            sq_patches[i].set_xy((x[i], min(y[i], y_pred[i])))
            sq_patches[i].set_width(abs_res[i] * 0.45)
            sq_patches[i].set_height(abs_res[i])
            
        status_box.set_text(
            "🎯 Фаза 3: Корінь повертає одиниці (RMSE)\n"
            f"• Беремо корінь із площі MSE: √{mse:.2f}\n"
            f"• Отримуємо сторону квадрата: RMSE = {rmse:.2f} $\n"
            "• Метрика знову у зрозумілих доларах!"
        )
        status_box.get_bbox_patch().set_edgecolor('#38bdf8')
        
    return res_lines + sq_patches + [status_box]

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=125)

out_dir = 'public/videos/ai-python/linear-regression-theory/quality-metrics'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'residuals_mae_mse_rmse_geometry.mp4')
output_webm = os.path.join(out_dir, 'residuals_mae_mse_rmse_geometry.webm')
output_gif = os.path.join(out_dir, 'residuals_mae_mse_rmse_geometry.gif')
poster_png = os.path.join(out_dir, 'residuals_geometry_poster.png')

print("Збереження MP4 (residuals_mae_mse_rmse_geometry)...")
ani.save(output_mp4, writer='ffmpeg', fps=10, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:06', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео 2.1 успішно згенеровано!")
