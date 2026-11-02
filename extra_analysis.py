"""Results-strengthening analyses: per-semester results table, bulk-vs-tail decomposition, mixture model,
AI-polished student code, and ChatGPT-vs-Claude attribution of flagged submissions.

Needs: features.csv / lexical.npz / ast.npz (features.py), embeddings/*.npz (embed.py), student_scores.csv
(analyze.py), data/polished/* (polish.py). Writes figures/extra_*.png and results_extra.json.
"""
import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler, normalize

import embed
import features

matplotlib.use("Agg")
ROOT = Path(__file__).parent
FIG = ROOT / "figures"
rng = np.random.default_rng(0)
INK, MUTED, AI, PRE_C, POST_C = "#0b0b0b", "#52514e", "#eb6834", "#b9b8b2", "#2a78d6"
CHATGPT, CLAUDE = "#1baf7a", "#d97757"
SEMS = ["Pre-2021", "Spring 2021", "Fall 2021", "Spring 2022", "Fall 2022", "Spring 2023", "Fall 2023", "Fall 2024", "Fall 2025"]
PRE_SEMS, POST = SEMS[:5], SEMS[5:]
LABELS = {"Pre-2021": "≤2020", **{s: s for s in SEMS[1:]}}
EMB = ["openai3large", "voyagecode", "codestral", "qwen3emb"]
REPS = ["lexical", "ast"] + EMB
STYLE_COLS = ["lines", "comment_ratio", "functions", "docstrings", "type_hints", "fstrings", "main_guard",
              "avg_name_len", "snake_case", "global_stmts", "enumerate", "range_len", "comprehensions",
              "try_except", "avg_line_len"]
CONDITION_NAMES = {"gpt4o-fixonly": "GPT-4o: \"fix only the bugs,\nkeep my style\"",
                   "gpt4omini-clean": "GPT-4o mini:\n\"fix and clean it up\"",
                   "gpt4o-clean": "GPT-4o:\n\"fix and clean it up\"",
                   "sonnet45-clean": "Claude Sonnet 4.5:\n\"fix and clean it up\""}
plt.rcParams.update({"figure.dpi": 160, "savefig.bbox": "tight", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#ecebe6", "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "font.size": 10.5, "axes.titleweight": "bold", "axes.titlesize": 12, "axes.edgecolor": "#b5b4ae",
                     "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white"})
out = {}

# ---------- Rebuild the main analysis's representations ----------
df = pd.read_csv(ROOT / "features.csv").fillna({"model": "", "variant": ""})
is_ai = (df.source == "ai").values
main_ai = is_ai & (df.variant == "assignment").values & df.model.isin(features.MAIN_MODELS).values
stu_rows = np.where(~is_ai)[0]
core = main_ai | ~is_ai
scores = pd.read_csv(ROOT / "student_scores.csv")
assert (scores.path.values == df.path.values[stu_rows]).all()
pre_mask = scores.group.isin(PRE_SEMS).values

polished = sorted((ROOT / "data/polished").glob("*/*.py"))
pol = pd.DataFrame({"path": [str(p.relative_to(ROOT)) for p in polished],
                    "condition": [p.parent.name for p in polished], "source": [p.name for p in polished]})
pol_code = [p.read_text(errors="replace") for p in polished]

full = features.load()
assert (full.path.values == df.path.values).all()
X, P = {}, {}
for name, prep in [("lexical", features.code_tokens), ("ast", features.ast_nodes)]:
    vec = TfidfVectorizer(token_pattern=r"\S+", ngram_range=(1, 3), min_df=2, sublinear_tf=True)
    X[name] = vec.fit_transform(full.code.map(prep)).tocsr()
    P[name] = vec.transform([prep(c) for c in pol_code]).tocsr()
