import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import subprocess
import os

# Set seed
np.random.seed(42)

# Generate 2D dataset
X, y = make_moons(n_samples=140, noise=0.28, random_state=42)
# Add a few challenging outliers
outliers_X = np.array([[-0.4, 0.9], [0.9, -0.5], [1.5, -0.2], [0.2, 0.1]])
outliers_y = np.array([1, 0, 0, 1])
X = np.vstack([X, outliers_X])
y = np.concatenate([y, outliers_y])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)

# Meshgrid for 2D decision boundary
x_min, x_max = X[:, 0].min() - 0.4, X[:, 0].max() + 0.4
y_min, y_max = X[:, 1].min() - 0.4, X[:, 1].max() + 0.4
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 150),
                     np.linspace(y_min, y_max, 150))
grid_points = np.c_[xx.ravel(), yy.ravel()]

# Depths to evaluate
all_depths = list(range(1, 16))
train_accs = []
test_accs = []
models = {}
preds = {}

for d in all_depths:
    clf = DecisionTreeClassifier(max_depth=d, random_state=42)
    clf.fit(X_train, y_train)
    models[d] = clf
    train_accs.append(accuracy_score(y_train, clf.predict(X_train)))
    test_accs.append(accuracy_score(y_test, clf.predict(X_test)))
    preds[d] = clf.predict(grid_points).reshape(xx.shape)

# Convert to errors (1 - acc)
train_errs = [1.0 - a for a in train_accs]
test_errs = [1.0 - a for a in test_accs]

# Frame schedule: 120 frames
# Smooth progression through depths 1..15, holding key stages:
# Depth 1: frames 0..14 (Underfitting)
# Depth 2: frames 15..28
# Depth 3: frames 29..48 (Sweet spot / Optimal)
# Depth 5: frames 49..68
# Depth 8: frames 69..88 (Overfitting begins)
# Depth 14: frames 89..120 (Extreme Overfitting)
frame_to_depth = (
    [1] * 15 +
    [2] * 14 +
    [3] * 20 +
    [5] * 20 +
    [8] * 20 +
    [14] * 31
)

# Setup figure
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 0.95], height_ratios=[1.0, 1.0],
                      wspace=0.18, hspace=0.32, left=0.06, right=0.96, top=0.90, bottom=0.08)

ax_space = fig.add_subplot(gs[:, 0])
ax_curve = fig.add_subplot(gs[0, 1])
ax_diag = fig.add_subplot(gs[1, 1])

for ax in [ax_space, ax_curve, ax_diag]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=11)
    ax.grid(True, color='#1f2937', linestyle='--', alpha=0.5)

# ax_space setup
ax_space.set_xlim(x_min, x_max)
ax_space.set_ylim(y_min, y_max)
ax_space.set_xlabel('Ознака X₁ (наприклад, вік клієнта / площа)', fontsize=13, color='#e5e7eb', labelpad=8)
ax_space.set_ylabel('Ознака X₂ (наприклад, дохід / кредитна історія)', fontsize=13, color='#e5e7eb', labelpad=8)
ax_space.set_title('2D Межа рішень: Еволюція глибини (max_depth)', fontsize=14, fontweight='bold', color='#38bdf8', pad=12)

# Training points
train_c0 = ax_space.scatter(X_train[y_train == 0, 0], X_train[y_train == 0, 1],
                            color='#38bdf8', s=60, edgecolors='#0284c7', linewidths=1.2, alpha=0.9,
                            label='Train: Клас 0 (Сині)', zorder=5)
train_c1 = ax_space.scatter(X_train[y_train == 1, 0], X_train[y_train == 1, 1],
                            color='#f43f5e', s=60, edgecolors='#be123c', linewidths=1.2, alpha=0.9,
                            label='Train: Клас 1 (Червоні)', zorder=5)

# Test points
test_pts = ax_space.scatter(X_test[:, 0], X_test[:, 1],
                            facecolors='none', edgecolors='#facc15', s=80, linewidths=1.8, marker='^',
                            label='Test вибірка (Контроль)', zorder=6)

ax_space.legend(loc='lower left', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10.5, framealpha=0.95)

card_space = ax_space.text(
    0.04, 0.96, '', transform=ax_space.transAxes,
    fontsize=12, color='#e5e7eb', verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.7', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    zorder=10
)

# ax_curve setup: Train vs Test error
ax_curve.set_xlim(0.5, 15.5)
ax_curve.set_ylim(-0.02, 0.42)
ax_curve.set_xlabel('Параметр max_depth (глибина дерева)', fontsize=12, color='#e5e7eb', labelpad=6)
ax_curve.set_ylabel('Помилка класифікації (1 - Accuracy)', fontsize=12, color='#e5e7eb', labelpad=6)
ax_curve.set_title('Крива валідації: Помилка на Train проти Test', fontsize=13, fontweight='bold', color='#fbbf24', pad=10)

