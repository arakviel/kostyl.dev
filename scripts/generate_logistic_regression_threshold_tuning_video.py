import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.linear_model import LogisticRegression
import subprocess

# Set font and style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

# -----------------------------------------------------------------------------
# Synthetic Exam Dataset (Exam 1 vs Exam 2, 2 classes)
# -----------------------------------------------------------------------------
np.random.seed(42)
n_samples = 40

# Class 0: Not admitted (lower scores)
x1_c0 = np.random.normal(45, 10, n_samples)
x2_c0 = np.random.normal(55, 10, n_samples)
y_c0 = np.zeros(n_samples, dtype=int)

# Class 1: Admitted (higher scores)
x1_c1 = np.random.normal(70, 9, n_samples)
x2_c1 = np.random.normal(80, 9, n_samples)
y_c1 = np.ones(n_samples, dtype=int)

X = np.vstack([np.column_stack([x1_c0, x2_c0]), np.column_stack([x1_c1, x2_c1])])
y = np.concatenate([y_c0, y_c1])

# Fit logistic regression
model = LogisticRegression(solver='lbfgs', C=1.0)
model.fit(X, y)
w1, w2 = model.coef_[0]
b = model.intercept_[0]

# Precompute probabilities for all samples
probs = model.predict_proba(X)[:, 1]

# Evaluation grid for 2D probability surface
xx, yy = np.meshgrid(np.linspace(20, 95, 200), np.linspace(30, 105, 200))
grid_points = np.c_[xx.ravel(), yy.ravel()]
zz = model.predict_proba(grid_points)[:, 1].reshape(xx.shape)

# Threshold schedule: 90 frames
# Sweeps: 0.15 -> 0.50 -> 0.85 -> 0.50
t_seq = np.concatenate([
    np.full(10, 0.15),
    np.linspace(0.15, 0.50, 25),
    np.full(10, 0.50),
    np.linspace(0.50, 0.85, 25),
    np.full(10, 0.85),
    np.linspace(0.85, 0.50, 15)
])
n_frames = len(t_seq)

fig = plt.figure(figsize=(15, 6.2), dpi=100)
fig.patch.set_facecolor('#F8FAFC')

gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 0.9])
ax_scatter = fig.add_subplot(gs[0])
ax_metrics = fig.add_subplot(gs[1])

