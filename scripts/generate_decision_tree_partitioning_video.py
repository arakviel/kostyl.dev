import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import subprocess
import os

# Set random seed for reproducible point clouds
np.random.seed(42)

# --- 1. Generate Synthetic 2D Dataset ---
# Class 0 (Дешева / Економ): small area OR far from center
n_c0 = 26
c0_x1_a = np.random.uniform(32, 68, 16)
c0_x2_a = np.random.uniform(7.5, 19, 16)
c0_x1_b = np.random.uniform(72, 108, 10)
c0_x2_b = np.random.uniform(13.5, 19.5, 10)
c0_x1 = np.concatenate([c0_x1_a, c0_x1_b])
c0_x2 = np.concatenate([c0_x2_a, c0_x2_b])

# Class 1 (Дорога / Преміум): larger area AND/OR close to center
n_c1 = 26
c1_x1_a = np.random.uniform(72, 108, 16)
c1_x2_a = np.random.uniform(2, 10.5, 16)
c1_x1_b = np.random.uniform(35, 68, 10)
c1_x2_b = np.random.uniform(2, 5.2, 10)
c1_x1 = np.concatenate([c1_x1_a, c1_x1_b])
c1_x2 = np.concatenate([c1_x2_a, c1_x2_b])

# Split parameters
split_x1 = 70.0       # Root split: Площа <= 70
split_x2_left = 6.0   # Left split: Відстань <= 6
split_x2_right = 12.0 # Right split: Відстань <= 12

n_frames = 120

fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.08, 1.0], wspace=0.18, left=0.06, right=0.96, top=0.88, bottom=0.08)

ax_space = fig.add_subplot(gs[0])
ax_tree = fig.add_subplot(gs[1])

# Styling subplots
for ax in [ax_space, ax_tree]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)

ax_space.tick_params(colors='#9ca3af', labelsize=11)
ax_space.grid(True, color='#1f2937', linestyle='--', alpha=0.5)
ax_space.set_xlim(25, 115)
ax_space.set_ylim(0, 21)
ax_space.set_xlabel('Ознака 1: Площа квартири (м²)', fontsize=13, color='#e5e7eb', labelpad=8, fontweight='medium')
ax_space.set_ylabel('Ознака 2: Відстань до центру (км)', fontsize=13, color='#e5e7eb', labelpad=8, fontweight='medium')
ax_space.set_title('Геометрія: Розбиття 2D-простору ознак', fontsize=15, fontweight='bold', color='#38bdf8', pad=12)

# Scatter points
scatter_c0 = ax_space.scatter(c0_x1, c0_x2, color='#38bdf8', s=65, edgecolors='#0284c7', linewidths=1.2, alpha=0.9, zorder=5, label='Клас 0: Дешева (Економ)')
scatter_c1 = ax_space.scatter(c1_x1, c1_x2, color='#f43f5e', s=65, edgecolors='#be123c', linewidths=1.2, alpha=0.9, zorder=5, label='Клас 1: Дорога (Преміум)')
ax_space.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5, framealpha=0.95)

# Boundary lines
line_split1, = ax_space.plot([], [], color='#fbbf24', linewidth=3.5, linestyle='-', zorder=6)
line_split2, = ax_space.plot([], [], color='#34d399', linewidth=3.0, linestyle='-', zorder=6)
line_split3, = ax_space.plot([], [], color='#a78bfa', linewidth=3.0, linestyle='-', zorder=6)

# Test query marker in 2D space
test_dot, = ax_space.plot([], [], marker='*', markersize=20, color='#facc15', markeredgecolor='#ffffff', markeredgewidth=2, zorder=10)
test_dot_label = ax_space.text(0, 0, '', color='#facc15', fontsize=11, fontweight='bold', zorder=11)

# Status card on 2D space
card_space = ax_space.text(0.04, 0.05, '', transform=ax_space.transAxes,
                           fontsize=11.5, family='sans-serif', fontweight='bold', color='#f3f4f6',
                           bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.95, lw=1.5),
                           zorder=12)

# Shading rectangles (4 regions)
patch_r1 = patches.Rectangle((25, 0), 45, 6, facecolor='#f43f5e', alpha=0.0, zorder=2)
patch_r2 = patches.Rectangle((25, 6), 45, 15, facecolor='#38bdf8', alpha=0.0, zorder=2)
patch_r3 = patches.Rectangle((70, 0), 45, 12, facecolor='#f43f5e', alpha=0.0, zorder=2)
patch_r4 = patches.Rectangle((70, 12), 45, 9, facecolor='#38bdf8', alpha=0.0, zorder=2)

