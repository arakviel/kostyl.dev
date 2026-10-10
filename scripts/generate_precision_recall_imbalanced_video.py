import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
import subprocess

# Set font and style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

# -----------------------------------------------------------------------------
# Highly Imbalanced Dataset: 950 negatives (95%) and 50 positives (5%)
# -----------------------------------------------------------------------------
np.random.seed(42)
n_neg = 950
n_pos = 50

probs_neg = np.random.beta(1.8, 8.0, n_neg)  # clustered near 0
probs_pos = np.random.beta(4.0, 3.0, n_pos)  # spread across 0.3 - 0.9

all_probs = np.concatenate([probs_neg, probs_pos])
y_true = np.concatenate([np.zeros(n_neg), np.ones(n_pos)])

# Compute full curves
fpr_full, tpr_full, roc_thresh = roc_curve(y_true, all_probs)
roc_auc = roc_auc_score(y_true, all_probs)

prec_full, rec_full, pr_thresh = precision_recall_curve(y_true, all_probs)
avg_prec = average_precision_score(y_true, all_probs)

# Threshold sweep from 0.95 down to 0.05 (85 frames)
t_sweep = np.concatenate([
    np.full(10, 0.90),
    np.linspace(0.90, 0.08, 60),
    np.full(15, 0.08)
])
n_frames = len(t_sweep)

fig, (ax_roc, ax_pr) = plt.subplots(1, 2, figsize=(15, 6.2), dpi=100)
fig.patch.set_facecolor('#F8FAFC')

# Subplot 1: ROC Curve
ax_roc.set_facecolor('#FFFFFF')
ax_roc.set_xlim(-0.02, 1.02)
ax_roc.set_ylim(-0.02, 1.02)
ax_roc.set_xlabel('False Positive Rate (FPR)', fontsize=11, fontweight='bold', color='#1E293B')
ax_roc.set_ylabel('True Positive Rate (Recall / TPR)', fontsize=11, fontweight='bold', color='#1E293B')
ax_roc.set_title(f'1. ROC-крива: Оманливий оптимізм (AUC = {roc_auc:.3f})', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
ax_roc.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

ax_roc.plot(fpr_full, tpr_full, color='#94A3B8', linestyle=':', linewidth=1.5, alpha=0.7)
ax_roc.plot([0, 1], [0, 1], 'k--', linewidth=1.5, alpha=0.5, label='Baseline (0.50)')
line_roc, = ax_roc.plot([], [], color='#2563EB', linewidth=3.2, label=f'ROC (AUC = {roc_auc:.3f})')
dot_roc, = ax_roc.plot([], [], marker='o', markersize=10, color='#DC2626', zorder=5)
badge_roc = ax_roc.text(0.35, 0.15, '', fontsize=9.8,
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='#EFF6FF', edgecolor='#93C5FD', alpha=0.95))
ax_roc.legend(loc='lower right', fontsize=9, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

# Subplot 2: Precision-Recall Curve
ax_pr.set_facecolor('#FFFFFF')
ax_pr.set_xlim(-0.02, 1.02)
ax_pr.set_ylim(-0.02, 1.02)
ax_pr.set_xlabel('Recall (Повнота)', fontsize=11, fontweight='bold', color='#1E293B')
ax_pr.set_ylabel('Precision (Точність)', fontsize=11, fontweight='bold', color='#1E293B')
ax_pr.set_title(f'2. PR-крива: Сувора реальність на меншості (AP = {avg_prec:.3f})', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
ax_pr.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

baseline_pr = n_pos / (n_neg + n_pos)
ax_pr.axhline(baseline_pr, color='#EF4444', linestyle='--', linewidth=1.8, label=f'Baseline (Частка класу 1 = {baseline_pr:.1%})')
ax_pr.plot(rec_full, prec_full, color='#94A3B8', linestyle=':', linewidth=1.5, alpha=0.7)
line_pr, = ax_pr.plot([], [], color='#F59E0B', linewidth=3.2, label=f'PR-крива (AP = {avg_prec:.3f})')
dot_pr, = ax_pr.plot([], [], marker='o', markersize=10, color='#DC2626', zorder=5)
badge_pr = ax_pr.text(0.05, 0.15, '', fontsize=9.8,
                      bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFBEB', edgecolor='#FCD34D', alpha=0.95))
ax_pr.legend(loc='upper right', fontsize=9, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

fig.suptitle('НЕЗБАЛАНСОВАНІ ДАНІ (95% ПРОТИ 5%): ROC-AUC ПРОТИ PR-AUC',
             fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)

def init():
    line_roc.set_data([], [])
    dot_roc.set_data([], [])
    line_pr.set_data([], [])
    dot_pr.set_data([], [])
    badge_roc.set_text('')
    badge_pr.set_text('')
    return [line_roc, dot_roc, line_pr, dot_pr, badge_roc, badge_pr]

def update(frame):
    t = t_sweep[frame]
    
    # Calculate live confusion matrix counts
    y_pred = (all_probs >= t).astype(int)
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tpr
    
    # Trace curves up to current threshold
    mask_roc = roc_thresh >= t
    line_roc.set_data(fpr_full[mask_roc], tpr_full[mask_roc])
    dot_roc.set_data([fpr], [tpr])
    
    mask_pr = np.append(pr_thresh >= t, True)
    if len(mask_pr) == len(rec_full):
        line_pr.set_data(rec_full[mask_pr], prec_full[mask_pr])
    dot_pr.set_data([recall], [precision])
    
    badge_roc.set_text(
        f"ПОРІГ: T = {t:.2f}\n"
        f"• FP = {fp} з 950 здорових\n"
        f"• FPR = {fpr*100:4.1f}% (виглядає малим!)\n"
        f"• TPR = {tpr*100:4.1f}%\n"
        f"Чому оптимістично: TN = {tn} маскує помилки FP"
    )
    
    badge_pr.set_text(
        f"ПОРІГ: T = {t:.2f}\n"
        f"• TP = {tp} (знайдені цілі)\n"
        f"• FP = {fp} (хибні тривоги)\n"
        f"• Precision = {precision*100:4.1f}%\n"
        f"• Recall = {recall*100:4.1f}%\n"
        f"Чому суворо: FP відразу обвалює точність!"
    )
    
    return [line_roc, dot_roc, line_pr, dot_pr, badge_roc, badge_pr]

ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=90)

out_dir = 'public/videos/ai-python/logistic-regression-classification/classification-metrics'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'precision_recall_imbalanced_dynamics.mp4')
output_webm = os.path.join(out_dir, 'precision_recall_imbalanced_dynamics.webm')
output_gif = os.path.join(out_dir, 'precision_recall_imbalanced_dynamics.gif')
poster_png = os.path.join(out_dir, 'precision_recall_imbalanced_dynamics_poster.png')

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

print("Відео precision_recall_imbalanced_dynamics успішно завершено!")
