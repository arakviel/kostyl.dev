import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import subprocess
import os

# Set seed
np.random.seed(42)

# Total dataset samples N = 12 (easy to visually track each numbered item)
N = 12
sample_ids = np.arange(1, N + 1)

# Generate 4 bootstrap rounds
n_trees = 4
bootstraps = []
oob_masks = []

for t in range(n_trees):
    # Sample with replacement
    sampled = np.random.choice(sample_ids, size=N, replace=True)
    bootstraps.append(sampled)
    in_bag = set(sampled)
    oob = [s not in in_bag for s in sample_ids]
    oob_masks.append(oob)

# Precalculate cumulative OOB stats for animation
# 120 frames total:
# 0..20: Show Original Dataset & Explain with-replacement logic
# 21..45: Draw Tree 1 Bootstrap (highlight in-bag vs OOB)
# 46..70: Draw Tree 2 Bootstrap
# 71..95: Draw Tree 3 Bootstrap
# 96..120: Draw Tree 4 Bootstrap & Summarize 63.2% / 36.8% limit

fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 1.0], height_ratios=[1.0, 1.0],
                      wspace=0.18, hspace=0.32, left=0.06, right=0.96, top=0.90, bottom=0.08)

ax_pool = fig.add_subplot(gs[0, 0])
ax_trees = fig.add_subplot(gs[1, 0])
ax_matrix = fig.add_subplot(gs[:, 1])

for ax in [ax_pool, ax_trees, ax_matrix]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=10)

# ax_pool setup: original dataset
ax_pool.set_xlim(-0.5, N - 0.5)
ax_pool.set_ylim(-0.8, 1.8)
ax_pool.set_xticks(range(N))
ax_pool.set_xticklabels([f"#{i}" for i in sample_ids], color='#9ca3af', fontsize=10)
ax_pool.set_yticks([])
ax_pool.set_title('Вихідний датасет: N = 12 навчальних об\'єктів', fontsize=13, fontweight='bold', color='#38bdf8', pad=10)

pool_circles = []
for i in range(N):
    c = plt.Circle((i, 0.5), 0.38, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=2.0)
    ax_pool.add_patch(c)
    ax_pool.text(i, 0.5, f"#{i+1}", ha='center', va='center', color='#ffffff', fontweight='bold', fontsize=10.5)
    pool_circles.append(c)

pool_status = ax_pool.text(
    0.04, 0.08, '', transform=ax_pool.transAxes,
    fontsize=11, color='#e5e7eb',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#1f2937', edgecolor='#374151', linewidth=1.2)
)

# ax_trees setup: active bootstrap bag
ax_trees.set_xlim(-0.5, N - 0.5)
ax_trees.set_ylim(-0.6, 2.2)
ax_trees.set_xticks(range(N))
ax_trees.set_xticklabels([f"Слот {i+1}" for i in range(N)], color='#9ca3af', fontsize=8.5)
ax_trees.set_yticks([])
ax_trees.set_title('Bootstrap-вибірка для поточного дерева (з поверненням)', fontsize=13, fontweight='bold', color='#10b981', pad=10)

bag_slots = []
bag_texts = []
for i in range(N):
    r = patches.Rectangle((i - 0.4, 0.2), 0.8, 0.9, facecolor='#1f2937', edgecolor='#4b5563', linewidth=1.5)
    ax_trees.add_patch(r)
    bag_slots.append(r)
    t = ax_trees.text(i, 0.65, '—', ha='center', va='center', color='#9ca3af', fontweight='bold', fontsize=10)
    bag_texts.append(t)

tree_status = ax_trees.text(
    0.04, 0.06, '', transform=ax_trees.transAxes,
    fontsize=11, color='#e5e7eb',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#1f2937', edgecolor='#374151', linewidth=1.2)
)

# ax_matrix setup: Table of Trees x Samples
ax_matrix.set_xlim(-1.2, N + 0.2)
ax_matrix.set_ylim(n_trees + 0.8, -0.6)
ax_matrix.set_xticks(range(N))
ax_matrix.set_xticklabels([f"#{i}" for i in sample_ids], color='#9ca3af', fontsize=9.5)
ax_matrix.set_yticks(range(n_trees))
ax_matrix.set_yticklabels([f"Дерево {t+1}" for t in range(n_trees)], color='#e5e7eb', fontsize=11, fontweight='medium')
ax_matrix.set_title('OOB-Матриця розподілу: In-Bag (навчання) vs Out-of-Bag (контроль)', fontsize=13, fontweight='bold', color='#fbbf24', pad=10)

matrix_cells = {}
matrix_texts = {}
for t in range(n_trees):
    for s in range(N):
        rect = patches.Rectangle((s - 0.45, t - 0.4), 0.9, 0.8, facecolor='#1f2937', edgecolor='#374151', linewidth=1.0)
        ax_matrix.add_patch(rect)
        matrix_cells[(t, s)] = rect
        txt = ax_matrix.text(s, t, '—', ha='center', va='center', color='#6b7280', fontsize=9.5, fontweight='bold')
        matrix_texts[(t, s)] = txt

