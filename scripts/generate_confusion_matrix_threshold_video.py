import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import subprocess

# Set font and style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

# -----------------------------------------------------------------------------
# Synthetic Dataset for 100 samples (60 negatives, 40 positives)
# -----------------------------------------------------------------------------
np.random.seed(42)
n_neg = 60
n_pos = 40

# Beta distributions for probabilities
probs_neg = np.random.beta(2.5, 6.0, n_neg)  # peak around 0.25
probs_pos = np.random.beta(6.0, 2.8, n_pos)  # peak around 0.70

all_probs = np.concatenate([probs_neg, probs_pos])
y_true = np.concatenate([np.zeros(n_neg, dtype=int), np.ones(n_pos, dtype=int)])

# Threshold sweep: 0.10 -> 0.50 -> 0.90 -> 0.50 (90 frames)
t_seq = np.concatenate([
    np.full(10, 0.12),
    np.linspace(0.12, 0.50, 25),
    np.full(10, 0.50),
    np.linspace(0.50, 0.88, 25),
    np.full(10, 0.88),
    np.linspace(0.88, 0.50, 15)
])
n_frames = len(t_seq)

fig = plt.figure(figsize=(15, 6.2), dpi=100)
fig.patch.set_facecolor('#F8FAFC')

gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.0])
ax_dist = fig.add_subplot(gs[0])
ax_matrix = fig.add_subplot(gs[1])

