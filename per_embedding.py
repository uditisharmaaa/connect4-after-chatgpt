"""Per-embedding analysis, nothing averaged across representations.

For each representation separately: PCA map coloured by k-means cluster, semester-by-semester cluster maps,
share of students in AI-dominated clusters, its own AI-vs-student classifier, effect sizes, and a check
that the result does not depend on the number of clusters.
Writes figures/emb_*.png and results_per_embedding.json.
"""
import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import normalize

from features import MAIN_MODELS

matplotlib.use("Agg")
ROOT = Path(__file__).parent
FIG = ROOT / "figures"
REPS = {"lexical": "Lexical TF-IDF", "ast": "AST structure", "openai3large": "OpenAI text-embedding-3-large",
        "voyagecode": "Voyage Code 4", "codestral": "Mistral Codestral Embed", "qwen3emb": "Qwen3-Embedding-8B",
        "jina": "Jina Code v2"}
SEMS = ["Pre-2021", "Spring 2021", "Fall 2021", "Spring 2022", "Fall 2022", "Spring 2023", "Fall 2023", "Fall 2024", "Fall 2025"]
PRE_SEMS, POST = SEMS[:5], SEMS[5:]
LABELS = {"Pre-2021": "≤2020", **{s: s for s in SEMS[1:]}}
SHORT = {"Pre-2021": "≤20", "Spring 2021": "S21", "Fall 2021": "F21", "Spring 2022": "S22", "Fall 2022": "F22",
         "Spring 2023": "S23", "Fall 2023": "F23", "Fall 2024": "F24", "Fall 2025": "F25"}
K, AI_SHARE = 12, 0.8
INK, MUTED, AI, PRE_C, POST_C = "#0b0b0b", "#52514e", "#eb6834", "#b9b8b2", "#2a78d6"
KIND_COLOR = {"AI-dominated (≥80% AI)": AI, "Mixed": "#9d8fd9", "Student-dominated (≤20% AI)": "#8fb3e3"}
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#ecebe6", "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "font.size": 10.5, "axes.titleweight": "bold", "axes.titlesize": 11.5, "axes.edgecolor": "#b5b4ae",
                     "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white"})

df = pd.read_csv(ROOT / "features.csv").fillna({"model": "", "variant": ""})
is_ai = (df.source == "ai").values
core = (is_ai & (df.variant == "assignment").values & df.model.isin(MAIN_MODELS).values) | ~is_ai
d = df[core].reset_index(drop=True)
rows = np.where(core)[0]
ai = (d.source == "ai").values
stu = ~ai
group = d.group.values
pre = np.isin(group, PRE_SEMS) & stu
post = np.isin(group, POST) & stu


def load(rep):
    if rep in ("lexical", "ast"):
        return normalize(sp.load_npz(ROOT / f"{rep}.npz").tocsr()[rows].toarray())
    z = np.load(ROOT / "embeddings" / f"{rep}.npz")
    lookup = dict(zip(z["paths"], range(len(z["paths"]))))
    if not all(p in lookup for p in d.path):
        return None
    E = z["vecs"][[lookup[p] for p in d.path]].astype(np.float64)
    return normalize(E - E.mean(0))


def wilson(k, n):
    lo, hi = stats.binomtest(int(k), int(n)).proportion_ci(method="wilson")
    return lo * 100, hi * 100


def cluster_share(X, k):
    km = KMeans(k, n_init=10, random_state=0).fit(X)
    ai_frac = pd.Series(ai).groupby(km.labels_).mean()
    in_ai = np.isin(km.labels_, ai_frac[ai_frac >= AI_SHARE].index)
    return km, ai_frac, in_ai