for p in [patch_r1, patch_r2, patch_r3, patch_r4]:
    ax_space.add_patch(p)

# Right subplot (Tree graph visualization)
ax_tree.set_xlim(-0.02, 1.02)
ax_tree.set_ylim(-0.05, 1.05)
ax_tree.axis('off')
ax_tree.set_title('Структура: Дерево рішень (CART)', fontsize=15, fontweight='bold', color='#fbbf24', pad=12)

# Perfectly spaced nodes without any overlaps
nodes = {
    'root': {'pos': (0.50, 0.90), 'size': (0.24, 0.12), 'text': 'Корінь:\nПлоща ≤ 70 м²?', 'color': '#fbbf24', 'bg': '#1e293b', 'fontsize': 10},
    'node_l': {'pos': (0.23, 0.54), 'size': (0.22, 0.12), 'text': 'Вузол 2:\nВідстань ≤ 6 км?', 'color': '#34d399', 'bg': '#1e293b', 'fontsize': 9.5},
    'node_r': {'pos': (0.77, 0.54), 'size': (0.22, 0.12), 'text': 'Вузол 3:\nВідстань ≤ 12 км?', 'color': '#a78bfa', 'bg': '#1e293b', 'fontsize': 9.5},
    'leaf_ll': {'pos': (0.11, 0.14), 'size': (0.19, 0.13), 'text': 'Листок 1:\nДОРОГА\n(Class 1)', 'color': '#f43f5e', 'bg': '#2a111a', 'fontsize': 8.5},
    'leaf_lr': {'pos': (0.35, 0.14), 'size': (0.19, 0.13), 'text': 'Листок 2:\nДЕШЕВА\n(Class 0)', 'color': '#38bdf8', 'bg': '#0c2238', 'fontsize': 8.5},
    'leaf_rl': {'pos': (0.65, 0.14), 'size': (0.19, 0.13), 'text': 'Листок 3:\nДОРОГА\n(Class 1)', 'color': '#f43f5e', 'bg': '#2a111a', 'fontsize': 8.5},
    'leaf_rr': {'pos': (0.89, 0.14), 'size': (0.19, 0.13), 'text': 'Листок 4:\nДЕШЕВА\n(Class 0)', 'color': '#38bdf8', 'bg': '#0c2238', 'fontsize': 8.5}
}

# Connectors with offset label placements
edges = [
    ('root', 'node_l', 'Так (≤ 70)', (-0.05, 0.02)),
    ('root', 'node_r', 'Ні (> 70)', (0.05, 0.02)),
    ('node_l', 'leaf_ll', 'Так (≤ 6)', (-0.04, 0.01)),
    ('node_l', 'leaf_lr', 'Ні (> 6)', (0.04, 0.01)),
    ('node_r', 'leaf_rl', 'Так (≤ 12)', (-0.04, 0.01)),
    ('node_r', 'leaf_rr', 'Ні (> 12)', (0.04, 0.01))
]

tree_elements = {}
for name, data in nodes.items():
    x, y = data['pos']
    w, h = data['size']
    box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                 boxstyle="round,pad=0.015,rounding_size=0.025",
                                 facecolor=data['bg'], edgecolor=data['color'], linewidth=2.0, alpha=0.0, zorder=5)
    ax_tree.add_patch(box)
    txt = ax_tree.text(x, y, data['text'], ha='center', va='center',
                       fontsize=data['fontsize'], fontweight='bold', color=data['color'], alpha=0.0, zorder=6,
                       linespacing=1.2)
    tree_elements[name] = {'box': box, 'text': txt, 'base_color': data['color']}

edge_elements = []
for p_name, c_name, lbl, offset in edges:
    px, py = nodes[p_name]['pos']
    cx, cy = nodes[c_name]['pos']
    ph = nodes[p_name]['size'][1] / 2
    ch = nodes[c_name]['size'][1] / 2
    line, = ax_tree.plot([], [], color='#4b5563', linewidth=2.0, linestyle='-', zorder=3)
    mid_x = (px + cx) / 2 + offset[0]
    mid_y = (py - ph + cy + ch) / 2 + offset[1]
    txt = ax_tree.text(mid_x, mid_y, lbl, ha='center', va='center', fontsize=8.5, color='#cbd5e1', fontweight='bold',
                       alpha=0.0, zorder=4)
    edge_elements.append({'p': p_name, 'c': c_name, 'line': line, 'text': txt, 'coords': ([px, cx], [py - ph, cy + ch])})

