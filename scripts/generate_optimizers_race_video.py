import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess

np.random.seed(42)

# 1. Еліптична функція втрат (типова для невмасштабованих ознак MSE):
# L(w, b) = 1.2 * w^2 + 0.3 * b^2 + 0.2 * w * b
w_range = np.linspace(-4.0, 4.0, 200)
b_range = np.linspace(-4.0, 4.0, 200)
W, B = np.meshgrid(w_range, b_range)
Z = 1.2 * W**2 + 0.3 * B**2 + 0.2 * W * B

def true_grad(w, b):
    # Градієнт за всією вибіркою (Batch)
    gw = 2.4 * w + 0.2 * b
    gb = 0.6 * b + 0.2 * w
    return gw, gb

n_steps = 35
w_init, b_init = -3.2, 3.5

# Симуляція 3 оптимізаторів
# 1. Batch GD
w_b, b_b = w_init, b_init
hist_b_w = [w_b]
hist_b_b = [b_b]
hist_b_loss = [1.2 * w_b**2 + 0.3 * b_b**2 + 0.2 * w_b * b_b]
lr_b = 0.22
for _ in range(n_steps):
    gw, gb = true_grad(w_b, b_b)
    w_b -= lr_b * gw
    b_b -= lr_b * gb
    hist_b_w.append(w_b)
    hist_b_b.append(b_b)
    hist_b_loss.append(1.2 * w_b**2 + 0.3 * b_b**2 + 0.2 * w_b * b_b)

# 2. SGD (1 семпл -> великий шум)
w_s, b_s = w_init, b_init
hist_s_w = [w_s]
hist_s_b = [b_s]
hist_s_loss = [1.2 * w_s**2 + 0.3 * b_s**2 + 0.2 * w_s * b_s]
lr_s = 0.18
for i in range(n_steps):
    gw, gb = true_grad(w_s, b_s)
    # сильний стохастичний шум
    noise_w = np.random.normal(0, 1.6)
    noise_b = np.random.normal(0, 1.4)
    w_s -= lr_s * (gw + noise_w)
    b_s -= lr_s * (gb + noise_b)
    hist_s_w.append(w_s)
    hist_s_b.append(b_s)
    hist_s_loss.append(1.2 * w_s**2 + 0.3 * b_s**2 + 0.2 * w_s * b_s)

# 3. Mini-batch GD (помірний шум)
w_m, b_m = w_init, b_init
hist_m_w = [w_m]
hist_m_b = [b_m]
hist_m_loss = [1.2 * w_m**2 + 0.3 * b_m**2 + 0.2 * w_m * b_m]
lr_m = 0.22
for i in range(n_steps):
    gw, gb = true_grad(w_m, b_m)
    # помірний шум
    noise_w = np.random.normal(0, 0.45)
    noise_b = np.random.normal(0, 0.40)
    w_m -= lr_m * (gw + noise_w)
    b_m -= lr_m * (gb + noise_b)
    hist_m_w.append(w_m)
    hist_m_b.append(b_m)
    hist_m_loss.append(1.2 * w_m**2 + 0.3 * b_m**2 + 0.2 * w_m * b_m)

# Пауза в кінці
pause = 15
total_frames = n_steps + 1 + pause

# Візуалізація
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

fig.suptitle("Битва оптимізаторів: як Batch, SGD та Mini-batch шукають мінімум", 
             fontsize=19, fontweight='bold', color='#f3f4f6', y=0.95)

# Контури на ax1
levels = np.logspace(-1, 1.4, 20)
ax1.contourf(W, B, Z, levels=levels, cmap='inferno', alpha=0.75, zorder=1)
ax1.contour(W, B, Z, levels=levels[::2], colors='#4b5563', linewidths=0.6, alpha=0.5, zorder=2)
ax1.plot(0, 0, marker='*', color='#fbbf24', markersize=18, zorder=6, label='Глобальний мінімум (0, 0)')

# Траєкторії
line_b, = ax1.plot([], [], color='#10b981', linewidth=2.5, label='Batch GD (стабільний, гладкий)', zorder=4)
pt_b, = ax1.plot([], [], marker='o', color='#10b981', markeredgecolor='#ffffff', markersize=9, zorder=7)