out = {}
for rep, name in REPS.items():
    X = load(rep)
    if X is None:
        print(f"skip {rep}: embeddings incomplete")
        continue
    P2 = PCA(2, random_state=0).fit(X)
    xy, var = P2.transform(X), P2.explained_variance_ratio_
    km, ai_frac, in_ai = cluster_share(X, K)
    kind = np.where(ai_frac.values >= AI_SHARE, "AI-dominated (≥80% AI)",
                    np.where(ai_frac.values <= 0.2, "Student-dominated (≤20% AI)", "Mixed"))
    kind_of = dict(zip(ai_frac.index, kind))

    # Own classifier for this representation only: AI vs pre-ChatGPT students, out-of-fold on the training set.
    train = ai | pre
    clf = LogisticRegression(max_iter=5000, class_weight="balanced")
    p = np.full(len(d), np.nan)
    p[train] = cross_val_predict(clf, X[train], ai[train].astype(int), cv=StratifiedKFold(5, shuffle=True, random_state=0),
                                 method="predict_proba")[:, 1]
    p[post] = clf.fit(X[train], ai[train].astype(int)).predict_proba(X[post])[:, 1]
    auc = roc_auc_score(ai[train], p[train])

    centroid = X[ai].mean(0)
    sim = X @ centroid
    zsim = (sim - sim[pre].mean()) / sim[pre].std()
    sem = {}
    for s in SEMS:
        m = stu & (group == s)
        n, kc, kf = int(m.sum()), int(in_ai[m].sum()), int((p[m] > 0.5).sum())
        row = {"n": n, "cluster_pct": 100 * kc / n, "cluster_ci": wilson(kc, n), "flag_pct": 100 * kf / n,
               "flag_ci": wilson(kf, n), "mean_sim": float(zsim[m].mean())}
        if s in POST:
            v, b = zsim[m], zsim[pre]
            row["d"] = float((v.mean() - b.mean()) / np.sqrt((v.var(ddof=1) + b.var(ddof=1)) / 2))
        sem[s] = row
    tab = lambda a: [[a[post].sum(), (~a[post]).sum()], [a[pre].sum(), (~a[pre]).sum()]]
    robust = {}
    for k in (8, 12, 16):
        _, _, ia = (km, ai_frac, in_ai) if k == K else cluster_share(X, k)
        robust[k] = {s: 100 * ia[stu & (group == s)].mean() for s in SEMS}
    out[rep] = {"name": name, "pca_variance": var.tolist(), "cluster_ai_share": ai_frac.round(3).to_dict(),
                "classifier_cv_auc": auc, "semesters": sem,
                "fisher_cluster_p": stats.fisher_exact(tab(in_ai), alternative="greater").pvalue,
                "fisher_flag_p": stats.fisher_exact(tab(p > 0.5), alternative="greater").pvalue,
                "k_robustness": robust}
    print(f"{rep}: F25 clusters {sem['Fall 2025']['cluster_pct']:.0f}%  flags {sem['Fall 2025']['flag_pct']:.0f}%  "
          f"pre clusters {100 * in_ai[pre].mean():.1f}%  AUC {auc:.3f}", flush=True)

    # Figure A: the cluster map.
    fig, ax = plt.subplots(figsize=(9.5, 7.2))
    for kd, color in KIND_COLOR.items():
        mk = np.array([kind_of[c] == kd for c in km.labels_])
        ax.scatter(*xy[mk & ai].T, s=7, color=color, alpha=0.35, edgecolor="none", marker="o")
        ax.scatter(*xy[mk & stu].T, s=22, facecolor="white", edgecolor=color, lw=1.1, marker="o",
                   label=f"{kd}: {int((mk & stu).sum())} students, {int((mk & ai).sum())} AI files")
    for c in ai_frac.index:
        cx, cy = xy[km.labels_ == c].mean(0)
        ax.annotate(f"{ai_frac[c]:.0%} AI", (cx, cy), fontsize=8.5, fontweight="bold", ha="center", va="center",
                    color=INK, bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": KIND_COLOR[kind_of[c]], "lw": 1})
    ax.set_xlabel(f"PC1 ({var[0]:.0%} of variance)")
    ax.set_ylabel(f"PC2 ({var[1]:.0%})")
    pre_pct = 100 * in_ai[pre].mean()
    ax.set_title(f"{name}: {K} k-means clusters on the PCA map\nStudents in AI-dominated clusters: {pre_pct:.1f}% before ChatGPT, "
                 f"{sem['Fall 2024']['cluster_pct']:.0f}% in Fall 2024, {sem['Fall 2025']['cluster_pct']:.0f}% in Fall 2025",
                 loc="left")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", bbox_to_anchor=(1.01, 1), title="Hollow = students, dots = AI",
              title_fontsize=8.5)
    fig.savefig(FIG / f"emb_{rep}_clusters.png")
    plt.close(fig)

    # Figure B: semester by semester, students coloured by the kind of cluster they fall in.
    fig, axes = plt.subplots(3, 3, figsize=(13, 11.5), sharex=True, sharey=True)
    for axp, s in zip(axes.ravel(), SEMS):
        m = stu & (group == s)
        axp.scatter(*xy[ai].T, s=4, color=AI, alpha=0.08, edgecolor="none")
        axp.scatter(*xy[pre].T, s=4, color="#dddcd7", edgecolor="none")
        axp.scatter(*xy[m & ~in_ai].T, s=14, color=POST_C if s in POST else "#8a8985", alpha=0.85, edgecolor="white", lw=0.3)
        axp.scatter(*xy[m & in_ai].T, s=34, color=AI, edgecolor=INK, lw=0.6, zorder=4)
        r = sem[s]
        axp.set_title(f"{LABELS[s]}: {r['cluster_pct']:.0f}% in AI clusters ({int(round(r['cluster_pct'] * r['n'] / 100))}/{r['n']})",
                      fontsize=10)
    fig.suptitle(f"{name}, semester by semester: students inside AI-dominated clusters are orange\n"
                 "(faint orange = AI files, light grey = all pre-ChatGPT students)", fontweight="bold", x=0.02, ha="left")
    fig.tight_layout()
    fig.savefig(FIG / f"emb_{rep}_clusters_by_semester.png")
    plt.close(fig)

