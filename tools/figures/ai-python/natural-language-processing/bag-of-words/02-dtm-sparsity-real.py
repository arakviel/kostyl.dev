#!/usr/bin/env python3
"""Матриця документ–слово на реальних даних (movie_reviews, CountVectorizer 5000) + збереження чисел для відео."""
import json
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import movie_reviews
from sklearn.feature_extraction.text import CountVectorizer

docs = [" ".join(movie_reviews.words(f)) for f in movie_reviews.fileids()]
vec = CountVectorizer(max_features=5000, lowercase=True, token_pattern=r'\b[a-z]+\b')
X = vec.fit_transform(docs)
n_docs, n_words = X.shape
total = n_docs * n_words
sparsity = (1 - X.nnz / total) * 100
dense_mb = total * 8 / 1024**2
sparse_mb = (X.data.nbytes + X.indices.nbytes + X.indptr.nbytes) / 1024**2
per_doc = X.getnnz(axis=1)

# вибірка для малюнка: перші 100 відгуків × кожен 25-й стовпець (200 стовпців)
sub = X[:100, ::25].toarray()
sub_nz = int((sub > 0).sum())

json.dump({
    "shape": [n_docs, n_words], "nnz": int(X.nnz), "sparsity_pct": round(sparsity, 2),
    "dense_mb": round(dense_mb, 1), "sparse_mb": round(sparse_mb, 1),
    "ratio": round(dense_mb / sparse_mb, 1), "mean_nonzero_per_doc": round(float(per_doc.mean()), 1),
    "median_nonzero_per_doc": float(np.median(per_doc)),
    "sub_shape": list(sub.shape), "sub_nnz": sub_nz,
}, open("tools/hyperframes/natural-language-processing/bow-05-sparsity/_data/dtm.json", "w"), indent=1)
np.save("tools/hyperframes/natural-language-processing/bow-05-sparsity/_data/sub.npy", sub.astype(np.uint8))

import sys
sys.path.insert(0, "tools/figures")
from _style import INK
fig = plt.figure(figsize=(12, 6.6))
gs = fig.add_gridspec(2, 2, height_ratios=[4, 1], width_ratios=[4, 1], hspace=0.28, wspace=0.12)
ax = fig.add_subplot(gs[0, 0])
im = ax.imshow(sub, aspect="auto", cmap="Blues", interpolation="nearest", vmin=0, vmax=4)
ax.set_xlabel("слово зі словника (кожне 25-те з 5000)", fontsize=12); ax.set_ylabel("номер відгуку", fontsize=12)
ax.set_title("перші 100 відгуків × 200 слів: темні клітинки — ненульові", fontsize=12.5)
cb = plt.colorbar(im, ax=ax, pad=0.02); cb.set_label("скільки разів слово є у відгуку (≥ 4 — один колір)", fontsize=10)
ah = fig.add_subplot(gs[0, 1])
ah.barh(range(100), (sub > 0).sum(axis=1), color="#2563EB"); ah.set_ylim(99.5, -0.5)
ah.set_xlabel("ненульових\nу вибірці", fontsize=10.5)
for sp in ("top", "right"): ah.spines[sp].set_visible(False)
st = fig.add_subplot(gs[1, :]); st.axis("off")
fm = lambda x, d=0: f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
txt = (f"Уся матриця: {n_docs} відгуків × {n_words} слів = {fm(total)} елементів. Нулів: {fm(sparsity, 2)}%; у середньому {per_doc.mean():.0f} різних слів на відгук.\n"
       f"Пам'ять: щільна {fm(dense_mb, 1)} МБ, розріджена (CSR) {fm(sparse_mb, 1)} МБ — у {dense_mb/sparse_mb:.0f} разів менше.")
st.text(0.5, 0.5, txt, transform=st.transAxes, fontsize=11.5, ha="center", va="center", bbox=dict(boxstyle="round,pad=0.7", facecolor="#DBEAFE", edgecolor=INK, linewidth=1.2))
plt.savefig("public/images/ai-python/natural-language-processing/bag-of-words/02-dtm-sparsity-real.png", dpi=200, bbox_inches="tight", facecolor="white")
print("ok")
