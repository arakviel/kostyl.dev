"""
Media for content/16.ai-python/15.cnn-image-classification/16.pneumonia-transfer-learning.md  (needs temp/xray_cache.pt)
Images -> public/images/ai-python/cnn-image-classification/pneumonia-transfer/
  01 examples + balance  02 hold-out vs test  03 model comparison  04 confusion matrix  05 threshold sweep  06 ROC  07 Grad-CAM  08 Grad-CAM errors
"""
import os, sys
sys.path.insert(0, "scripts")
import numpy as np
import torch, torch.nn.functional as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from xray_core import Pre, metrics, load_cache, XTR, YTR, XTE, YTE, NTE, HO_IDX, TR_IDX

plt.rcParams["font.family"] = "DejaVu Sans"
IMG = "public/images/ai-python/cnn-image-classification/pneumonia-transfer"
os.makedirs(IMG, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
KCOL = {"scratch": MUTED, "frozen": CYAN, "finetune": GREEN}
KNAME = {"scratch": "з нуля", "frozen": "заморожена ResNet-18", "finetune": "донавчена ResNet-18"}
def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def despine(ax): [ax.spines[s].set_visible(False) for s in ("top", "right")]
def title(ax, t): ax.set_title(t, fontsize=12.5, fontweight="bold", color=INK)
def gray(ax, x): ax.imshow(x.numpy(), cmap="gray", vmin=0, vmax=255); ax.set_xticks([]); ax.set_yticks([])
def keys(C, kind, w=False): return sorted(k for k in C if k[0] == kind and k[2] == w)

def img01():
    fig = plt.figure(figsize=(12, 5.4)); gs = fig.add_gridspec(2, 5, width_ratios=[1, 1, 1, 1, 1.5])
    rng = np.random.RandomState(1)
    for r, (cls, lab, col) in enumerate(((0, "норма", GREEN), (1, "пневмонія", RED))):
        idx = rng.choice((YTR == cls).nonzero().flatten().numpy(), 4, replace=False)
        for c, i in enumerate(idx):
            ax = fig.add_subplot(gs[r, c]); gray(ax, XTR[i])
            if c == 0: ax.set_ylabel(lab, color=col, fontsize=12, fontweight="bold")
    ax = fig.add_subplot(gs[:, 4]); w = .38
    ax.bar([0 - w / 2, 1 - w / 2], [1341, 234], w, color=GREEN, label="норма"); ax.bar([0 + w / 2, 1 + w / 2], [3875, 390], w, color=RED, label="пневмонія")
    for x, v in zip([-w / 2, w / 2, 1 - w / 2, 1 + w / 2], [1341, 3875, 234, 390]): ax.text(x, v + 60, str(v), ha="center", fontsize=10, fontweight="bold", color=INK)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["навчальний набір", "тестовий набір"]); ax.legend(frameon=False); despine(ax); title(ax, "Кількість знімків")
    save_png(fig, "01.png")

def img02(C):
    fig, ax = plt.subplots(figsize=(10, 4.8)); x = 0; ticks = []; labs = []
    for kind in ("scratch", "frozen", "finetune"):
        ks = keys(C, kind)
        for j, k in enumerate(ks):
            h = C[k]["hist"][-1]["hold"]["acc"] * 100; t = C[k]["hist"][-1]["test"]["acc"] * 100
            ax.bar(x - .2, h, .38, color=KCOL[kind], alpha=.45, label="hold-out" if kind == "scratch" and j == 0 else None); ax.bar(x + .2, t, .38, color=KCOL[kind], label="тест" if kind == "scratch" and j == 0 else None)
            ax.text(x - .2, h + .6, f"{h:.0f}", ha="center", fontsize=9, color=INK); ax.text(x + .2, t + .6, f"{t:.0f}", ha="center", fontsize=9, fontweight="bold", color=INK); x += 1
        ticks.append(x - 2); labs.append(KNAME[kind]); x += .6
    ax.axhline(62.5, color=RED, ls="--", lw=1.5); ax.text(-.6, 58.5, "«завжди пневмонія»: 62,5%", ha="left", color=RED, fontsize=10)
    ax.set_xticks(ticks); ax.set_xticklabels(labs, fontsize=11); ax.set_ylim(50, 102); ax.set_ylabel("точність, %", color=MUTED)
    title(ax, "Одна й та сама мережа: hold-out (світліше) та тест (насичено); три зерна на метод"); ax.legend(frameon=False, loc="lower right"); despine(ax)
    save_png(fig, "02.png")

