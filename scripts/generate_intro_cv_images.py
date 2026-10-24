"""
Script to generate high-resolution educational diagrams for:
content/16.ai-python/15.cnn-image-classification/01.intro-computer-vision.md
Target directory:
public/images/ai-python/cnn-image-classification/intro-computer-vision/
Files:
- 01.png: Grayscale image representation as 2D pixel matrix (5x5)
- 02.png: real photo patch (sklearn flower.jpg, 4x4) decomposed into R, G, B channels
- 03.png: Parameter explosion comparison (MNIST vs ImageNet in Dense network)
- 04.png: Spatial locality principle and loss of 2D topology in flattening
- 05.png: real MNIST digit 3 shifted by 5 px: flattened vectors almost entirely differ
- 06.png: Hierarchical feature representation in CNN (Edges -> Textures -> Objects)
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Aesthetics setup
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

OUT_DIR = "public/images/ai-python/cnn-image-classification/intro-computer-vision"
os.makedirs(OUT_DIR, exist_ok=True)

def draw_cell_borders(ax, rows, cols, color='#CBD5E1', linewidth=1.0):
    """Draw crisp grid lines along the cell edges instead of cell centers."""
    for r in range(rows + 1):
        ax.axhline(r - 0.5, color=color, linewidth=linewidth)
    for c in range(cols + 1):
        ax.axvline(c - 0.5, color=color, linewidth=linewidth)


# -----------------------------------------------------------------------------
# 1. 01.png: Grayscale 5x5 representation
# -----------------------------------------------------------------------------
def generate_01():
    print("Generating 01.png (polished)...")
    image = np.array([
        [0,   0,   0,   0,   0],
        [0, 255, 255, 255,   0],
        [0, 255,   0, 255,   0],
        [0, 255, 255, 255,   0],
        [0,   0,   0,   0,   0]
    ], dtype=np.uint8)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Left: Visual appearance
    ax = axes[0]
    ax.set_facecolor('#F8FAFC')
    ax.imshow(image, cmap='gray', vmin=0, vmax=255)
    ax.set_title('1. Візуальне зображення (5×5 пікселів)', fontsize=12, fontweight='bold', color='#0F172A', pad=14)
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xlabel('Координата X (стовпчик)', fontsize=10, color='#334155', labelpad=8)
    ax.set_ylabel('Координата Y (рядок)', fontsize=10, color='#334155', labelpad=8)
    draw_cell_borders(ax, 5, 5, color='#EF4444', linewidth=1.2)
    ax.tick_params(colors='#475569')

    # Annotate coordinate labels inside cells
    for r in range(5):
        for c in range(5):
            val = image[r, c]
            txt_color = '#0F172A' if val == 255 else '#94A3B8'
            ax.text(c, r, f"({r},{c})", ha='center', va='center', fontsize=8, color=txt_color, fontweight='bold')

    # Right: Numerical matrix with dedicated colorbar
    ax2 = axes[1]
    ax2.set_facecolor('#F8FAFC')
    im2 = ax2.imshow(image, cmap='Blues', vmin=0, vmax=255)
    ax2.set_title('2. Масив значень у пам\'яті (uint8: 0–255)', fontsize=12, fontweight='bold', color='#0F172A', pad=14)
    ax2.set_xticks(range(5))
    ax2.set_yticks(range(5))
    ax2.set_xlabel('Координата X (стовпчик)', fontsize=10, color='#334155', labelpad=8)
    ax2.set_ylabel('Координата Y (рядок)', fontsize=10, color='#334155', labelpad=8)
    draw_cell_borders(ax2, 5, 5, color='#CBD5E1', linewidth=1.2)
    ax2.tick_params(colors='#475569')

    for r in range(5):
        for c in range(5):
            val = image[r, c]
            txt_color = '#FFFFFF' if val > 128 else '#0F172A'
            ax2.text(c, r, f"{val}", ha='center', va='center', fontsize=12, fontweight='bold', color=txt_color)

    # Colorbar on right without overlap
    fig.subplots_adjust(top=0.86, bottom=0.14, left=0.08, right=0.86, wspace=0.35)
    cax = fig.add_axes([0.89, 0.18, 0.025, 0.64])
    cbar = fig.colorbar(im2, cax=cax)
    cbar.set_label('Інтенсивність: 0 (чорний) → 255 (білий)', fontsize=9.5, color='#1E293B', labelpad=10)
    cbar.ax.tick_params(colors='#475569')

    fig.suptitle("Представлення чорно-білого зображення у пам'яті: форма (5, 5, 1)", 
                 fontsize=14, fontweight='bold', color='#0F172A', y=0.97)
    plt.savefig(os.path.join(OUT_DIR, "01.png"), dpi=300)
    plt.close()


# -----------------------------------------------------------------------------
# 2. 02.png: RGB representation with channel decomposition
# -----------------------------------------------------------------------------
def generate_02():
    print("Generating 02.png (real photo patch -> 3 channels)...")
    from sklearn.datasets import load_sample_image
    photo = load_sample_image("flower.jpg")
    r0, c0, n = 222, 444, 4
    patch = photo[r0:r0 + n, c0:c0 + n]

    fig = plt.figure(figsize=(16, 4.3), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    gs = fig.add_gridspec(1, 5, width_ratios=[2.0, 1.15, 1, 1, 1], wspace=0.18)

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(photo)
    ax0.add_patch(patches.Rectangle((c0 - 12, r0 - 12), 28, 28, fill=False, edgecolor='#F59E0B', linewidth=3))
    ax0.set_title(f"Фото: {photo.shape[0]}×{photo.shape[1]} пікселів\nТензор {photo.shape}", fontsize=11.5,
                  fontweight='bold', color='#0F172A', pad=10)
    ax0.set_xticks([]); ax0.set_yticks([])

    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(patch, interpolation='nearest')
    draw_cell_borders(ax1, n, n, color='#FFFFFF', linewidth=2.0)
    ax1.add_patch(patches.Rectangle((-0.5, -0.5), 1, 1, fill=False, edgecolor='#F59E0B', linewidth=4))
    ax1.set_title(f"Ділянка {n}×{n} (збільшено)\nТензор {patch.shape}", fontsize=11.5,
                  fontweight='bold', color='#0F172A', pad=10)
    ax1.set_xlabel("піксель (0, 0) = [%d, %d, %d]" % tuple(patch[0, 0]), fontsize=10.5, color='#B45309', fontweight='bold')
    ax1.set_xticks([]); ax1.set_yticks([])

    info = [("R: червоний", 0, 'Reds', '#DC2626'), ("G: зелений", 1, 'Greens', '#16A34A'), ("B: синій", 2, 'Blues', '#2563EB')]
    for k, (title, ch, cmap, col) in enumerate(info):
        ax = fig.add_subplot(gs[0, 2 + k])
        ax.imshow(patch[:, :, ch], cmap=cmap, vmin=0, vmax=255)
        draw_cell_borders(ax, n, n, color='#CBD5E1', linewidth=1.2)
        ax.add_patch(patches.Rectangle((-0.5, -0.5), 1, 1, fill=False, edgecolor='#F59E0B', linewidth=4))
        for r in range(n):
            for c in range(n):
                v = int(patch[r, c, ch])
                ax.text(c, r, str(v), ha='center', va='center', fontsize=12, fontweight='bold',
                        color='#FFFFFF' if v > 140 else '#0F172A')
        ax.set_title(f"{title}\nматриця {n}×{n}", fontsize=11, fontweight='bold', color=col, pad=10)
        ax.set_xticks([]); ax.set_yticks([])

    fig.suptitle("Кольорове фото — це три таблиці чисел (канали), складені в стос",
                 fontsize=13.5, fontweight='bold', color='#0F172A', y=1.04)
    plt.savefig(os.path.join(OUT_DIR, "02.png"), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


# -----------------------------------------------------------------------------
def generate_03():
    print("Generating 03.png (polished)...")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Panel 1: Number of input neurons
    ax1 = axes[0]
    ax1.set_facecolor('#F8FAFC')
    categories = ['MNIST\n(28×28×1)', 'ImageNet\n(224×224×3)']
    inputs = [784, 150528]
    colors = ['#3B82F6', '#EF4444']

    bars1 = ax1.bar(categories, inputs, color=colors, width=0.45, edgecolor='#0F172A', linewidth=1.2)
    ax1.set_title('1. Кількість вхідних пікселів (нейронів)', fontsize=12, fontweight='bold', color='#0F172A', pad=14)
    ax1.set_ylabel('Кількість нейронів у вхідному шарі', fontsize=10, color='#1E293B')
    ax1.set_yscale('log')
    ax1.set_ylim(100, 1.5e6)  # Generous headroom to prevent overlapping title
    ax1.grid(True, which='both', linestyle='--', alpha=0.4, color='#94A3B8')
    ax1.tick_params(colors='#334155')

    # Value callouts with bounding boxes
    ax1.text(0, 1600, "784 нейрони\n(базова форма)", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1D4ED8',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#3B82F6'))
    ax1.text(1, 280000, "150,528 нейронів\n(в 192 рази більше!)", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#B91C1C',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor='#EF4444'))

    # Panel 2: Number of weights in first hidden layer
    ax2 = axes[1]
    ax2.set_facecolor('#F8FAFC')
    categories2 = ['MNIST → Dense(128)\n784 × 128', 'ImageNet → Dense(512)\n150,528 × 512']
    weights = [100352, 77070336]
    bars2 = ax2.bar(categories2, weights, color=colors, width=0.45, edgecolor='#0F172A', linewidth=1.2)
    ax2.set_title('2. Кількість параметрів (ваг) 1-го прихованого шару', fontsize=12, fontweight='bold', color='#0F172A', pad=14)
    ax2.set_ylabel('Кількість вагових коефіцієнтів', fontsize=10, color='#1E293B')
    ax2.set_yscale('log')
    ax2.set_ylim(1e4, 1.2e9)  # Headroom
    ax2.grid(True, which='both', linestyle='--', alpha=0.4, color='#94A3B8')
    ax2.tick_params(colors='#334155')

    # Value callouts
    ax2.text(0, 220000, "100,352 параметрів\n(~0.4 МБ пам'яті)", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1D4ED8',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#3B82F6'))
    ax2.text(1, 150000000, "77,070,336 параметрів!\n(~294 МБ лише для 1 шару)", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#B91C1C',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor='#EF4444'))

    fig.suptitle("Катастрофічний вибух параметрів у Dense-мережах при зростанні роздільної здатності",
                 fontsize=13.5, fontweight='bold', color='#0F172A', y=0.97)
    fig.subplots_adjust(top=0.84, bottom=0.14, left=0.08, right=0.96, wspace=0.25)
    plt.savefig(os.path.join(OUT_DIR, "03.png"), dpi=300)
    plt.close()


# -----------------------------------------------------------------------------
# 4. 04.png: Spatial Locality
# -----------------------------------------------------------------------------
def generate_04():
    print("Generating 04.png (polished)...")
    np.random.seed(42)
    img_size = 64
    cat_img = np.full((img_size, img_size), 60, dtype=np.uint8)
    
    # Head circle
    yy, xx = np.ogrid[:img_size, :img_size]
    mask_head = ((xx - 32)**2 + (yy - 34)**2) < 22**2
    cat_img[mask_head] = 140

    # Left eye
    mask_eye_left = ((xx - 24)**2 + (yy - 26)**2) < 4**2
    cat_img[mask_eye_left] = 240
    # Pupil
    mask_pupil_left = ((xx - 24)**2 + (yy - 26)**2) < 2**2
    cat_img[mask_pupil_left] = 20

    # Right eye
    mask_eye_right = ((xx - 40)**2 + (yy - 26)**2) < 4**2
    cat_img[mask_eye_right] = 240
    mask_pupil_right = ((xx - 40)**2 + (yy - 26)**2) < 2**2
    cat_img[mask_pupil_right] = 20

    # Nose
    mask_nose = ((xx - 32)**2 + (yy - 37)**2) < 3**2
    cat_img[mask_nose] = 200

    # Noise
    noise = np.random.randint(-12, 12, (img_size, img_size))
    cat_img = np.clip(cat_img.astype(int) + noise, 0, 255).astype(np.uint8)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.3), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # 1. Full Image with bounding box
    ax1 = axes[0]
    ax1.imshow(cat_img, cmap='gray', vmin=0, vmax=255)
    ax1.set_title('1. Зображення 64×64\n(Двовимірний простір пікселів)', fontsize=11.5, fontweight='bold', color='#0F172A', pad=12)
    rect = patches.Rectangle((19.5, 21.5), 9, 9, linewidth=2.5, edgecolor='#EF4444', facecolor='none')
    ax1.add_patch(rect)
    ax1.text(24, 15, 'Локальний патерн\n(Око)', ha='center', fontsize=9.5, fontweight='bold', color='#DC2626',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEF2F2', edgecolor='#EF4444'))
    ax1.set_xticks([0, 20, 40, 60])
    ax1.set_yticks([0, 20, 40, 60])
    ax1.tick_params(colors='#475569')

    # 2. Zoomed patch
    ax2 = axes[1]
    patch_data = cat_img[22:31, 20:29]
    ax2.imshow(patch_data, cmap='gray', vmin=0, vmax=255)
    ax2.set_title('2. Збільшений фрагмент 9×9\nСусідні пікселі формують об\'єкт', fontsize=11.5, fontweight='bold', color='#0F172A', pad=12)
    ax2.set_xticks(range(9))
    ax2.set_yticks(range(9))
    draw_cell_borders(ax2, 9, 9, color='#EF4444', linewidth=0.8)
    ax2.tick_params(colors='#475569')

    for r in range(9):
        for c in range(9):
            val = patch_data[r, c]
            tc = '#FFFFFF' if val < 100 else '#0F172A'
            ax2.text(c, r, f"{val}", ha='center', va='center', fontsize=7.5, color=tc, fontweight='bold')

    # 3. Dense Flattening explanation
    ax3 = axes[2]
    ax3.set_facecolor('#F8FAFC')
    ax3.axis('off')
    ax3.set_title('3. Проблема Dense-мережі:\nРозрив просторової топології', fontsize=11.5, fontweight='bold', color='#0F172A', pad=12)

    msg_box = (
        "[!] РОЗГОРТАННЯ У ВЕКТОР (FLATTEN):\n\n"
        "• Піксель [25, 24] та піксель [25, 25]\n"
        "  у векторі сусіди: індекси 1624 та 1625.\n\n"
        "• АЛЕ вертикальний сусід [26, 24]\n"
        "  опиняється на відстані +64 позиції\n"
        "  (індекс 1688)!\n\n"
        "• Для Dense-мережі пікселі — це просто\n"
        "  ізольовані некорельовані змінні.\n"
        "  Мережа втрачає 2D геометрію зображення."
    )
    ax3.text(0.08, 0.5, msg_box, fontsize=10, color='#0F172A', va='center', ha='left',
             linespacing=1.6,
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#F1F5F9', edgecolor='#94A3B8', linewidth=1.2))

    fig.suptitle("Локальність ознак (Spatial Locality): інформація закодована у групах сусідніх пікселів",
                 fontsize=13.5, fontweight='bold', color='#0F172A', y=0.97)
    fig.subplots_adjust(top=0.84, bottom=0.12, left=0.06, right=0.96, wspace=0.25)
    plt.savefig(os.path.join(OUT_DIR, "04.png"), dpi=300)
    plt.close()


# -----------------------------------------------------------------------------
# 5. 05.png: Translation invariance problem
# -----------------------------------------------------------------------------
def generate_05():
    print("Generating 05.png (real digit 3 shifted by 5 px)...")
    data = np.load("temp/mnist.npz")
    img = data["x_train"][12]
    assert data["y_train"][12] == 3
    shifted = np.roll(img, 5, axis=1)
    a, b = img > 128, shifted > 128
    both, only_a, only_b = a & b, a & ~b, ~a & b

    overlap = np.zeros(img.shape + (3,))
    overlap[only_a] = (0.23, 0.51, 0.96)   # blue: only original
    overlap[only_b] = (0.98, 0.45, 0.09)   # orange: only shifted
    overlap[both] = (0.06, 0.73, 0.51)     # green: same index in both

    fig = plt.figure(figsize=(15, 7.2))
    gs = fig.add_gridspec(2, 3, height_ratios=[4.4, 1.6], hspace=0.75, wspace=0.12)
    titles = ["Цифра «3» по центру", "Та сама «3», зсунута на 5 пікселів вправо",
              "Де яскраві пікселі збігаються"]
    for k, (m, t) in enumerate(zip([img, shifted, None], titles)):
        ax = fig.add_subplot(gs[0, k])
        if m is not None:
            ax.imshow(m, cmap='gray', vmin=0, vmax=255)
        else:
            ax.imshow(overlap)
        ax.set_title(t, fontsize=12, fontweight='bold', color='#0F172A', pad=8)
        ax.set_xticks([]); ax.set_yticks([])
    axs = fig.axes
    axs[2].set_xlabel(f"збіг: {both.sum()} із {a.sum()} яскравих пікселів ({both.sum() / a.sum() * 100:.0f}%)",
                      fontsize=11, color='#0F172A', fontweight='bold')
    from matplotlib.lines import Line2D
    axs[2].legend(handles=[Line2D([0], [0], marker='s', color='w', markerfacecolor=c, markersize=11, label=l)
                           for c, l in [('#10B981', 'яскравий в обох'), ('#3B82F6', 'лише в оригіналі'), ('#F97316', 'лише в зсунутому')]],
                  loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=3, fontsize=8.5, frameon=False, columnspacing=1.0, handletextpad=0.3)

    for k, (m, t) in enumerate([(img, "Вектор оригіналу (784 числа)"), (shifted, "Вектор зсунутої цифри (784 числа)")]):
        ax = fig.add_subplot(gs[1, k])
        ax.imshow(m.reshape(1, -1), cmap='gray', aspect='auto', vmin=0, vmax=255, interpolation='nearest')
        ax.set_title(t, fontsize=10.5, color='#475569', pad=4)
        ax.set_yticks([]); ax.set_xticks([0, 392, 783]); ax.set_xticklabels(["0", "392", "783"], fontsize=9)
    ax = fig.add_subplot(gs[1, 2])
    diff = (img.flatten() != shifted.flatten()).astype(float)
    ax.imshow(diff.reshape(1, -1), cmap='Reds', aspect='auto', vmin=0, vmax=1, interpolation='nearest')
    ax.set_title(f"Позиції вектора, де значення змінилось: {int(diff.sum())} із 784", fontsize=10.5, color='#B91C1C', pad=4)
    ax.set_yticks([]); ax.set_xticks([0, 392, 783]); ax.set_xticklabels(["0", "392", "783"], fontsize=9)

    fig.suptitle("Для Dense-шару зсунута цифра — майже інший вхід", fontsize=14, fontweight='bold', color='#0F172A', y=0.99)
    plt.savefig(os.path.join(OUT_DIR, "05.png"), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


# -----------------------------------------------------------------------------
def generate_06():
    print("Generating 06.png (polished)...")
    fig, ax = plt.subplots(figsize=(14, 5.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    stages = [
        {
            'title': 'Рівень 1: Низькорівневі ознаки\n(Ранні згорткові шари)',
            'desc': 'Виявлення елементарних патернів:\n• Горизонтальні та вертикальні краї\n• Кути, лінії, контрасти яскравості\n• Колірні градієнти',
            'example': 'Фокус: Фільтри 3×3, 5×5 (Собель тощо)',
            'bg': '#EFF6FF',
            'border': '#3B82F6',
            'x': 0.05,
            'w': 0.26
        },
        {
            'title': 'Рівень 2: Середньорівневі ознаки\n(Проміжні згорткові шари)',
            'desc': 'Комбінація країв у структури:\n• Текстури (хутро, сітка, дерево)\n• Геометричні фігури (кола, овали)\n• Окремі деталі (око, ніс, вухо, колесо)',
            'example': 'Фокус: Збільшене рецептивне поле',
            'bg': '#FEF3C7',
            'border': '#F59E0B',
            'x': 0.37,
            'w': 0.26
        },
        {
            'title': 'Рівень 3: Високорівневі ознаки\n(Глибокі згорткові шари)',
            'desc': 'Семантичні цілісні образи:\n• Силуети тварин (кіт, собака)\n• Транспортні засоби (автомобіль)\n• Обличчя, складні об\'єкти сцени',
            'example': 'Фокус: Класифікація об\'єкта в цілому',
            'bg': '#ECFDF5',
            'border': '#10B981',
            'x': 0.69,
            'w': 0.26
        }
    ]

    for stage in stages:
        rect = patches.FancyBboxPatch(
            (stage['x'], 0.12), stage['w'], 0.74,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=stage['bg'],
            edgecolor=stage['border'],
            linewidth=2.0
        )
        ax.add_patch(rect)

        cx = stage['x'] + stage['w'] / 2
        ax.text(cx, 0.76, stage['title'], ha='center', va='center',
                fontsize=11, fontweight='bold', color='#0F172A')

        ax.plot([stage['x'] + 0.02, stage['x'] + stage['w'] - 0.02], [0.68, 0.68],
                color=stage['border'], linewidth=1.2, linestyle='--')

        ax.text(stage['x'] + 0.02, 0.46, stage['desc'], ha='left', va='center',
                fontsize=9.5, color='#1E293B', linespacing=1.6)

        ax.text(cx, 0.20, stage['example'], ha='center', va='center',
                fontsize=9, fontweight='bold', color=stage['border'],
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFFFFF', edgecolor=stage['border'], linewidth=1))

    # Clean arrows between stages
    ax.annotate('', xy=(0.36, 0.49), xytext=(0.32, 0.49),
                arrowprops=dict(facecolor='#0F172A', edgecolor='#0F172A', width=2.5, headwidth=9, headlength=9))
    ax.annotate('', xy=(0.68, 0.49), xytext=(0.64, 0.49),
                arrowprops=dict(facecolor='#0F172A', edgecolor='#0F172A', width=2.5, headwidth=9, headlength=9))

    ax.text(0.34, 0.54, 'Згортка +\nПулінг', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#475569')
    ax.text(0.66, 0.54, 'Згортка +\nПулінг', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#475569')

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.axis('off')

    fig.suptitle("Ієрархічне представлення ознак у CNN: від простих країв до цілісних об'єктів",
                 fontsize=14, fontweight='bold', color='#0F172A', y=0.96)
    fig.subplots_adjust(top=0.88, bottom=0.08, left=0.04, right=0.96)
    plt.savefig(os.path.join(OUT_DIR, "06.png"), dpi=300)
    plt.close()

if __name__ == '__main__':
    generate_01()
    generate_02()
    generate_03()
    generate_04()
    generate_05()
    generate_06()
    print("All intro CV images regenerated successfully in:", OUT_DIR)
