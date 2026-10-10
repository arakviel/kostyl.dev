import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import subprocess
import os

# Set seed
np.random.seed(42)

# Figure setup
fig = plt.figure(figsize=(16, 9), facecolor='#0b0f19')
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.0], height_ratios=[1.15, 0.85],
                      wspace=0.18, hspace=0.30, left=0.06, right=0.96, top=0.90, bottom=0.08)

ax_bag = fig.add_subplot(gs[0, 0])
ax_rf = fig.add_subplot(gs[0, 1])
ax_corr = fig.add_subplot(gs[1, 0])
ax_vote = fig.add_subplot(gs[1, 1])

for ax in [ax_bag, ax_rf, ax_corr, ax_vote]:
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#374151')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#9ca3af', labelsize=10)

# Titles
ax_bag.set_title('Простий Bagging: Усі 4 ознаки доступні кожному вузлу', fontsize=13, fontweight='bold', color='#f43f5e', pad=10)
ax_rf.set_title('Random Forest: Випадкова підвибірка (max_features = √4 = 2)', fontsize=13, fontweight='bold', color='#10b981', pad=10)
ax_corr.set_title('Кореляція між деревами (нижче = краще усереднення)', fontsize=13, fontweight='bold', color='#fbbf24', pad=10)
ax_vote.set_title('Ансамблеве голосування за новий тестовий об\'єкт', fontsize=13, fontweight='bold', color='#38bdf8', pad=10)

ax_bag.set_xlim(0, 10)
ax_bag.set_ylim(0, 6)
ax_bag.axis('off')

ax_rf.set_xlim(0, 10)
ax_rf.set_ylim(0, 6)
ax_rf.axis('off')

# Bagging tree nodes visualization (all pick strong feature X1)
bag_trees_data = [
    ("Дерево 1", "X₁ (Дохід)", "X₁ домінує"),
    ("Дерево 2", "X₁ (Дохід)", "X₁ домінує"),
    ("Дерево 3", "X₁ (Дохід)", "X₁ домінує")
]

for idx, (tname, feat, desc) in enumerate(bag_trees_data):
    y_pos = 4.5 - idx * 1.7
    r = patches.Rectangle((0.8, y_pos - 0.5), 8.4, 1.2, facecolor='#1f2937', edgecolor='#ef4444', linewidth=1.5)
    ax_bag.add_patch(r)
    ax_bag.text(1.2, y_pos + 0.1, tname, color='#e5e7eb', fontweight='bold', fontsize=11)
    ax_bag.text(3.6, y_pos + 0.1, f"Корінь: {feat}", color='#f87171', fontweight='bold', fontsize=11)
    ax_bag.text(6.8, y_pos + 0.1, f"[{desc}]", color='#9ca3af', fontsize=10)
    # Available features badges
    ax_bag.text(1.2, y_pos - 0.35, "Доступні: {X₁, X₂, X₃, X₄} ➔ Обирає найсильнішу X₁", color='#6b7280', fontsize=9.5)

# RF tree nodes visualization (random subsets force variety)
rf_trees_data = [
    ("Дерево 1", "{X₂, X₄}", "X₂ (Вік)", "X₁ приховано! Досліджує X₂"),
    ("Дерево 2", "{X₁, X₃}", "X₁ (Дохід)", "Бачить X₁, обирає її"),
    ("Дерево 3", "{X₃, X₄}", "X₃ (Рейтинг)", "Шукає патерн у Рейтингу")
]

rf_boxes = []
for idx, (tname, subset, choice, desc) in enumerate(rf_trees_data):
    y_pos = 4.5 - idx * 1.7
    r = patches.Rectangle((0.8, y_pos - 0.5), 8.4, 1.2, facecolor='#1f2937', edgecolor='#10b981', linewidth=1.5)
    ax_rf.add_patch(r)
    rf_boxes.append(r)
    ax_rf.text(1.2, y_pos + 0.1, tname, color='#e5e7eb', fontweight='bold', fontsize=11)
    ax_rf.text(3.4, y_pos + 0.1, f"Випадкові: {subset}", color='#34d399', fontweight='bold', fontsize=10.5)
    ax_rf.text(6.4, y_pos + 0.1, f"Корінь: {choice}", color='#6ee7b7', fontweight='bold', fontsize=10.5)
    ax_rf.text(1.2, y_pos - 0.35, f"Результат: {desc}", color='#9ca3af', fontsize=9.5)

