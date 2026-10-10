import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess

# Set font and style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

# Evaluation grid
x = np.linspace(-6, 6, 500)

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

# 96 frames total:
# Frames 0..47: Varying w (b=0)
#   w goes: 0.2 -> 0.6 -> 1.2 -> 2.5 -> 5.0 -> -1.5 -> 1.5
# Frames 48..95: Varying b (w=1.5 fixed)
#   b goes: -4.0 -> -2.0 -> 0.0 -> +2.0 -> +4.0 -> 0.0

w_vals = []
b_vals = []

# Part 1: w animation
w_seq = np.concatenate([
    np.linspace(0.2, 5.0, 32),
    np.linspace(5.0, -1.8, 12),
    np.linspace(-1.8, 1.5, 8)
])
for w in w_seq:
    w_vals.append(w)
    b_vals.append(0.0)

# Part 2: b animation
b_seq = np.concatenate([
    np.linspace(0.0, -4.0, 16),
    np.linspace(-4.0, 4.0, 24),
    np.linspace(4.0, 0.0, 8)
])
for b in b_seq:
    w_vals.append(1.5)
    b_vals.append(b)

total_frames = len(w_vals)

fig = plt.figure(figsize=(15, 6.2), dpi=100)
fig.patch.set_facecolor('#F8FAFC')

# Subplots: Left is the sigmoid curve (width 60%), Right is engineering metrics & explanation (width 40%)
gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 0.9])
ax_curve = fig.add_subplot(gs[0])
ax_info = fig.add_subplot(gs[1])

