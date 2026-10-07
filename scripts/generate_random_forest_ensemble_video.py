import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import subprocess
import os

# Set seed for reproducible data
np.random.seed(42)

# Generate 2D dataset with noise and a couple of tough outliers
X, y = make_moons(n_samples=90, noise=0.26, random_state=42)

# Add 4 explicit outlier points to highlight severe overfitting in single tree
outliers_X = np.array([
    [-0.5, 0.9],
    [0.8, -0.6],
    [1.6, -0.3],
    [0.1, 0.2]
])
outliers_y = np.array([1, 0, 0, 1])

X = np.vstack([X, outliers_X])
y = np.concatenate([y, outliers_y])

# Scale to realistic domain: e.g. "Дохід" vs "Кредитний рейтинг" or Area vs Age
# Let's keep normalized [-1.5, 2.5] x [-1.0, 1.5] for clean mathematical elegance,
# with labels: "Ознака X₁ (Дохід клієнта)" and "Ознака X₂ (Кредитна історія)"
x_min, x_max = X[:, 0].min() - 0.4, X[:, 0].max() + 0.4
y_min, y_max = X[:, 1].min() - 0.4, X[:, 1].max() + 0.4
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 150),
                     np.linspace(y_min, y_max, 150))
grid_points = np.c_[xx.ravel(), yy.ravel()]

# Single deep tree (frozen overfit baseline)
dt = DecisionTreeClassifier(max_depth=None, random_state=42)
dt.fit(X, y)
Z_dt = dt.predict(grid_points).reshape(xx.shape)

# Sequence of forest sizes for animation
# 120 frames total (10 seconds at 12 fps)
# Phase 1 (0..15): Start with 1 tree in forest
# Phase 2 (16..75): Rapid progressive accumulation from 2 to 60 trees
# Phase 3 (76..95): Growth from 60 to 100 trees (fine stabilization)
# Phase 4 (96..120): Hold finale with smooth decision boundary and test metrics
tree_counts = []
for frame in range(120):
    if frame < 15:
        count = 1
    elif frame < 75:
        progress = (frame - 15) / 60.0
        count = int(1 + 59 * (progress ** 1.5))
    elif frame < 95:
        progress = (frame - 75) / 20.0
        count = int(60 + 40 * progress)
    else:
        count = 100
    tree_counts.append(max(1, count))

# Pre-train random forests for key counts to make animation generation ultra-fast
forest_cache = {}
unique_counts = sorted(list(set(tree_counts)))
for c in unique_counts:
    rf = RandomForestClassifier(n_estimators=c, max_depth=None, random_state=42)
    rf.fit(X, y)
    proba = rf.predict_proba(grid_points)[:, 1].reshape(xx.shape)
    forest_cache[c] = proba

# Setup Figure
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.16, left=0.06, right=0.96, top=0.88, bottom=0.08)

ax_dt = fig.add_subplot(gs[0])
ax_rf = fig.add_subplot(gs[1])

for ax in [ax_dt, ax_rf]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=10.5)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.5)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Ознака 1: Дохід клієнта (X₁)', fontsize=12.5, color='#e5e7eb', labelpad=8)
    ax.set_ylabel('Ознака 2: Кредитний рейтинг (X₂)', fontsize=12.5, color='#e5e7eb', labelpad=8)

fig.suptitle('Bagging у дії: подолання перенавчання та згладжування меж рішень',
             fontsize=17, fontweight='bold', color='#f3f4f6', y=0.96)

ax_dt.set_title('1. Одиночне глибоке дерево (Decision Tree, d=None)', fontsize=14, fontweight='bold', color='#f43f5e', pad=10)
ax_rf.set_title('2. Ансамбль Random Forest (Голосування більшості)', fontsize=14, fontweight='bold', color='#10b981', pad=10)

# Static background contour for Single Decision Tree
ax_dt.contourf(xx, yy, Z_dt, levels=2, colors=['#0f2b48', '#421626'], alpha=0.6, zorder=1)
ax_dt.contour(xx, yy, Z_dt, levels=[0.5], colors=['#f43f5e'], linewidths=2.8, linestyles='--', zorder=3)

# Scatter points on both axes
for ax in [ax_dt, ax_rf]:
    ax.scatter(X[y == 0, 0], X[y == 0, 1], color='#38bdf8', edgecolors='#0284c7', s=55, linewidths=1.2, alpha=0.9, zorder=5, label='Клас 0 (Відхилено)')
    ax.scatter(X[y == 1, 0], X[y == 1, 1], color='#f43f5e', edgecolors='#be123c', s=55, linewidths=1.2, alpha=0.9, zorder=5, label='Клас 1 (Схвалено)')

