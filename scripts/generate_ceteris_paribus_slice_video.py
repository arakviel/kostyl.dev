import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess
import os

np.random.seed(42)

# Regression model: Price = w1 * Area + w2 * Distance + b
w1 = 0.52   # +520 $/m^2
w2 = -3.5   # -3 500 $/km
b = 20.0    # 20 000 $

# Grid for 3D plane
area_grid = np.linspace(30, 110, 40)
dist_grid = np.linspace(0.5, 6.0, 40)
A, D = np.meshgrid(area_grid, dist_grid)
Price_plane = w1 * A + w2 * D + b

# Generate some realistic 3D scatter points
n_pts = 35
pts_area = np.random.uniform(35, 105, n_pts)
pts_dist = np.random.uniform(1.0, 5.5, n_pts)
pts_price = w1 * pts_area + w2 * pts_dist + b + np.random.normal(0, 2.5, n_pts)

# Frames: sweeping distance from 1.0 km to 5.5 km and back
n_frames = 65
t = np.linspace(0, np.pi, n_frames)
sweep_dist = 1.0 + 4.2 * (np.sin(t)**2)

fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1.0], wspace=0.2, left=0.05, right=0.95, top=0.86, bottom=0.1)

ax1 = fig.add_subplot(gs[0], projection='3d')
ax2 = fig.add_subplot(gs[1])

# Setup ax1 3D
ax1.set_facecolor('#0b0f19')
ax1.tick_params(colors='#9ca3af', labelsize=9.5)
ax1.xaxis.pane.fill = False
ax1.yaxis.pane.fill = False
ax1.zaxis.pane.fill = False
ax1.xaxis.pane.set_edgecolor('#1f2937')
ax1.yaxis.pane.set_edgecolor('#1f2937')
ax1.zaxis.pane.set_edgecolor('#1f2937')
ax1.grid(True, color='#1f2937', linestyle=':')

# Setup ax2 2D
ax2.set_facecolor('#111827')
for spine in ax2.spines.values():
    spine.set_color('#374151')
ax2.tick_params(colors='#9ca3af', labelsize=11)
ax2.grid(True, color='#1f2937', linestyle='--', alpha=0.6)

fig.suptitle("Принцип Ceteris Paribus: Ізольований вплив ознаки при фіксації інших", 
             fontsize=17, fontweight='bold', color='#f3f4f6', y=0.95)

# Plot static 3D regression plane
surf = ax1.plot_surface(A, D, Price_plane, alpha=0.35, cmap='viridis', edgecolor='none')
ax1.scatter(pts_area, pts_dist, pts_price, color='#38bdf8', s=35, alpha=0.7, edgecolors='#0284c7')

ax1.set_xlim(30, 110)
ax1.set_ylim(0.5, 6.0)
ax1.set_zlim(10, 80)
ax1.set_xlabel('Площа x1 (м²)', fontsize=11, color='#e5e7eb', labelpad=8)
ax1.set_ylabel('Метро x2 (км)', fontsize=11, color='#e5e7eb', labelpad=8)
ax1.set_zlabel('Ціна y (тис. $)', fontsize=11, color='#e5e7eb', labelpad=8)
ax1.set_title('3D простір: площина моделі та січна площина', fontsize=13, fontweight='bold', color='#38bdf8', pad=10)
ax1.view_init(elev=22, azim=-62)

# Dynamic 3D intersection line & slice plane
slice_line_3d, = ax1.plot([], [], [], color='#fbbf24', linewidth=4.0, zorder=10)

# Right: 2D Projection (Area vs Price for the slice)
ax2.set_xlim(25, 115)
ax2.set_ylim(10, 80)
ax2.set_xlabel('Площа квартири x1 (м²)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax2.set_ylabel('Передбачена ціна ŷ (тис. $)', fontsize=12.5, color='#e5e7eb', labelpad=8)
ax2.set_title('2D проекція зрізу: нахил w1 є НЕЗМІННИМ', fontsize=13.5, fontweight='bold', color='#fbbf24', pad=10)

# Guide lines for other slices
ax2.plot(area_grid, w1 * area_grid + w2 * 1.0 + b, color='#475569', linestyle=':', linewidth=1.5, label='Зріз: 1.0 км (близько)')
ax2.plot(area_grid, w1 * area_grid + w2 * 3.0 + b, color='#475569', linestyle=':', linewidth=1.5, label='Зріз: 3.0 км (середньо)')
ax2.plot(area_grid, w1 * area_grid + w2 * 5.0 + b, color='#475569', linestyle=':', linewidth=1.5, label='Зріз: 5.0 км (далеко)')

slice_line_2d, = ax2.plot([], [], color='#fbbf24', linewidth=3.5, label='Поточний активний зріз')
ax2.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=9.5)

card_2d = ax2.text(0.04, 0.52, '', transform=ax2.transAxes,
                   fontsize=11.5, family='monospace', fontweight='bold', color='#f3f4f6',
                   bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#fbbf24', alpha=0.92))

def init():
    slice_line_3d.set_data([], [])
    slice_line_3d.set_3d_properties([])
    slice_line_2d.set_data([], [])
    card_2d.set_text('')
    return [slice_line_3d, slice_line_2d, card_2d]

def update(frame):
    d_val = sweep_dist[frame]
    
    # 3D slice line
    line_y_3d = w1 * area_grid + w2 * d_val + b
    slice_line_3d.set_data(area_grid, np.full_like(area_grid, d_val))
    slice_line_3d.set_3d_properties(line_y_3d)
    
    # 2D slice line
    slice_line_2d.set_data(area_grid, line_y_3d)
    
    eff_intercept = w2 * d_val + b
    card_2d.set_text(
        f"Фіксовано x2: {d_val:.2f} км (const)\n"
        f"Рівняння 2D:  ŷ = {w1:.2f}·x1 + ({eff_intercept:.1f})\n"
        f"Кут нахилу:   w1 = {w1*1000:.0f} $/м² (НЕ ЗМІНЮЄТЬСЯ!)\n"
        f"Висновок:     Зсувається лише рівень цін,\n"
        f"              а питома вага площі стабільна!"
    )
    
    return [slice_line_3d, slice_line_2d, card_2d]

ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=125)

out_dir = 'public/videos/ai-python/linear-regression-theory/multiple-regression'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'ceteris_paribus_slice.mp4')
output_webm = os.path.join(out_dir, 'ceteris_paribus_slice.webm')
output_gif = os.path.join(out_dir, 'ceteris_paribus_slice.gif')
poster_png = os.path.join(out_dir, 'ceteris_paribus_poster.png')

print("Збереження MP4 (ceteris_paribus_slice)...")
ani.save(output_mp4, writer='ffmpeg', fps=10, dpi=100,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постера...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:03', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео 3.2 успішно згенеровано!")