line_m, = ax1.plot([], [], color='#38bdf8', linewidth=2.2, label='Mini-batch GD (збалансований)', zorder=4)
pt_m, = ax1.plot([], [], marker='o', color='#38bdf8', markeredgecolor='#ffffff', markersize=9, zorder=7)

line_s, = ax1.plot([], [], color='#f43f5e', linewidth=1.8, linestyle='--', label='SGD (стохастичний шум)', zorder=3)
pt_s, = ax1.plot([], [], marker='o', color='#f43f5e', markeredgecolor='#ffffff', markersize=9, zorder=7)

ax1.set_xlim(-3.8, 3.8)
ax1.set_ylim(-3.8, 3.8)
ax1.set_xlabel('Параметр (w)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Параметр (b)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_title('Траєкторії оптимізаторів на лініях рівня втрат', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='lower left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

# Графік Loss на ax2
loss_b_plot, = ax2.plot([], [], color='#10b981', linewidth=2.5, label='Batch GD')
loss_m_plot, = ax2.plot([], [], color='#38bdf8', linewidth=2.2, label='Mini-batch GD')
loss_s_plot, = ax2.plot([], [], color='#f43f5e', linewidth=1.8, linestyle='--', label='SGD')

ax2.set_xlim(0, n_steps)
ax2.set_ylim(-0.5, 18)
ax2.set_xlabel('Ітерація (крок оновлення)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Значення функції втрат (Loss)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_title('Зниження втрат: монотонне vs шумне', fontsize=14, fontweight='bold', color='#fbbf24', pad=10)
ax2.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

info_box = ax2.text(0.05, 0.45, '', transform=ax2.transAxes,
                    fontsize=11.5, family='monospace', color='#f9fafb',
                    bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#374151', alpha=0.9))

def init():
    line_b.set_data([], [])
    pt_b.set_data([], [])
    line_m.set_data([], [])
    pt_m.set_data([], [])
    line_s.set_data([], [])
    pt_s.set_data([], [])
    loss_b_plot.set_data([], [])
    loss_m_plot.set_data([], [])
    loss_s_plot.set_data([], [])
    info_box.set_text('')
    return [line_b, pt_b, line_m, pt_m, line_s, pt_s, loss_b_plot, loss_m_plot, loss_s_plot, info_box]

def update(frame):
    step = min(frame, n_steps)
    
    line_b.set_data(hist_b_w[:step+1], hist_b_b[:step+1])
    pt_b.set_data([hist_b_w[step]], [hist_b_b[step]])
    loss_b_plot.set_data(range(step+1), hist_b_loss[:step+1])
    
    line_m.set_data(hist_m_w[:step+1], hist_m_b[:step+1])
    pt_m.set_data([hist_m_w[step]], [hist_m_b[step]])
    loss_m_plot.set_data(range(step+1), hist_m_loss[:step+1])
    
    line_s.set_data(hist_s_w[:step+1], hist_s_b[:step+1])
    pt_s.set_data([hist_s_w[step]], [hist_s_b[step]])
    loss_s_plot.set_data(range(step+1), hist_s_loss[:step+1])
    
    info_box.set_text(
        f"Крок: {step:2d}/{n_steps}\n"
        f"Batch Loss:      {hist_b_loss[step]:.3f}\n"
        f"Mini-batch Loss: {hist_m_loss[step]:.3f}\n"
        f"SGD Loss:        {hist_s_loss[step]:.3f}"
    )
    
    return [line_b, pt_b, line_m, pt_m, line_s, pt_s, loss_b_plot, loss_m_plot, loss_s_plot, info_box]

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True, interval=140)

output_mp4 = 'public/videos/ai-python/linear-regression-theory/gradient-descent/optimizers_race.mp4'
output_webm = 'public/videos/ai-python/linear-regression-theory/gradient-descent/optimizers_race.webm'
output_gif = 'public/videos/ai-python/linear-regression-theory/gradient-descent/optimizers_race.gif'
poster_png = 'public/videos/ai-python/linear-regression-theory/gradient-descent/optimizers_race_poster.png'

print("Збереження MP4...")
ani.save(output_mp4, writer='ffmpeg', fps=10, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:02', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Усі файли успішно згенеровано!")
