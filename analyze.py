"""Semester-by-semester comparison of student Connect 4 code against ChatGPT and Claude generations.

Reads features.csv / lexical.npz / ast.npz (features.py) and embeddings/*.npz (embed.py).
Writes figures/*.png and results.json.
"""
import json
import re
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
from sklearn.preprocessing import StandardScaler, normalize

from features import (AVAILABLE_FROM, ERA_MODEL, FAMILY, FIRST_AI_SEMESTER, MAIN_MODELS, MODEL_NAMES,
                      MODEL_RELEASE, OTHER_MODELS, SEMESTERS)

matplotlib.use("Agg")
ROOT = Path(__file__).parent
# BASELINE=2021 drops the "Pre-2021" folder, whose spec predates the 2-5 player requirement (sensitivity check).
BASELINE = __import__("os").environ.get("BASELINE", "all")
SUFFIX = "" if BASELINE == "all" else "_baseline2021"
FIG = ROOT / f"figures{SUFFIX}"
FIG.mkdir(exist_ok=True)
for old in FIG.glob("*.png"):
    old.unlink()
rng = np.random.default_rng(0)
PER_MODEL, PER_VARIANT = 300, 100

PRE, POST, AI, INK, MUTED, LIGHT = "#8a8985", "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#dddcd7"
CHATGPT, CLAUDE = "#1baf7a", "#d97757"
MODEL_COLORS = dict(zip(MAIN_MODELS, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]))
VARIANT_COLORS = {"assignment": "#2a78d6", "short": "#1baf7a", "disguise": "#6250d6"}
VARIANT_NAMES = {"assignment": "Full assignment pasted", "short": "Short one-line request",
                 "disguise": "Asked to look human-written"}
ALL_REPS = {"lexical": "Lexical TF-IDF", "ast": "AST structure", "openai3large": "OpenAI text-embedding-3-large",
            "voyagecode": "Voyage Code 4", "codestral": "Mistral Codestral Embed", "qwen3emb": "Qwen3-Embedding-8B"}
STYLE_COLS = ["lines", "comment_ratio", "functions", "docstrings", "type_hints", "fstrings", "main_guard",
              "avg_name_len", "snake_case", "global_stmts", "enumerate", "range_len", "comprehensions",
              "try_except", "avg_line_len"]
STYLE_LABELS = {"lines": "Non-blank lines", "comment_ratio": "Comment-line share", "functions": "Functions defined",
                "docstrings": "Docstrings", "type_hints": "Type-hinted functions", "fstrings": "f-strings",
                "main_guard": "if __name__ == '__main__'", "avg_name_len": "Avg identifier length",
                "snake_case": "Share of snake_case names", "global_stmts": "global statements",
                "enumerate": "enumerate() calls", "range_len": "range(len(...)) calls",
                "comprehensions": "Comprehensions", "try_except": "try/except blocks",
                "avg_line_len": "Avg line length (chars)"}

plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.color": "#e6e5e0",
                     "grid.linewidth": 0.6, "axes.axisbelow": True, "font.size": 10,
                     "axes.titleweight": "bold", "axes.titlesize": 10.5, "axes.edgecolor": "#b5b4ae",
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK,
                     "figure.facecolor": "white"})

# ---------- Load and balance ----------
full = pd.read_csv(ROOT / "features.csv").fillna({"model": "", "variant": ""})
index_in_folder = full.path.str.extract(r"_(\d+)\.py$")[0].astype(float)
keep = (full.source == "student") | ((full.variant == "assignment") & (index_in_folder < PER_MODEL)) | \
       ((full.variant != "assignment") & (index_in_folder < PER_VARIANT))
keep &= ~full.model.isin(["qwencoder"])
if BASELINE == "2021":
    keep &= full.group != "Pre-2021"
rows = np.where(keep.values)[0]
df = full.iloc[rows].reset_index(drop=True)
is_ai = (df.source == "ai").values
main_ai = is_ai & (df.variant == "assignment").values & df.model.isin(MAIN_MODELS).values
core = main_ai | ~is_ai
X = {"lexical": sp.load_npz(ROOT / "lexical.npz").tocsr()[rows], "ast": sp.load_npz(ROOT / "ast.npz").tocsr()[rows]}
for enc in ALL_REPS:
    f = ROOT / "embeddings" / f"{enc}.npz"
    if enc in X or not f.exists():
        continue
    z = np.load(f)
    lookup = dict(zip(z["paths"], range(len(z["paths"]))))
    if not all(p in lookup for p in df.path[core]):
        print(f"skipping {enc}: embeddings incomplete")
        continue
    E = np.zeros((len(df), z["vecs"].shape[1]))
    E[core] = z["vecs"][[lookup[p] for p in df.path[core]]]
    E[core] = normalize(E[core] - E[core].mean(0))
    X[enc] = E
REPS = {k: v for k, v in ALL_REPS.items() if k in X}
TEXT_REPS = {k: REPS[k] for k in ("lexical", "ast")}
FIRST_COL = set(list(REPS)[::3 if len(REPS) <= 6 else 4])
print("representations:", list(REPS))
stu = df[~is_ai].copy()
stu_idx = np.where(~is_ai)[0]
sem_order = [s for s in SEMESTERS if s in set(stu.group)]
sem_pos = {s: i for i, s in enumerate(sem_order)}
chatgpt_x = sem_pos[FIRST_AI_SEMESTER] - 0.5
pre_mask = ~stu.post_chatgpt.values.astype(bool)
models = [m for m in MAIN_MODELS if (main_ai & (df.model == m).values).any()]
SEM_TIME = {"Pre-2021": 2020.2, "Spring 2021": 2021.2, "Fall 2021": 2021.8, "Spring 2022": 2022.2,
            "Fall 2022": 2022.8, "Spring 2023": 2023.2, "Fall 2023": 2023.8, "Fall 2024": 2024.8, "Fall 2025": 2025.8}
t = stu.group.map(SEM_TIME).values
results = {"representations": REPS,
           "counts": {"students": stu.group.value_counts().reindex(sem_order).to_dict(),
                      "ai": df[is_ai].group.value_counts().sort_index().to_dict()}}
fig_no = [0]


def save(fig, name):
    fig_no[0] += 1
    fig.savefig(FIG / f"{fig_no[0]:02d}_{name}.png")
    plt.close(fig)


def dense(M):
    return np.asarray(M.todense()) if sp.issparse(M) else np.asarray(M)


def sim_to(rep, mask):
    """Mean cosine similarity of every student to the AI files selected by mask."""
    centroid = np.asarray(X[rep][mask].mean(0)).ravel()
    return np.asarray(X[rep][stu_idx] @ centroid).ravel()


def zscore(v):
    return (v - v[pre_mask].mean()) / v[pre_mask].std()


def per_semester(values):
    g = pd.Series(values, index=stu.index).groupby(stu.group)
    return g.mean().reindex(sem_order), (1.96 * g.sem()).reindex(sem_order)


def chatgpt_line(ax, label=True):
    ax.axvline(chatgpt_x, color=MUTED, ls="--", lw=1)
    if label:
        ax.text(chatgpt_x + 0.07, 0.98, "ChatGPT\nreleased", transform=ax.get_xaxis_transform(),
                va="top", fontsize=7, color=MUTED)


def short_sem(s):
    return s.replace("Spring ", "S'").replace("Fall ", "F'").replace("20", "", 1).replace("Pre-21", "<2021") \
        if s != "Pre-2021" else "<2021"


def semester_axis(ax, short=False):
    ax.set_xticks(range(len(sem_order)))
    if short:
        ax.set_xticklabels([short_sem(s) for s in sem_order], fontsize=7)
    else:
        ax.set_xticklabels(sem_order, rotation=35, ha="right", fontsize=8.5)


def sem_colors():
    return [POST if s in ERA_MODEL else PRE for s in sem_order]


def dots_by_semester(ax, m, ci, ylabel="", short=False):
    ax.plot(range(len(m)), m.values, color="#c9c8c3", lw=1, zorder=1)
    ax.errorbar(range(len(m)), m.values, yerr=ci.values, fmt="none", ecolor=MUTED, lw=1, capsize=2.5, zorder=2)
    ax.scatter(range(len(m)), m.values, c=sem_colors(), s=42, zorder=3, edgecolor="white", lw=0.8)
    semester_axis(ax, short)
    ax.set_ylabel(ylabel)
    chatgpt_line(ax, label=not short)


def rep_grid(title, height=7.2):
    n = len(REPS)
    cols = 3 if n <= 6 else 4
    fig, axes = plt.subplots(int(np.ceil(n / cols)), cols, figsize=(5.2 * cols, height), squeeze=False)
    for ax in axes.ravel()[n:]:
        ax.axis("off")
    fig.suptitle(title, fontweight="bold", y=1.0)
    return fig, dict(zip(REPS, axes.ravel()))


