import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess
import os

np.random.seed(42)

# Total frames
n_frames = 80

# 1. Left Data: Regression (Area -> Continuous Price)
x_reg = np.linspace(30, 110, 30)
y_reg = 0.52 * x_reg + 7.5 + np.random.normal(0, 2.5, 30)

# Regression line
x_line = np.linspace(25, 115, 100)
y_line = 0.52 * x_line + 7.5

# Test point movement in regression (from 35 to 105 m^2 back and forth)
t = np.linspace(0, 2 * np.pi, n_frames)
scan_x = 70 + 35 * np.sin(t)
scan_y = 0.52 * scan_x + 7.5

# 2. Right Data: Classification (Area vs Distance to Center -> Class 0 or 1)
n_class_pts = 20
c0_area = np.random.normal(50, 12, n_class_pts)
c0_dist = np.random.normal(12, 3, n_class_pts)

c1_area = np.random.normal(85, 14, n_class_pts)
c1_dist = np.random.normal(4, 2, n_class_pts)

# Decision boundary line in classification: x2 = -0.15 * x1 + 17
x_clf_line = np.linspace(30, 110, 100)
y_clf_boundary = -0.15 * x_clf_line + 18.5

# Test point moving across the boundary
clf_test_x1 = 70 + 35 * np.sin(t)
clf_test_x2 = 10 - 7 * np.sin(t)

# Create figure
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, wspace=0.22, left=0.07, right=0.95, top=0.86, bottom=0.1)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

for ax in [ax1, ax2]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
    ax.tick_params(colors='#9ca3af', labelsize=11)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.6)

fig.suptitle("Фундаментальна відмінність: Регресія проти Класифікації", 
             fontsize=18, fontweight='bold', color='#f3f4f6', y=0.95)

# Left: Regression Plot
ax1.scatter(x_reg, y_reg, color='#38bdf8', s=55, alpha=0.8, edgecolors='#0284c7', label='Спостереження (квартири)')
ax1.plot(x_line, y_line, color='#0284c7', linewidth=2.8, linestyle='--', label='Модель регресії: ŷ = f(x)')
reg_cursor, = ax1.plot([], [], marker='o', markersize=14, color='#f43f5e', markeredgecolor='#ffffff', markeredgewidth=2.5, zorder=6)
reg_proj_x, = ax1.plot([], [], color='#f43f5e', linestyle=':', linewidth=1.8)
reg_proj_y, = ax1.plot([], [], color='#f43f5e', linestyle=':', linewidth=1.8)

