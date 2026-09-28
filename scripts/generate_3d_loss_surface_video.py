import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import subprocess

# 1. Створення 3D поверхні MSE: L(w, b) = (w - 2)^2 + (b - 1)^2 + 0.5 * (w - 2)*(b - 1)
w_vals = np.linspace(-1.0, 5.0, 60)
b_vals = np.linspace(-2.0, 4.0, 60)
W, B = np.meshgrid(w_vals, b_vals)
Z = (W - 2.0)**2 + 1.2 * (B - 1.0)**2 + 0.4 * (W - 2.0) * (B - 1.0)

# 2. Траєкторія градієнтного спуску
w_curr, b_curr = -0.5, 3.5
lr = 0.14
n_steps = 45

w_traj = [w_curr]
b_traj = [b_curr]
z_traj = [(w_curr - 2.0)**2 + 1.2 * (b_curr - 1.0)**2 + 0.4 * (w_curr - 2.0) * (b_curr - 1.0)]

for _ in range(n_steps):
    gw = 2 * (w_curr - 2.0) + 0.4 * (b_curr - 1.0)
    gb = 2.4 * (b_curr - 1.0) + 0.4 * (w_curr - 2.0)
    w_curr -= lr * gw
    b_curr -= lr * gb
    w_traj.append(w_curr)
    b_traj.append(b_curr)
    z_traj.append((w_curr - 2.0)**2 + 1.2 * (b_curr - 1.0)**2 + 0.4 * (w_curr - 2.0) * (b_curr - 1.0))

w_traj = np.array(w_traj)
b_traj = np.array(b_traj)
z_traj = np.array(z_traj)

total_frames = 90  # 360 градусів обертання (4 градуси на кадр)

# 3. Налаштування візуалізації
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1], wspace=0.15, left=0.05, right=0.95, top=0.88, bottom=0.08)

ax1 = fig.add_subplot(gs[0], projection='3d')
ax2 = fig.add_subplot(gs[1])

ax1.set_facecolor('#0b0f19')
# Стилізація осей 3D
ax1.xaxis.pane.set_edgecolor('#1f2937')
ax1.yaxis.pane.set_edgecolor('#1f2937')
ax1.zaxis.pane.set_edgecolor('#1f2937')
ax1.xaxis.pane.fill = False
ax1.yaxis.pane.fill = False
ax1.zaxis.pane.fill = False
ax1.grid(color='#374151', linestyle='--', alpha=0.5)

ax1.tick_params(colors='#9ca3af', labelsize=10)
ax1.set_xlabel('Вага (w)', fontsize=12, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Зсув (b)', fontsize=12, color='#e5e7eb', labelpad=8)
ax1.set_zlabel('MSE (L)', fontsize=12, color='#e5e7eb', labelpad=8)
ax1.set_title('3D параболоїд функції втрат та спуск на дно чаші', fontsize=14, fontweight='bold', color='#38bdf8', pad=12)

# Рендеринг поверхні
surf = ax1.plot_surface(W, B, Z, cmap='viridis', alpha=0.78, edgecolor='#334155', linewidth=0.25, zorder=1)

# Траєкторія 3D
line_3d, = ax1.plot([], [], [], color='#f43f5e', linewidth=3, zorder=5)
point_3d, = ax1.plot([], [], [], marker='o', color='#fbbf24', markeredgecolor='#ffffff', markeredgewidth=2, markersize=10, zorder=6)
min_point = ax1.plot([2.0], [1.0], [0.0], marker='*', color='#10b981', markersize=14, zorder=4)

# 2D проєкція ліній рівня на ax2
ax2.set_facecolor('#111827')
for spine in ax2.spines.values():
    spine.set_color('#374151')
ax2.tick_params(colors='#9ca3af', labelsize=11)
ax2.grid(True, color='#1f2937', linestyle='--', alpha=0.6)

levels = np.logspace(-0.5, 1.4, 22)
ax2.contourf(W, B, Z, levels=levels, cmap='viridis', alpha=0.85)
ax2.contour(W, B, Z, levels=levels[::2], colors='#4b5563', linewidths=0.6, alpha=0.5)
ax2.plot(2.0, 1.0, marker='*', color='#10b981', markersize=16, label='Оптимум (w*=2, b*=1)')

line_2d, = ax2.plot([], [], color='#f43f5e', linewidth=2.5, label='Траєкторія спуску')
point_2d, = ax2.plot([], [], marker='o', color='#fbbf24', markeredgecolor='#ffffff', markersize=9)

ax2.set_xlim(-1.0, 5.0)
ax2.set_ylim(-2.0, 4.0)
ax2.set_xlabel('Параметр (w)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Параметр (b)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_title('2D мапа ліній рівня (вид зверху)', fontsize=14, fontweight='bold', color='#fbbf24', pad=10)
ax2.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

fig.suptitle("Тривимірна геометрія функції втрат MSE: спуск та обертання", 
             fontsize=19, fontweight='bold', color='#f3f4f6', y=0.96)

status_box = ax2.text(0.05, 0.05, '', transform=ax2.transAxes,
                      fontsize=11.5, family='monospace', color='#f9fafb',
                      bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))

def init():
    line_3d.set_data([], [])
    line_3d.set_3d_properties([])
    point_3d.set_data([], [])
    point_3d.set_3d_properties([])
    line_2d.set_data([], [])
    point_2d.set_data([], [])
    status_box.set_text('')
    return line_2d, point_2d, status_box

def update(frame):
    # Обертання камери
    azim = -60 + frame * 3.0
    elev = 28 + 6 * np.sin(frame * np.pi / 45)
    ax1.view_init(elev=elev, azim=azim)
    
    # Крок спуску
    step = min(frame, n_steps)
    
    # Оновлення 3D траєкторії
    line_3d.set_data(w_traj[:step+1], b_traj[:step+1])
    line_3d.set_3d_properties(z_traj[:step+1])
    point_3d.set_data([w_traj[step]], [b_traj[step]])
    point_3d.set_3d_properties([z_traj[step]])
    
    # Оновлення 2D траєкторії
    line_2d.set_data(w_traj[:step+1], b_traj[:step+1])
    point_2d.set_data([w_traj[step]], [b_traj[step]])
    
    status_box.set_text(
        f"Крок: {step:2d}/{n_steps}\n"
        f"w = {w_traj[step]:+.3f}\n"
        f"b = {b_traj[step]:+.3f}\n"
        f"MSE = {z_traj[step]:.4f}"
    )
    
    return line_2d, point_2d, status_box

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=100)

output_mp4 = 'public/videos/ai-python/linear-regression-theory/gradient-descent/3d_loss_surface_descent.mp4'
output_webm = 'public/videos/ai-python/linear-regression-theory/gradient-descent/3d_loss_surface_descent.webm'
output_gif = 'public/videos/ai-python/linear-regression-theory/gradient-descent/3d_loss_surface_descent.gif'
poster_png = 'public/videos/ai-python/linear-regression-theory/gradient-descent/3d_loss_surface_poster.png'

print("Збереження MP4...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:03', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("3D поверхня успішно згенерована!")
