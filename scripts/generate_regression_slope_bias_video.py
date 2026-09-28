import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess
import os

# Set random seed for reproducibility
np.random.seed(42)

# Generate apartment dataset: Area (m^2) vs Price (thousands $)
n_points = 28
x = np.linspace(25, 100, n_points)
true_w = 0.55   # 550 $/m^2 -> 0.55 thousand $/m^2
true_b = 6.0    # 6 thousand $ base bias
noise = np.random.normal(0, 3.2, n_points)
y = true_w * x + true_b + noise

# Setup frames:
# Phase 1: w sweeps from -0.2 to 1.1 with fixed b = 6.0 (35 frames)
# Phase 2: b sweeps from -2.0 to 14.0 with fixed w = 0.55 (35 frames)
# Phase 3: settle on optimal fit with residuals popping up (25 frames)
frames_p1 = 35
frames_p2 = 35
frames_p3 = 25
total_frames = frames_p1 + frames_p2 + frames_p3

w_p1 = np.linspace(-0.2, 1.1, frames_p1)
b_p1 = np.full(frames_p1, true_b)

w_p2 = np.full(frames_p2, true_w)
b_p2 = np.linspace(-2.0, 14.0, frames_p2)

# Phase 3 stays optimal
w_p3 = np.full(frames_p3, true_w)
b_p3 = np.full(frames_p3, true_b)

w_all = np.concatenate([w_p1, w_p2, w_p3])
b_all = np.concatenate([b_p1, b_p2, b_p3])

# Create figure
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 1.0], wspace=0.25, left=0.07, right=0.95, top=0.86, bottom=0.1)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

for ax in [ax1, ax2]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
    ax.tick_params(colors='#9ca3af', labelsize=11)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.6)

fig.suptitle("Геометрія прямої лінійної регресії: Роль нахилу (w) та зсуву (b)", 
             fontsize=18, fontweight='bold', color='#f3f4f6', y=0.95)

# Left Subplot: Data points and Regression Line
ax1.scatter(x, y, color='#38bdf8', s=70, alpha=0.9, edgecolors='#0284c7', linewidth=1.5, zorder=4, label='Квартири (вибірка даних)')
x_line = np.linspace(15, 110, 100)
reg_line, = ax1.plot([], [], color='#f43f5e', linewidth=3.5, zorder=5, label='Регресійна пряма ŷ = w·x + b')
pivot_dot, = ax1.plot([], [], marker='o', markersize=10, color='#fbbf24', markeredgecolor='#ffffff', markeredgewidth=1.5, zorder=6)

# Residual segments (shown in phase 3)
residual_lines = [ax1.plot([], [], color='#a855f7', linestyle=':', linewidth=1.8, alpha=0.8, zorder=3)[0] for _ in range(n_points)]

ax1.set_xlim(15, 110)
ax1.set_ylim(-5, 75)
ax1.set_xlabel('Площа квартири x (м²)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Ціна y (тис. $)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_title('Простір спостережень: обертання та зсув прямої', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

# Status banner on ax1
phase_text = ax1.text(0.04, 0.65, '', transform=ax1.transAxes,
                      fontsize=11.5, fontweight='bold', family='sans-serif', color='#f3f4f6',
                      bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.92))

# Right Subplot: Dynamic Dashboard (Gauges, Equations, Loss)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')

# Dashboard panels using ax2 coordinates
# Title card
ax2.text(5, 9.2, "Панель керування параметрами", ha='center', va='center',
         fontsize=15, fontweight='bold', color='#fbbf24')

# Formula display box
formula_box = ax2.text(5, 7.6, '', ha='center', va='center', fontsize=15, family='monospace',
                       fontweight='bold', color='#38bdf8',
                       bbox=dict(boxstyle='round,pad=0.7', facecolor='#1e293b', edgecolor='#0284c7', linewidth=2))

# Parameter w card
ax2.add_patch(plt.Rectangle((0.5, 4.3), 9.0, 2.0, facecolor='#1f2937', edgecolor='#374151'))
w_title = ax2.text(1.0, 5.7, "Коефіцієнт нахилу (w / weight):", fontsize=12, fontweight='bold', color='#e5e7eb')
w_val_text = ax2.text(8.5, 5.7, '', ha='right', fontsize=13, fontweight='bold', family='monospace', color='#10b981')
w_interp_text = ax2.text(1.0, 4.8, '', fontsize=10.5, color='#9ca3af')

# Parameter b card
ax2.add_patch(plt.Rectangle((0.5, 1.8), 9.0, 2.0, facecolor='#1f2937', edgecolor='#374151'))
b_title = ax2.text(1.0, 3.2, "Вільний член (b / bias):", fontsize=12, fontweight='bold', color='#e5e7eb')
b_val_text = ax2.text(8.5, 3.2, '', ha='right', fontsize=13, fontweight='bold', family='monospace', color='#a855f7')
b_interp_text = ax2.text(1.0, 2.3, '', fontsize=10.5, color='#9ca3af')

