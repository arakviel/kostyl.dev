#!/usr/bin/env python3
"""Візуалізація іграшкових векторів у 2D просторі."""
import matplotlib.pyplot as plt
import numpy as np

# Іграшкові вектори з лекції
embeddings = {
    "king":   np.array([0.8, 0.6]),
    "queen":  np.array([0.7, 0.7]),
    "man":    np.array([0.6, 0.3]),
    "woman":  np.array([0.5, 0.6]),
    "cat":    np.array([-0.3, 0.5]),
    "dog":    np.array([-0.2, 0.4]),
}

fig, ax = plt.subplots(figsize=(10, 8), facecolor='#070b14')
ax.set_facecolor('#070b14')

words = list(embeddings.keys())
coords = np.array(list(embeddings.values()))

# Розділити на групи
humans = ["king", "queen", "man", "woman"]
animals = ["cat", "dog"]

# Малювання точок
for word, coord in embeddings.items():
    if word in humans:
        color = '#10b981'
        marker = 'o'
        size = 250
    else:
        color = '#06b6d4'
        marker = 's'
        size = 250
    
    ax.scatter(coord[0], coord[1], s=size, c=color, marker=marker,
              edgecolor='#0f172a', linewidth=2, zorder=3)
    
    # Мітки
    ax.annotate(word, (coord[0], coord[1]), fontsize=12, color='#e2e8f0',
               fontweight='bold', ha='center', xytext=(0, -25), 
               textcoords='offset points')

# Лінії між близькими словами
close_pairs = [("king", "queen"), ("man", "woman"), ("cat", "dog")]
for w1, w2 in close_pairs:
    c1, c2 = embeddings[w1], embeddings[w2]
    ax.plot([c1[0], c2[0]], [c1[1], c2[1]], color='#334155', 
           linewidth=2, linestyle='--', alpha=0.6, zorder=1)

# Області
from matplotlib.patches import Ellipse

# Люди
human_center = np.mean([embeddings[w] for w in humans], axis=0)
ellipse1 = Ellipse(human_center, 0.5, 0.6, angle=30, 
                   facecolor='#10b981', alpha=0.1, edgecolor='#10b981', 
                   linewidth=2, linestyle='--')
ax.add_patch(ellipse1)
ax.text(human_center[0] + 0.1, human_center[1] + 0.35, 'Люди', 
       fontsize=11, color='#10b981', fontweight='bold', ha='center')

# Тварини
animal_center = np.mean([embeddings[w] for w in animals], axis=0)
ellipse2 = Ellipse(animal_center, 0.3, 0.25, 
                   facecolor='#06b6d4', alpha=0.1, edgecolor='#06b6d4', 
                   linewidth=2, linestyle='--')
ax.add_patch(ellipse2)
ax.text(animal_center[0], animal_center[1] - 0.2, 'Тварини', 
       fontsize=11, color='#06b6d4', fontweight='bold', ha='center')

# Осі
ax.axhline(0, color='#334155', linewidth=1, linestyle='-', alpha=0.5)
ax.axvline(0, color='#334155', linewidth=1, linestyle='-', alpha=0.5)

ax.set_xlabel('Вимір 1', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_ylabel('Вимір 2', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_title('Іграшкові вектори: схожі слова згруповані в просторі', 
            fontsize=14, color='#e2e8f0', fontweight='bold', pad=20)

ax.set_xlim(-0.6, 1.0)
ax.set_ylim(0.1, 0.9)

# Легенда
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#10b981', 
           markersize=10, label='Люди', linestyle='None', markeredgecolor='#0f172a', markeredgewidth=1.5),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#06b6d4', 
           markersize=10, label='Тварини', linestyle='None', markeredgecolor='#0f172a', markeredgewidth=1.5),
]
legend = ax.legend(handles=legend_elements, loc='upper right', fontsize=11, framealpha=0.95)
legend.get_frame().set_facecolor('#0f172a')
legend.get_frame().set_edgecolor('#334155')
for text in legend.get_texts():
    text.set_color('#e2e8f0')

ax.tick_params(colors='#e2e8f0', labelsize=10)
ax.grid(alpha=0.2, color='#334155', linestyle='--')
for spine in ax.spines.values():
    spine.set_color('#334155')

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/from-one-hot-to-embeddings/04-2d-embeddings.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 04-2d-embeddings.png створено")
