import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import subprocess
import os

np.random.seed(42)

# Sample dataset
x = np.array([1.5, 2.8, 3.9, 5.2, 6.7, 8.1, 9.4])
true_w, true_b = 1.3, 2.5
noise = np.array([0.5, -0.8, 0.4, -0.3, 0.9, -0.6, 0.2])
y = true_w * x + true_b + noise

y_mean = np.mean(y)
ss_tot = np.sum((y - y_mean) ** 2)

# Optimal regression fit
w_opt, b_opt = np.polyfit(x, y, 1)

# Frame counts:
# Phase 1: Baseline mean (0-25)
# Phase 2: Rotating to optimal (26-60)
# Phase 3: Inverting to bad model (61-90)
f_p1 = 25
f_p2 = 35
f_p3 = 30
total_frames = f_p1 + f_p2 + f_p3

# Trajectories of w and b across frames
w_p1 = np.full(f_p1, 0.0)
b_p1 = np.full(f_p1, y_mean)

# Phase 2: from (0, y_mean) to (w_opt, b_opt)
w_p2 = np.linspace(0.0, w_opt, f_p2)
b_p2 = np.linspace(y_mean, b_opt, f_p2)

# Phase 3: from (w_opt, b_opt) to bad slope (-0.8, y_mean + 4.5)
w_p3 = np.linspace(w_opt, -0.9, f_p3)
b_p3 = np.linspace(b_opt, y_mean + 4.5, f_p3)

w_all = np.concatenate([w_p1, w_p2, w_p3])
b_all = np.concatenate([b_p1, b_p2, b_p3])

# Create figure
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

fig.suptitle("Сутність коефіцієнта детермінації R²: від бейслайну середнього до моделі", 
             fontsize=18, fontweight='bold', color='#f3f4f6', y=0.95)

# Left Subplot: Data points and active model line
ax1.scatter(x, y, color='#38bdf8', s=85, edgecolors='#0284c7', linewidth=2, zorder=6, label='Фактичні дані (y)')
mean_line = ax1.axhline(y_mean, color='#9ca3af', linestyle=':', linewidth=2, zorder=3, label=f'Бейслайн: середнє ȳ = {y_mean:.1f}')

x_plot = np.linspace(0, 11, 100)
model_line, = ax1.plot([], [], color='#10b981', linewidth=3.2, zorder=5, label='Поточна модель: ŷ = w·x + b')

res_lines = [ax1.plot([], [], color='#f43f5e', linewidth=2.0, linestyle='-', zorder=4)[0] for _ in range(len(x))]
sq_patches = [patches.Rectangle((0, 0), 0, 0, facecolor='#f43f5e', edgecolor='#fda4af', alpha=0.35, linewidth=1.2, zorder=2) for _ in range(len(x))]
for p in sq_patches:
    ax1.add_patch(p)

ax1.set_xlim(0, 11)
ax1.set_ylim(-2, 19)
ax1.set_xlabel('Вхідна ознака x', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Цільова змінна y', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax1.set_title('Простір даних: порівняння дисперсій SS_tot та SS_res', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

status_box = ax1.text(0.04, 0.65, '', transform=ax1.transAxes,
                      fontsize=11.5, family='sans-serif', fontweight='bold', color='#f3f4f6',
                      bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.92))

# Right Subplot: R^2 Dashboard and Dial
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')

ax2.text(5, 9.2, "Діагностика якості R² (Score)", ha='center', va='center',
         fontsize=15, fontweight='bold', color='#fbbf24')

# Formula banner
ax2.add_patch(plt.Rectangle((0.5, 6.7), 9.0, 1.9, facecolor='#1f2937', edgecolor='#38bdf8', linewidth=1.5))
ax2.text(5, 7.9, "R² = 1 - (SS_res / SS_tot)", ha='center', va='center',
         fontsize=15, family='monospace', fontweight='bold', color='#38bdf8')
formula_sub = ax2.text(5, 7.2, "Частка дисперсії, пояснена моделлю", ha='center', va='center',
                       fontsize=10.5, color='#9ca3af')

# Card 1: SS_tot (Baseline Variance)
ax2.add_patch(plt.Rectangle((0.5, 4.4), 9.0, 1.9, facecolor='#1f2937', edgecolor='#374151'))
ax2.text(1.0, 5.7, "SS_tot (Загальна дисперсія даних):", fontsize=11.5, fontweight='bold', color='#e5e7eb')
sstot_val = ax2.text(8.5, 5.7, f"{ss_tot:.1f}", ha='right', fontsize=12.5, family='monospace', fontweight='bold', color='#9ca3af')
ax2.text(1.0, 4.9, "Сума квадратів відхилень від наївного середнього ȳ", fontsize=10, color='#9ca3af')

