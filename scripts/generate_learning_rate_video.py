import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess

# 1. Функція втрат L(w) = w^2 (проста ідеальна парабола для наочності)
w_vals = np.linspace(-4.5, 4.5, 300)
loss_vals = w_vals ** 2

# Початкова точка
w_start = -3.8
n_steps = 22

# Три швидкості навчання
lrs = {
    'small': {'lr': 0.05, 'color': '#38bdf8', 'label': 'α = 0.05 (Занадто малий: повільно)'},
    'optimal': {'lr': 0.35, 'color': '#10b981', 'label': 'α = 0.35 (Оптимальний: швидка збіжність)'},
    'large': {'lr': 1.04, 'color': '#f43f5e', 'label': 'α = 1.04 (Занадто великий: дивергенція)'}
}

# Симуляція траєкторій
trajectories = {}
for key, conf in lrs.items():
    lr = conf['lr']
    w_hist = [w_start]
    loss_hist = [w_start ** 2]
    w = w_start
    for _ in range(n_steps):
        grad = 2 * w
        w = w - lr * grad
        w_hist.append(w)
        loss_hist.append(w ** 2)
    trajectories[key] = {
        'w': np.array(w_hist),
        'loss': np.array(loss_hist)
    }

# Додаємо кадри паузи в кінці
pause_frames = 15
total_frames = n_steps + 1 + pause_frames

# 2. Налаштування візуалізації
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

fig.suptitle("Порівняння динаміки Learning Rate (α) на функції втрат L(w) = w²", 
             fontsize=19, fontweight='bold', color='#f3f4f6', y=0.95)

# Лівий графік (Парабола і стрибки точок)
ax1.plot(w_vals, loss_vals, color='#475569', linewidth=2.5, linestyle='-', zorder=1)
ax1.axvline(0, color='#64748b', linestyle=':', alpha=0.5)
ax1.scatter([0], [0], color='#fbbf24', marker='*', s=250, zorder=3, label='Глобальний мінімум (w* = 0)')

lines = {}
points = {}
for key, conf in lrs.items():
    line, = ax1.plot([], [], color=conf['color'], linewidth=2.2, linestyle='-', marker='.', markersize=6, alpha=0.85, zorder=4)
    point, = ax1.plot([], [], color=conf['color'], marker='o', markeredgecolor='#ffffff', markeredgewidth=2, markersize=12, zorder=5, label=conf['label'])
    lines[key] = line
    points[key] = point

ax1.set_xlim(-4.8, 4.8)
ax1.set_ylim(-1, 20)
ax1.set_xlabel('Параметр (w)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Функція втрат L(w)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_title('Траєкторія кроків на чаші втрат', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='upper center', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

# Правий графік (Графік кривої втрат Loss vs Step)
loss_plots = {}
for key, conf in lrs.items():
    l_plot, = ax2.plot([], [], color=conf['color'], linewidth=2.5, label=conf['label'])
    loss_plots[key] = l_plot

ax2.set_xlim(0, n_steps)
ax2.set_ylim(-1, 20)
ax2.set_xlabel('Номер кроку (ітерація)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Значення втрат (Loss)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_title('Криві збіжності: спадання vs вибух помилки', fontsize=14, fontweight='bold', color='#fbbf24', pad=10)
ax2.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

status_box = ax1.text(0.04, 0.05, '', transform=ax1.transAxes, 
                      fontsize=12, family='monospace', color='#f9fafb',
                      bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))

def init():
    for key in lrs:
        lines[key].set_data([], [])
        points[key].set_data([], [])
        loss_plots[key].set_data([], [])
    status_box.set_text('')
    return list(lines.values()) + list(points.values()) + list(loss_plots.values()) + [status_box]

def update(frame):
    step = min(frame, n_steps)
    
    for key in lrs:
        w_hist = trajectories[key]['w'][:step+1]
        l_hist = trajectories[key]['loss'][:step+1]
        
        lines[key].set_data(w_hist, l_hist)
        points[key].set_data([w_hist[-1]], [l_hist[-1]])
        loss_plots[key].set_data(range(step+1), l_hist)
        
    w_opt = trajectories['optimal']['w'][step]
    l_opt = trajectories['optimal']['loss'][step]
    w_div = trajectories['large']['w'][step]
    l_div = trajectories['large']['loss'][step]
    
    status_box.set_text(
        f"Крок: {step:2d}/{n_steps}\n"
        f"Оптимальний α: w={w_opt:+.3f}, Loss={l_opt:.3f}\n"
        f"Вибуховий α:   w={w_div:+.3f}, Loss={l_div:.3f}"
    )
    
    return list(lines.values()) + list(points.values()) + list(loss_plots.values()) + [status_box]

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True, interval=160)

output_mp4 = 'public/videos/ai-python/linear-regression-theory/gradient-descent/learning_rate_dynamics.mp4'
output_webm = 'public/videos/ai-python/linear-regression-theory/gradient-descent/learning_rate_dynamics.webm'
output_gif = 'public/videos/ai-python/linear-regression-theory/gradient-descent/learning_rate_dynamics.gif'
poster_png = 'public/videos/ai-python/linear-regression-theory/gradient-descent/learning_rate_poster.png'

print("Збереження MP4...")
ani.save(output_mp4, writer='ffmpeg', fps=8, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=8,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:02', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Усі файли успішно створено!")