# ax_corr: Correlation bars
models_corr = ['Простий\nBagging', 'Random\nForest']
corr_bars = ax_corr.bar(models_corr, [0.86, 0.28], color=['#ef4444', '#10b981'], edgecolor='#374151', width=0.45, linewidth=1.5)
ax_corr.set_ylim(0, 1.15)
ax_corr.set_ylabel('Коефіцієнт кореляції між деревами (ρ)', fontsize=11, color='#e5e7eb', labelpad=6)
ax_corr.text(0, 0.92, "ρ = 0.86\n(Схожі дерева)", ha='center', va='bottom', color='#fca5a5', fontweight='bold', fontsize=10.5)
ax_corr.text(1, 0.34, "ρ = 0.28\n(Різноманітні!)", ha='center', va='bottom', color='#a7f3d0', fontweight='bold', fontsize=10.5)

# ax_vote: Voting process
ax_vote.set_xlim(0, 10)
ax_vote.set_ylim(0, 5)
ax_vote.axis('off')

vote_card = ax_vote.text(
    0.05, 0.95, '', transform=ax_vote.transAxes,
    fontsize=11.5, color='#e5e7eb', verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.7', facecolor='#1f2937', edgecolor='#38bdf8', linewidth=1.5, alpha=0.95),
    linespacing=1.45
)

fig.suptitle('Анімація Random Subspace: Як випадковий вибір ознак усуває кореляцію дерев',
             fontsize=17, fontweight='bold', color='#ffffff', y=0.97)

def init():
    return []

def update(frame):
    # Progress through stages
    if frame < 40:
        stage = "Bagging"
        vote_card.set_text(
            "• Проблема простого Bagging:\n"
            "  Якщо у датасеті є одна домінуюча ознака (наприклад, Дохід),\n"
            "  майже кожне дерево зробить перше розбиття саме за нею.\n"
            "  Дерева стають клонами-близнюками і помиляються синхронно!"
        )
        vote_card.get_bbox_patch().set_edgecolor('#ef4444')
    elif frame < 80:
        stage = "Subspace"
        vote_card.set_text(
            "• Рішення Лео Бреймана (Random Subspace):\n"
            "  У кожному вузлі алгоритм 'ховає' більшість ознак,\n"
            "  дозволяючи дереву обирати лише з m = √p випадкових кандидатів.\n"
            "  Це змушує ліс знаходити приховані альтернативні закономірності!"
        )
        vote_card.get_bbox_patch().set_edgecolor('#10b981')
    else:
        stage = "Ensemble Vote"
        vote_card.set_text(
            "• Голосування консиліуму експертів:\n"
            "  - Дерево 1: Клас 1 (бачить вік і борг)\n"
            "  - Дерево 2: Клас 0 (випадкова локальна помилка)\n"
            "  - Дерево 3: Клас 1 (бачить кредитний рейтинг)\n"
            "  🏆 Фінальне рішення більшості: Клас 1 (2 проти 1) — помилка виправлена!"
        )
        vote_card.get_bbox_patch().set_edgecolor('#38bdf8')

    return [vote_card]

ani = animation.FuncAnimation(fig, update, frames=120, init_func=init, interval=83)

out_dir = 'public/videos/ai-python/decision-trees-random-forest/random-forest'
os.makedirs(out_dir, exist_ok=True)

output_mp4 = os.path.join(out_dir, 'random_forest_feature_subspace.mp4')
output_webm = os.path.join(out_dir, 'random_forest_feature_subspace.webm')
output_gif = os.path.join(out_dir, 'random_forest_feature_subspace.gif')
poster_png = os.path.join(out_dir, 'random_forest_feature_subspace_poster.png')

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

print("Відео random_forest_feature_subspace успішно згенеровано!")