def ols(y, cols):
    """OLS with intercept and HC1-robust SEs."""
    A = np.column_stack([np.ones(len(y))] + cols)
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    bread = np.linalg.inv(A.T @ A)
    cov = bread @ (A.T @ (A * resid[:, None] ** 2)) @ bread * len(y) / (len(y) - A.shape[1])
    return beta, np.sqrt(np.diag(cov))


def pre_post_tests(v):
    pre, post = v[pre_mask], v[~pre_mask]
    d = (post.mean() - pre.mean()) / np.sqrt((pre.var(ddof=1) + post.var(ddof=1)) / 2)
    boots = []
    for _ in range(1000):
        a, b = rng.choice(pre, len(pre)), rng.choice(post, len(post))
        boots.append((b.mean() - a.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2))
    return {"pre_mean": float(pre.mean()), "post_mean": float(post.mean()), "cohens_d": float(d),
            "d_ci": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
            "mannwhitney_p": float(stats.mannwhitneyu(post, pre, alternative="greater").pvalue),
            "spearman_rho_time": float(stats.spearmanr(t, v).statistic)}


sims = {rep: sim_to(rep, main_ai) for rep in REPS}
Z = {rep: zscore(sims[rep]) for rep in REPS}
consensus = np.mean([Z[r] for r in REPS], axis=0)

# ======================= Part 1: data =======================
fig, axes = plt.subplots(1, 2, figsize=(13, 4.2), gridspec_kw={"width_ratios": [1.4, 1]})
counts = stu.group.value_counts().reindex(sem_order)
axes[0].bar(range(len(counts)), counts.values, color=sem_colors(), width=0.68)
for i, v in enumerate(counts.values):
    axes[0].text(i, v + 2, str(v), ha="center", fontsize=8, color=INK)
semester_axis(axes[0])
chatgpt_line(axes[0])
axes[0].set_title(f"Student submissions: {len(stu)} across {len(sem_order)} semesters")
mc = [(MODEL_NAMES[m], int((main_ai & (df.model == m).values).sum()), CHATGPT if FAMILY[m] == "ChatGPT" else CLAUDE) for m in models]
axes[1].barh([x[0] for x in mc], [x[1] for x in mc], color=[x[2] for x in mc])
for i, x in enumerate(mc):
    axes[1].text(x[1] + 4, i, f"{x[1]}  ({MODEL_RELEASE[models[i]]})", va="center", fontsize=8)
axes[1].invert_yaxis()
axes[1].set_xlim(0, PER_MODEL * 1.45)
axes[1].set_title(f"AI generations: {sum(x[1] for x in mc)} (green = ChatGPT, terracotta = Claude)")
save(fig, "dataset")

fig, axes = plt.subplots(1, 2, figsize=(14, 4))
for col, label, color in [("spec_five_checkers", "Defines all 5 checkers (X O V H M)", "#2a78d6"),
                          ("spec_clear", "Clears screen with os.system('clear')", "#1baf7a"),
                          ("spec_random", "Uses random for first player", "#6250d6")]:
    m = stu.groupby("group")[col].mean().reindex(sem_order) * 100
    axes[0].plot(range(len(m)), m.values, marker="o", lw=2, ms=5, color=color, label=label)
semester_axis(axes[0])
chatgpt_line(axes[0])
axes[0].set_ylim(0, 105)
axes[0].set_ylabel("% of submissions")
axes[0].set_title("The assignment spec stayed stable across semesters")
axes[0].legend(frameon=False, fontsize=8, loc="lower left")
parses = stu.groupby("group").parses.mean().reindex(sem_order) * 100
ai_parse = [df[main_ai & (df.model == m).values].parses.mean() * 100 for m in models]
axes[1].bar(range(len(sem_order)), parses.values, color=sem_colors(), width=0.68)
axes[1].bar(np.arange(len(models)) + len(sem_order) + 0.6, ai_parse, color=[CHATGPT if FAMILY[m] == "ChatGPT" else CLAUDE for m in models], width=0.68)
axes[1].set_xticks(list(range(len(sem_order))) + list(np.arange(len(models)) + len(sem_order) + 0.6))
axes[1].set_xticklabels(sem_order + [MODEL_NAMES[m] for m in models], rotation=45, ha="right", fontsize=7.5)
axes[1].set_ylim(80, 101)
axes[1].set_ylabel("% syntactically valid Python")
axes[1].set_title("Almost all files parse, students and AI alike")
results["spec_stability"] = {c: (stu.groupby("group")[c].mean().reindex(sem_order) * 100).round(1).to_dict()
                             for c in ["spec_five_checkers", "spec_clear", "spec_random"]}
save(fig, "spec_and_validity")

fig, ax = plt.subplots(figsize=(12, 4.2))
data = [stu[stu.group == s].lines.values for s in sem_order] + [df[main_ai & (df.model == m).values].lines.values for m in models]
labels = sem_order + [MODEL_NAMES[m] for m in models]
bp = ax.boxplot(data, patch_artist=True, showfliers=False, widths=0.6, medianprops={"color": INK})
for patch, lab, k in zip(bp["boxes"], labels, range(len(labels))):
    if k < len(sem_order):
        patch.set_facecolor(POST if lab in ERA_MODEL else PRE)
    else:
        patch.set_facecolor(CHATGPT if FAMILY[models[k - len(sem_order)]] == "ChatGPT" else CLAUDE)
    patch.set_edgecolor("white")
ax.set_xticks(range(1, len(labels) + 1))
ax.set_xticklabels(labels, rotation=35, ha="right")
ax.axvline(len(sem_order) + 0.5, color=MUTED, lw=1)
ax.set_ylabel("Non-blank lines of code")
ax.set_title("Submission length: students by semester vs AI models (ChatGPT green, Claude terracotta)")
save(fig, "code_length")

# ======================= Part 2: is student code moving toward AI? =======================
results["similarity_to_ai"] = {rep: {"by_semester": per_semester(sims[rep])[0].round(4).to_dict(),
                                     **pre_post_tests(sims[rep])} for rep in REPS}
fig, axs = rep_grid("similarity of each semester's student code to AI code, under every representation")
for rep, ax in axs.items():
    m, ci = per_semester(sims[rep])
    dots_by_semester(ax, m, ci, "Cosine sim. to AI" if rep in FIRST_COL else "", short=True)
    r = results["similarity_to_ai"][rep]
    ax.set_title(f"{REPS[rep]}\nd = {r['cohens_d']:+.2f}, p = {r['mannwhitney_p']:.1e}")
fig.tight_layout()
save(fig, "similarity_to_ai_all_encoders")

fig, ax = plt.subplots(figsize=(9, 4.8))
for rep in REPS:
    m, _ = per_semester(Z[rep])
    ax.plot(range(len(m)), m.values, color="#b9b8b2", lw=1, zorder=1)
m, ci = per_semester(consensus)
ax.fill_between(range(len(m)), m - ci, m + ci, color=POST, alpha=0.15, lw=0)
ax.plot(range(len(m)), m.values, color=POST, lw=2.5, marker="o", ms=6, zorder=3, label="Average across all representations")
ax.plot([], [], color="#b9b8b2", lw=1, label="Each individual representation")
ax.axhline(0, color=MUTED, lw=1)
semester_axis(ax)
chatgpt_line(ax)
ax.set_ylabel("Similarity to AI\n(SDs above the pre-ChatGPT average)")
ax.set_title("Every representation agrees on the direction; the consensus rises after ChatGPT")
ax.legend(frameon=False, fontsize=8.5, loc="upper left", bbox_to_anchor=(0, 0.88))
results["consensus_by_semester"] = m.round(3).to_dict()
save(fig, "consensus_shift")

fig, ax = plt.subplots(figsize=(8.5, 4.6))
order = sorted(REPS, key=lambda r: results["similarity_to_ai"][r]["cohens_d"])
for i, rep in enumerate(order):
    r = results["similarity_to_ai"][rep]
    ax.errorbar(r["cohens_d"], i, xerr=[[r["cohens_d"] - r["d_ci"][0]], [r["d_ci"][1] - r["cohens_d"]]],
                fmt="o", color=POST, ms=7, capsize=3, lw=1.5)
    ax.text(r["d_ci"][1] + 0.02, i, f"{r['cohens_d']:+.2f}", va="center", fontsize=8.5, color=INK)
ax.axvline(0, color=MUTED, lw=1)
for x, lab in [(0.2, "small"), (0.5, "medium"), (0.8, "large")]:
    ax.axvline(x, color=LIGHT, lw=1, ls=":")
    ax.text(x, len(order) - 0.4, lab, fontsize=7, color=MUTED, ha="center")
