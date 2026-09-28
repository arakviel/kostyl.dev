import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import subprocess

np.random.seed(42)

# 1. Генерація 3D даних: y = w1*x1 + w2*x2 + b
n_points = 35
x1 = np.random.uniform(20, 100, n_points)     # Площа (м2)
x2 = np.random.uniform(1, 4, n_points)       # Кількість кімнат
true_w1, true_w2, true_b = 0.8, 15.0, 30.0   # Справжні параметри
noise = np.random.normal(0, 6.0, n_points)
y = true_w1 * x1 + true_w2 * x2 + true_b + noise

# Нормалізація для стабільного градієнтного спуску
x1_norm = (x1 - np.mean(x1)) / np.std(x1)
x2_norm = (x2 - np.mean(x2)) / np.std(x2)
y_norm = (y - np.mean(y)) / np.std(y)

# Сітка для площини
grid_x1 = np.linspace(20, 100, 20)
grid_x2 = np.linspace(1, 4, 20)
X1_mesh, X2_mesh = np.meshgrid(grid_x1, grid_x2)

X1_mesh_norm = (X1_mesh - np.mean(x1)) / np.std(x1)
X2_mesh_norm = (X2_mesh - np.mean(x2)) / np.std(x2)

# 2. Градієнтний спуск
lr = 0.12
n_epochs = 40
w1_curr, w2_curr, b_curr = -0.5, 0.0, 0.0

w1_hist, w2_hist, b_hist, loss_hist = [], [], [], []

for _ in range(n_epochs):
    w1_hist.append(w1_curr)
    w2_hist.append(w2_curr)
    b_hist.append(b_curr)
    
    y_pred = w1_curr * x1_norm + w2_curr * x2_norm + b_curr
    err = y_norm - y_pred
    loss = np.mean(err**2)
    loss_hist.append(loss)
    
    gw1 = -2 * np.mean(x1_norm * err)
    gw2 = -2 * np.mean(x2_norm * err)
    gb = -2 * np.mean(err)
    
    w1_curr -= lr * gw1
    w2_curr -= lr * gw2
    b_curr -= lr * gb

# Перерахунок у фізичні одиниці для візуалізації
w1_real = np.array(w1_hist) * (np.std(y) / np.std(x1))
w2_real = np.array(w2_hist) * (np.std(y) / np.std(x2))
b_real = np.mean(y) + np.array(b_hist)*np.std(y) - w1_real*np.mean(x1) - w2_real*np.mean(x2)

pause = 15
total_frames = n_epochs + pause

# 3. Налаштування візуалізації
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 1], wspace=0.15, left=0.05, right=0.95, top=0.88, bottom=0.08)

ax1 = fig.add_subplot(gs[0], projection='3d')
ax2 = fig.add_subplot(gs[1])

# Стилізація ax1 (3D)
ax1.set_facecolor('#0b0f19')
ax1.xaxis.pane.set_edgecolor('#1f2937')
ax1.yaxis.pane.set_edgecolor('#1f2937')
ax1.zaxis.pane.set_edgecolor('#1f2937')
ax1.xaxis.pane.fill = False
ax1.yaxis.pane.fill = False
ax1.zaxis.pane.fill = False
ax1.grid(color='#374151', linestyle='--', alpha=0.5)

ax1.tick_params(colors='#9ca3af', labelsize=10)
ax1.set_xlabel('Площа x1 (м²)', fontsize=12, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Кімнати x2', fontsize=12, color='#e5e7eb', labelpad=8)
ax1.set_zlabel('Ціна y (тис. $)', fontsize=12, color='#e5e7eb', labelpad=8)
ax1.set_title('3D простір: підгонка регресійної площини до хмари точок', fontsize=14, fontweight='bold', color='#38bdf8', pad=12)

# Точки даних
ax1.scatter(x1, x2, y, color='#38bdf8', s=55, alpha=0.9, edgecolors='#0284c7', linewidth=1.5, zorder=5)

# Стилізація ax2 (Loss)
ax2.set_facecolor('#111827')
for spine in ax2.spines.values():
    spine.set_color('#374151')
ax2.tick_params(colors='#9ca3af', labelsize=11)
ax2.grid(True, color='#1f2937', linestyle='--', alpha=0.6)

loss_line, = ax2.plot([], [], color='#f43f5e', linewidth=3, label='MSE втрати (Loss)')
curr_loss_pt, = ax2.plot([], [], marker='o', color='#f43f5e', markeredgecolor='#ffffff', markersize=9)

ax2.set_xlim(0, n_epochs)
ax2.set_ylim(0, max(loss_hist) * 1.1)
ax2.set_xlabel('Епоха навчання', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Похибка MSE (нормована)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_title('Спадання похибки моделі', fontsize=14, fontweight='bold', color='#fbbf24', pad=10)
ax2.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

fig.suptitle("Підгонка регресійної площини y = w₁x₁ + w₂x₂ + b у тривимірному просторі", 
             fontsize=18, fontweight='bold', color='#f3f4f6', y=0.96)

status_box = ax2.text(0.06, 0.45, '', transform=ax2.transAxes,
                      fontsize=11.5, family='monospace', color='#f9fafb',
                      bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))

current_surf = [None]

def init():
    loss_line.set_data([], [])
    curr_loss_pt.set_data([], [])
    status_box.set_text('')
    return [loss_line, curr_loss_pt, status_box]

def update(frame):
    step = min(frame, n_epochs - 1)
    
    # Плавне обертання камери навколо сцени
    azim = -50 + frame * 2.2
    elev = 22 + 5 * np.sin(frame * np.pi / 35)
    ax1.view_init(elev=elev, azim=azim)
    
    # Видалення попередньої поверхні площини
    if current_surf[0] is not None:
        current_surf[0].remove()
        
    # Розрахунок площини
    w1_val = w1_real[step]
    w2_val = w2_real[step]
    b_val = b_real[step]
    
    Z_mesh = w1_val * X1_mesh + w2_val * X2_mesh + b_val
    current_surf[0] = ax1.plot_surface(X1_mesh, X2_mesh, Z_mesh, cmap='coolwarm', alpha=0.55,
                                      edgecolor='#64748b', linewidth=0.2, zorder=2)
    
    # Оновлення графіка втрат
    loss_line.set_data(range(step+1), loss_hist[:step+1])
    curr_loss_pt.set_data([step], [loss_hist[step]])
    
    status_box.set_text(
        f"Епоха: {step+1:2d}/{n_epochs}\n"
        f"ŷ = {w1_val:.2f}·x₁ + {w2_val:.2f}·x₂ + {b_val:.1f}\n"
        f"MSE: {loss_hist[step]:.4f}\n"
        f"Ціль: ŷ = {true_w1:.1f}·x₁ + {true_w2:.1f}·x₂ + {true_b:.1f}"
    )
    
    return [loss_line, curr_loss_pt, status_box]

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=120)

output_mp4 = 'public/videos/ai-python/linear-regression-theory/multiple-regression/3d_plane_fitting.mp4'
output_webm = 'public/videos/ai-python/linear-regression-theory/multiple-regression/3d_plane_fitting.webm'
output_gif = 'public/videos/ai-python/linear-regression-theory/multiple-regression/3d_plane_fitting.gif'
poster_png = 'public/videos/ai-python/linear-regression-theory/multiple-regression/3d_plane_poster.png'

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

print("3D площина успішно згенерована!")
