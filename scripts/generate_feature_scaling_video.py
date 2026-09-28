import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess
import os

# Set random seed
np.random.seed(42)

# Unscaled loss: L(w1, w2) = 15 * w1^2 + 0.3 * w2^2 (condition number = 50)
# Scaled loss: L(w1, w2) = 1.0 * w1^2 + 1.0 * w2^2 (condition number = 1)

n_steps = 45

# Gradient descent for unscaled (oscillating)
lr_unscaled = 0.062
w_unscaled = np.zeros((n_steps, 2))
w_unscaled[0] = [-3.8, 4.0]

for i in range(1, n_steps):
    grad_w1 = 30.0 * w_unscaled[i-1, 0]
    grad_w2 = 0.6 * w_unscaled[i-1, 1]
    w_unscaled[i, 0] = w_unscaled[i-1, 0] - lr_unscaled * grad_w1
    w_unscaled[i, 1] = w_unscaled[i-1, 1] - lr_unscaled * grad_w2

# Gradient descent for scaled (direct)
lr_scaled = 0.35
w_scaled = np.zeros((n_steps, 2))
w_scaled[0] = [-3.8, 4.0]

for i in range(1, n_steps):
    grad_w1 = 2.0 * w_scaled[i-1, 0]
    grad_w2 = 2.0 * w_scaled[i-1, 1]
    w_scaled[i, 0] = w_scaled[i-1, 0] - lr_scaled * grad_w1
    w_scaled[i, 1] = w_scaled[i-1, 1] - lr_scaled * grad_w2

# Setup grid for contours
grid_w1 = np.linspace(-4.5, 4.5, 120)
grid_w2 = np.linspace(-4.5, 4.5, 120)
W1, W2 = np.meshgrid(grid_w1, grid_w2)

Loss_unscaled = 15.0 * W1**2 + 0.3 * W2**2
Loss_scaled = 1.0 * W1**2 + 1.0 * W2**2

# Pause at end
pause_frames = 15
total_frames = n_steps + pause_frames

fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, wspace=0.22, left=0.07, right=0.95, top=0.86, bottom=0.1)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

for ax in [ax1, ax2]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
    ax.tick_params(colors='#9ca3af', labelsize=11)

fig.suptitle("Масштабування ознак (Feature Scaling): Ліквідація зигзагів у багатовимірній оптимізації", 
             fontsize=17, fontweight='bold', color='#f3f4f6', y=0.95)

# Left: Unscaled contour plot
levels_unscaled = np.array([2, 8, 20, 45, 80, 140, 220])
cs1 = ax1.contour(W1, W2, Loss_unscaled, levels=levels_unscaled, colors='#475569', linewidths=1.2, alpha=0.7)
ax1.clabel(cs1, inline=True, fontsize=8, colors='#64748b')
ax1.plot(0, 0, marker='*', markersize=14, color='#fbbf24', markeredgecolor='#ffffff', label='Мінімум втрат (w*)')

traj_unscaled, = ax1.plot([], [], color='#f43f5e', linewidth=2.4, marker='o', markersize=5, label='Траєкторія градієнтного спуску')
cur_pt_unscaled, = ax1.plot([], [], marker='o', markersize=10, color='#f43f5e', markeredgecolor='#ffffff', markeredgewidth=2)