for enc in EMB:
    z = np.load(ROOT / "embeddings" / f"{enc}.npz")
    lookup = dict(zip(z["paths"], range(len(z["paths"]))))
    E = np.zeros((len(df), z["vecs"].shape[1]))
    E[core] = z["vecs"][[lookup[p] for p in df.path[core]]]
    mean = E[core].mean(0)
    E[core] = normalize(E[core] - mean)
    X[enc] = E
    cache = ROOT / "embeddings" / f"polished_{enc}.npz"
    have = {}
    if cache.exists():
        zc = np.load(cache)
        have = dict(zip(zc["paths"], zc["vecs"]))
    todo = [p for p in pol.path if p not in have]
    for i in range(0, len(todo), 16):
        batch = todo[i:i + 16]
        vecs = embed.embed_batch(enc, [embed.strip_comments((ROOT / f).read_text(errors="replace"),
                                                            embed.CHAR_LIMIT.get(enc, embed.MAX_CHARS)) for f in batch])
        have.update(zip(batch, np.array(vecs, dtype=np.float32)))
    if todo:
        keys = sorted(have)
        np.savez(cache, paths=np.array(keys), vecs=np.vstack([have[k] for k in keys]))
    P[enc] = normalize(np.vstack([have[p] for p in pol.path]) - mean)


def consensus_of(rows_x):
    """Consensus similarity to AI (pre-ChatGPT SD units), exactly as analyze.py computes it."""
    zs = []
    for r in REPS:
        c = np.asarray(X[r][main_ai].mean(0)).ravel()
        s_stu = np.asarray(X[r][stu_rows] @ c).ravel()
        mu, sd = s_stu[pre_mask].mean(), s_stu[pre_mask].std()
        zs.append((np.asarray(rows_x[r] @ c).ravel() - mu) / sd)
    return np.mean(zs, axis=0)


assert np.allclose(consensus_of({r: X[r][stu_rows] for r in REPS}), scores.consensus.values, atol=1e-6)
pol["consensus"] = consensus_of(P)

# Same classifiers as analyze.py, fit on AI vs pre-ChatGPT students, applied to the polished files.
train = np.r_[np.where(main_ai)[0], stu_rows[pre_mask]]
y = np.r_[np.ones(main_ai.sum()), np.zeros(pre_mask.sum())]
scaler = StandardScaler().fit(df[STYLE_COLS].values)
style_all = scaler.transform(df[STYLE_COLS].values)
style_pol = scaler.transform(pd.DataFrame([features.style_features(c) for c in pol_code])[STYLE_COLS].values)
probs = []
for r in REPS + ["style"]:
    Xt = style_all[train] if r == "style" else X[r][train]
    Xp = style_pol if r == "style" else P[r]
    probs.append(LogisticRegression(max_iter=5000, class_weight="balanced").fit(Xt, y).predict_proba(Xp)[:, 1])
pol["p_ai"] = np.mean(probs, axis=0)
orig = scores.set_index(scores.path.str.split("/").str[-1])
pol["orig_consensus"] = orig.loc[pol.source, "consensus"].values
pol["orig_p_ai"] = orig.loc[pol.source, "p_ai"].values
pol["lines"] = [features.style_features(c)["lines"] for c in pol_code]

ai_cons = pd.read_csv(ROOT / "ai_scores.csv").consensus.values
post_flag_cons = scores[(~pre_mask) & (scores.p_ai > 0.5)].consensus.values
summary = pol.groupby("condition").agg(n=("path", "size"), consensus=("consensus", "mean"), orig=("orig_consensus", "mean"),
                                       flagged=("p_ai", lambda v: (v > 0.5).mean() * 100),
                                       median_p=("p_ai", "median")).reindex(list(CONDITION_NAMES))
out["polishing"] = {"summary": summary.round(3).to_dict(orient="index"),
                    "originals_flagged_pct": float((pol.drop_duplicates("source").orig_p_ai > 0.5).mean() * 100),
                    "ai_from_scratch_consensus_median": float(np.median(ai_cons)),
                    "post_students_flagged_consensus_median": float(np.median(post_flag_cons))}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6.2), gridspec_kw={"width_ratios": [2.1, 1]})
groups = [("Original student code\n(pre-ChatGPT)", pol.drop_duplicates("source").orig_consensus.values, PRE_C)]
groups += [(CONDITION_NAMES[c], pol[pol.condition == c].consensus.values, "#8fb3e3" if "fixonly" in c else POST_C)
           for c in CONDITION_NAMES]
groups += [("Post-ChatGPT students\nflagged AI-like", post_flag_cons, "#f3b38f"), ("AI from scratch", ai_cons, AI)]
for i, (name, v, color) in enumerate(groups):
    jitter = np.random.default_rng(i).uniform(-0.28, 0.28, len(v))
    ax1.scatter(np.full(len(v), i) + jitter, v, s=10, color=color, alpha=0.65, edgecolor="none")
    ax1.plot([i - 0.32, i + 0.32], [np.median(v)] * 2, color=INK, lw=2.2)
    ax1.text(i, np.median(v) + 0.25, f"{np.median(v):.1f}", ha="center", fontsize=9, fontweight="bold")