# Legend
ax_dt.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=9.5, framealpha=0.95)
ax_rf.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=9.5, framealpha=0.95)

# Diagnostic cards on subplots
card_dt = ax_dt.text(0.04, 0.04,
                     "• Стан: Катастрофічне перенавчання\n"
                     "  Дерево завчило кожен випадковий шум\n"
                     "  Межі: рвані гострі прямокутні острови\n"
                     "  Дисперсія (Variance): МАКСИМАЛЬНА",
                     transform=ax_dt.transAxes,
                     fontsize=11, family='sans-serif', fontweight='bold', color='#fecdd3',
                     bbox=dict(boxstyle='round,pad=0.55', facecolor='#1e293b', edgecolor='#f43f5e', alpha=0.95, lw=1.5),
                     zorder=10)

card_rf = ax_rf.text(0.04, 0.04, '',
                     transform=ax_rf.transAxes,
                     fontsize=11, family='sans-serif', fontweight='bold', color='#f3f4f6',
                     bbox=dict(boxstyle='round,pad=0.55', facecolor='#1e293b', edgecolor='#10b981', alpha=0.95, lw=1.5),
                     zorder=10)

# Dynamic elements container for RF plot
rf_contour_artists = []

def init():
    card_rf.set_text("• Ініціалізація ансамблю...")
    return [card_rf]

def update(frame):
    global rf_contour_artists
    # Remove old contour fills safely
    for artist in rf_contour_artists:
        try:
            artist.remove()
        except Exception:
            for coll in getattr(artist, 'collections', []):
                try:
                    coll.remove()
                except Exception:
                    pass
    rf_contour_artists.clear()

    k = tree_counts[frame]
    proba = forest_cache[k]

    # Draw probability field
    # 0 = Class 0 (dark blue), 1 = Class 1 (dark red)
    cf = ax_rf.contourf(xx, yy, proba, levels=np.linspace(0, 1, 11), cmap='coolwarm', alpha=0.55, zorder=1)
    # Decision boundary at threshold 0.5
    cb = ax_rf.contour(xx, yy, proba, levels=[0.5], colors=['#fbbf24'], linewidths=3.0, linestyles='-', zorder=3)
    rf_contour_artists.extend([cf, cb])

    # Dynamic status text
    variance_pct = max(1.0, 100.0 / np.sqrt(k))
    if k == 1:
        card_rf.set_text(
            f"• Дерев в ансамблі: K = {k}\n"
            f"  Одне дерево має такі самі шумові вади\n"
            f"  Дисперсія: 100% (висока нестабільність)\n"
            f"  Статус: Старт процедури Bagging"
        )
        card_rf.get_bbox_patch().set_edgecolor('#fbbf24')
    elif k < 15:
        card_rf.set_text(
            f"• Дерев в ансамблі: K = {k}\n"
            f"  Перші дерева компенсують помилки сусіда\n"
            f"  Дисперсія: ~{variance_pct:.0f}% (помітне спадання)\n"
            f"  Статус: Гострі кути починають згладжуватися"
        )
        card_rf.get_bbox_patch().set_edgecolor('#38bdf8')
    elif k < 60:
        card_rf.set_text(
            f"• Дерев в ансамблі: K = {k}\n"
            f"  Випадкові викиди ігноруються більшістю\n"
            f"  Дисперсія: ~{variance_pct:.0f}% (радикальне згасання)\n"
            f"  Статус: Межа наближається до плавної кривої"
        )
        card_rf.get_bbox_patch().set_edgecolor('#34d399')
    else:
        card_rf.set_text(
            f"• Дерев в ансамблі: K = {k} (Фінал)\n"
            f"  Повний консенсус мудрості натовпу\n"
            f"  Дисперсія: ~{variance_pct:.0f}% (шум повністю погашено)\n"
            f"  Статус: Ідеальна гармонійна межа рішень"
        )
        card_rf.get_bbox_patch().set_edgecolor('#10b981')

    return [card_rf]

n_frames = len(tree_counts)
print("Генерація анімації Random Forest FuncAnimation...")
ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=83)

out_dir = 'public/videos/ai-python/decision-trees-random-forest/random-forest'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'random_forest_variance_reduction.mp4')
output_webm = os.path.join(out_dir, 'random_forest_variance_reduction.webm')
output_gif = os.path.join(out_dir, 'random_forest_variance_reduction.gif')
poster_png = os.path.join(out_dir, 'random_forest_variance_reduction_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно збережено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:08', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відеоматеріали для Random Forest успішно згенеровано!")