ax_curve.set_facecolor('#FFFFFF')
ax_curve.set_xlim(-6, 6)
ax_curve.set_ylim(-0.05, 1.05)
ax_curve.axhline(0.0, color='#94A3B8', linestyle=':', linewidth=1.0)
ax_curve.axhline(1.0, color='#94A3B8', linestyle=':', linewidth=1.0)
ax_curve.axhline(0.5, color='#EF4444', linestyle='--', linewidth=1.5, alpha=0.8, label='Поріг невизначеності P = 0.5')
ax_curve.axvline(0.0, color='#94A3B8', linestyle=':', linewidth=1.0)
ax_curve.set_xlabel('Вхідний аргумент x', fontsize=11, fontweight='bold', color='#1E293B')
ax_curve.set_ylabel('Ймовірність σ(w·x + b)', fontsize=11, fontweight='bold', color='#1E293B')
ax_curve.set_title('Графік сигмоїдної функції та зона невизначеності', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
ax_curve.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

line_sig, = ax_curve.plot([], [], color='#2563EB', linewidth=3.0, label='σ(w·x + b)')
center_dot, = ax_curve.plot([], [], marker='o', markersize=10, color='#DC2626', zorder=5, label='Точка перегину (P=0.5)')
thresh_v_line = ax_curve.axvline(0, color='#DC2626', linestyle=':', linewidth=1.8, alpha=0.7)

# Shaded uncertainty band between P=0.1 and P=0.9
import matplotlib.patches as mpatches
uncertainty_band = mpatches.Rectangle((-2, -0.05), 4, 1.1, color='#3B82F6', alpha=0.15, label='Зона невизначеності [0.1, 0.9]')
ax_curve.add_patch(uncertainty_band)

ax_curve.legend(loc='upper left', fontsize=8.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

# Setup ax_info
ax_info.set_facecolor('#FFFFFF')
ax_info.axis('off')

fig.suptitle('ДИНАМІЧНА АНАТОМІЯ СИГМОЇДИ: КЕРУВАННЯ ВАГОЮ (w) ТА ЗСУВОМ (b)',
             fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)

def init():
    line_sig.set_data([], [])
    center_dot.set_data([], [])
    return [line_sig, center_dot]

def update(frame):
    curr_w = w_vals[frame]
    curr_b = b_vals[frame]
    is_part1 = (frame < len(w_seq))
    
    z = curr_w * x + curr_b
    sig_vals = sigmoid(z)
    line_sig.set_data(x, sig_vals)
    
    # Point where z = 0 => x0 = -b / w
    if abs(curr_w) > 1e-4:
        x0 = -curr_b / curr_w
    else:
        x0 = 0.0
    
    center_dot.set_data([x0], [0.5])
    thresh_v_line.set_xdata([x0, x0])
    
    # Uncertainty interval: z in [-ln(9), ln(9)] approx [-2.197, 2.197]
    if abs(curr_w) > 1e-3:
        x_low = (-2.197 - curr_b) / curr_w
        x_high = (2.197 - curr_b) / curr_w
        x_min_band = min(x_low, x_high)
        x_max_band = max(x_low, x_high)
        uncertainty_width = x_max_band - x_min_band
        uncertainty_band.set_x(x_min_band)
        uncertainty_band.set_width(uncertainty_width)
        uncertainty_band.set_visible(True)
    else:
        uncertainty_width = 999.0
        uncertainty_band.set_visible(False)
        
    ax_info.clear()
    ax_info.axis('off')
    
    # Phase text and badge
    if is_part1:
        phase_title = "ФАЗА 1: ЗМІНА ВАГИ (w) ПРИ b = 0"
        phase_badge_color = "#DBEAFE"
        phase_border_color = "#3B82F6"
        explanation = (
            f"• Параметр w відповідає за КРУТИЗНУ переходу:\n"
            f"  - Мале |w| (<0.5): полога крива, широка зона невпевненості.\n"
            f"  - Велике |w| (>3.0): різкий стрибок, модель діє як пороговий перемикач.\n"
            f"  - w < 0: дзеркальне відбиття (вищий x -> нижча ймовірність)."
        )
    else:
        phase_title = "ФАЗА 2: ГОРИЗОНТАЛЬНИЙ ЗСУВ (b) ПРИ w = 1.5"
        phase_badge_color = "#FEF3C7"
        phase_border_color = "#F59E0B"
        explanation = (
            f"• Параметр b зміщує точку перегину по осі X:\n"
            f"  - Формула порогу 50%: x_0 = -b / w = {-curr_b/curr_w:+.2f}\n"
            f"  - b > 0: зсуває криву ЛІВОРУЧ (клас 1 легше досягти)\n"
            f"  - b < 0: зсуває криву ПРАВОРУЧ (клас 1 важче досягти)\n"
            f"  - Форма та крутизна кривої при цьому не змінюються!"
        )
        
    info_box = (
        f"{phase_title}\n"
        f"---------------------------------------------------\n"
        f"ПОТОЧНІ ПАРАМЕТРИ:\n"
        f"  • Вага (w):      {curr_w:+.2f}\n"
        f"  • Зміщення (b):  {curr_b:+.2f}\n"
        f"  • Рівняння z:    z = ({curr_w:+.2f})·x + ({curr_b:+.2f})\n\n"
        f"ВЛАСТИВОСТІ МОДЕЛІ:\n"
        f"  • Поріг P=0.5:   x_0 = {x0:+.2f}\n"
        f"  • Ширина зони невизначеності [0.1, 0.9]: {uncertainty_width:.2f}\n"
        f"  • Крутизна в центрі (dσ/dx): {abs(curr_w)*0.25:.3f}\n\n"
        f"ІНЖЕНЕРНИЙ ВИСНОВОК:\n"
        f"{explanation}"
    )
    
    ax_info.text(0.05, 0.95, info_box, transform=ax_info.transAxes, fontsize=10.5,
                 verticalalignment='top', fontfamily='DejaVu Sans',
                 bbox=dict(boxstyle='round,pad=0.8', facecolor=phase_badge_color, edgecolor=phase_border_color, alpha=0.9))
    
    return [line_sig, center_dot, thresh_v_line]

ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, interval=80)

out_dir = 'public/videos/ai-python/logistic-regression-classification/classification-basics'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'logistic_regression_sigmoid_parameters.mp4')
output_webm = os.path.join(out_dir, 'logistic_regression_sigmoid_parameters.webm')
output_gif = os.path.join(out_dir, 'logistic_regression_sigmoid_parameters.gif')
poster_png = os.path.join(out_dir, 'logistic_regression_sigmoid_parameters_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно створено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:04', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео logistic_regression_sigmoid_parameters успішно завершено!")