ax1.set_xticks(range(len(groups)))
ax1.set_xticklabels([g[0] for g in groups], fontsize=8.3, rotation=25, ha="right")
ax1.set_ylabel("Similarity to AI code (SDs vs pre-ChatGPT students)")
ax1.set_title("AI-polished student code lands where the typical 2024-25 student sits,\nfar from AI code written from scratch", loc="left")
ax1.axhline(0, color=MUTED, lw=0.8)
rates = [(CONDITION_NAMES[c].replace("\n", " "), summary.loc[c, "flagged"]) for c in CONDITION_NAMES]
rates = [("Original student code", out["polishing"]["originals_flagged_pct"])] + rates
rate_colors = [PRE_C] + ["#8fb3e3" if "fixonly" in c else POST_C for c in CONDITION_NAMES]
ax2.barh([r[0] for r in rates][::-1], [r[1] for r in rates][::-1], color=rate_colors[::-1], height=0.6)
for i, (name, v) in enumerate(rates[::-1]):
    ax2.text(v + 1.5, i, f"{v:.0f}%", va="center", fontsize=10, fontweight="bold")
ax2.set_xlim(0, 110)
ax2.tick_params(axis="y", labelsize=8.5)
ax2.set_xlabel("% classified AI-like by the same detector")
ax2.set_title("How often the detector flags it", loc="left")
fig.tight_layout()
fig.savefig(FIG / "extra_1_ai_polishing.png")
plt.close(fig)

# ---------- Per-semester results table ----------
pre_c = scores.consensus.values[pre_mask]
pre_flag = (scores.p_ai.values[pre_mask] > 0.5)
rows = []
for s in SEMS:
    m = (scores.group == s).values
    v = scores.consensus.values[m]
    f = scores.p_ai.values[m] > 0.5
    lo, hi = stats.binomtest(int(f.sum()), len(f)).proportion_ci(method="wilson")
    row = {"semester": s, "n": int(m.sum()), "mean_sim": v.mean(), "flagged": int(f.sum()), "flag_pct": f.mean() * 100,
           "flag_lo": lo * 100, "flag_hi": hi * 100}
    if s in POST:
        d = (v.mean() - pre_c.mean()) / np.sqrt((v.var(ddof=1) + pre_c.var(ddof=1)) / 2)
        boots = []
        for _ in range(2000):
            a, b = rng.choice(pre_c, len(pre_c)), rng.choice(v, len(v))
            boots.append((b.mean() - a.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2))
        row.update(d=d, d_lo=np.percentile(boots, 2.5), d_hi=np.percentile(boots, 97.5),
                   p_sim=stats.mannwhitneyu(v, pre_c, alternative="greater").pvalue,
                   p_flag=stats.fisher_exact([[f.sum(), (~f).sum()], [pre_flag.sum(), (~pre_flag).sum()]],
                                             alternative="greater").pvalue)
    rows.append(row)
tab = pd.DataFrame(rows)
post_idx = tab.semester.isin(POST)
for col in ("p_sim", "p_flag"):
    ps = tab.loc[post_idx, col].values
    order = np.argsort(ps)
    adj, run = np.empty(len(ps)), 0
    for rank, i in enumerate(order):
        run = max(run, min(1, (len(ps) - rank) * ps[i]))
        adj[i] = run
    tab.loc[post_idx, col + "_holm"] = adj
pooled_post = scores.p_ai.values[~pre_mask] > 0.5
out["pooled_flag_test"] = {"pre": f"{pre_flag.sum()}/{len(pre_flag)}", "post": f"{pooled_post.sum()}/{len(pooled_post)}",
                           "fisher_p": stats.fisher_exact([[pooled_post.sum(), (~pooled_post).sum()],
                                                           [pre_flag.sum(), (~pre_flag).sum()]], alternative="greater").pvalue}

