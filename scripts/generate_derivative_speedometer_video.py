import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Wedge
import subprocess

# 1. Траєкторія x від -2.5 до +2.5
n_frames = 60
x_vals = np.linspace(-2.5, 2.5, n_frames)

x_curve = np.linspace(-3.0, 3.0, 200)
y_parabola = x_curve ** 2
y_abs = np.abs(x_curve)

# Пауза в кінці
pause = 15
total_frames = n_frames + pause

# 2. Створення фігури
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

fig.suptitle("Геометрія похідної: плавна дотична (MSE) проти гострого кута (MAE)", 
             fontsize=18, fontweight='bold', color='#f3f4f6', y=0.95)

# Панель 1: Диференційовна функція MSE (y = x^2)
ax1.plot(x_curve, y_parabola, color='#38bdf8', linewidth=3, label='Гладка функція MSE: y = x²')
ax1.axhline(0, color='#4b5563', linestyle=':', alpha=0.5)
ax1.axvline(0, color='#4b5563', linestyle=':', alpha=0.5)

tangent_mse, = ax1.plot([], [], color='#f43f5e', linewidth=2.5, label='Дотична лінія (похідна)')
point_mse, = ax1.plot([], [], marker='o', color='#fbbf24', markeredgecolor='#ffffff', markeredgewidth=2, markersize=11)

ax1.set_xlim(-3.2, 3.2)
ax1.set_ylim(-1.5, 8.5)
ax1.set_xlabel('Аргумент (x)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Значення функції f(x)', fontsize=13, color='#e5e7eb', labelpad=8)
ax1.set_title('Диференційовна: у кожній точці є єдина дотична', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='upper center', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

# Індикатор швидкості (Спідометр похідної)
hud_mse = ax1.text(0.04, 0.55, '', transform=ax1.transAxes,
                    fontsize=12, family='monospace', color='#f9fafb',
                    bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))

# Панель 2: Недиференційована функція MAE (y = |x|)
ax2.plot(x_curve, y_abs, color='#10b981', linewidth=3, label='Функція з кутом MAE: y = |x|')
ax2.axhline(0, color='#4b5563', linestyle=':', alpha=0.5)
ax2.axvline(0, color='#4b5563', linestyle=':', alpha=0.5)

tangent_mae, = ax2.plot([], [], color='#f43f5e', linewidth=2.5, label='Нахил стінки')
point_mae, = ax2.plot([], [], marker='o', color='#fbbf24', markeredgecolor='#ffffff', markeredgewidth=2, markersize=11)

# Кілька ліній у нулі при зламі
conflicting_lines = [ax2.plot([], [], color='#ef4444', linestyle='--', linewidth=1.5, alpha=0.8)[0] for _ in range(4)]

ax2.set_xlim(-3.2, 3.2)
ax2.set_ylim(-1.5, 8.5)
ax2.set_xlabel('Аргумент (x)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Значення функції f(x)', fontsize=13, color='#e5e7eb', labelpad=8)
ax2.set_title('Недиференційовна в нулі: гострий злам (кутова точка)', fontsize=14, fontweight='bold', color='#10b981', pad=10)
ax2.legend(loc='upper center', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5)

hud_mae = ax2.text(0.04, 0.55, '', transform=ax2.transAxes,
                    fontsize=12, family='monospace', color='#f9fafb',
                    bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#10b981', alpha=0.9))

def init():
    tangent_mse.set_data([], [])
    point_mse.set_data([], [])
    tangent_mae.set_data([], [])
    point_mae.set_data([], [])
    for line in conflicting_lines:
        line.set_data([], [])
    hud_mse.set_text('')
    hud_mae.set_text('')
    return [tangent_mse, point_mse, tangent_mae, point_mae, hud_mse, hud_mae] + conflicting_lines

def update(frame):
    idx = min(frame, n_frames - 1)
    x = x_vals[idx]
    
    # 1. Оновлення MSE
    y_mse = x ** 2
    slope_mse = 2 * x
    dx = 1.2
    x_tangent = np.array([x - dx, x + dx])
    y_tangent = y_mse + slope_mse * (x_tangent - x)
    
    tangent_mse.set_data(x_tangent, y_tangent)
    point_mse.set_data([x], [y_mse])
    
    state_str = "«плюс» (зростає)" if slope_mse > 0.05 else ("«мінус» (спадає)" if slope_mse < -0.05 else "НУЛЬ (мінімум!)")
    hud_mse.set_text(
        f"Точка:   x = {x:+.2f}, y = {y_mse:.2f}\n"
        f"Похідна: dy/dx = {slope_mse:+.2f}\n"
        f"Спідометр: {abs(slope_mse):.2f} од/с\n"
        f"Статус:  {state_str}"
    )
    
    # 2. Оновлення MAE
    y_mae = abs(x)
    point_mae.set_data([x], [y_mae])
    
    # Перевірка наближення до нуля
    if abs(x) < 0.15:
        tangent_mae.set_data([], [])
        # Показуємо 4 суперечливі дотичні
        angles = [-0.8, -0.3, 0.4, 0.9]
        for i, ang in enumerate(angles):
            xs = np.array([-1.5, 1.5])
            ys = y_mae + ang * xs
            conflicting_lines[i].set_data(xs, ys)
        hud_mae.set_text(
            f"Точка:   x = {x:+.2f}, y = {y_mae:.2f}\n"
            f"Похідна: НЕ ІСНУЄ (NaN)!\n"
            f"Злам:    гострий кут\n"
            f"Статус:  дотична невизначена"
        )
    else:
        for line in conflicting_lines:
            line.set_data([], [])
        slope_mae = 1.0 if x > 0 else -1.0
        x_tangent_mae = np.array([x - dx, x + dx])
        y_tangent_mae = y_mae + slope_mae * (x_tangent_mae - x)
        tangent_mae.set_data(x_tangent_mae, y_tangent_mae)
        hud_mae.set_text(
            f"Точка:   x = {x:+.2f}, y = {y_mae:.2f}\n"
            f"Похідна: dy/dx = {slope_mae:+.1f}\n"
            f"Швидкість стала (|нахил| = 1)\n"
            f"Статус:  {'спадає' if slope_mae < 0 else 'зростає'}"
        )
        
    return [tangent_mse, point_mse, tangent_mae, point_mae, hud_mse, hud_mae] + conflicting_lines

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=120)

output_mp4 = 'public/videos/ai-python/linear-regression-theory/gradient-descent/derivative_speedometer_tangent.mp4'
output_webm = 'public/videos/ai-python/linear-regression-theory/gradient-descent/derivative_speedometer_tangent.webm'
output_gif = 'public/videos/ai-python/linear-regression-theory/gradient-descent/derivative_speedometer_tangent.gif'
poster_png = 'public/videos/ai-python/linear-regression-theory/gradient-descent/derivative_speedometer_poster.png'

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

print("Відео похідної успішно створено!")