fig.suptitle('Як дерево рішень ділить простір: від предикатів до прямокутних меж',
             fontsize=17, fontweight='bold', color='#f3f4f6', y=0.96)

def init():
    line_split1.set_data([], [])
    line_split2.set_data([], [])
    line_split3.set_data([], [])
    test_dot.set_data([], [])
    test_dot_label.set_text('')
    card_space.set_text('Старт: вибірка з 52 квартир\nОчікування першого розбиття...')
    tree_elements['root']['box'].set_alpha(1.0)
    tree_elements['root']['text'].set_alpha(1.0)
    return [line_split1, line_split2, line_split3, test_dot, card_space]

def update(frame):
    # Phase 0..15: Init & Root
    if frame < 16:
        card_space.set_text(
            "• Крок 0: Початковий простір ознак\n"
            "  Жодних меж. Усі 52 квартири разом.\n"
            "  Алгоритм шукає поріг найвищої чистоти."
        )
        card_space.get_bbox_patch().set_edgecolor('#fbbf24')
        tree_elements['root']['box'].set_alpha(1.0)
        tree_elements['root']['text'].set_alpha(1.0)
        line_split1.set_data([], [])
        line_split2.set_data([], [])
        line_split3.set_data([], [])
        test_dot.set_data([], [])
        test_dot_label.set_text('')

    # Phase 16..35: First split at x1 = 70
    elif 16 <= frame < 36:
        f = frame - 16
        curr_x = 35 + (70 - 35) * min(1.0, f / 14)
        line_split1.set_data([curr_x, curr_x], [0, 21])
        if f >= 14:
            line_split1.set_color('#fbbf24')
            card_space.set_text(
                "• Спліт 1 (Корінь): [Площа ≤ 70 м²]\n"
                "  Вертикальна лінія ділить простір навпіл\n"
                "  Ліворуч: компактні; Праворуч: просторі"
            )
            for edge in edge_elements[:2]:
                edge['line'].set_data(edge['coords'][0], edge['coords'][1])
                edge['text'].set_alpha(1.0)
            tree_elements['node_l']['box'].set_alpha(1.0)
            tree_elements['node_l']['text'].set_alpha(1.0)
            tree_elements['node_r']['box'].set_alpha(1.0)
            tree_elements['node_r']['text'].set_alpha(1.0)

    # Phase 36..55: Second split in left region at x2 = 6
    elif 36 <= frame < 56:
        f = frame - 36
        curr_y = 18 - (18 - 6) * min(1.0, f / 14)
        line_split2.set_data([25, 70], [curr_y, curr_y])
        if f >= 14:
            line_split2.set_color('#34d399')
            card_space.set_text(
                "• Спліт 2 (Ліва гілка): [Відстань ≤ 6 км]\n"
                "  Горизонтальна лінія ділить ЛІВУ зону\n"
                "  Листок 1: центр (Дорога); Листок 2: околиця"
            )
            for edge in edge_elements[2:4]:
                edge['line'].set_data(edge['coords'][0], edge['coords'][1])
                edge['text'].set_alpha(1.0)
            tree_elements['leaf_ll']['box'].set_alpha(1.0)
            tree_elements['leaf_ll']['text'].set_alpha(1.0)
            tree_elements['leaf_lr']['box'].set_alpha(1.0)
            tree_elements['leaf_lr']['text'].set_alpha(1.0)

    # Phase 56..75: Third split in right region at x2 = 12
    elif 56 <= frame < 76:
        f = frame - 56
        curr_y = 19 - (19 - 12) * min(1.0, f / 14)
        line_split3.set_data([70, 115], [curr_y, curr_y])
        if f >= 14:
            line_split3.set_color('#a78bfa')
            card_space.set_text(
                "• Спліт 3 (Права гілка): [Відстань ≤ 12 км]\n"
                "  Горизонтальна лінія ділить ПРАВУ зону\n"
                "  Сформовано 4 ортогональні сектори"
            )
            for edge in edge_elements[4:6]:
                edge['line'].set_data(edge['coords'][0], edge['coords'][1])
                edge['text'].set_alpha(1.0)
            tree_elements['leaf_rl']['box'].set_alpha(1.0)
            tree_elements['leaf_rl']['text'].set_alpha(1.0)
            tree_elements['leaf_rr']['box'].set_alpha(1.0)
            tree_elements['leaf_rr']['text'].set_alpha(1.0)

    # Phase 76..85: Region color filling
    elif 76 <= frame < 86:
        f = frame - 76
        alpha_val = 0.22 * (f / 9.0)
        patch_r1.set_alpha(alpha_val)
        patch_r2.set_alpha(alpha_val)
        patch_r3.set_alpha(alpha_val)
        patch_r4.set_alpha(alpha_val)
        card_space.set_text(
            "• Регіони рішень (Decision Regions)\n"
            "  Кожен прямокутник закріплюється за класом\n"
            "  Червоний = Дорога, Блакитний = Дешева"
        )
        card_space.get_bbox_patch().set_edgecolor('#10b981')

    # Phase 86..112: Interactive test sample classification
    elif 86 <= frame < 113:
        f = frame - 86
        if f < 13:
            # Query 1: (48, 3.8) -> Leaf 1
            qx, qy = 48, 3.8
            test_dot.set_data([qx], [qy])
            test_dot_label.set_position((qx + 2.5, qy + 0.8))
            test_dot_label.set_text("Об'єкт А (48 м², 3.8 км)")
            card_space.set_text(
                "• Інференс: Об'єкт А (48 м², 3.8 км)\n"
                "  1. Площа ≤ 70? ТАК ➔ Ліворуч\n"
                "  2. Відстань ≤ 6? ТАК ➔ Листок 1\n"
                "  Прогноз: ДОРОГА (Преміум)"
            )
            card_space.get_bbox_patch().set_edgecolor('#f43f5e')
            # highlight tree path: root -> node_l -> leaf_ll
            tree_elements['root']['box'].set_edgecolor('#facc15')
            tree_elements['node_l']['box'].set_edgecolor('#facc15')
            tree_elements['leaf_ll']['box'].set_edgecolor('#facc15')
            tree_elements['leaf_ll']['box'].set_linewidth(3.5)
        else:
            # Query 2: (92, 16.5) -> Leaf 4
            qx, qy = 92, 16.5
            test_dot.set_data([qx], [qy])
            test_dot_label.set_position((qx - 32, qy + 0.8))
            test_dot_label.set_text("Об'єкт Б (92 м², 16.5 км)")
            card_space.set_text(
                "• Інференс: Об'єкт Б (92 м², 16.5 км)\n"
                "  1. Площа ≤ 70? НІ ➔ Праворуч\n"
                "  2. Відстань ≤ 12? НІ ➔ Листок 4\n"
                "  Прогноз: ДЕШЕВА (Економ)"
            )
            card_space.get_bbox_patch().set_edgecolor('#38bdf8')
            # reset prev highlights and highlight root -> node_r -> leaf_rr
            tree_elements['node_l']['box'].set_edgecolor(tree_elements['node_l']['base_color'])
            tree_elements['leaf_ll']['box'].set_edgecolor(tree_elements['leaf_ll']['base_color'])
            tree_elements['leaf_ll']['box'].set_linewidth(2.0)
            tree_elements['node_r']['box'].set_edgecolor('#facc15')
            tree_elements['leaf_rr']['box'].set_edgecolor('#facc15')
            tree_elements['leaf_rr']['box'].set_linewidth(3.5)

    # Phase 113..120: Hold conclusion before loop
    else:
        card_space.set_text(
            "• Готова модель дерева рішень\n"
            "  Простір розбито на прямокутні сегменти\n"
            "  Кожен листок відповідає одній комірці сітки"
        )
        card_space.get_bbox_patch().set_edgecolor('#10b981')
        tree_elements['root']['box'].set_edgecolor(tree_elements['root']['base_color'])
        tree_elements['node_r']['box'].set_edgecolor(tree_elements['node_r']['base_color'])
        tree_elements['leaf_rr']['box'].set_edgecolor(tree_elements['leaf_rr']['base_color'])
        tree_elements['leaf_rr']['box'].set_linewidth(2.0)

    return [line_split1, line_split2, line_split3, test_dot, card_space]

print("Генерація оновленої анімації FuncAnimation...")
ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=83)

out_dir = 'public/videos/ai-python/decision-trees-random-forest/decision-trees'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'decision_tree_2d_space_partitioning.mp4')
output_webm = os.path.join(out_dir, 'decision_tree_2d_space_partitioning.webm')
output_gif = os.path.join(out_dir, 'decision_tree_2d_space_partitioning.gif')
poster_png = os.path.join(out_dir, 'decision_tree_2d_space_partitioning_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно створено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:07', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Усі оновлені відеоматеріали успішно скомпільовано!")