# ---------- Bulk vs tail ----------
thr = np.percentile(pre_c, 99)
bulk, tail, contrib = [], [], []
for s in SEMS:
    v = scores.consensus.values[(scores.group == s).values]
    in_tail = v > thr
    k = int(in_tail.sum())
    lo, hi = stats.binomtest(k, len(v)).proportion_ci(method="wilson")
    med_boot = [np.median(rng.choice(v, len(v))) for _ in range(1000)]
    bulk.append((np.median(v), np.percentile(med_boot, 2.5), np.percentile(med_boot, 97.5)))
    tail.append((in_tail.mean() * 100, lo * 100, hi * 100))
    shift = v.mean() - pre_c.mean()
    from_tail = ((v[in_tail] - pre_c.mean()).sum()) / len(v)
    contrib.append((shift, from_tail, shift - from_tail))
    gm1 = GaussianMixture(1, random_state=0).fit(v.reshape(-1, 1))
    gm2 = GaussianMixture(2, random_state=0, n_init=5).fit(v.reshape(-1, 1))
    tab.loc[tab.semester == s, "delta_bic"] = gm1.bic(v.reshape(-1, 1)) - gm2.bic(v.reshape(-1, 1))
tab["median_sim"] = [b[0] for b in bulk]
tab["tail_pct"] = [t[0] for t in tail]
tab["shift_from_tail"] = [c[1] for c in contrib]
tab["shift_from_bulk"] = [c[2] for c in contrib]
out["tail_threshold_pre_p99"] = thr
out["semester_table"] = tab.round(5).to_dict(orient="records")

fig, axes = plt.subplots(1, 3, figsize=(17, 5))
x = np.arange(len(SEMS))
cols = [POST_C if s in POST else PRE_C for s in SEMS]
b = np.array(bulk)
axes[0].errorbar(x, b[:, 0], yerr=[b[:, 0] - b[:, 1], b[:, 2] - b[:, 0]], fmt="none", ecolor=MUTED, capsize=3, lw=1)
axes[0].scatter(x, b[:, 0], c=cols, s=60, edgecolor=INK, lw=0.6, zorder=3)
axes[0].axhline(np.median(pre_c), color=MUTED, ls=":", lw=1)
axes[0].set_title("The median submission rises too,\nmost sharply from Fall 2024", loc="left")
axes[0].set_ylabel("Median similarity to AI (SDs)")
t = np.array(tail)
axes[1].bar(x, t[:, 0], color=[AI if s in POST else PRE_C for s in SEMS], width=0.65, zorder=2)
axes[1].errorbar(x, t[:, 0], yerr=[t[:, 0] - t[:, 1], t[:, 2] - t[:, 0]], fmt="none", ecolor=MUTED, capsize=3, lw=1, zorder=3)
for i, v in enumerate(t[:, 0]):
    axes[1].text(i, t[i, 2] + 1.5, f"{v:.0f}%", ha="center", fontsize=9, fontweight="bold")
axes[1].set_title("The share beyond anything seen before\nChatGPT jumps from ≤3% to about 40%", loc="left")
axes[1].set_ylabel(f"% above the pre-ChatGPT 99th percentile ({thr:.1f} SD)")
cb = np.array(contrib)
axes[2].bar(x, cb[:, 2], color="#9db8de", width=0.65, label="from students within the pre-ChatGPT range")
axes[2].bar(x, cb[:, 1], bottom=np.where(cb[:, 2] > 0, cb[:, 2], 0), color=AI, width=0.65,
            label="from students beyond the pre-ChatGPT range")
axes[2].axhline(0, color=MUTED, lw=0.8)
axes[2].set_title("Where each semester's rise in average\nsimilarity comes from", loc="left")
axes[2].set_ylabel("Change in mean similarity vs pre-ChatGPT (SDs)")
axes[2].legend(frameon=False, fontsize=8.5, loc="upper left")
for ax in axes:
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS[s] for s in SEMS], rotation=35, ha="right", fontsize=8.5)
    ax.axvline(4.5, color=MUTED, ls="--", lw=1)