ax.set_yticks(range(len(order)))
ax.set_yticklabels([REPS[r] for r in order])
ax.set_xlabel("Effect size (Cohen's d): post-ChatGPT vs pre-ChatGPT similarity to AI, 95% bootstrap CI")
ax.set_title("Headline effect size under every representation")
save(fig, "effect_size_forest")

fig, axs = rep_grid("how close is each submission to its single nearest AI 'twin'?")
results["nearest_ai_neighbour"] = {}
ai_rows = np.where(main_ai)[0]
for rep, ax in axs.items():
    mx = dense(X[rep][stu_idx] @ X[rep][ai_rows].T).max(1)
    m, ci = per_semester(mx)
    dots_by_semester(ax, m, ci, "Max cosine sim." if rep in FIRST_COL else "", short=True)
    r = pre_post_tests(mx)
    ax.set_title(f"{REPS[rep]}\nd = {r['cohens_d']:+.2f}")
    results["nearest_ai_neighbour"][rep] = {"by_semester": m.round(4).to_dict(), **r}
fig.tight_layout()
save(fig, "nearest_ai_twin")

fig, axs = rep_grid("interrupted time series: was similarity already rising before ChatGPT?")
results["interrupted_time_series"] = {}
grid_t = np.linspace(2020, 2026, 50)
for rep, ax in axs.items():
    z = Z[rep]
    lr = stats.linregress(t[pre_mask], z[pre_mask])
    m, ci = per_semester(z)
    xs = [SEM_TIME[s] for s in sem_order]
    ax.errorbar(xs, m.values, yerr=ci.values, fmt="none", ecolor=MUTED, lw=1, capsize=2)
    ax.scatter(xs, m.values, c=sem_colors(), s=36, zorder=3, edgecolor="white")
    ax.plot(grid_t, lr.intercept + lr.slope * grid_t, color=PRE, ls="--", lw=1.4)
    gap = z[~pre_mask] - (lr.intercept + lr.slope * t[~pre_mask])
    ax.axvline(2022.92, color=MUTED, ls=":", lw=1)
    ax.set_title(f"{REPS[rep]}\npre-slope {lr.slope:+.2f}/yr, gap above trend {gap.mean():+.2f} SD")
    results["interrupted_time_series"][rep] = {"pre_slope_per_year": lr.slope, "pre_slope_p": lr.pvalue,
                                               "post_gap_vs_trend_sd": float(gap.mean()),
                                               "post_gap_p": float(stats.ttest_1samp(gap, 0).pvalue)}
fig.tight_layout()
save(fig, "interrupted_time_series")

post = (~pre_mask).astype(float)
loglines = np.log(stu.lines.values.clip(1))
specs = [("No controls", lambda: [post]), ("+ code length", lambda: [post, loglines]),
         ("+ length + pre-existing trend", lambda: [post, loglines, t - 2020])]
results["controlled_effect"] = {}
fig, ax = plt.subplots(figsize=(9, 5.2))
for k, (name, cols) in enumerate(specs):
    for i, rep in enumerate(REPS):
        beta, se = ols(Z[rep], cols())
        results["controlled_effect"].setdefault(rep, {})[name] = {"post_effect_sd": beta[1], "ci95": 1.96 * se[1]}
        ax.errorbar(beta[1], i + (k - 1) * 0.22, xerr=1.96 * se[1], fmt="os^"[k], ms=6, capsize=2, lw=1.2,
                    color=["#b9b8b2", "#7fb0e8", POST][k], label=name if i == 0 else None)
ax.axvline(0, color=MUTED, lw=1)
ax.set_yticks(range(len(REPS)))
ax.set_yticklabels(REPS.values())
ax.invert_yaxis()
ax.set_xlabel("Post-ChatGPT jump in similarity to AI (pre-ChatGPT SDs, 95% CI)")
ax.set_title("The jump survives controls for code length and any pre-existing trend")
ax.legend(frameon=False, fontsize=8, loc="lower right")
save(fig, "controlled_effect")

# ======================= Part 3: ChatGPT vs Claude, and which model =======================
fam_mask = {f: main_ai & (df.model.map(FAMILY) == f).values for f in ("ChatGPT", "Claude")}
fig, axs = rep_grid("similarity to ChatGPT-generated vs Claude-generated code (SDs vs pre-ChatGPT)")
results["family"] = {}
for rep, ax in axs.items():
    for fam, color in [("ChatGPT", CHATGPT), ("Claude", CLAUDE)]:
        m, ci = per_semester(zscore(sim_to(rep, fam_mask[fam])))
        ax.plot(range(len(m)), m.values, marker="o", ms=4, lw=1.8, color=color, label=fam)
        ax.fill_between(range(len(m)), m - ci, m + ci, color=color, alpha=0.12, lw=0)
        results["family"].setdefault(rep, {})[fam] = m.round(3).to_dict()
    ax.axhline(0, color=MUTED, lw=1)
    semester_axis(ax, short=True)
    chatgpt_line(ax, label=False)
    ax.set_title(REPS[rep])
axs["lexical"].legend(frameon=False, fontsize=8)
fig.tight_layout()
save(fig, "chatgpt_vs_claude")

model_z = {rep: {m: zscore(sim_to(rep, main_ai & (df.model == m).values)) for m in models} for rep in REPS}
grid = pd.DataFrame({MODEL_NAMES[m]: per_semester(np.mean([model_z[r][m] for r in REPS], axis=0))[0] for m in models})
results["semester_by_model_consensus"] = grid.round(3).to_dict()
fig, ax = plt.subplots(figsize=(10, 5.6))
lim = np.abs(grid.values).max()
im = ax.imshow(grid.values, cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto")
ax.set_xticks(range(len(grid.columns)))
ax.set_xticklabels([f"{c}\n({MODEL_RELEASE[m]})" for c, m in zip(grid.columns, models)], fontsize=8)
ax.set_yticks(range(len(grid)))
ax.set_yticklabels(grid.index)
ax.grid(False)
for i, s in enumerate(grid.index):
    for j, m in enumerate(models):
        v = grid.values[i, j]
        unavailable = SEMESTERS.index(AVAILABLE_FROM[m]) > SEMESTERS.index(s)
        ax.text(j, i, f"{v:+.2f}" + ("*" if unavailable and s in ERA_MODEL else ""), ha="center", va="center",
                fontsize=8, color="white" if abs(v) > lim * 0.6 else INK, fontweight="bold" if ERA_MODEL.get(s) == m else "normal")
        if ERA_MODEL.get(s) == m:
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, lw=2, ec=INK))
ax.axhline(sem_pos[FIRST_AI_SEMESTER] - 0.5, color=INK, lw=1.5)
fig.colorbar(im, ax=ax, label="Similarity, SDs vs pre-ChatGPT (avg of all representations)")
ax.set_title("Every semester vs every model (boxed = most popular model that semester;\n"
             "* = model not released yet when those students submitted)")
save(fig, "semester_model_heatmap")

fig, axs = rep_grid("Appendix A: semester × model heatmap under each representation", height=9)
for rep, ax in axs.items():
    g = pd.DataFrame({MODEL_NAMES[m]: per_semester(model_z[rep][m])[0] for m in models})
    lim_r = np.abs(g.values).max()
    ax.imshow(g.values, cmap="RdBu_r", vmin=-lim_r, vmax=lim_r, aspect="auto")
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels([MODEL_NAMES[m].replace("Claude ", "") for m in models], rotation=60, ha="right", fontsize=6.5)
    ax.set_yticks(range(len(sem_order)))
    ax.set_yticklabels([short_sem(s) for s in sem_order], fontsize=7)
    ax.grid(False)
    ax.axhline(sem_pos[FIRST_AI_SEMESTER] - 0.5, color=INK, lw=1)
    ax.set_title(REPS[rep])
fig.tight_layout()
save(fig, "appendix_heatmaps_by_encoder")

fig, ax = plt.subplots(figsize=(11, 5))
post_sems = [s for s in sem_order if s in ERA_MODEL]
results["release_placebo"] = {}
for k, s in enumerate(post_sems):
    sem_mask = (stu.group == s).values
    for j, m in enumerate(models):
        v = np.mean([model_z[r][m][sem_mask].mean() for r in REPS])
        available = SEMESTERS.index(AVAILABLE_FROM[m]) <= SEMESTERS.index(s)
        x = k + (j - (len(models) - 1) / 2) * 0.09
        ax.scatter(x, v, s=70, color=MODEL_COLORS[m] if available else "white", edgecolor=MODEL_COLORS[m],
                   lw=1.8, zorder=3, label=MODEL_NAMES[m] if k == 0 else None)
        results["release_placebo"].setdefault(s, {})[MODEL_NAMES[m]] = {"z": float(v), "available": available}
