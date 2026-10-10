import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.metrics import roc_curve, roc_auc_score
import subprocess

# Set font and style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

# -----------------------------------------------------------------------------
# Generate synthetic dataset for smooth ROC curve
# -----------------------------------------------------------------------------
np.random.seed(42)
n_samples = 400
probs_0 = np.random.normal(0.32, 0.14, n_samples)
probs_1 = np.random.normal(0.68, 0.14, n_samples)

probs_0 = np.clip(probs_0, 0.01, 0.99)
probs_1 = np.clip(probs_1, 0.01, 0.99)

all_probs = np.concatenate([probs_0, probs_1])
y_true = np.concatenate([np.zeros(n_samples), np.ones(n_samples)])

# Compute full true ROC curve
fpr_full, tpr_full, thresholds_full = roc_curve(y_true, all_probs)
auc_val = roc_auc_score(y_true, all_probs)

# Threshold sweep from 1.0 down to 0.0 in 90 frames
# frames: 0..8 start at 1.0, 9..75 sweeps 1.0 -> 0.0, 76..90 pause at 0.0
sweep_thresholds = np.concatenate([
    np.full(10, 0.99),
    np.linspace(0.99, 0.01, 65),
    np.full(15, 0.01)
])
n_frames = len(sweep_thresholds)

fig = plt.figure(figsize=(15, 6.2), dpi=100)
fig.patch.set_facecolor('#F8FAFC')

gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.0])
ax_dist = fig.add_subplot(gs[0])
ax_roc = fig.add_subplot(gs[1])

# Left subplot: Distributions
ax_dist.set_facecolor('#FFFFFF')
ax_dist.set_xlim(-0.02, 1.02)
ax_dist.set_ylim(0, 3.8)
ax_dist.set_xlabel('Передбачена ймовірність P(y=1)', fontsize=11, fontweight='bold', color='#1E293B')
ax_dist.set_ylabel('Щільність імовірності', fontsize=11, fontweight='bold', color='#1E293B')
ax_dist.set_title('1. Розподіл класів та рухомий поріг зрізу T', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
ax_dist.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

# Plot normal distribution curves
x_grid = np.linspace(0, 1, 300)
from scipy.stats import norm
pdf_0 = norm.pdf(x_grid, 0.32, 0.14)
pdf_1 = norm.pdf(x_grid, 0.68, 0.14)

ax_dist.plot(x_grid, pdf_0, color='#2563EB', linewidth=2.5, label='Клас 0 (Здорові)')
ax_dist.fill_between(x_grid, pdf_0, color='#3B82F6', alpha=0.25)
ax_dist.plot(x_grid, pdf_1, color='#DC2626', linewidth=2.5, label='Клас 1 (Хворі)')
ax_dist.fill_between(x_grid, pdf_1, color='#EF4444', alpha=0.25)

t_line = ax_dist.axvline(0.99, color='#0F172A', linestyle='--', linewidth=2.8, label='Поріг T')
badge_t = ax_dist.text(0.99, 3.4, 'T = 0.99', ha='center', va='bottom', fontsize=10.5, fontweight='bold',
                       color='#FFFFFF', bbox=dict(boxstyle='round,pad=0.3', facecolor='#0F172A', edgecolor='#0F172A'))

ax_dist.legend(loc='upper center', fontsize=9, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

# Right subplot: ROC Space
ax_roc.set_facecolor('#FFFFFF')
ax_roc.set_xlim(-0.02, 1.02)
ax_roc.set_ylim(-0.02, 1.02)
ax_roc.set_xlabel('False Positive Rate (FPR = FP / Негативні)', fontsize=11, fontweight='bold', color='#1E293B')
ax_roc.set_ylabel('True Positive Rate (TPR / Recall = TP / Позитивні)', fontsize=11, fontweight='bold', color='#1E293B')
ax_roc.set_title(f'2. Побудова ROC-кривої (AUC = {auc_val:.3f})', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
ax_roc.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

# Baseline diagonal
ax_roc.plot([0, 1], [0, 1], color='#64748B', linestyle=':', linewidth=2.0, label='Випадковий класифікатор (AUC = 0.50)')
line_roc_trace, = ax_roc.plot([], [], color='#2563EB', linewidth=3.2, label=f'ROC-крива (AUC = {auc_val:.3f})')
current_dot, = ax_roc.plot([], [], marker='o', markersize=11, color='#DC2626', zorder=5, label='Поточна точка (FPR, TPR)')

# Info text badge on ROC
roc_info = ax_roc.text(0.40, 0.25, '', fontsize=10.0,
                       bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC', edgecolor='#CBD5E1', alpha=0.95))

ax_roc.legend(loc='lower right', fontsize=8.8, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

fig.suptitle('ЯК БУДУЄТЬСЯ ROC-КРИВА: ВІД РУХОМОГО ПОРОГУ ДО ПЛОЩІ AUC',
             fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)

def init():
    line_roc_trace.set_data([], [])
    current_dot.set_data([], [])
    roc_info.set_text('')
    return [line_roc_trace, current_dot, t_line, badge_t, roc_info]

def update(frame):
    t = sweep_thresholds[frame]
    
    # Update threshold on dist
    t_line.set_xdata([t, t])
    badge_t.set_position((t, 3.4))
    badge_t.set_text(f'T = {t:.2f}')
    
    # Calculate current FPR and TPR
    y_pred = (all_probs >= t).astype(int)
    fp = np.sum((y_true == 0) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    curr_fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    curr_tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    
    # Trace ROC up to this threshold
    # In ROC curve, threshold drops from high to low => points move from (0,0) to (1,1)
    mask = thresholds_full >= t
    line_roc_trace.set_data(fpr_full[mask], tpr_full[mask])
    current_dot.set_data([curr_fpr], [curr_tpr])
    
    roc_info.set_text(
        f"ПОТОЧНИЙ СТАН:\n"
        f"• Поріг T = {t:.2f}\n"
        f"• FPR (Хибна тривога): {curr_fpr*100:5.1f}%\n"
        f"• TPR (Повнота/Recall): {curr_tpr*100:5.1f}%\n"
        f"• ROC-AUC = {auc_val:.3f}"
    )
    
    return [line_roc_trace, current_dot, t_line, badge_t, roc_info]

ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, interval=90)

out_dir = 'public/videos/ai-python/logistic-regression-classification/classification-metrics'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'roc_curve_sweep_dynamics.mp4')
output_webm = os.path.join(out_dir, 'roc_curve_sweep_dynamics.webm')
output_gif = os.path.join(out_dir, 'roc_curve_sweep_dynamics.gif')
poster_png = os.path.join(out_dir, 'roc_curve_sweep_dynamics_poster.png')

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

print("Відео roc_curve_sweep_dynamics успішно завершено!")