# Left Subplot: Distributions & Moving Threshold
ax_dist.set_facecolor('#FFFFFF')
ax_dist.set_xlim(-0.02, 1.02)
ax_dist.set_ylim(-1, 28)
ax_dist.set_xlabel('Передбачена ймовірність P(клас 1)', fontsize=11, fontweight='bold', color='#1E293B')
ax_dist.set_ylabel('Кількість спостережень (пацієнтів)', fontsize=11, fontweight='bold', color='#1E293B')
ax_dist.set_title('Розподіл ймовірностей та пороговий зріз', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
ax_dist.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

bins = np.linspace(0, 1, 25)
hist_neg, _ = np.histogram(probs_neg, bins=bins)
hist_pos, _ = np.histogram(probs_pos, bins=bins)
bin_centers = 0.5 * (bins[:-1] + bins[1:])

# Static plot outlines
ax_dist.bar(bin_centers, hist_neg, width=0.038, alpha=0.4, color='#3B82F6', label='Клас 0 (60 здорових)', edgecolor='#1D4ED8')
ax_dist.bar(bin_centers, hist_pos, width=0.038, alpha=0.4, color='#EF4444', label='Клас 1 (40 хворих)', edgecolor='#B91C1C')

thresh_line = ax_dist.axvline(0.5, color='#0F172A', linestyle='--', linewidth=3.0, label='Поріг T')
thresh_badge = ax_dist.text(0.5, 25, 'T = 0.50', ha='center', va='bottom', fontsize=11, fontweight='bold',
                            color='#FFFFFF', bbox=dict(boxstyle='round,pad=0.4', facecolor='#0F172A', edgecolor='#0F172A'))

ax_dist.legend(loc='upper right', fontsize=9, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

fig.suptitle('ДИНАМІКА CONFUSION MATRIX ТА МЕТРИК ПРИ ЗМІНІ ПОРОГУ',
             fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)

def init():
    return [thresh_line, thresh_badge]

def update(frame):
    t = t_seq[frame]
    
    # Update threshold line on dist plot
    thresh_line.set_xdata([t, t])
    thresh_badge.set_position((t, 24.5))
    thresh_badge.set_text(f'T = {t:.2f}')
    
    # Calculate confusion matrix components
    y_pred = (all_probs >= t).astype(int)
    
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    
    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Right subplot: Clear and redraw Confusion Matrix + Bars
    ax_matrix.clear()
    ax_matrix.set_facecolor('#FFFFFF')
    ax_matrix.axis('off')
    
    # Mode interpretation
    if t < 0.35:
        mode_header = "РЕЖИМ ВИСОКОГО RECALL (ОНКОСКРИНІНГ / FRAUD)"
        mode_bg = "#FEF3C7"
        mode_border = "#F59E0B"
        note = "Мінімум пропущених хворих (FN -> 0), але багато хибних тривог (FP)."
    elif t > 0.65:
        mode_header = "РЕЖИМ ВИСОКОГО PRECISION (СПАМ-ФІЛЬТР / БАНИ)"
        mode_bg = "#EDE9FE"
        mode_border = "#8B5CF6"
        note = "Жодних невинних звинувачень (FP -> 0), але пропускаємо частину цілей (FN)."
    else:
        mode_header = "СТАНДАРТНИЙ БАЛАНС (T = 0.50)"
        mode_bg = "#DCFCE7"
        mode_border = "#16A34A"
        note = "Рівноправний компроміс між помилками I роду (FP) та II роду (FN)."
        
    # Draw 2x2 grid in normalized coords [0.05, 0.45] width, [0.45, 0.85] height
    # TN box
    ax_matrix.add_patch(mpatches.Rectangle((0.05, 0.65), 0.42, 0.20, facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=2.0))
    ax_matrix.text(0.26, 0.77, f"TN = {tn}", ha='center', va='center', fontsize=15, fontweight='bold', color='#15803D')
    ax_matrix.text(0.26, 0.69, "Істинно Негативні", ha='center', va='center', fontsize=9.5, color='#1E293B')
    
    # FP box
    ax_matrix.add_patch(mpatches.Rectangle((0.53, 0.65), 0.42, 0.20, facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=2.0))
    ax_matrix.text(0.74, 0.77, f"FP = {fp}", ha='center', va='center', fontsize=15, fontweight='bold', color='#B91C1C')
    ax_matrix.text(0.74, 0.69, "Помилка I роду (Хибна тривога)", ha='center', va='center', fontsize=9.0, color='#1E293B')
    
    # FN box
    ax_matrix.add_patch(mpatches.Rectangle((0.05, 0.40), 0.42, 0.20, facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=2.0))
    ax_matrix.text(0.26, 0.52, f"FN = {fn}", ha='center', va='center', fontsize=15, fontweight='bold', color='#B91C1C')
    ax_matrix.text(0.26, 0.44, "Помилка II роду (Пропуск цілі)", ha='center', va='center', fontsize=9.0, color='#1E293B')
    
    # TP box
    ax_matrix.add_patch(mpatches.Rectangle((0.53, 0.40), 0.42, 0.20, facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=2.0))
    ax_matrix.text(0.74, 0.52, f"TP = {tp}", ha='center', va='center', fontsize=15, fontweight='bold', color='#15803D')
    ax_matrix.text(0.74, 0.44, "Істинно Позитивні", ha='center', va='center', fontsize=9.5, color='#1E293B')
    
    # Headers
    ax_matrix.text(0.26, 0.88, "Прогноз: 0", ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')
    ax_matrix.text(0.74, 0.88, "Прогноз: 1", ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')
    ax_matrix.text(0.01, 0.75, "Факт: 0", ha='right', va='center', fontsize=10.5, fontweight='bold', color='#0F172A')
    ax_matrix.text(0.01, 0.50, "Факт: 1", ha='right', va='center', fontsize=10.5, fontweight='bold', color='#0F172A')
    
    # Metrics Text & ASCII Progress Bars
    metrics_str = (
        f"{mode_header}\n"
        f"---------------------------------------------------\n"
        f"• Accuracy    : {accuracy*100:5.1f}%   [{'█'*int(accuracy*14)}{'░'*(14-int(accuracy*14))}]\n"
        f"• Precision   : {precision*100:5.1f}%   [{'█'*int(precision*14)}{'░'*(14-int(precision*14))}]\n"
        f"• Recall (TPR): {recall*100:5.1f}%   [{'█'*int(recall*14)}{'░'*(14-int(recall*14))}]\n"
        f"• Specificity : {specificity*100:5.1f}%   [{'█'*int(specificity*14)}{'░'*(14-int(specificity*14))}]\n"
        f"• F1-Score    : {f1*100:5.1f}%   [{'█'*int(f1*14)}{'░'*(14-int(f1*14))}]\n\n"
        f"💡 {note}"
    )
    
    ax_matrix.text(0.04, 0.35, metrics_str, transform=ax_matrix.transAxes, fontsize=10.0,
                   verticalalignment='top', fontfamily='DejaVu Sans',
                   bbox=dict(boxstyle='round,pad=0.7', facecolor=mode_bg, edgecolor=mode_border, alpha=0.9))
    
    return [thresh_line, thresh_badge]

ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=90)

out_dir = 'public/videos/ai-python/logistic-regression-classification/classification-metrics'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'confusion_matrix_threshold_dynamics.mp4')
output_webm = os.path.join(out_dir, 'confusion_matrix_threshold_dynamics.webm')
output_gif = os.path.join(out_dir, 'confusion_matrix_threshold_dynamics.gif')
poster_png = os.path.join(out_dir, 'confusion_matrix_threshold_dynamics_poster.png')

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

print("Відео confusion_matrix_threshold_dynamics успішно завершено!")