# MSE Loss bar at bottom
ax2.text(1.0, 0.8, "Помилка моделі (MSE):", fontsize=11.5, fontweight='bold', color='#e5e7eb')
loss_val_text = ax2.text(8.5, 0.8, '', ha='right', fontsize=12, fontweight='bold', family='monospace', color='#f43f5e')

def init():
    reg_line.set_data([], [])
    pivot_dot.set_data([], [])
    for rl in residual_lines:
        rl.set_data([], [])
    phase_text.set_text('')
    formula_box.set_text('')
    w_val_text.set_text('')
    w_interp_text.set_text('')
    b_val_text.set_text('')
    b_interp_text.set_text('')
    loss_val_text.set_text('')
    return [reg_line, pivot_dot, phase_text, formula_box, w_val_text, w_interp_text, b_val_text, b_interp_text, loss_val_text] + residual_lines

def update(frame):
    w = w_all[frame]
    b = b_all[frame]
    
    # Compute line
    y_pred_line = w * x_line + b
    reg_line.set_data(x_line, y_pred_line)
    
    # Predictions for sample points & MSE
    y_pred_pts = w * x + b
    mse = np.mean((y - y_pred_pts) ** 2)
    
    formula_box.set_text(f"Ціна = {w:+.2f} × Площа {b:+.2f}")
    w_val_text.set_text(f"{w:+.2f} тис. $/м²")
    b_val_text.set_text(f"{b:+.2f} тис. $")
    loss_val_text.set_text(f"{mse:.1f} (тис. $)²")
    
    if frame < frames_p1:
        # Phase 1: slope rotation
        pivot_dot.set_data([0], [b])
        phase_text.set_text(
            "📍 Фаза 1: Обертання прямої вагами w\n"
            f"• b = {b:.1f} (зафіксовано як вісь обертання)\n"
            f"• w змінює кут: {w:+.2f}"
        )
        phase_text.get_bbox_patch().set_edgecolor('#38bdf8')
        w_interp_text.set_text(f"Кожен +1 м² змінює ціну на {w*1000:+.0f}$")
        b_interp_text.set_text("Базова ціна на осі Y залишається фіксованою")
        for rl in residual_lines:
            rl.set_data([], [])
            
    elif frame < frames_p1 + frames_p2:
        # Phase 2: bias shift
        pivot_dot.set_data([0], [b])
        phase_text.set_text(
            "📍 Фаза 2: Паралельний зсув прямої параметром b\n"
            f"• w = {w:.2f} (кут нахилу зафіксовано)\n"
            f"• b рухає пряму паралельно: {b:+.1f} тис. $"
        )
        phase_text.get_bbox_patch().set_edgecolor('#a855f7')
        w_interp_text.set_text("Кут нахилу зафіксовано оптимальним (0.55)")
        b_interp_text.set_text(f"Базова вартість: {b*1000:+.0f}$ при площі 0 м²")
        for rl in residual_lines:
            rl.set_data([], [])
            
    else:
        # Phase 3: optimal state + residuals
        pivot_dot.set_data([0], [b])
        progress = (frame - (frames_p1 + frames_p2)) / frames_p3
        phase_text.set_text(
            "✅ Оптимальне узгодження (Найкраща модель)\n"
            f"• w = {w:.2f} (550 $/м²)\n"
            f"• b = {b:.1f} (6 000 $ базовий зсув)\n"
            "• Фіолетові пунктири: мінімальні залишки (ei)"
        )
        phase_text.get_bbox_patch().set_edgecolor('#10b981')
        w_interp_text.set_text("Кожен 1 м² площі стабільно додає 550$")
        b_interp_text.set_text("Базова ціна відповідає мінімальній оцінці")
        
        # Display residual lines
        for i in range(n_points):
            residual_lines[i].set_data([x[i], x[i]], [y[i], y_pred_pts[i]])
            
    return [reg_line, pivot_dot, phase_text, formula_box, w_val_text, w_interp_text, b_val_text, b_interp_text, loss_val_text] + residual_lines

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=120)

out_dir = 'public/videos/ai-python/linear-regression-theory/regression-task'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'slope_bias_dynamics.mp4')
output_webm = os.path.join(out_dir, 'slope_bias_dynamics.webm')
output_gif = os.path.join(out_dir, 'slope_bias_dynamics.gif')
poster_png = os.path.join(out_dir, 'slope_bias_poster.png')

print("Збереження MP4 (slope_bias_dynamics)...")
ani.save(output_mp4, writer='ffmpeg', fps=10, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:08', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео 1.1 успішно згенеровано!")
