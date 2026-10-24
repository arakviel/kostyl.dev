"""
Generates 07.png for content/16.ai-python/15.cnn-image-classification/01.intro-computer-vision.md
Real MNIST digit "7": full image (28x28) + zoomed 10x10 crop with raw pixel values.
Source: temp/mnist.npz
Target: public/images/ai-python/cnn-image-classification/intro-computer-vision/07.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'DejaVu Sans'
OUT_DIR = "public/images/ai-python/cnn-image-classification/intro-computer-vision"
os.makedirs(OUT_DIR, exist_ok=True)

data = np.load("temp/mnist.npz")
idx = 101  # a clean, unambiguous "7" (y_train[101] == 7)
assert data["y_train"][idx] == 7
img = data["x_train"][idx]

r0, c0, size = 6, 10, 10  # crop through the top bar of the "7"
crop = img[r0:r0 + size, c0:c0 + size]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={"width_ratios": [1, 1.25]})
fig.patch.set_facecolor("white")

ax1.imshow(img, cmap="gray", vmin=0, vmax=255)
ax1.add_patch(patches.Rectangle((c0 - 0.5, r0 - 0.5), size, size, fill=False, edgecolor="#F59E0B", linewidth=3))
ax1.set_title("Цифра «7» з MNIST: 28×28 = 784 пікселі", fontsize=13, fontweight="bold", color="#0F172A", pad=12)
ax1.set_xticks([]); ax1.set_yticks([])

ax2.imshow(crop, cmap="gray", vmin=0, vmax=255)
for r in range(size):
    for c in range(size):
        v = int(crop[r, c])
        ax2.text(c, r, str(v), ha="center", va="center", fontsize=9,
                 color="white" if v < 128 else "#0F172A", fontweight="bold")
for k in range(size + 1):
    ax2.axhline(k - 0.5, color="#475569", linewidth=0.6)
    ax2.axvline(k - 0.5, color="#475569", linewidth=0.6)
for s in ax2.spines.values():
    s.set_edgecolor("#F59E0B"); s.set_linewidth(3)
ax2.set_title("Збільшена ділянка 10×10: кожен піксель — число 0…255", fontsize=13, fontweight="bold", color="#0F172A", pad=12)
ax2.set_xticks([]); ax2.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "07.png"), dpi=200, facecolor="white")
print("saved 07.png")
