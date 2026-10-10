import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import subprocess
import os

# Set seed for reproducible points
np.random.seed(42)

# Generate 1D dataset: Class 0 (Сині) and Class 1 (Червоні)
# Feature X in range [0, 10]
n_pts = 35
# Class 0 centered around 3.2, Class 1 centered around 6.8 with slight overlap
c0_x = np.clip(np.random.normal(loc=3.2, scale=1.1, size=n_pts), 0.5, 9.5)
c1_x = np.clip(np.random.normal(loc=6.8, scale=1.1, size=n_pts), 0.5, 9.5)

# Calculate total entropy of parent
n_total = 2 * n_pts
p0_parent = 0.5
p1_parent = 0.5
H_parent = - (p0_parent * np.log2(p0_parent) + p1_parent * np.log2(p1_parent))

def calc_entropy(labels):
    if len(labels) == 0:
        return 0.0
    p0 = np.mean(labels == 0)
    p1 = 1.0 - p0
    h = 0.0
    if p0 > 0:
        h -= p0 * np.log2(p0)
    if p1 > 0:
        h -= p1 * np.log2(p1)
    return h

def calc_gini(labels):
    if len(labels) == 0:
        return 0.0
    p0 = np.mean(labels == 0)
    p1 = 1.0 - p0
    return 1.0 - (p0**2 + p1**2)

# Precalculate Information Gain along threshold range
s_values = np.linspace(1.2, 8.8, 120)
all_x = np.concatenate([c0_x, c1_x])
all_y = np.concatenate([np.zeros(n_pts, dtype=int), np.ones(n_pts, dtype=int)])

ig_values = []
gini_gain_values = []
for s in s_values:
    left_mask = all_x <= s
    right_mask = ~left_mask
    
    n_L = np.sum(left_mask)
    n_R = np.sum(right_mask)
    
    if n_L == 0 or n_R == 0:
        ig_values.append(0.0)
        gini_gain_values.append(0.0)
        continue
        
    H_L = calc_entropy(all_y[left_mask])
    H_R = calc_entropy(all_y[right_mask])
    ig = H_parent - (n_L / n_total) * H_L - (n_R / n_total) * H_R
    ig_values.append(max(0.0, ig))

best_idx = np.argmax(ig_values)
best_threshold = s_values[best_idx]
best_ig = ig_values[best_idx]

# Setup plot
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 1.0], height_ratios=[1.0, 1.0],
                      wspace=0.18, hspace=0.32, left=0.06, right=0.96, top=0.90, bottom=0.08)

ax_points = fig.add_subplot(gs[:, 0])
ax_curve = fig.add_subplot(gs[0, 1])
ax_bars = fig.add_subplot(gs[1, 1])

# Styling
for ax in [ax_points, ax_curve, ax_bars]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=11)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.5)

# ax_points styling
ax_points.set_xlim(0.5, 9.5)
ax_points.set_ylim(-0.8, 4.2)
ax_points.set_xlabel('Числова ознака X (наприклад, рівень цукру або дохід)', fontsize=13, color='#e5e7eb', labelpad=8)
ax_points.set_ylabel('Розподіл об\'єктів / Вісь розбиття', fontsize=13, color='#e5e7eb', labelpad=8)
ax_points.set_title('1D Ознака: Пошук оптимального порогу розбиття', fontsize=15, fontweight='bold', color='#38bdf8', pad=12)

# Scatter points with jitter for visibility
np.random.seed(7)
jitter0 = np.random.uniform(0.6, 1.8, n_pts)
jitter1 = np.random.uniform(2.2, 3.4, n_pts)