ax_curve.plot(all_depths, train_errs, color='#38bdf8', linewidth=2.5, linestyle='--', label='Train Error (падає до 0%)')
ax_curve.plot(all_depths, test_errs, color='#f43f5e', linewidth=2.8, label='Test Error (зростає при перенавчанні)')
ax_curve.axvline(3, color='#10b981', linestyle=':', linewidth=2.0, label='Оптимальна зона (d = 3)')
ax_curve.legend(loc='upper right', facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb', fontsize=10)

marker_train, = ax_curve.plot([], [], marker='o', markersize=9, color='#38bdf8', markeredgecolor='#ffffff', markeredgewidth=2)
marker_test, = ax_curve.plot([], [], marker='s', markersize=9, color='#f43f5e', markeredgecolor='#ffffff', markeredgewidth=2)

# ax_diag setup
ax_diag.set_xlim(0, 1)
ax_diag.set_ylim(0, 1)
ax_diag.axis('off')

diag_text = ax_diag.text(
    0.05, 0.95, '',
    fontsize=12, color='#e5e7eb', verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.8', facecolor='#1f2937', edgecolor='#374151', linewidth=1.5, alpha=0.95),
    linespacing=1.45
)

fig.suptitle('Анімація перенавчання: Як надмірна глибина руйнує узагальнення дерева рішень',
             fontsize=17, fontweight='bold', color='#ffffff', y=0.97)

contour_artists = []

def init():
    marker_train.set_data([], [])
    marker_test.set_data([], [])
    return [marker_train, marker_test]

def update(frame):
    d = frame_to_depth[frame]
    Z = preds[d]
    clf = models[d]
    
    # Remove old contour safely
    for artist in contour_artists:
        try:
            artist.remove()
        except Exception:
            for coll in getattr(artist, 'collections', []):
                try:
                    coll.remove()
                except Exception:
                    pass
    contour_artists.clear()
            
    # Redraw decision boundary contour
    cf = ax_space.contourf(xx, yy, Z, levels=[-0.5, 0.5, 1.5],
                           colors=['#0284c7', '#be123c'], alpha=0.28, zorder=1)
    cb = ax_space.contour(xx, yy, Z, levels=[0.5], colors=['#fbbf24'], linewidths=2.5, zorder=2)
    contour_artists.extend([cf, cb])
    
    tr_err = train_errs[d - 1]
    te_err = test_errs[d - 1]
    n_leaves = clf.get_n_leaves()
    
    marker_train.set_data([d], [tr_err])
    marker_test.set_data([d], [te_err])
    
    # Diagnosis logic
    if d <= 2:
        verdict = "Недонавчання (High Bias): межа занадто груба, багато помилок."
        border_col = '#38bdf8'
        status_box = (
            "• Стан моделі: Недонавчання (Underfitting)\n"
            "• Дерево ще занадто просте, не вловлює форму розподілу\n"
            "• Train помилка та Test помилка обидві високі"
        )
    elif d == 3:
        verdict = "Оптимальна модель (Sweet Spot): найкраще узагальнення на Test!"
        border_col = '#10b981'
        status_box = (
            "• Стан моделі: Оптимальний баланс (Good Fit)\n"
            "• Межа рішень плавна, прямокутні блоки не реагують на шум\n"
            "• Мінімальна помилка на нових даних (Test Error мінімальна)"
        )
    elif d <= 5:
        verdict = "Початок перенавчання: з'являються локальні вирізи під шум."
        border_col = '#fbbf24'
        status_box = (
            "• Стан моделі: Початок перенавчання\n"
            "• Дерево починає створювати мікро-зони навколо випадкових точок\n"
            "• Train Error продовжує падати, але Test Error вже не покращується"
        )
    else:
        verdict = "Глибоке перенавчання (Overfitting): ізольовані кишені під кожен викид!"
        border_col = '#f43f5e'
        status_box = (
            "• Стан моделі: Критичне перенавчання (High Variance)\n"
            "• Дерево запам'ятало кожен викид, створюючи мініатюрні острівці\n"
            "• Train Error = 0% (ідеально на трейні), але Test Error стрімко зросла!"
        )
        
    card_space.set_text(
        f"• Глибина: max_depth = {d} | Листків: {n_leaves}\n"
        f"  Помилка Train: {tr_err*100:.1f}% | Test: {te_err*100:.1f}%\n"
        f"  {verdict}"
    )
    card_space.get_bbox_patch().set_edgecolor(border_col)
    
    diag_text.set_text(
        f"• Діагностика поведінки моделі:\n\n"
        f"{status_box}\n\n"
        f"• Як запобігти цьому на практиці:\n"
        f"1. max_depth (наприклад, 3-5 замість None)\n"
        f"2. min_samples_split (заборона ділити вузол, де мало прикладів)\n"
        f"3. min_samples_leaf (гарантія мінімальної кількості об'єктів у листку)"
    )
    diag_text.get_bbox_patch().set_edgecolor(border_col)
    
    return [marker_train, marker_test, card_space, diag_text]

ani = animation.FuncAnimation(fig, update, frames=120, init_func=init, interval=83)

out_dir = 'public/videos/ai-python/decision-trees-random-forest/decision-trees'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'decision_tree_overfitting_depth_dynamics.mp4')
output_webm = os.path.join(out_dir, 'decision_tree_overfitting_depth_dynamics.webm')
output_gif = os.path.join(out_dir, 'decision_tree_overfitting_depth_dynamics.gif')
poster_png = os.path.join(out_dir, 'decision_tree_overfitting_depth_dynamics_poster.png')

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

print("Відео decision_tree_overfitting_depth_dynamics успішно згенеровано!")