ax.axhline(0, color=MUTED, lw=1)
ax.set_xticks(range(len(post_sems)))
ax.set_xticklabels(post_sems)
ax.set_ylabel("Similarity to the model\n(SDs vs pre-ChatGPT, avg of all representations)")
ax.set_title("Release-date placebo: filled = model existed that semester, hollow = released later")
ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
save(fig, "release_date_placebo")

# ======================= Part 4: how many students? =======================
train = np.r_[np.where(main_ai)[0], stu_idx[pre_mask]]
y = np.r_[np.ones(main_ai.sum()), np.zeros(pre_mask.sum())]
style = StandardScaler().fit_transform(df[STYLE_COLS].values)
inputs = {**{r: X[r] for r in REPS}, "style": style}
cv = StratifiedKFold(5, shuffle=True, random_state=0)
Pr, lex_coefs = {}, None
results["classifier"] = {}
for name, Xi in inputs.items():
    clf = LogisticRegression(max_iter=5000, C=1.0, class_weight="balanced")
    p = np.full(len(df), np.nan)
    p[train] = cross_val_predict(clf, Xi[train], y, cv=cv, method="predict_proba")[:, 1]
    rest = np.setdiff1d(np.arange(len(df)), train)
    clf.fit(Xi[train], y)
    p[rest] = clf.predict_proba(Xi[rest])[:, 1]
    if name == "lexical":
        lex_coefs = clf.coef_[0]
    Pr[name] = p
    results["classifier"][name] = {"cv_auc": float(roc_auc_score(y, p[train]))}
Pr["ensemble"] = np.mean([Pr[k] for k in inputs], axis=0)
# Prompt-variant files have no neural embeddings, so anything evaluated on them uses the lexical+AST+style ensemble.
Pr["text_ensemble"] = np.mean([Pr[k] for k in ("lexical", "ast", "style")], axis=0)
for k in ("ensemble", "text_ensemble"):
    results["classifier"][k] = {"cv_auc": float(roc_auc_score(y, Pr[k][train]))}
flag = {k: v > 0.5 for k, v in Pr.items()}
fpr = {k: float(flag[k][stu_idx[pre_mask]].mean()) for k in Pr}
tpr = {k: float(flag[k][main_ai].mean()) for k in Pr}
tpr_disguise = {k: float(flag[k][is_ai & (df.variant == "disguise").values].mean()) for k in Pr}
for k in Pr:
    rate = pd.Series(flag[k][stu_idx], index=stu.index).groupby(stu.group).mean().reindex(sem_order) * 100
    results["classifier"][k].update(fpr=fpr[k], tpr=tpr[k], tpr_disguise=tpr_disguise[k], pct_flagged=rate.round(1).to_dict())

fig, ax = plt.subplots(figsize=(11, 4.8))
for k in inputs:
    rate = pd.Series(results["classifier"][k]["pct_flagged"]).reindex(sem_order)
    ax.plot(range(len(sem_order)), rate.values, color="#c9c8c3", lw=1, marker="o", ms=3)
rate = pd.Series(results["classifier"]["ensemble"]["pct_flagged"]).reindex(sem_order)
ax.plot(range(len(sem_order)), rate.values, color=INK, lw=2.5, marker="o", ms=6, label="Ensemble of all classifiers")
for i, v in enumerate(rate.values):
    ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=8, color=INK)
ax.plot([], [], color="#c9c8c3", lw=1, marker="o", ms=3, label="Each single classifier")
semester_axis(ax)
chatgpt_line(ax)
ax.set_ylabel("% of submissions classified AI-like")
ax.set_title("Share of submissions flagged by AI-vs-student classifiers\n"
             "(pre-ChatGPT values are out-of-fold false positives)")
ax.legend(frameon=False, fontsize=8.5, loc="upper left", bbox_to_anchor=(0, 0.86))
save(fig, "classifier_flag_rate")

fig, ax = plt.subplots(figsize=(8, 4.6))
names = list(inputs) + ["ensemble"]
aucs = [results["classifier"][k]["cv_auc"] for k in names]
fprs = [fpr[k] * 100 for k in names]
ax.barh([REPS.get(k, {"style": "Style features", "ensemble": "Ensemble"}.get(k)) for k in names], fprs,
        color=[INK if k == "ensemble" else POST for k in names])
for i, (a, f) in enumerate(zip(aucs, fprs)):
    ax.text(f + 0.1, i, f"FPR {f:.1f}%  ·  AUC {a:.3f}", va="center", fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("False-positive rate on pre-ChatGPT students (%)")
ax.set_xlim(0, max(fprs) * 1.9 + 1)
ax.set_title("Classifier accuracy (5-fold cross-validated)")
save(fig, "classifier_accuracy")


def prevalence(flags, fpr_, tpr_):
    return np.clip((flags.mean() - fpr_) / (tpr_ - fpr_), 0, 1)


fig, ax = plt.subplots(figsize=(10, 4.8))
results["prevalence"] = {}
for label, clf_name, tp, color, offset in [
        (f"If students pasted the assignment (full ensemble, recall {tpr['ensemble']:.0%})", "ensemble", tpr["ensemble"], POST, -0.12),
        (f"If students asked for human-looking code (text ensemble, recall {tpr_disguise['text_ensemble']:.0%})",
         "text_ensemble", tpr_disguise["text_ensemble"], "#6250d6", 0.12)]:
    est, lo, hi = [], [], []
    for s in sem_order:
        f = flag[clf_name][stu_idx[(stu.group == s).values]]
        boots = [prevalence(rng.choice(f, len(f)), fpr[clf_name], tp) for _ in range(2000)]
        est.append(prevalence(f, fpr[clf_name], tp) * 100)
        lo.append(np.percentile(boots, 2.5) * 100)
        hi.append(np.percentile(boots, 97.5) * 100)
    est, lo, hi = map(np.array, (est, lo, hi))
    ax.errorbar(np.arange(len(sem_order)) + offset, est, yerr=[est - lo, hi - est], fmt="o", color=color, ms=6,
                capsize=3, lw=1.3, label=label)
    results["prevalence"][label] = {s: {"est": e, "lo": a, "hi": b} for s, e, a, b in zip(sem_order, est, lo, hi)}
semester_axis(ax)
chatgpt_line(ax)
ax.set_ylim(-3, max(60, float(np.max(hi)) + 10))
ax.set_ylabel("Estimated % AI-assisted\n(false-positive corrected, 95% CI)")
ax.set_title("Estimated share of AI-assisted submissions per semester (Rogan-Gladen correction)")
ax.legend(frameon=False, fontsize=8, loc="upper left")
save(fig, "estimated_ai_prevalence")

fig, ax = plt.subplots(figsize=(10, 4.4))
parts = ax.violinplot([Pr["ensemble"][stu_idx[(stu.group == s).values]] for s in sem_order],
                      positions=range(len(sem_order)), showmedians=True, widths=0.8)
for body, c in zip(parts["bodies"], sem_colors()):
    body.set_facecolor(c)
    body.set_alpha(0.65)
for key in ("cmedians", "cmins", "cmaxes", "cbars"):
    parts[key].set_color(MUTED)
    parts[key].set_linewidth(1)
ax.axhline(0.5, color=MUTED, ls=":", lw=1)
semester_axis(ax)
chatgpt_line(ax)
ax.set_ylabel("P(AI), ensemble")
ax.set_title("The distribution shifts: post-ChatGPT semesters grow a high-probability tail")
save(fig, "ai_probability_distribution")

vocab = json.loads((ROOT / "vocab.json").read_text())
order = np.argsort(lex_coefs)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for ax, idx, color, title in [(axes[0], order[::-1][:18], AI, "Token patterns that signal AI"),
                              (axes[1], order[:18], PRE, "Token patterns that signal a pre-ChatGPT student")]:
    ax.barh([vocab["lexical"][i][:42] for i in idx], np.abs(lex_coefs[idx]), color=color)
    ax.invert_yaxis()
    ax.set_title(title)
    ax.set_xlabel("|logistic-regression weight|")
    ax.tick_params(axis="y", labelsize=8)
fig.suptitle("What the lexical classifier keys on (STR = string literal, NUM = number)", fontweight="bold", y=1.01)
save(fig, "top_distinguishing_tokens")
results["top_tokens"] = {"ai": [vocab["lexical"][i] for i in order[::-1][:25]], "human": [vocab["lexical"][i] for i in order[:25]]}

variant_models = [m for m in models if (is_ai & (df.model == m).values & (df.variant == "disguise").values).any()]
fig, ax = plt.subplots(figsize=(10, 4.2))
results["detection_by_prompt"] = {}
for k, var in enumerate(["assignment", "short", "disguise"]):
    rates = [flag["text_ensemble"][is_ai & (df.model == m).values & (df.variant == var).values].mean() * 100 for m in variant_models]
    ax.bar(np.arange(len(variant_models)) + (k - 1) * 0.27, rates, 0.27, color=VARIANT_COLORS[var], label=VARIANT_NAMES[var])
    results["detection_by_prompt"][var] = dict(zip([MODEL_NAMES[m] for m in variant_models], rates))
ax.set_xticks(range(len(variant_models)))
ax.set_xticklabels([MODEL_NAMES[m] for m in variant_models])
ax.set_ylabel("% detected as AI")
ax.set_ylim(0, 105)
ax.set_title("Detection under prompts the classifier never trained on (lexical+AST+style ensemble)")
ax.legend(frameon=False, fontsize=8, loc="lower left")
save(fig, "detection_by_prompt")

# ======================= Part 5: style =======================
fig, axes = plt.subplots(3, 5, figsize=(19, 10))
results["style_by_semester"] = {}
for ax, col in zip(axes.ravel(), STYLE_COLS):
    m, ci = per_semester(stu[col].values)
    ax.errorbar(range(len(m)), m.values, yerr=ci.values, color=POST, marker="o", ms=4, lw=1.5, capsize=2)
    ax.axhline(df[fam_mask["ChatGPT"]][col].mean(), color=CHATGPT, lw=1.5, ls="--")
    ax.axhline(df[fam_mask["Claude"]][col].mean(), color=CLAUDE, lw=1.5, ls="--")
    ax.axvline(chatgpt_x, color=MUTED, ls=":", lw=1)
    semester_axis(ax, short=True)
    rho = stats.spearmanr(t, stu[col].values)
    ax.set_title(STYLE_LABELS[col], fontsize=9)
    ax.text(0.02, 0.97, f"ρ={rho.statistic:+.2f}", transform=ax.transAxes, va="top", fontsize=7.5, color=MUTED)
    results["style_by_semester"][col] = {**m.round(3).to_dict(), "ChatGPT_mean": float(df[fam_mask["ChatGPT"]][col].mean()),
                                         "Claude_mean": float(df[fam_mask["Claude"]][col].mean()),
                                         "spearman_rho": float(rho.statistic), "p": float(rho.pvalue)}
axes[0, 0].legend(["Students (95% CI)", "ChatGPT average", "Claude average"], frameon=False, fontsize=7)
fig.suptitle("Coding-style habits by semester vs ChatGPT and Claude averages", fontweight="bold")
fig.tight_layout()
save(fig, "style_features_by_semester")

fig, axes = plt.subplots(3, 5, figsize=(19, 10))
for ax, col in zip(axes.ravel(), STYLE_COLS):
    vals = [df[main_ai & (df.model == m).values][col].mean() for m in models] + [stu[pre_mask][col].mean(), stu[~pre_mask][col].mean()]
    labels = [MODEL_NAMES[m] for m in models] + ["Students, pre", "Students, post"]
    ax.barh(labels, vals, color=[CHATGPT if FAMILY[m] == "ChatGPT" else CLAUDE for m in models] + [PRE, POST])
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=7)
    ax.set_title(STYLE_LABELS[col], fontsize=9)