ax1.set_xlim(25, 115)
ax1.set_ylim(15, 75)
ax1.set_xlabel('Площа квартири (м²)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Ціна квартири (тис. $)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax1.set_title('1. Регресія: Прогноз неперервної величини (ŷ ∈ ℝ)', fontsize=14, fontweight='bold', color='#38bdf8', pad=10)
ax1.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

reg_card = ax1.text(0.04, 0.65, '', transform=ax1.transAxes,
                    fontsize=12, family='monospace', fontweight='bold', color='#f3f4f6',
                    bbox=dict(boxstyle='round,pad=0.7', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.95))

# Right: Classification Plot
ax2.scatter(c0_area, c0_dist, color='#f43f5e', s=60, alpha=0.85, edgecolors='#be123c', label='Клас 0: Відхилити кредит')
ax2.scatter(c1_area, c1_dist, color='#10b981', s=60, alpha=0.85, edgecolors='#047857', label='Клас 1: Схвалити кредит')

# Shaded background regions for decision boundary
ax2.fill_between(x_clf_line, y_clf_boundary, 22, color='#f43f5e', alpha=0.12, label='Регіон класу 0')
ax2.fill_between(x_clf_line, 0, y_clf_boundary, color='#10b981', alpha=0.12, label='Регіон класу 1')
ax2.plot(x_clf_line, y_clf_boundary, color='#fbbf24', linewidth=3.0, linestyle='-', label='Розділова межа (Decision Boundary)')

clf_cursor, = ax2.plot([], [], marker='D', markersize=14, color='#fbbf24', markeredgecolor='#ffffff', markeredgewidth=2.5, zorder=6)

ax2.set_xlim(25, 115)
ax2.set_ylim(0, 20)
ax2.set_xlabel('Площа позичальника (м²)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Відстань до центру (км)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax2.set_title('2. Класифікація: Поділ простору на класи (ŷ ∈ {0, 1})', fontsize=14, fontweight='bold', color='#fbbf24', pad=10)
ax2.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=9.5)

clf_card = ax2.text(0.04, 0.12, '', transform=ax2.transAxes,
                    fontsize=12, family='monospace', fontweight='bold', color='#f3f4f6',
                    bbox=dict(boxstyle='round,pad=0.7', facecolor='#1e293b', edgecolor='#fbbf24', alpha=0.95))

def init():
    reg_cursor.set_data([], [])
    reg_proj_x.set_data([], [])
    reg_proj_y.set_data([], [])
    reg_card.set_text('')
    clf_cursor.set_data([], [])
    clf_card.set_text('')
    return [reg_cursor, reg_proj_x, reg_proj_y, reg_card, clf_cursor, clf_card]

def update(frame):
    # Regression Update
    cur_x = scan_x[frame]
    cur_y = scan_y[frame]
    reg_cursor.set_data([cur_x], [cur_y])
    reg_proj_x.set_data([cur_x, cur_x], [15, cur_y])
    reg_proj_y.set_data([25, cur_x], [cur_y, cur_y])
    
    price_dollars = cur_y * 1000
    reg_card.set_text(
        f"Вхід (x):  {cur_x:.1f} м²\n"
        f"Прогноз:   {cur_y:.2f} тис. $\n"
        f"Ціна чек:  {price_dollars:,.0f} $\n"
        f"Тип:       НЕПЕРЕРВНЕ ЧИСЛО"
    )
    
    # Classification Update
    cx1 = clf_test_x1[frame]
    cx2 = clf_test_x2[frame]
    clf_cursor.set_data([cx1], [cx2])
    
    # Decision boundary value: dist_boundary = -0.15 * cx1 + 18.5
    bound_val = -0.15 * cx1 + 18.5
    is_class_1 = (cx2 <= bound_val)
    
    if is_class_1:
        clf_card.set_text(
            f"Ознака x1: {cx1:.1f} м²\n"
            f"Ознака x2: {cx2:.1f} км\n"
            f"Статус:    СХВАЛЕНО (Клас 1)\n"
            f"Рішення:   ДИСКРЕТНЕ ПЕРЕМИКАННЯ"
        )
        clf_card.get_bbox_patch().set_edgecolor('#10b981')
        clf_cursor.set_color('#10b981')
    else:
        clf_card.set_text(
            f"Ознака x1: {cx1:.1f} м²\n"
            f"Ознака x2: {cx2:.1f} км\n"
            f"Статус:    ВІДХИЛЕНО (Клас 0)\n"
            f"Рішення:   ДИСКРЕТНЕ ПЕРЕМИКАННЯ"
        )
        clf_card.get_bbox_patch().set_edgecolor('#f43f5e')
        clf_cursor.set_color('#f43f5e')
        
    return [reg_cursor, reg_proj_x, reg_proj_y, reg_card, clf_cursor, clf_card]

ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=125)

out_dir = 'public/videos/ai-python/linear-regression-theory/regression-task'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'regression_vs_classification.mp4')
output_webm = os.path.join(out_dir, 'regression_vs_classification.webm')
output_gif = os.path.join(out_dir, 'regression_vs_classification.gif')
poster_png = os.path.join(out_dir, 'regression_vs_classification_poster.png')

print("Збереження MP4 (regression_vs_classification)...")
ani.save(output_mp4, writer='ffmpeg', fps=10, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:04', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео 1.2 успішно згенеровано!")