# Card 2: SS_res (Model Residual Variance)
ax2.add_patch(plt.Rectangle((0.5, 2.3), 9.0, 1.9, facecolor='#1f2937', edgecolor='#374151'))
ax2.text(1.0, 3.6, "SS_res (Залишкова помилка моделі):", fontsize=11.5, fontweight='bold', color='#e5e7eb')
ssres_val = ax2.text(8.5, 3.6, '', ha='right', fontsize=12.5, family='monospace', fontweight='bold', color='#f43f5e')
ssres_sub = ax2.text(1.0, 2.8, '', fontsize=10, color='#9ca3af')

# Big Indicator Box at Bottom: R^2 Score
r2_box = ax2.add_patch(plt.Rectangle((0.5, 0.4), 9.0, 1.6, facecolor='#1e293b', edgecolor='#10b981', linewidth=2))
r2_score_text = ax2.text(5, 1.2, '', ha='center', va='center', fontsize=18, family='monospace', fontweight='bold', color='#10b981')

def init():
    model_line.set_data([], [])
    for rl in res_lines:
        rl.set_data([], [])
    for p in sq_patches:
        p.set_width(0)
        p.set_height(0)
    status_box.set_text('')
    ssres_val.set_text('')
    ssres_sub.set_text('')
    r2_score_text.set_text('')
    return [model_line, status_box, ssres_val, ssres_sub, r2_score_text] + res_lines + sq_patches

def update(frame):
    w = w_all[frame]
    b = b_all[frame]
    
    y_pred_pts = w * x + b
    res = y - y_pred_pts
    ss_res = np.sum(res ** 2)
    r2 = 1.0 - (ss_res / ss_tot)
    
    model_line.set_data(x_plot, w * x_plot + b)
    
    # Update residuals & squares
    for i in range(len(x)):
        res_lines[i].set_data([x[i], x[i]], [y_pred_pts[i], y[i]])
        side = abs(res[i])
        sq_patches[i].set_xy((x[i], min(y[i], y_pred_pts[i])))
        sq_patches[i].set_width(side * 0.45)
        sq_patches[i].set_height(side)
        
    ssres_val.set_text(f"{ss_res:.1f}")
    
    if frame < f_p1:
        # Phase 1: Baseline
        status_box.set_text(
            "📍 Фаза 1: Бейслайн середнього (R² = 0.00)\n"
            "• Модель прогнозує тупе середнє ȳ\n"
            f"• SS_res дорівнює SS_tot = {ss_tot:.1f}\n"
            "• Модель не пояснює жодної варіації"
        )
        status_box.get_bbox_patch().set_edgecolor('#9ca3af')
        model_line.set_color('#9ca3af')
        r2_box.set_edgecolor('#9ca3af')
        r2_score_text.set_color('#9ca3af')
        r2_score_text.set_text(f"R² = 0.00 (0% пояснено)")
        ssres_sub.set_text("Помилка дорівнює дисперсії всього датасету")
        
    elif frame < f_p1 + f_p2:
        # Phase 2: Optimal learning
        status_box.set_text(
            "📈 Фаза 2: Навчання моделі (R² зростає)\n"
            f"• Пряма адаптується під точки (w={w:.2f})\n"
            f"• SS_res стискається: {ss_res:.1f}\n"
            f"• R² = {max(0, r2):.2f} (пояснено {max(0, r2)*100:.0f}% дисперсії!)"
        )
        status_box.get_bbox_patch().set_edgecolor('#10b981')
        model_line.set_color('#10b981')
        r2_box.set_edgecolor('#10b981')
        r2_score_text.set_color('#10b981')
        r2_score_text.set_text(f"R² = {r2:.2f} ({r2*100:.0f}% пояснено)")
        ssres_sub.set_text("Залишкові помилки стрімко зменшуються")
        
    else:
        # Phase 3: Inverted bad model (R^2 < 0)
        status_box.set_text(
            "⚠️ Фаза 3: Жахлива модель (R² < 0)\n"
            f"• Нахил перевернуто в інший бік (w={w:.2f})\n"
            f"• SS_res ({ss_res:.1f}) перевищує SS_tot ({ss_tot:.1f})!\n"
            "• Модель гірша за тупе передбачення середнього!"
        )
        status_box.get_bbox_patch().set_edgecolor('#f43f5e')
        model_line.set_color('#f43f5e')
        r2_box.set_edgecolor('#f43f5e')
        r2_score_text.set_color('#f43f5e')
        r2_score_text.set_text(f"R² = {r2:.2f} (ГІРШЕ ЗА СЕРЕДНЄ!)")
        ssres_sub.set_text("Помилка моделі перевищує базову дисперсію даних")
        
    return [model_line, status_box, ssres_val, ssres_sub, r2_score_text] + res_lines + sq_patches

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=125)

out_dir = 'public/videos/ai-python/linear-regression-theory/quality-metrics'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'r_squared_dynamics.mp4')
output_webm = os.path.join(out_dir, 'r_squared_dynamics.webm')
output_gif = os.path.join(out_dir, 'r_squared_dynamics.gif')
poster_png = os.path.join(out_dir, 'r_squared_poster.png')

print("Збереження MP4 (r_squared_dynamics)...")
ani.save(output_mp4, writer='ffmpeg', fps=10, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:06', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео 2.2 успішно згенеровано!")