fig.suptitle("Each model's style fingerprint vs students before and after ChatGPT", fontweight="bold")
fig.tight_layout()
save(fig, "style_features_by_model")

pre_sd = stu[pre_mask][STYLE_COLS].std().replace(0, 1)
ai_z = (df[main_ai][STYLE_COLS].mean() - stu[pre_mask][STYLE_COLS].mean()) / pre_sd
post_z = (stu[~pre_mask][STYLE_COLS].mean() - stu[pre_mask][STYLE_COLS].mean()) / pre_sd
fig, ax = plt.subplots(figsize=(9, 6))
idx = np.argsort(ai_z.values)
ax.barh(np.arange(len(idx)) + 0.2, ai_z.values[idx], 0.4, color=AI, label="AI generations (all models)")
ax.barh(np.arange(len(idx)) - 0.2, post_z.values[idx], 0.4, color=POST, label="Post-ChatGPT students")
ax.set_yticks(range(len(idx)))
ax.set_yticklabels([STYLE_LABELS[STYLE_COLS[i]] for i in idx], fontsize=8)
ax.axvline(0, color=MUTED, lw=1)
ax.set_xlabel("Difference from pre-ChatGPT students (SDs)")
agree = float(np.mean(np.sign(ai_z.values) == np.sign(post_z.values)))
ax.set_title(f"Students drift in AI's direction on {agree:.0%} of style features,\nbut only part of the way")
ax.legend(frameon=False, fontsize=8)
results["style_direction_agreement"] = agree
save(fig, "style_shift_direction")

fig, axs = rep_grid("are classmates' submissions becoming more alike each other?")
results["classmate_similarity"] = {}
for rep, ax in axs.items():
    vals, cis = [], []
    for s in sem_order:
        M = X[rep][stu_idx[(stu.group == s).values]]
        S = dense(M @ M.T)
        per_student = (S.sum(1) - np.diag(S)) / (len(S) - 1)
        vals.append(per_student.mean())
        cis.append(1.96 * per_student.std() / np.sqrt(len(S)))
    dots_by_semester(ax, pd.Series(vals, index=sem_order), pd.Series(cis, index=sem_order),
                     "Sim. to classmates" if rep in FIRST_COL else "", short=True)
    ax.set_title(REPS[rep])
    results["classmate_similarity"][rep] = dict(zip(sem_order, map(float, vals)))
fig.tight_layout()
save(fig, "classmate_homogeneity")

fig, ax = plt.subplots(figsize=(7.5, 6))
C = np.corrcoef([sims[r] for r in REPS])
im = ax.imshow(C, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(len(REPS)))
ax.set_xticklabels(REPS.values(), rotation=45, ha="right", fontsize=8)
ax.set_yticks(range(len(REPS)))
ax.set_yticklabels(REPS.values(), fontsize=8)
ax.grid(False)
for i in range(len(REPS)):
    for j in range(len(REPS)):
        ax.text(j, i, f"{C[i, j]:.2f}", ha="center", va="center", fontsize=7.5, color="white" if C[i, j] > 0.6 else INK)
fig.colorbar(im, ax=ax, label="Pearson r across students")
ax.set_title("Do the representations agree on WHICH students look AI-like?")
results["encoder_agreement"] = pd.DataFrame(C, index=list(REPS), columns=list(REPS)).round(3).to_dict()
save(fig, "encoder_agreement")

# ======================= Part 6: PCA maps and clustering =======================
fit_rows = main_ai | ~is_ai
pcs = {}
for rep in REPS:
    Xr = X[rep] if rep not in ("lexical", "ast") else normalize(dense(X[rep]) - dense(X[rep][fit_rows]).mean(0))
    pca = PCA(2, random_state=0).fit(Xr[fit_rows])
    pcs[rep] = (pca.transform(Xr), pca.explained_variance_ratio_)

ai_cluster_share = {}
for rep in REPS:
    Xr = X[rep] if rep not in ("lexical", "ast") else normalize(dense(X[rep]))
    rows_fit = np.where(fit_rows)[0]
    km = KMeans(12, n_init=10, random_state=0).fit(Xr[rows_fit])
    lab = np.full(len(df), -1)
    lab[rows_fit] = km.labels_
    ai_frac = pd.Series(is_ai[rows_fit]).groupby(km.labels_).mean()
    ai_clusters = set(ai_frac[ai_frac >= 0.8].index)
    share = pd.Series(np.isin(lab[stu_idx], list(ai_clusters)), index=stu.index).groupby(stu.group).mean().reindex(sem_order) * 100
    ai_cluster_share[rep] = share
results["ai_cluster_share"] = {r: s.round(1).to_dict() for r, s in ai_cluster_share.items()}

for rep in REPS:
    P2, var = pcs[rep]
    fig, axes = plt.subplots(3, 3, figsize=(13, 12), sharex=True, sharey=True)
    ai_c = P2[main_ai].mean(0)
    for ax, s in zip(axes.ravel(), sem_order):
        sm = stu_idx[(stu.group == s).values]
        ax.scatter(*P2[main_ai].T, s=5, color=AI, alpha=0.12, edgecolor="none")
        ax.scatter(*P2[stu_idx[pre_mask]].T, s=5, color=LIGHT, alpha=0.9, edgecolor="none")
        color = POST if s in ERA_MODEL else PRE
        ax.scatter(*P2[sm].T, s=14, color=color, alpha=0.85, edgecolor="white", lw=0.3)
        c = P2[sm].mean(0)
        ax.scatter(*ai_c, s=170, marker="*", color=AI, edgecolor=INK, lw=0.7, zorder=5)
        ax.scatter(*c, s=90, marker="X", color=color, edgecolor=INK, lw=0.7, zorder=5)
        ax.set_title(f"{s}  (n={len(sm)}, {ai_cluster_share[rep][s]:.0f}% in AI clusters)", fontsize=9.5)
    for ax in axes[-1]:
        ax.set_xlabel(f"PC1 ({var[0]:.0%})")
    for ax in axes[:, 0]:
        ax.set_ylabel(f"PC2 ({var[1]:.0%})")
    fig.suptitle(f"PCA map, semester by semester: {REPS[rep]}\norange haze = AI generations, light grey = all pre-ChatGPT "
                 "students, X = semester centre, ★ = AI centre", fontweight="bold")
    fig.tight_layout()
    save(fig, f"pca_by_semester_{rep}")