ax1.set_xlim(-4.5, 4.5)
ax1.set_ylim(-4.5, 4.5)
ax1.set_xlabel('Вага w1 (Площа: 30..150 м²)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Вага w2 (Кімнати: 1..5)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax1.set_title('1. БЕЗ масштабування: Вузький еліпс ("глибока щілина")', fontsize=13.5, fontweight='bold', color='#f43f5e', pad=10)
ax1.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

card_unscaled = ax1.text(0.04, 0.05, '', transform=ax1.transAxes,
                         fontsize=11.5, family='monospace', fontweight='bold', color='#f3f4f6',
                         bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#f43f5e', alpha=0.92))

# Right: Scaled contour plot
levels_scaled = np.array([0.5, 2, 4.5, 8, 12.5, 18, 24.5])
cs2 = ax2.contour(W1, W2, Loss_scaled, levels=levels_scaled, colors='#475569', linewidths=1.2, alpha=0.7)
ax2.clabel(cs2, inline=True, fontsize=8, colors='#64748b')
ax2.plot(0, 0, marker='*', markersize=14, color='#fbbf24', markeredgecolor='#ffffff', label='Мінімум втрат (w*)')

traj_scaled, = ax2.plot([], [], color='#10b981', linewidth=2.4, marker='o', markersize=5, label='Траєкторія градієнтного спуску')
cur_pt_scaled, = ax2.plot([], [], marker='o', markersize=10, color='#10b981', markeredgecolor='#ffffff', markeredgewidth=2)

ax2.set_xlim(-4.5, 4.5)
ax2.set_ylim(-4.5, 4.5)
ax2.set_xlabel('Вага w1 (StandardScaler, z-score)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Вага w2 (StandardScaler, z-score)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax2.set_title('2. З StandardScaler: Ідеальні симетричні концентричні кола', fontsize=13.5, fontweight='bold', color='#10b981', pad=10)
ax2.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

card_scaled = ax2.text(0.04, 0.05, '', transform=ax2.transAxes,
                       fontsize=11.5, family='monospace', fontweight='bold', color='#f3f4f6',
                       bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#10b981', alpha=0.92))

def init():
    traj_unscaled.set_data([], [])
    cur_pt_unscaled.set_data([], [])
    card_unscaled.set_text('')
    traj_scaled.set_data([], [])
    cur_pt_scaled.set_data([], [])
    card_scaled.set_text('')
    return [traj_unscaled, cur_pt_unscaled, card_unscaled, traj_scaled, cur_pt_scaled, card_scaled]

def update(frame):
    idx = min(frame, n_steps - 1)
    
    # Unscaled update
    traj_unscaled.set_data(w_unscaled[:idx+1, 0], w_unscaled[:idx+1, 1])
    cur_pt_unscaled.set_data([w_unscaled[idx, 0]], [w_unscaled[idx, 1]])
    
    loss_u = 15.0 * w_unscaled[idx, 0]**2 + 0.3 * w_unscaled[idx, 1]**2
    card_unscaled.set_text(
        f"Крок:       {idx + 1} / {n_steps}\n"
        f"Поточний L: {loss_u:.2f}\n"
        f"Динаміка:   Хаотичні ЗИГЗАГИ\n"
        f"Сходимість: ДУЖЕ ПОВІЛЬНА"
    )
    
    # Scaled update
    traj_scaled.set_data(w_scaled[:idx+1, 0], w_scaled[:idx+1, 1])
    cur_pt_scaled.set_data([w_scaled[idx, 0]], [w_scaled[idx, 1]])
    
    loss_s = 1.0 * w_scaled[idx, 0]**2 + 1.0 * w_scaled[idx, 1]**2
    card_scaled.set_text(
        f"Крок:       {min(idx + 1, 12)} / 12 (зійшовся!)\n"
        f"Поточний L: {loss_s:.4f}\n"
        f"Динаміка:   ПРЯМИЙ РУХ У ЦЕНТР\n"
        f"Сходимість: МИТТЄВА (ідеальна)"
    )
    
    return [traj_unscaled, cur_pt_unscaled, card_unscaled, traj_scaled, cur_pt_scaled, card_scaled]

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=130)

out_dir = 'public/videos/ai-python/linear-regression-theory/multiple-regression'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'feature_scaling_optimization.mp4')
output_webm = os.path.join(out_dir, 'feature_scaling_optimization.webm')
output_gif = os.path.join(out_dir, 'feature_scaling_optimization.gif')
poster_png = os.path.join(out_dir, 'feature_scaling_poster.png')

print("Збереження MP4 (feature_scaling_optimization)...")
ani.save(output_mp4, writer='ffmpeg', fps=10, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:04', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео 3.1 успішно згенеровано!")