ax_points.scatter(c0_x, jitter0, color='#38bdf8', s=70, edgecolors='#0284c7', linewidths=1.2, alpha=0.85, label='Клас 0 (Сині, N=35)')
ax_points.scatter(c1_x, jitter1, color='#f43f5e', s=70, edgecolors='#be123c', linewidths=1.2, alpha=0.85, label='Клас 1 (Червоні, N=35)')
ax_points.legend(loc='upper left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=11, framealpha=0.95)

# Boundary line and zones on ax_points
split_line = ax_points.axvline(s_values[0], color='#fbbf24', linewidth=3.5, linestyle='-', zorder=5)
left_rect = patches.Rectangle((0.5, -1), s_values[0] - 0.5, 6, facecolor='#38bdf8', alpha=0.08, zorder=1)
right_rect = patches.Rectangle((s_values[0], -1), 9.5 - s_values[0], 6, facecolor='#f43f5e', alpha=0.08, zorder=1)
ax_points.add_patch(left_rect)
ax_points.add_patch(right_rect)

# Status card on ax_points
card_points = ax_points.text(
    0.04, 0.04, '', transform=ax_points.transAxes,
    fontsize=11.5, color='#e5e7eb', verticalalignment='bottom',
    bbox=dict(boxstyle='round,pad=0.7', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    zorder=10
)

# ax_curve: Information Gain curve
ax_curve.set_xlim(0.5, 9.5)
ax_curve.set_ylim(-0.05, 0.75)
ax_curve.set_xlabel('Поріг розбиття s', fontsize=12, color='#e5e7eb', labelpad=6)
ax_curve.set_ylabel('Information Gain (біт)', fontsize=12, color='#e5e7eb', labelpad=6)
ax_curve.set_title('Приріст інформації: IG(s) = H(батько) - H_зважена(діти)', fontsize=13, fontweight='bold', color='#10b981', pad=10)

curve_line, = ax_curve.plot([], [], color='#10b981', linewidth=2.5, label='Крива IG(s)')
current_dot, = ax_curve.plot([], [], marker='o', markersize=9, color='#fbbf24', markeredgecolor='#ffffff', markeredgewidth=2)
opt_star = ax_curve.plot(best_threshold, best_ig, marker='*', markersize=14, color='#facc15', label=f'Оптимум: s={best_threshold:.2f} (IG={best_ig:.2f})')[0]
ax_curve.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

# ax_bars: Entropy of Left and Right node
bar_labels = ['Батьківський\nвузол', 'Ліва гілка\n(X ≤ s)', 'Права гілка\n(X > s)']
bar_colors = ['#a78bfa', '#38bdf8', '#f43f5e']
bars = ax_bars.bar(bar_labels, [H_parent, 0.0, 0.0], color=bar_colors, edgecolor='#374151', linewidth=1.5, width=0.55)
ax_bars.set_ylim(0, 1.25)
ax_bars.set_ylabel('Ентропія H (невизначеність)', fontsize=12, color='#e5e7eb', labelpad=6)
ax_bars.set_title('Порівняння ентропії вузлів (менше = чистіше)', fontsize=13, fontweight='bold', color='#a78bfa', pad=10)

bar_texts = [
    ax_bars.text(i, 0.1, '', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#ffffff')
    for i in range(3)
]

fig.suptitle('Анімація вибору розбиття: Пошук максимального Information Gain у дереві',
             fontsize=17, fontweight='bold', color='#ffffff', y=0.97)

def init():
    split_line.set_xdata([s_values[0], s_values[0]])
    curve_line.set_data([], [])
    current_dot.set_data([], [])
    return [split_line, curve_line, current_dot]

def update(frame):
    s = s_values[frame]
    split_line.set_xdata([s, s])
    
    # Update zones
    left_rect.set_width(max(0.01, s - 0.5))
    right_rect.set_x(s)
    right_rect.set_width(max(0.01, 9.5 - s))
    
    # Subset points
    left_mask = all_x <= s
    right_mask = ~left_mask
    n_L = np.sum(left_mask)
    n_R = np.sum(right_mask)
    
    H_L = calc_entropy(all_y[left_mask]) if n_L > 0 else 0.0
    H_R = calc_entropy(all_y[right_mask]) if n_R > 0 else 0.0
    current_ig = ig_values[frame]
    
    # Status card
    card_points.set_text(
        f"• Поточний поріг розбиття: s = {s:.2f}\n"
        f"  Ліва гілка (X ≤ s): {n_L} точок | H = {H_L:.2f}\n"
        f"  Права гілка (X > s): {n_R} точок | H = {H_R:.2f}\n"
        f"  Приріст інформації: IG = {current_ig:.3f} біт"
    )
    
    # Curve
    curve_line.set_data(s_values[:frame+1], ig_values[:frame+1])
    current_dot.set_data([s], [current_ig])
    
    # Bars
    bars[0].set_height(H_parent)
    bars[1].set_height(H_L)
    bars[2].set_height(H_R)
    
    bar_texts[0].set_position((0, H_parent + 0.03))
    bar_texts[0].set_text(f"{H_parent:.2f}")
    
    bar_texts[1].set_position((1, H_L + 0.03))
    bar_texts[1].set_text(f"{H_L:.2f}")
    
    bar_texts[2].set_position((2, H_R + 0.03))
    bar_texts[2].set_text(f"{H_R:.2f}")
    
    if abs(s - best_threshold) < 0.15:
        card_points.get_bbox_patch().set_edgecolor('#10b981')
        card_points.get_bbox_patch().set_linewidth(2.5)
    else:
        card_points.get_bbox_patch().set_edgecolor('#374151')
        card_points.get_bbox_patch().set_linewidth(1.5)
        
    return [split_line, curve_line, current_dot, card_points]

n_frames = 120
ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=83)

out_dir = 'public/videos/ai-python/decision-trees-random-forest/decision-trees'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'decision_tree_information_gain.mp4')
output_webm = os.path.join(out_dir, 'decision_tree_information_gain.webm')
output_gif = os.path.join(out_dir, 'decision_tree_information_gain.gif')
poster_png = os.path.join(out_dir, 'decision_tree_information_gain_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно створено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:06', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео decision_tree_information_gain успішно згенеровано!")