# Left subplot: 2D feature plane
ax_scatter.set_facecolor('#FFFFFF')
ax_scatter.set_xlim(22, 93)
ax_scatter.set_ylim(32, 103)
ax_scatter.set_xlabel('Іспит 1 (бали)', fontsize=11, fontweight='bold', color='#1E293B')
ax_scatter.set_ylabel('Іспит 2 (бали)', fontsize=11, fontweight='bold', color='#1E293B')
ax_scatter.set_title('Простір ознак та динамічна межа при зміні порогу', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
ax_scatter.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

# Static background contours of probability
contour = ax_scatter.contourf(xx, yy, zz, levels=np.linspace(0, 1, 21), cmap='RdYlGn', alpha=0.25)
cbar = fig.colorbar(contour, ax=ax_scatter, fraction=0.046, pad=0.04)
cbar.set_label('Ймовірність P(y=1)', fontsize=9.5, color='#1E293B')

# Base points
sc_c0 = ax_scatter.scatter(X[y == 0, 0], X[y == 0, 1], color='#EF4444', s=60, edgecolors='#1E293B', linewidths=1.0, label='Справжній Клас 0 (Не вступив)')
sc_c1 = ax_scatter.scatter(X[y == 1, 0], X[y == 1, 1], color='#10B981', s=60, edgecolors='#1E293B', linewidths=1.0, label='Справжній Клас 1 (Вступив)')

# Dynamic decision boundary line
line_bound, = ax_scatter.plot([], [], color='#1E293B', linestyle='--', linewidth=3.0, label='Межа рішення (P = Поріг)')
ax_scatter.legend(loc='lower right', fontsize=8.5, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

fig.suptitle('НАЛАШТУВАННЯ ПОРОГУ РІШЕННЯ: БАЛАНС ТОЧНОСТІ ТА ПОВНОТИ',
             fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)

def init():
    line_bound.set_data([], [])
    return [line_bound]

def update(frame):
    threshold = t_seq[frame]
    
    # Boundary equation: w1 * x1 + w2 * x2 + b = logit(threshold)
    logit_t = np.log(threshold / (1.0 - threshold))
    
    # x2 as a function of x1: x2 = (logit_t - b - w1 * x1) / w2
    x1_line = np.linspace(20, 95, 100)
    x2_line = (logit_t - b - w1 * x1_line) / w2
    line_bound.set_data(x1_line, x2_line)
    
    # Classification decisions at current threshold
    y_pred = (probs >= threshold).astype(int)
    
    tp = int(np.sum((y == 1) & (y_pred == 1)))
    fp = int(np.sum((y == 0) & (y_pred == 1)))
    tn = int(np.sum((y == 0) & (y_pred == 0)))
    fn = int(np.sum((y == 1) & (y_pred == 0)))
    
    accuracy = (tp + tn) / len(y)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Context message based on threshold
    if threshold < 0.35:
        mode_title = "НИЗЬКИЙ ПОРІГ (T < 0.35): РЕЖИМ ЧУТЛИВОСТІ"
        badge_bg = "#FEF3C7"
        badge_border = "#F59E0B"
        biz_context = (
            "• Мета: не пропустити жодного позитивного випадку (High Recall).\n"
            "• Приклад: скринінг важких хвороб або виявлення шахрайства.\n"
            "• Наслідок: Recall близький до 100%, але зростає кількість хибних тривог (FP)."
        )
    elif threshold > 0.65:
        mode_title = "ВИСОКИЙ ПОРІГ (T > 0.65): КОНСЕРВАТИВНИЙ РЕЖИМ"
        badge_bg = "#EDE9FE"
        badge_border = "#8B5CF6"
        biz_context = (
            "• Мета: абсолютна впевненість перед дією (High Precision).\n"
            "• Приклад: блокування акаунтів, спам-фільтр, автоматичне списання коштів.\n"
            "• Наслідок: Precision максимальний, але частина позитивних об'єктів втрачається (FN)."
        )
    else:
        mode_title = "СТАНДАРТНИЙ ПОРІГ (T = 0.50): СИМЕТРИЧНИЙ БАЛАНС"
        badge_bg = "#DCFCE7"
        badge_border = "#22C55E"
        biz_context = (
            "• Мета: рівноправний компроміс між помилками I та II роду.\n"
            "• Стандартне налаштування scikit-learn за замовчуванням.\n"
            "• Оптимально, коли витрати від FP та FN приблизно однакові."
        )
        
    ax_metrics.clear()
    ax_metrics.axis('off')
    
    metrics_report = (
        f"{mode_title}\n"
        f"---------------------------------------------------\n"
        f"ПОТОЧНИЙ ПОРІГ КЛАСИФІКАЦІЇ:  T = {threshold:.2f}\n"
        f"Правило: Прогноз = 1, якщо P(y=1) >= {threshold:.2f}\n\n"
        f"МАТРИЦЯ ПОМИЛОК (CONFUSION MATRIX):\n"
        f"  • True Positives  (TP) : {tp:2d}   (Вгадали клас 1)\n"
        f"  • False Positives (FP) : {fp:2d}   (Хибна тривога)\n"
        f"  • True Negatives  (TN) : {tn:2d}   (Вгадали клас 0)\n"
        f"  • False Negatives (FN) : {fn:2d}   (Пропущений клас 1)\n\n"
        f"КЛЮЧОВІ МЕТРИКИ:\n"
        f"  • Accuracy  : {accuracy*100:5.1f}%   [{'█'*int(accuracy*15)}{'░'*(15-int(accuracy*15))}]\n"
        f"  • Precision : {precision*100:5.1f}%   [{'█'*int(precision*15)}{'░'*(15-int(precision*15))}]\n"
        f"  • Recall    : {recall*100:5.1f}%   [{'█'*int(recall*15)}{'░'*(15-int(recall*15))}]\n"
        f"  • F1-Score  : {f1*100:5.1f}%   [{'█'*int(f1*15)}{'░'*(15-int(f1*15))}]\n\n"
        f"БІЗНЕС-СЕНС НАЛАШТУВАННЯ:\n"
        f"{biz_context}"
    )
    
    ax_metrics.text(0.04, 0.95, metrics_report, transform=ax_metrics.transAxes, fontsize=10.0,
                    verticalalignment='top', fontfamily='DejaVu Sans',
                    bbox=dict(boxstyle='round,pad=0.8', facecolor=badge_bg, edgecolor=badge_border, alpha=0.9))
    
    return [line_bound]

ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=90)

out_dir = 'public/videos/ai-python/logistic-regression-classification/classification-basics'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'logistic_regression_threshold_tuning.mp4')
output_webm = os.path.join(out_dir, 'logistic_regression_threshold_tuning.webm')
output_gif = os.path.join(out_dir, 'logistic_regression_threshold_tuning.gif')
poster_png = os.path.join(out_dir, 'logistic_regression_threshold_tuning_poster.png')

print("Збереження MP4 через ffmpeg...")
ani.save(output_mp4, writer='ffmpeg', fps=12, dpi=110,
         extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-crf', '18'])
print("MP4 успішно створено:", output_mp4)

print("Генерація WebM...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-c:v', 'libvpx-vp9', '-b:v', '1.2M', output_webm], check=True)

print("Генерація GIF...")
subprocess.run(['ffmpeg', '-y', '-i', output_mp4, '-vf', 'fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', output_gif], check=True)

print("Генерація постерного кадру (poster.png)...")
subprocess.run(['ffmpeg', '-y', '-ss', '00:00:03', '-i', output_mp4, '-vframes', '1', poster_png], check=True)

print("Відео logistic_regression_threshold_tuning успішно завершено!")