fig, axs = rep_grid("PCA overview: AI (orange), pre-ChatGPT students (grey), post-ChatGPT students (blue)", height=8)
for rep, ax in axs.items():
    P2, var = pcs[rep]
    ax.scatter(*P2[main_ai].T, s=4, color=AI, alpha=0.25, edgecolor="none")
    ax.scatter(*P2[stu_idx[pre_mask]].T, s=7, color=PRE, alpha=0.7, edgecolor="none")
    ax.scatter(*P2[stu_idx[~pre_mask]].T, s=7, color=POST, alpha=0.7, edgecolor="none")
    ax.set_title(f"{REPS[rep]}  (PC1+2 = {var.sum():.0%} var.)")
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout()
save(fig, "pca_overview_all_encoders")

fig, axs = rep_grid("path of the average student submission through each encoder's PCA space "
                    "(green ★ = ChatGPT centre, terracotta ★ = Claude centre)", height=8)
for rep, ax in axs.items():
    P2, _ = pcs[rep]
    ax.scatter(*P2[stu_idx].T, s=4, color=LIGHT, edgecolor="none")
    for fam, color in [("ChatGPT", CHATGPT), ("Claude", CLAUDE)]:
        ax.scatter(*P2[fam_mask[fam]].mean(0), s=200, marker="*", color=color, edgecolor=INK, lw=0.6, zorder=4)
    cents = np.array([P2[stu_idx[(stu.group == s).values]].mean(0) for s in sem_order])
    ax.plot(*cents.T, color=MUTED, lw=1, zorder=3)
    ax.scatter(*cents.T, c=sem_colors(), s=36, edgecolor=INK, lw=0.5, zorder=5)
    ax.annotate(short_sem(sem_order[0]), cents[0], xytext=(4, -9), textcoords="offset points", fontsize=7)
    ax.annotate(short_sem(sem_order[-1]), cents[-1], xytext=(4, 4), textcoords="offset points", fontsize=7)
    ax.set_title(REPS[rep])
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout()
save(fig, "semester_centroid_paths")

fig, ax = plt.subplots(figsize=(10, 4.8))
for rep in REPS:
    ax.plot(range(len(sem_order)), ai_cluster_share[rep].values, color="#c9c8c3", lw=1, marker="o", ms=3)
mean_share = pd.concat(ai_cluster_share, axis=1).mean(1)
ax.plot(range(len(sem_order)), mean_share.values, color=INK, lw=2.5, marker="o", ms=6, label="Average across representations")
ax.plot([], [], color="#c9c8c3", lw=1, label="Each representation")
for i, v in enumerate(mean_share.values):
    ax.text(i, v + 1.2, f"{v:.0f}%", ha="center", fontsize=8)
semester_axis(ax)
chatgpt_line(ax)
ax.set_ylabel("% of students in AI-dominated clusters")
ax.set_title("Unsupervised check: k-means (k=12) on students + AI;\nshare of students landing in clusters that are ≥80% AI")
ax.legend(frameon=False, fontsize=8.5, loc="upper left", bbox_to_anchor=(0, 0.86))
results["ai_cluster_share_mean"] = mean_share.round(1).to_dict()
save(fig, "ai_cluster_share")

# ======================= Part 7: prompts and other vendors =======================
fig, ax = plt.subplots(figsize=(9.5, 4.6))
results["prompt_sensitivity"] = {}
for var in ["assignment", "short", "disguise"]:
    mask = is_ai & (df.variant == var).values & df.model.isin(variant_models).values
    m, ci = per_semester(np.mean([zscore(sim_to(r, mask)) for r in TEXT_REPS], axis=0))
    ax.plot(range(len(m)), m.values, marker="o", ms=5, lw=2, color=VARIANT_COLORS[var], label=VARIANT_NAMES[var])
    ax.fill_between(range(len(m)), m - ci, m + ci, color=VARIANT_COLORS[var], alpha=0.1, lw=0)
    results["prompt_sensitivity"][var] = m.round(3).to_dict()
ax.axhline(0, color=MUTED, lw=1)
semester_axis(ax)
chatgpt_line(ax)
ax.set_ylabel("Similarity (pre-ChatGPT SDs,\navg of lexical + AST)")
ax.set_title("The post-ChatGPT shift appears however the AI was prompted")
ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0, 0.88))
save(fig, "prompt_sensitivity")

others = [m for m in OTHER_MODELS if (is_ai & (df.model == m).values & (df.variant == "assignment").values).any()]
if others:
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    pools = {"ChatGPT models": (fam_mask["ChatGPT"], CHATGPT), "Claude models": (fam_mask["Claude"], CLAUDE)}
    for m, c in zip(others, ["#6250d6", "#eda100", "#8a8985"]):
        pools[MODEL_NAMES[m]] = (is_ai & (df.model == m).values & (df.variant == "assignment").values, c)
    results["other_vendors"] = {}
    for name, (mask, color) in pools.items():
        m, _ = per_semester(np.mean([zscore(sim_to(r, mask)) for r in TEXT_REPS], axis=0))
        ax.plot(range(len(m)), m.values, marker="o", ms=4, lw=2 if "models" in name else 1.3, color=color, label=name,
                ls="-" if "models" in name else "--")
        results["other_vendors"][name] = m.round(3).to_dict()
    ax.axhline(0, color=MUTED, lw=1)
    semester_axis(ax)
    chatgpt_line(ax)
    ax.set_ylabel("Similarity (pre-ChatGPT SDs)")
    ax.set_title("Appendix B: other vendors (Gemini, DeepSeek, Llama), lexical + AST")
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0, 0.88))
    save(fig, "appendix_other_vendors")

# ======================= Part 8: advanced tests of the semester-by-semester trend =======================
import builtins
import io
import keyword
import tokenize
import zlib

from sklearn.decomposition import TruncatedSVD

sem_arrays = lambda v, sems: [v[(stu.group == s).values] for s in sems]
pre_sems = [s for s in sem_order if s not in ERA_MODEL]


def jonckheere(v, sems):
    """Jonckheere-Terpstra test for an increasing trend across ordered groups (normal approximation)."""
    arrs = sem_arrays(v, sems)
    J = sum(stats.mannwhitneyu(arrs[j], arrs[i]).statistic for i in range(len(arrs)) for j in range(i + 1, len(arrs)))
    n = np.array([len(a) for a in arrs])
    N = n.sum()
    mean = (N ** 2 - (n ** 2).sum()) / 4
    var = (N ** 2 * (2 * N + 3) - (n ** 2 * (2 * n + 3)).sum()) / 72
    zj = (J - mean) / np.sqrt(var)
    return float(zj), float(stats.norm.sf(zj))


def holm(ps):
    order = np.argsort(ps)
    adj = np.empty(len(ps))
    running = 0
    for rank, i in enumerate(order):
        running = max(running, min(1, (len(ps) - rank) * ps[i]))
        adj[i] = running
    return adj


results["trend_tests"] = {}
fig, ax = plt.subplots(figsize=(10, 5))
for i, rep in enumerate(list(REPS) + ["consensus"]):
    v = consensus if rep == "consensus" else Z[rep]
    row = {name: jonckheere(v, sems) for name, sems in
           [("all semesters", sem_order), ("post-ChatGPT only", post_sems), ("pre-ChatGPT only (placebo)", pre_sems)]}
    results["trend_tests"][rep] = row
    for k, (name, (zj, p)) in enumerate(row.items()):
        ax.scatter(zj, i + (k - 1) * 0.22, s=55, marker="os^"[k], color=[POST, "#1baf7a", PRE][k],
                   label=name if i == 0 else None, zorder=3)
ax.axvline(1.645, color=MUTED, ls=":", lw=1)
ax.text(1.7, -0.9, "p = 0.05", fontsize=7.5, color=MUTED)
ax.axvline(0, color=MUTED, lw=1)
ax.set_yticks(range(len(REPS) + 1))
ax.set_yticklabels(list(REPS.values()) + ["Consensus (average)"])
ax.invert_yaxis()
ax.set_xlabel("Jonckheere-Terpstra z for an increasing trend across ordered semesters")
ax.set_title("Advanced 1: ordered-trend test: does similarity to AI rise semester after semester?")
ax.legend(frameon=False, fontsize=8, loc="lower right")
save(fig, "trend_test_jonckheere")

