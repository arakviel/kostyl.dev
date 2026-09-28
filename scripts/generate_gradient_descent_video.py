import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch

# 1. Генерація даних
np.random.seed(42)
n_samples = 30
x = np.linspace(-2, 4, n_samples)
true_w, true_b = 1.8, 2.5
noise = np.random.normal(0, 0.8, n_samples)
y = true_w * x + true_b + noise

# 2. Налаштування сітки втрат MSE для контурного графіка
w_grid = np.linspace(-1.0, 4.0, 150)
b_grid = np.linspace(-1.0, 6.0, 150)
W, B = np.meshgrid(w_grid, b_grid)

# Loss L(w, b) = 1/n sum((y - (w*x + b))^2)
# Розрахунок матриці втрат
Z = np.zeros_like(W)
for i in range(len(x)):
    Z += (y[i] - (W * x[i] + B)) ** 2
Z /= len(x)

# 3. Симуляція градієнтного спуску
lr = 0.08
epochs = 45

w_history = []
b_history = []
loss_history = []

w_curr = -0.5
b_curr = 0.0

for epoch in range(epochs):
    w_history.append(w_curr)
    b_history.append(b_curr)
    
    y_pred = w_curr * x + b_curr
    err = y - y_pred
    loss = np.mean(err ** 2)
    loss_history.append(loss)
    
    dw = -2 * np.mean(x * err)
    db = -2 * np.mean(err)
    
    w_curr -= lr * dw
    b_curr -= lr * db

# Додаємо кілька статичних кадрів у кінці для фіксації результату
total_frames = epochs + 20
w_history += [w_history[-1]] * 20
b_history += [b_history[-1]] * 20
loss_history += [loss_history[-1]] * 20

# 4. Налаштування візуалізації (Стиль: Dark Slate Modern)
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1], wspace=0.25, left=0.07, right=0.95, top=0.86, bottom=0.1)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

for ax in [ax1, ax2]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
    ax.tick_params(colors='#9ca3af', labelsize=11)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.6)

# Заголовок фігури
title_text = fig.suptitle("Анімація градієнтного спуску в лінійній регресії", 
                          fontsize=19, fontweight='bold', color='#f3f4f6', y=0.95)

# Лівій графік (Простір даних)
ax1.scatter(x, y, color='#38bdf8', s=60, alpha=0.9, edgecolors='#0284c7', linewidth=1.5, zorder=4, label='Дані спостережень (x, y)')
line_reg, = ax1.plot([], [], color='#f43f5e', linewidth=3.5, zorder=5, label='Поточна модель y = w·x + b')
ax1.plot(x, true_w * x + true_b, color='#10b981', linestyle=':', linewidth=2, alpha=0.7, zorder=3, label='Ідеальна пряма y*')
ax1.set_xlim(-2.5, 4.5)
ax1.set_ylim(-3, 13)
ax1.set_xlabel('Ознака (x)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Цільова змінна (y)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_title('Простір даних: припасування лінії', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

# Правий графік (Контури функції втрат)
levels = np.logspace(np.log10(Z.min() + 0.01), np.log10(Z.max()), 24)
cp = ax2.contourf(W, B, Z, levels=levels, cmap='magma', alpha=0.85, zorder=1)
ax2.contour(W, B, Z, levels=levels[::2], colors='#4b5563', linewidths=0.6, alpha=0.6, zorder=2)

# Точка глобального мінімуму
opt_w, opt_b = w_history[-1], b_history[-1]
ax2.plot(opt_w, opt_b, marker='*', color='#fbbf24', markersize=14, zorder=6, label=f'Оптимум (w*={opt_w:.2f}, b*={opt_b:.2f})')

path_line, = ax2.plot([], [], color='#38bdf8', linewidth=2.2, linestyle='-', zorder=5)
current_point, = ax2.plot([], [], marker='o', color='#f43f5e', markeredgecolor='#ffffff', markeredgewidth=2, markersize=11, zorder=7, label='Поточна точка (w, b)')

ax2.set_xlim(-1.0, 4.0)
ax2.set_ylim(-1.0, 6.0)
ax2.set_xlabel('Вага (w)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Зсув (b)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_title('Простір втрат: спуск до мінімуму MSE', fontsize=14, fontweight='bold', color='#fbbf24', pad=10)
ax2.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

# Інформаційна плашка знизу
stats_box = ax1.text(0.03, 0.05, '', transform=ax1.transAxes, 
                     fontsize=12, family='monospace', color='#f9fafb',
                     bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#0284c7', alpha=0.9))

def init():
    line_reg.set_data([], [])
    path_line.set_data([], [])
    current_point.set_data([], [])
    stats_box.set_text('')
    return line_reg, path_line, current_point, stats_box

def update(frame):
    curr_epoch = min(frame, epochs - 1)
    w_val = w_history[curr_epoch]
    b_val = b_history[curr_epoch]
    l_val = loss_history[curr_epoch]
    
    # Оновлення прямої
    y_line = w_val * x + b_val
    line_reg.set_data(x, y_line)
    
    # Оновлення шляху оптимізатора
    path_line.set_data(w_history[:curr_epoch+1], b_history[:curr_epoch+1])
    current_point.set_data([w_val], [b_val])
    
    # Текст статусу
    stats_box.set_text(
        f"Епоха: {curr_epoch + 1:2d}/{epochs}\n"
        f"w = {w_val:+.3f} | b = {b_val:+.3f}\n"
        f"Помилка MSE = {l_val:.4f}"
    )
    
    return line_reg, path_line, current_point, stats_box

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True, interval=120)

output_mp4 = 'public/videos/ai-python/linear-regression-theory/gradient-descent/gradient_descent_visualization.mp4'
output_webm = 'public/videos/ai-python/linear-regression-theory/gradient-descent/gradient_descent_visualization.webm'

print("Рендеринг MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=100, 
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 збережено:", output_mp4)

# Також згенеруємо webm для максимальної сумісності
import subprocess
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)
print("WebM збережено:", output_webm)