def img03(C):
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
    groups = [("scratch", False), ("frozen", False), ("finetune", False), ("finetune", True)]
    names = ["з нуля", "заморожена", "донавчена", "донавчена\n+ ваги класів"]; cols = [MUTED, CYAN, GREEN, PURPLE]
    for a, (m, t) in zip(axs, (("acc", "Точність (accuracy), %"), ("recall", "Повнота (recall) для пневмонії, %"), ("spec", "Специфічність (норма розпізнана), %"))):
        for i, (kind, w) in enumerate(groups):
            v = np.array([C[k]["hist"][-1]["test"][m] * 100 for k in keys(C, kind, w)])
            a.bar(i, v.mean(), .65, color=cols[i]); a.plot([i] * len(v), v, "o", color=INK, ms=5, alpha=.7); a.text(i, v.max() + 1.2, f"{v.mean():.1f}", ha="center", fontsize=11, fontweight="bold", color=INK)
        a.set_xticks(range(4)); a.set_xticklabels(names, fontsize=9.5); title(a, t); despine(a)
    axs[0].set_ylim(50, 100); axs[1].set_ylim(90, 101); axs[2].set_ylim(0, 100)
    save_png(fig, "03.png")

def img04(C):
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.4))
    for a, k, t in zip(axs, (("finetune", 2, False), ("finetune", 0, False)), ("зерно 2 (найкраще)", "зерно 0 (найгірше)")):
        m = metrics(C[k]["pt"], YTE); cm = np.array([[m["tn"], m["fp"]], [m["fn"], m["tp"]]])
        a.imshow(cm, cmap="Blues", vmin=0, vmax=400)
        for i in range(2):
            for j in range(2): a.text(j, i, f"{cm[i, j]}", ha="center", va="center", fontsize=20, fontweight="bold", color="white" if cm[i, j] > 200 else INK)
        a.set_xticks([0, 1]); a.set_xticklabels(["передбачено:\nнорма", "передбачено:\nпневмонія"]); a.set_yticks([0, 1]); a.set_yticklabels(["справді\nнорма", "справді\nпневмонія"])
        title(a, f"Донавчена ResNet-18, {t}")
    save_png(fig, "04.png")

def sweep(p, y, ths): 
    r = [metrics(p, y, t) for t in ths]; return [np.array([m[k] for m in r]) * 100 for k in ("recall", "precision", "spec")]
def img05(C):
    k = ("finetune", 2, False); ths = np.linspace(0.01, 0.999, 120)
    fig, axs = plt.subplots(1, 2, figsize=(14, 4.8), sharey=True)
    for a, (p, y, t) in zip(axs, ((C[k]["ph"], YTR[HO_IDX], "hold-out (з навчального набору)"), (C[k]["pt"], YTE, "тестовий набір"))):
        rec, pre, spe = sweep(p, y, ths)
        a.plot(ths, rec, color=RED, lw=3, label="повнота (recall)"); a.plot(ths, pre, color=AMBER, lw=3, label="точність позитивних (precision)"); a.plot(ths, spe, color=GREEN, lw=3, label="специфічність")
        a.axvline(.5, color=MUTED, ls=":"); title(a, t); a.set_xlabel("поріг", color=MUTED); despine(a)
    axs[0].legend(frameon=False, fontsize=10, loc="lower left"); axs[0].set_ylabel("%", color=MUTED)
    save_png(fig, "05.png")

def roc(p, y):
    o = torch.argsort(p, descending=True); yy = y[o].numpy(); tpr = np.concatenate([[0], np.cumsum(yy) / yy.sum()]); fpr = np.concatenate([[0], np.cumsum(1 - yy) / (1 - yy).sum()]); return fpr, tpr, np.trapezoid(tpr, fpr)