fig.tight_layout()
fig.savefig(FIG / "extra_2_bulk_vs_tail.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(9.5, 4.4))
pt = tab[post_idx]
for i, r in enumerate(pt.itertuples()):
    ax.errorbar(r.d, i, xerr=[[r.d - r.d_lo], [r.d_hi - r.d]], fmt="o", color=POST_C, ms=8, capsize=4, lw=1.6)
    stars = "***" if r.p_sim_holm < 0.001 else "**" if r.p_sim_holm < 0.01 else "*" if r.p_sim_holm < 0.05 else "n.s."
    ax.text(r.d_hi + 0.05, i, f"d = {r.d:.2f} {stars}", va="center", fontsize=9.5)
for xv, lab in [(0.2, "small"), (0.5, "medium"), (0.8, "large")]:
    ax.axvline(xv, color="#dddcd7", ls=":", lw=1)
    ax.text(xv, -0.75, lab, ha="center", fontsize=8, color=MUTED)
ax.axvline(0, color=MUTED, lw=1)
ax.set_yticks(range(len(pt)))
ax.set_yticklabels(pt.semester)
ax.set_xlim(-0.2, 2.6)
ax.set_ylim(-0.95, len(pt) - 0.5)
ax.set_xlabel("Effect size vs all pre-ChatGPT students (Cohen's d, 95% bootstrap CI)")
ax.set_title("Each post-ChatGPT semester vs the pre-ChatGPT baseline: the effect grows every semester", loc="left")
fig.savefig(FIG / "extra_3_semester_effects.png")
plt.close(fig)

# ---------- ChatGPT vs Claude attribution ----------
fam = df.model.map(features.FAMILY).values
ai_idx = np.where(main_ai)[0]
y_fam = (fam[ai_idx] == "Claude").astype(int)
fam_probs, fam_auc = [], {}
flagged_rows = stu_rows[scores.p_ai.values > 0.5]
for r in REPS:
    clf = LogisticRegression(max_iter=5000, class_weight="balanced")
    cvp = cross_val_predict(clf, X[r][ai_idx], y_fam, cv=StratifiedKFold(5, shuffle=True, random_state=0),
                            method="predict_proba")[:, 1]
    fam_auc[r] = roc_auc_score(y_fam, cvp)
    fam_probs.append(clf.fit(X[r][ai_idx], y_fam).predict_proba(X[r][flagged_rows])[:, 1])
p_claude = np.mean(fam_probs, axis=0)
flag_tab = scores[scores.p_ai > 0.5][["group"]].copy()
flag_tab["p_claude"] = p_claude
attrib = flag_tab.groupby("group").p_claude.agg(n="size", claude_like=lambda v: int((v > 0.5).sum()),
                                                 mean_p_claude="mean").reindex(POST).dropna()
out["attribution"] = {"family_classifier_cv_auc": fam_auc, "by_semester": attrib.round(3).to_dict(orient="index"),
                      "overall_chatgpt_like": int((p_claude <= 0.5).sum()), "overall_claude_like": int((p_claude > 0.5).sum())}

fig, ax = plt.subplots(figsize=(9, 4))
xs = np.arange(len(attrib))
gpt = (attrib.n - attrib.claude_like).values
ax.bar(xs, gpt, color=CHATGPT, width=0.6, label="closer to ChatGPT code")
ax.bar(xs, attrib.claude_like.values, bottom=gpt, color=CLAUDE, width=0.6, label="closer to Claude code")
for i, (g_, c_) in enumerate(zip(gpt, attrib.claude_like.values)):
    ax.text(i, g_ + c_ + 0.3, f"{int(g_)} / {int(g_ + c_)} ChatGPT-like", ha="center", fontsize=9)
ax.set_xticks(xs)
ax.set_xticklabels(attrib.index)
ax.set_ylabel("Submissions classified AI-like")
ax.set_ylim(0, attrib.n.max() * 1.25)
ax.set_title(f"Which family the AI-like submissions resemble (family classifier AUC {np.mean(list(fam_auc.values())):.2f})",
             loc="left")
ax.legend(frameon=False, fontsize=9, loc="upper left")
fig.savefig(FIG / "extra_4_chatgpt_vs_claude_attribution.png")
plt.close(fig)

(ROOT / "results_extra.json").write_text(json.dumps(out, indent=2, default=float))
print(json.dumps({k: v for k, v in out.items() if k != "semester_table"}, indent=1, default=lambda o: round(float(o), 4)))
print(tab[["semester", "n", "flag_pct", "d", "p_sim_holm", "p_flag_holm", "median_sim", "tail_pct",
           "shift_from_bulk", "shift_from_tail", "delta_bic"]].round(3).to_string())