reps = list(out)
# Figure C: AI-cluster share per semester, one panel per representation, same scale.
cols = 4
fig, axes = plt.subplots(int(np.ceil(len(reps) / cols)), cols, figsize=(18, 8.5), sharey=True)
for ax in axes.ravel()[len(reps):]:
    ax.axis("off")
for ax, rep in zip(axes.ravel(), reps):
    sem = out[rep]["semesters"]
    v = np.array([sem[s]["cluster_pct"] for s in SEMS])
    lo = np.array([sem[s]["cluster_ci"][0] for s in SEMS])
    hi = np.array([sem[s]["cluster_ci"][1] for s in SEMS])
    x = np.arange(len(SEMS))
    ax.bar(x, v, color=[AI if s in POST else PRE_C for s in SEMS], width=0.65, zorder=2)
    ax.errorbar(x, v, yerr=[v - lo, hi - v], fmt="none", ecolor=MUTED, lw=0.9, capsize=2, zorder=3)
    for i in (7, 8):
        ax.text(i, hi[i] + 1.5, f"{v[i]:.0f}%", ha="center", fontsize=8.5, fontweight="bold")
    ax.axvline(4.5, color=MUTED, ls="--", lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels([SHORT[s] for s in SEMS], fontsize=7.5)
    ax.set_title(f"{out[rep]['name']}\nbefore ChatGPT: {np.average([sem[s]['cluster_pct'] for s in PRE_SEMS], weights=[sem[s]['n'] for s in PRE_SEMS]):.1f}%"
                 f"   ·   Fisher p = {out[rep]['fisher_cluster_p']:.0e}", fontsize=10)
axes[0, 0].set_ylabel("% of students in AI-dominated clusters")
axes[1, 0].set_ylabel("% of students in AI-dominated clusters")
fig.suptitle("Each representation on its own, nothing averaged: the share of students in AI-dominated k-means clusters",
             fontweight="bold", x=0.02, ha="left")
fig.tight_layout()
fig.savefig(FIG / "emb_summary_cluster_share.png")
plt.close(fig)

# Figure D: two heatmaps, representation x semester, for the cluster share and the per-representation classifier.
fig, axes = plt.subplots(1, 2, figsize=(17, 4.6), gridspec_kw={"wspace": 0.04})
for ax, key, title in [(axes[0], "cluster_pct", "% of students in AI-dominated clusters (unsupervised)"),
                       (axes[1], "flag_pct", "% flagged by that representation's own classifier")]:
    M = np.array([[out[r]["semesters"][s][key] for s in SEMS] for r in reps])
    im = ax.imshow(M, cmap="Oranges", vmin=0, vmax=40, aspect="auto")
    for i in range(len(reps)):
        for j in range(len(SEMS)):
            ax.text(j, i, f"{M[i, j]:.0f}", ha="center", va="center", fontsize=8.5, color="white" if M[i, j] > 24 else INK)
    ax.set_xticks(range(len(SEMS)))
    ax.set_xticklabels([LABELS[s] for s in SEMS], rotation=30, ha="right", fontsize=8.5)
    ax.set_yticks(range(len(reps)))
    ax.set_yticklabels([out[r]["name"] for r in reps] if key == "cluster_pct" else [], fontsize=8.5)
    ax.axvline(4.5, color=INK, lw=1.5)
    ax.grid(False)
    ax.set_title(title, loc="left")
fig.colorbar(im, ax=axes, label="% of the semester's students", shrink=0.9)
fig.suptitle("Every representation, every semester: the jump after ChatGPT appears in each one separately",
             fontweight="bold", x=0.02, ha="left", y=1.04)
fig.savefig(FIG / "emb_summary_heatmaps.png")
plt.close(fig)

# Figure E: does the number of clusters matter?
fig, ax = plt.subplots(figsize=(10, 4.4))
w = 0.26
for k_i, (k, shade) in enumerate([(8, 0.45), (12, 0.75), (16, 1.0)]):
    pre_v = [np.average([out[r]["k_robustness"][k][s] for s in PRE_SEMS], weights=[out[r]["semesters"][s]["n"] for s in PRE_SEMS]) for r in reps]
    f25 = [out[r]["k_robustness"][k]["Fall 2025"] for r in reps]
    x = np.arange(len(reps)) + (k_i - 1) * w
    ax.bar(x, f25, w, color=AI, alpha=shade, label=f"Fall 2025, k = {k}")
    ax.scatter(x, pre_v, color=INK, s=14, zorder=3, label="pre-ChatGPT average" if k_i == 0 else None)
ax.set_xticks(range(len(reps)))
ax.set_xticklabels([out[r]["name"] for r in reps], fontsize=8.5, rotation=20, ha="right")
ax.set_ylabel("% of students in AI-dominated clusters")
ax.set_title("The result does not depend on choosing 12 clusters: 8, 12 and 16 give similar answers", loc="left")
ax.legend(frameon=False, fontsize=8.5, ncol=4, loc="upper left")
fig.savefig(FIG / "emb_k_robustness.png")
plt.close(fig)

(ROOT / "results_per_embedding.json").write_text(json.dumps(out, indent=2, default=float))
print(pd.DataFrame({out[r]["name"]: {**{SHORT[s]: round(out[r]["semesters"][s]["cluster_pct"], 1) for s in SEMS},
                                     "flagF25": round(out[r]["semesters"]["Fall 2025"]["flag_pct"], 1),
                                     "dF25": round(out[r]["semesters"]["Fall 2025"]["d"], 2),
                                     "AUC": round(out[r]["classifier_cv_auc"], 3)} for r in reps}).T.to_string())