pairs = list(zip(sem_order[:-1], sem_order[1:]))
raw_p = [stats.mannwhitneyu(consensus[(stu.group == b).values], consensus[(stu.group == a).values], alternative="greater").pvalue
         for a, b in pairs]
adj_p = holm(np.array(raw_p))
m_cons, ci_cons = per_semester(consensus)
fig, ax = plt.subplots(figsize=(11, 4.8))
dots_by_semester(ax, m_cons, ci_cons, "Consensus similarity to AI (SDs)")
for k, ((a, b), p) in enumerate(zip(pairs, adj_p)):
    y_top = max(m_cons[a] + ci_cons[a], m_cons[b] + ci_cons[b]) + 0.12
    txt = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
    ax.annotate("", xy=(k + 1, y_top), xytext=(k, y_top), arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1})
    ax.text(k + 0.5, y_top + 0.04, txt, ha="center", fontsize=8, color=INK if p < 0.05 else MUTED)
ax.set_ylim(m_cons.min() - 0.5, (m_cons + ci_cons).max() + 0.45)
ax.set_title("Advanced 2: semester-to-semester steps (one-sided Mann-Whitney, Holm-corrected)")
results["adjacent_steps"] = {f"{a} -> {b}": {"p_raw": float(r), "p_holm": float(h)} for (a, b), r, h in zip(pairs, raw_p, adj_p)}
save(fig, "adjacent_semester_steps")


def reduced(rep, dims=64):
    if sp.issparse(X[rep]):
        return normalize(TruncatedSVD(dims, random_state=0).fit(X[rep][core]).transform(X[rep]))
    return normalize(PCA(dims, random_state=0).fit(X[rep][core]).transform(X[rep]))


ai_sample = rng.choice(np.where(main_ai)[0], 400, replace=False)
metric_sem = {}
results["mmd"], results["separability_auc"], results["knn_ai_share"] = {}, {}, {}
for rep in REPS:
    R = reduced(rep)
    S_idx = np.r_[stu_idx, ai_sample]
    D = np.clip(2 - 2 * R[S_idx] @ R[S_idx].T, 0, None)
    gamma = 1 / np.median(D[np.triu_indices(len(D), 1)])
    K = np.exp(-gamma * D)
    n_stu = len(stu_idx)
    Kaa = K[n_stu:, n_stu:]
    aa = (Kaa.sum() - np.trace(Kaa)) / (len(Kaa) * (len(Kaa) - 1))
    mmd, mmd_ci = {}, {}
    for s in sem_order:
        loc = np.where((stu.group == s).values)[0]

        def mmd2(ix):
            Kss = K[np.ix_(ix, ix)]
            ss = (Kss.sum() - np.trace(Kss)) / (len(ix) * (len(ix) - 1))
            return ss + aa - 2 * K[np.ix_(ix, np.arange(n_stu, len(K)))].mean()
        mmd[s] = float(mmd2(loc))
        boots = [mmd2(rng.choice(loc, len(loc))) for _ in range(150)]
        mmd_ci[s] = (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))
    results["mmd"][rep] = {"mmd2": mmd, "ci": mmd_ci}

    aucs = {}
    for s in sem_order:
        loc = stu_idx[(stu.group == s).values]
        vals = []
        for seed in range(3):
            ai_pick = np.random.default_rng(seed).choice(np.where(main_ai)[0], len(loc), replace=False)
            Xi = X[rep][np.r_[loc, ai_pick]]
            yi = np.r_[np.zeros(len(loc)), np.ones(len(loc))]
            pr = cross_val_predict(LogisticRegression(max_iter=3000), Xi, yi,
                                   cv=StratifiedKFold(5, shuffle=True, random_state=seed), method="predict_proba")[:, 1]
            vals.append(roc_auc_score(yi, pr))
        aucs[s] = float(np.mean(vals))
    results["separability_auc"][rep] = aucs

    pool = np.r_[stu_idx[pre_mask], rng.choice(np.where(main_ai)[0], pre_mask.sum(), replace=False)]
    pool_ai = is_ai[pool]
    sims_pool = R[stu_idx] @ R[pool].T
    sims_pool[np.equal.outer(stu_idx, pool)] = -np.inf
    nn = np.argsort(-sims_pool, axis=1)[:, :20]
    share = pool_ai[nn].mean(1) * 100
    results["knn_ai_share"][rep] = per_semester(share)[0].round(2).to_dict()
    metric_sem.setdefault("Similarity to AI centroid", {})[rep] = per_semester(sims[rep])[0]
    metric_sem.setdefault("Distribution distance to AI (MMD, lower = closer)", {})[rep] = -pd.Series(mmd).reindex(sem_order)
    metric_sem.setdefault("Separability from AI (1 - AUC)", {})[rep] = 1 - pd.Series(aucs).reindex(sem_order)
    metric_sem.setdefault("AI share of 20 nearest neighbours", {})[rep] = per_semester(share)[0]

fig, axs = rep_grid("Advanced 3: distribution distance (MMD²) between each semester's students and AI code. Lower = closer")
for rep, ax in axs.items():
    m = pd.Series(results["mmd"][rep]["mmd2"]).reindex(sem_order)
    lo = m - pd.Series({s: c[0] for s, c in results["mmd"][rep]["ci"].items()}).reindex(sem_order)
    hi = pd.Series({s: c[1] for s, c in results["mmd"][rep]["ci"].items()}).reindex(sem_order) - m
    ax.errorbar(range(len(m)), m.values, yerr=[lo.values, hi.values], fmt="none", ecolor=MUTED, lw=1, capsize=2)
    ax.scatter(range(len(m)), m.values, c=sem_colors(), s=40, zorder=3, edgecolor="white")
    ax.plot(range(len(m)), m.values, color="#c9c8c3", lw=1, zorder=1)
    semester_axis(ax, short=True)
    chatgpt_line(ax, label=False)
    ax.set_title(REPS[rep])
fig.tight_layout()
save(fig, "mmd_distance_to_ai")

fig, axs = rep_grid("Advanced 4: how well can a classifier tell each semester apart from AI? (cross-validated AUC; lower = more AI-like)")
for rep, ax in axs.items():
    m = pd.Series(results["separability_auc"][rep]).reindex(sem_order)
    ax.plot(range(len(m)), m.values, color="#c9c8c3", lw=1)
    ax.scatter(range(len(m)), m.values, c=sem_colors(), s=40, zorder=3, edgecolor="white")
    semester_axis(ax, short=True)
    chatgpt_line(ax, label=False)
    ax.set_title(REPS[rep])
fig.tight_layout()
save(fig, "separability_auc_by_semester")

fig, axs = rep_grid("Advanced 5: of each submission's 20 nearest neighbours (balanced pool of pre-ChatGPT students and AI), what % are AI?")
for rep, ax in axs.items():
    m = pd.Series(results["knn_ai_share"][rep]).reindex(sem_order)
    ax.plot(range(len(m)), m.values, color="#c9c8c3", lw=1)
    ax.scatter(range(len(m)), m.values, c=sem_colors(), s=40, zorder=3, edgecolor="white")
    semester_axis(ax, short=True)
    chatgpt_line(ax, label=False)
    ax.set_title(REPS[rep])
fig.tight_layout()
save(fig, "knn_ai_neighbour_share")

codes = {i: (ROOT / df.path[i]).read_text(errors="replace") for i in np.r_[stu_idx, ai_sample]}

def clean(code):
    return "\n".join(l.split("#")[0].rstrip() for l in code.splitlines() if l.split("#")[0].strip()).encode()


cl = {i: clean(c) for i, c in codes.items()}
clen = {i: len(zlib.compress(b, 9)) for i, b in cl.items()}
ncd = np.zeros(len(stu_idx))
for k, i in enumerate(stu_idx):
    vals = [(len(zlib.compress(cl[i] + cl[j], 9)) - min(clen[i], clen[j])) / max(clen[i], clen[j]) for j in ai_sample[:250]]
    ncd[k] = np.mean(vals)
results["ncd_to_ai"] = {"by_semester": per_semester(ncd)[0].round(4).to_dict(), **pre_post_tests(-ncd)}
fig, ax = plt.subplots(figsize=(9, 4.4))
m, ci = per_semester(ncd)
dots_by_semester(ax, m, ci, "Mean compression distance to AI\n(lower = more similar)")
ax.set_title("Advanced 6: model-free check: normalized compression distance (zlib) to AI code")
save(fig, "compression_distance")
metric_sem["Compression distance (NCD, lower = closer)"] = {"zlib": -per_semester(ncd)[0]}

SKIP = set(keyword.kwlist) | set(dir(builtins)) | {"self", "i", "j", "k", "x", "y", "_"}


