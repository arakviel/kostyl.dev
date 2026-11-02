"""Реальні ваги уваги BERT (bert-base-uncased): шар 4, голова 11. Слово «it» дивиться на «animal».
Запуск: uv run --python 3.13 --with matplotlib --with torch --with transformers python <цей файл>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

import torch
from transformers import AutoTokenizer, AutoModel

s = "the animal did not cross the street because it was too tired"
tk = AutoTokenizer.from_pretrained("bert-base-uncased")
m = AutoModel.from_pretrained("bert-base-uncased", attn_implementation="eager")
b = tk(s, return_tensors="pt")
toks = tk.convert_ids_to_tokens(b["input_ids"][0])
with torch.no_grad():
    A = m(**b, output_attentions=True).attentions[3][0, 10].numpy()   # шар 4, голова 11 (нумерація з 1)
it = toks.index("it")
print({t: round(float(v), 2) for t, v in zip(toks, A[it])})

fig, ax = plt.subplots(figsize=(7.4, 6.2))
im = ax.imshow(A, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(len(toks))); ax.set_xticklabels(toks, rotation=60, ha="left", fontsize=12)
ax.set_yticks(range(len(toks))); ax.set_yticklabels(toks, fontsize=12)
ax.xaxis.tick_top()
ax.set_xlabel("на які слова дивиться (ключі)", fontsize=12); ax.set_ylabel("слово-запит", fontsize=12)
ax.xaxis.set_label_position("top")
ax.add_patch(plt.Rectangle((-0.5, it - 0.5), len(toks), 1, fill=False, ec="#DC2626", lw=2.2))
ax.text(toks.index("animal"), it, f"{A[it, toks.index('animal')]:.2f}", ha="center", va="center", color="white", fontsize=11.5, fontweight="bold")
fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
save(fig, __file__)