# Legend badges on ax_matrix
ax_matrix.text(
    0.04, 0.04, '', transform=ax_matrix.transAxes,
    fontsize=11.5, color='#e5e7eb', verticalalignment='bottom',
    bbox=dict(boxstyle='round,pad=0.7', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    linespacing=1.4
)
matrix_card = ax_matrix.texts[-1]

fig.suptitle('Анімація Bootstrap & OOB: Як формуються випадкові підвибірки у лісі',
             fontsize=17, fontweight='bold', color='#ffffff', y=0.97)

def init():
    return []

def update(frame):
    # Phase calculation
    if frame < 20:
        current_tree = 0
        phase = 0
    elif frame < 45:
        current_tree = 0
        phase = 1
    elif frame < 70:
        current_tree = 1
        phase = 2
    elif frame < 95:
        current_tree = 2
        phase = 3
    else:
        current_tree = 3
        phase = 4

    # Pool status
    pool_status.set_text(
        "• Кожен крок Bootstrap бере випадковий об'єкт з пулу, копіює його у вибірку і ПОВЕРТАЄ назад."
    )
    
    # Active bootstrap bag display
    cur_samples = bootstraps[current_tree]
    counts = {}
    for sid in cur_samples:
        counts[sid] = counts.get(sid, 0) + 1
        
    for i in range(N):
        sid = cur_samples[i]
        bag_texts[i].set_text(f"#{sid}")
        if counts[sid] > 1:
            bag_slots[i].set_facecolor('#065f46')
            bag_slots[i].set_edgecolor('#34d399')
            bag_texts[i].set_color('#6ee7b7')
        else:
            bag_slots[i].set_facecolor('#1e293b')
            bag_slots[i].set_edgecolor('#38bdf8')
            bag_texts[i].set_color('#e0f2fe')
            
    n_unique = len(counts)
    n_oob = N - n_unique
    oob_pct = (n_oob / N) * 100
    inbag_pct = (n_unique / N) * 100
    
    tree_status.set_text(
        f"• Дерево {current_tree + 1}: Унікальних: {n_unique}/{N} ({inbag_pct:.1f}%) | "
        f"Не потрапили (OOB): {n_oob} шт. ({oob_pct:.1f}%)"
    )

    # Highlight pool items according to active tree
    for i in range(N):
        sid = i + 1
        c = counts.get(sid, 0)
        if c == 0:
            pool_circles[i].set_facecolor('#7f1d1d')
            pool_circles[i].set_edgecolor('#f43f5e')
        elif c == 1:
            pool_circles[i].set_facecolor('#0f172a')
            pool_circles[i].set_edgecolor('#38bdf8')
        else:
            pool_circles[i].set_facecolor('#064e3b')
            pool_circles[i].set_edgecolor('#34d399')

    # Update matrix up to current tree
    for t in range(n_trees):
        if t <= current_tree:
            t_counts = {}
            for sid in bootstraps[t]:
                t_counts[sid] = t_counts.get(sid, 0) + 1
                
            for s in range(N):
                sid = s + 1
                cnt = t_counts.get(sid, 0)
                if cnt > 0:
                    matrix_cells[(t, s)].set_facecolor('#064e3b')
                    matrix_cells[(t, s)].set_edgecolor('#10b981')
                    matrix_texts[(t, s)].set_text(f"×{cnt}" if cnt > 1 else "In")
                    matrix_texts[(t, s)].set_color('#a7f3d0')
                else:
                    matrix_cells[(t, s)].set_facecolor('#7f1d1d')
                    matrix_cells[(t, s)].set_edgecolor('#f43f5e')
                    matrix_texts[(t, s)].set_text("OOB")
                    matrix_texts[(t, s)].set_color('#fca5a5')
        else:
            for s in range(N):
                matrix_cells[(t, s)].set_facecolor('#1f2937')
                matrix_cells[(t, s)].set_edgecolor('#374151')
                matrix_texts[(t, s)].set_text("—")
                matrix_texts[(t, s)].set_color('#6b7280')

    matrix_card.set_text(
        "• Легенда OOB-матриці:\n"
        "  [In / ×k] Зелений — об'єкт потрапив у навчання (In-Bag)\n"
        "  [OOB] Червоний — об'єкт випав, дерево його не бачило!\n\n"
        "• Чому це важливо:\n"
        "  Кожен приклад у середньому OOB для 36.8% дерев лісу.\n"
        "  Ці дерева голосують за нього як незалежні тестові експерти!\n"
        "  Тестування без жодного розділення вибірки (Zero Overhead)."
    )

    return []

ani = animation.FuncAnimation(fig, update, frames=120, init_func=init, interval=83)

out_dir = 'public/videos/ai-python/decision-trees-random-forest/random-forest'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'random_forest_bootstrap_oob.mp4')
output_webm = os.path.join(out_dir, 'random_forest_bootstrap_oob.webm')
output_gif = os.path.join(out_dir, 'random_forest_bootstrap_oob.gif')
poster_png = os.path.join(out_dir, 'random_forest_bootstrap_oob_poster.png')

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

print("Відео random_forest_bootstrap_oob успішно згенеровано!")