def identifiers(code):
    names = set()
    try:
        for tkn in tokenize.generate_tokens(io.StringIO(code).readline):
            if tkn.type == tokenize.NAME and tkn.string not in SKIP and len(tkn.string) > 2:
                names.add(tkn.string)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        names = set(re.findall(r"[A-Za-z_]\w{2,}", code)) - SKIP
    return names


ident = {i: identifiers((ROOT / df.path[i]).read_text(errors="replace")) for i in np.r_[stu_idx, np.where(main_ai)[0]]}
pre_ids = stu_idx[pre_mask]
select = rng.choice(pre_ids, len(pre_ids) // 2, replace=False)
held = np.setdiff1d(stu_idx, select)
ai_ids = np.where(main_ai)[0]
vocab_ids = {n for i in ai_ids for n in ident[i]}
ai_df = {n: np.mean([n in ident[i] for i in ai_ids]) for n in vocab_ids}
sel_df = {n: np.mean([n in ident[i] for i in select]) for n in vocab_ids}
log_odds = {n: np.log((ai_df[n] + 0.01) / (sel_df[n] + 0.01)) for n in vocab_ids if ai_df[n] >= 0.15}
signature = sorted(log_odds, key=log_odds.get, reverse=True)[:20]
held_stu = stu.loc[np.isin(stu_idx, held)]
uses = np.array([sum(n in ident[i] for n in signature) for i in held])
sig_m = pd.Series(uses, index=held_stu.index).groupby(held_stu.group).mean().reindex(sem_order)
sig_ci = (1.96 * pd.Series(uses, index=held_stu.index).groupby(held_stu.group).sem()).reindex(sem_order)
results["signature_identifiers"] = {"names": signature, "mean_used_by_semester": sig_m.round(3).to_dict(),
                                    "ai_mean": float(np.mean([sum(n in ident[i] for n in signature) for i in ai_ids]))}
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5), gridspec_kw={"width_ratios": [1, 1.25]})
dots_by_semester(axes[0], sig_m, sig_ci, "Signature identifiers used (of 20)")
axes[0].set_title("Advanced 7: how many of AI's 20 favourite identifiers each submission uses\n"
                  "(names chosen on a held-out half of pre-ChatGPT students; that half excluded here)")
heat = pd.DataFrame({s: [np.mean([n in ident[i] for i in held[(held_stu.group == s).values]]) * 100 for n in signature]
                     for s in sem_order}, index=signature)
heat["AI"] = [ai_df[n] * 100 for n in signature]
im = axes[1].imshow(heat.values, cmap="Blues", aspect="auto", vmin=0, vmax=100)
axes[1].set_xticks(range(heat.shape[1]))
axes[1].set_xticklabels([short_sem(s) for s in sem_order] + ["AI"], fontsize=8)
axes[1].set_yticks(range(len(signature)))
axes[1].set_yticklabels(signature, fontsize=8, family="monospace")
axes[1].axvline(sem_pos[FIRST_AI_SEMESTER] - 0.5, color=INK, lw=1)
axes[1].axvline(len(sem_order) - 0.5, color=INK, lw=1.5)
axes[1].grid(False)
fig.colorbar(im, ax=axes[1], label="% of submissions using the name")
axes[1].set_title("Which names, and when they appear")
fig.tight_layout()
save(fig, "ai_signature_identifiers")
metric_sem["AI signature identifiers used"] = {"names": sig_m}
metric_sem["Classifier: % flagged AI-like"] = {"ensemble": pd.Series(results["classifier"]["ensemble"]["pct_flagged"]).reindex(sem_order)}
metric_sem["Students in AI-dominated clusters"] = {"kmeans": pd.concat(ai_cluster_share, axis=1).mean(1)}
metric_sem["Similarity to nearest AI twin"] = {r: pd.Series(results["nearest_ai_neighbour"][r]["by_semester"]).reindex(sem_order) for r in REPS}

ev = {}
for name, per_rep in metric_sem.items():
    scaled = [(srs - srs.min()) / (srs.max() - srs.min()) for srs in per_rep.values()]
    ev[name] = pd.concat(scaled, axis=1).mean(1)
ev = pd.DataFrame(ev).T[sem_order]
rho_col = [stats.spearmanr(range(len(sem_order)), ev.loc[n].values).statistic for n in ev.index]
results["evidence_matrix"] = {n: {**ev.loc[n].round(2).to_dict(), "spearman_rho": float(r)} for n, r in zip(ev.index, rho_col)}
fig, ax = plt.subplots(figsize=(13, 5.8))
lim = 1
im = ax.imshow(ev.values, cmap="Reds", vmin=0, vmax=1, aspect="auto")
ax.set_xticks(range(len(sem_order)))
ax.set_xticklabels(sem_order, rotation=30, ha="right")
ax.set_yticks(range(len(ev)))
ax.set_yticklabels([f"{n}   (ρ = {r:+.2f})" for n, r in zip(ev.index, rho_col)], fontsize=8.5)
ax.grid(False)
for i in range(ev.shape[0]):
    for j in range(ev.shape[1]):
        v = ev.values[i, j]
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8, color="white" if v > 0.6 else INK)
ax.axvline(sem_pos[FIRST_AI_SEMESTER] - 0.5, color=INK, lw=1.5)
fig.colorbar(im, ax=ax, label="0 = least AI-like semester, 1 = most AI-like semester")
ax.set_title("Advanced 8: evidence matrix: nine independent measures of 'AI-likeness', every semester\n"
             "(ρ = Spearman rank correlation with time across the 9 semesters)")
save(fig, "evidence_matrix")

months = {"Spring 2023": 4, "Fall 2023": 10, "Fall 2024": 22, "Fall 2025": 34}
fig, ax = plt.subplots(figsize=(8, 4.6))
xs = [months[s] for s in post_sems]
ys = ev[post_sems].mean(0).values
ax.scatter(0, ev[pre_sems].mean(0).mean(), s=70, color=PRE, zorder=3, label="Pre-ChatGPT average")
ax.scatter(xs, ys, s=70, color=POST, zorder=3, label="Post-ChatGPT semesters")
for x_, y_, s in zip(xs, ys, post_sems):
    ax.annotate(s, (x_, y_), xytext=(6, -3), textcoords="offset points", fontsize=8)
fit = stats.linregress(xs, ys)
grid_m = np.linspace(0, 36, 20)
ax.plot(grid_m, fit.intercept + fit.slope * grid_m, color=POST, ls="--", lw=1.2)
ax.set_xlabel("Months between ChatGPT's release and the submission deadline")
ax.set_ylabel("Average AI-likeness across all\nevidence-matrix measures (0-1 scale)")
ax.set_title(f"Advanced 9: dose-response: +{fit.slope * 12:.2f} per year of AI availability on a 0-1 scale (r = {fit.rvalue:.2f})")
ax.legend(frameon=False, fontsize=8)
results["dose_response"] = {"slope_per_year": fit.slope * 12, "r": fit.rvalue, "p": fit.pvalue}
save(fig, "dose_response_months")

pre_stats = {r: (sims[r][pre_mask].mean(), sims[r][pre_mask].std()) for r in REPS}
export = stu[["path", "group", "lines"]].copy()
export["consensus"] = consensus
export["p_ai"] = Pr["ensemble"][stu_idx]
export["signature_ids"] = [sum(n in ident[i] for n in signature) for i in stu_idx]
export["held_out_for_signatures"] = np.isin(stu_idx, held)
for r in REPS:
    export[f"z_{r}"] = Z[r]
export.to_csv(ROOT / f"student_scores{SUFFIX}.csv", index=False)
ai_rows_all = np.where(main_ai)[0]
ai_export = df.loc[ai_rows_all, ["path", "model"]].copy()
ai_export["consensus"] = np.mean([(np.asarray(X[r][ai_rows_all] @ np.asarray(X[r][main_ai].mean(0)).ravel()).ravel()
                                   - pre_stats[r][0]) / pre_stats[r][1] for r in REPS], axis=0)
ai_export["p_ai"] = Pr["ensemble"][ai_rows_all]
ai_export.to_csv(ROOT / f"ai_scores{SUFFIX}.csv", index=False)

(ROOT / f"results{SUFFIX}.json").write_text(json.dumps(results, indent=2, default=float))
print(json.dumps({"effect": {r: round(results["similarity_to_ai"][r]["cohens_d"], 3) for r in REPS},
                  "its": {r: {k: round(v, 3) for k, v in results["interrupted_time_series"][r].items()} for r in REPS},
                  "flagged": results["classifier"]["ensemble"]["pct_flagged"],
                  "fpr_tpr": (fpr["ensemble"], tpr["ensemble"], tpr_disguise["ensemble"]),
                  "cluster": results["ai_cluster_share_mean"], "consensus": results["consensus_by_semester"],
                  "style_agree": agree}, indent=1, default=float))