def img06(C):
    fig, ax = plt.subplots(figsize=(6.4, 6)); 
    for kind in ("scratch", "frozen", "finetune"):
        k = (kind, 2, False); f, t, a = roc(C[k]["pt"], YTE); ax.plot(f, t, color=KCOL[kind], lw=3, label=f"{KNAME[kind]} (AUC {a:.3f})")
    ax.plot([0, 1], [0, 1], color=MUTED, ls="--"); ax.set_xlabel("частка здорових, названих хворими", color=MUTED); ax.set_ylabel("повнота (recall)", color=MUTED); title(ax, "ROC на тестовому наборі, зерно 2"); ax.legend(frameon=False, loc="lower right"); despine(ax)
    save_png(fig, "06.png")

def cam(model, x):
    acts = {}; h = model.net.layer4.register_forward_hook(lambda m, i, o: acts.update(a=o))
    model.eval(); x = x.unsqueeze(0).unsqueeze(0).float() / 255; x.requires_grad_(False)
    out = model(x); a = acts["a"]; a.retain_grad(); score = out[0, 1]; model.zero_grad(); 
    g = torch.autograd.grad(score, a)[0]; h.remove()
    w = g.mean((2, 3), keepdim=True); c = F.relu((w * a).sum(1, keepdim=True)); c = F.interpolate(c, size=x.shape[-2:], mode="bilinear", align_corners=False)[0, 0]
    return (c / (c.max() + 1e-8)).detach(), torch.softmax(out, 1)[0, 1].item()

def load_model(C, k): m = Pre(False); m.load_state_dict(C[k]["state"]); return m.eval()
def overlay(ax, x, c, text, col):
    ax.imshow(x.numpy(), cmap="gray", vmin=0, vmax=255); ax.imshow(c.numpy(), cmap="jet", alpha=.42, vmin=0, vmax=1); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(text, fontsize=10, color=col, fontweight="bold")

def pick(C, k):
    p = C[k]["pt"]; pred = (p >= .5).long(); out = {}
    for name, cond in (("TP", (pred == 1) & (YTE == 1)), ("TN", (pred == 0) & (YTE == 0)), ("FP", (pred == 1) & (YTE == 0)), ("FN", (pred == 0) & (YTE == 1))):
        out[name] = cond.nonzero().flatten().tolist()
    return out
def img07(C):
    k = ("finetune", 2, False); model = load_model(C, k); ids = pick(C, k); rng = np.random.RandomState(3)
    fig, axs = plt.subplots(2, 6, figsize=(16, 5.6)); sel = {"TP": rng.choice(ids["TP"], 6, replace=False), "TN": rng.choice(ids["TN"], 6, replace=False)}
    for r, (nm, lab, col) in enumerate((("TP", "пневмонія знайдена", RED), ("TN", "норма впізнана", GREEN))):
        for c, i in enumerate(sel[nm]):
            cm, p = cam(model, XTE[i]); overlay(axs[r, c], XTE[i], cm, f"{lab}\nP(пневм.) = {p:.2f}", col)
    save_png(fig, "07.png"); print("TP ids", list(map(int, sel["TP"])), "TN ids", list(map(int, sel["TN"])))
def img08(C):
    k = ("finetune", 2, False); model = load_model(C, k); ids = pick(C, k); rng = np.random.RandomState(5)
    fig, axs = plt.subplots(2, 6, figsize=(16, 5.6)); sel = {"FP": rng.choice(ids["FP"], 6, replace=False), "FN": np.array(ids["FN"][:6])}
    for a in axs.ravel(): a.axis("off")
    for r, (nm, lab, col) in enumerate((("FP", "хибна тривога", AMBER), ("FN", "пропущена пневмонія", RED))):
        for c, i in enumerate(sel[nm]):
            axs[r, c].axis("on"); cm, p = cam(model, XTE[i]); overlay(axs[r, c], XTE[i], cm, f"{lab}\nP(пневм.) = {p:.2f}", col)
    save_png(fig, "08.png"); print("FN", len(ids["FN"]), "FP", len(ids["FP"]))

if __name__ == "__main__":
    C = load_cache(); img01(); img02(C); img03(C); img04(C); img05(C); img06(C); img07(C); img08(C)
