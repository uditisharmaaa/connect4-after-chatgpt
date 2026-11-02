"""Presentation charts of the semester-by-semester story, plus the Binoculars zero-shot check.

Reads student_scores.csv / ai_scores.csv (analyze.py), results.json and binoculars_scores.npz (binoculars.py).
Writes figures/story_*.png and results_story.json.
"""
import json
from datetime import date
from pathlib import Path

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score

matplotlib.use("Agg")
ROOT = Path(__file__).parent
FIG = ROOT / "figures"
INK, MUTED, LIGHT, AI = "#0b0b0b", "#52514e", "#e6e5e0", "#eb6834"
SEMS = ["Pre-2021", "Spring 2021", "Fall 2021", "Spring 2022", "Fall 2022", "Spring 2023", "Fall 2023", "Fall 2024", "Fall 2025"]
POST = SEMS[5:]
DATES = {"Pre-2021": date(2020, 3, 15), "Spring 2021": date(2021, 3, 15), "Fall 2021": date(2021, 10, 15),
         "Spring 2022": date(2022, 3, 15), "Fall 2022": date(2022, 10, 15), "Spring 2023": date(2023, 3, 15),
         "Fall 2023": date(2023, 10, 15), "Fall 2024": date(2024, 10, 15), "Fall 2025": date(2025, 10, 7)}
LABELS = {"Pre-2021": "≤2020", **{s: s for s in SEMS[1:]}}
CHATGPT = date(2022, 11, 30)
RELEASES = [(date(2022, 11, 30), "ChatGPT (GPT-3.5)"), (date(2023, 3, 14), "GPT-4"), (date(2024, 5, 13), "GPT-4o, free"),
            (date(2024, 7, 18), "GPT-4o mini"), (date(2025, 4, 14), "GPT-4.1"), (date(2025, 8, 7), "GPT-5"),
            (date(2025, 9, 29), "Claude Sonnet 4.5")]
# Sequential blue ramp, light (oldest) to dark (newest): colour encodes time.
RAMP = ["#d7e3f4", "#c3d6ef", "#aec8ea", "#97b8e4", "#80a8de", "#5f91d6", "#3f7bcf", "#2563b8", "#174a91"]
SEM_COLOR = dict(zip(SEMS, RAMP))
BANDS = [("Clearly student-like", 0, 0.05, "#c9d9ee"), ("Leaning student", 0.05, 0.5, "#8fb3e3"),
         ("Leaning AI", 0.5, 0.95, "#f3b38f"), ("Indistinguishable from AI", 0.95, 1.01, "#d9541c")]

plt.rcParams.update({"figure.dpi": 160, "savefig.bbox": "tight", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.color": "#ecebe6", "grid.linewidth": 0.6,
                     "axes.axisbelow": True, "font.size": 10.5, "axes.titleweight": "bold", "axes.titlesize": 12,
                     "axes.edgecolor": "#b5b4ae", "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white"})

stu = pd.read_csv(ROOT / "student_scores.csv")
ai = pd.read_csv(ROOT / "ai_scores.csv")
res = json.loads((ROOT / "results.json").read_text())
stu["flag"] = stu.p_ai > 0.5
story = {}


def wilson(k, n):
    lo, hi = stats.binomtest(k, n).proportion_ci(method="wilson")
    return lo * 100, hi * 100


def mark_releases(ax, labels=True, y=1.0):
    ax.axvspan(CHATGPT, date(2026, 3, 1), color="#f6f3ee", zorder=0, lw=0)
    for d, name in RELEASES:
        ax.axvline(d, color="#c9c8c3", lw=0.8, ls=":", zorder=1)
        if labels:
            ax.text(d, y, name, transform=ax.get_xaxis_transform(), rotation=90, va="top", ha="right",
                    fontsize=7, color=MUTED)


def date_axis(ax):
    ax.set_xlim(date(2019, 12, 1), date(2026, 3, 1))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


# ---------------- 1. Timeline: % AI-like + average similarity ----------------
g = stu.groupby("group")
rows = []
for s in SEMS:
    sub = stu[stu.group == s]
    k, n = int(sub.flag.sum()), len(sub)
    lo, hi = wilson(k, n)
    rows.append((s, k, n, 100 * k / n, lo, hi, sub.consensus.mean(), 1.96 * sub.consensus.sem()))
tl = pd.DataFrame(rows, columns=["sem", "k", "n", "pct", "lo", "hi", "sim", "sim_ci"])
story["timeline"] = tl.round(3).to_dict(orient="records")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8.2), sharex=True, gridspec_kw={"height_ratios": [1.35, 1], "hspace": 0.28})
xs = [DATES[s] for s in SEMS]
cols = [SEM_COLOR[s] if s in POST else "#b9b8b2" for s in SEMS]
for s, x, r in zip(SEMS, xs, tl.itertuples()):
    ax1.bar(x, r.pct, width=110, color=AI if s in POST else "#b9b8b2", zorder=3, edgecolor="white", lw=1.5)
    ax1.errorbar(x, r.pct, yerr=[[r.pct - r.lo], [r.hi - r.pct]], color=MUTED, lw=1, capsize=3, zorder=4)
    ax1.text(x, r.hi + 1.2, f"{r.pct:.0f}%", ha="center", fontsize=11, fontweight="bold", color=INK, zorder=5)
    ax1.text(x, -3.2, f"{r.k}/{r.n}", ha="center", fontsize=7.5, color=MUTED)
    ax1.text(x, -6.2, LABELS[s].replace(" ", "\n"), ha="center", va="top", fontsize=8, color=INK)
mark_releases(ax1)
ax1.set_ylim(-13, 58)
ax1.set_yticks(range(0, 60, 10))
ax1.tick_params(labelbottom=True)
ax1.axhline(0, color=MUTED, lw=0.8)
ax1.set_ylabel("Submissions that look AI-written (%)")
ax1.set_title("Roughly 1 in 5 Connect 4 submissions now looks AI-written. Before ChatGPT: 1 in 401.", loc="left", fontsize=14)
fig.text(0.125, 0.035, "Top: share of each semester's submissions classified AI-like (ensemble classifier, 0.25% false-positive rate); "
         "95% Wilson intervals; flagged/total under each bar.\nBottom: mean similarity to AI code across six representations, "
         "95% CI. Shaded = after ChatGPT; dotted lines = model releases.", fontsize=8.5, color=MUTED, va="top")
ax2.plot(xs, tl.sim, color="#c9c8c3", lw=1.2, zorder=2)
ax2.errorbar(xs, tl.sim, yerr=tl.sim_ci, fmt="none", ecolor=MUTED, lw=1, capsize=3, zorder=3)
ax2.scatter(xs, tl.sim, s=80, c=[SEM_COLOR[s] for s in SEMS], edgecolor=INK, lw=0.6, zorder=4)
for x, s, v in zip(xs, SEMS, tl.sim):
    ax2.annotate(LABELS[s], (x, v), xytext=(0, -18), textcoords="offset points", ha="center", fontsize=7.5, color=MUTED)
ax2.axhline(0, color=MUTED, lw=0.8)
mark_releases(ax2, labels=False)
date_axis(ax2)
ax2.set_ylabel("Average similarity to AI code\n(SDs vs pre-ChatGPT students)")
ax2.set_title("…and the average submission has drifted toward AI style the whole time", loc="left", fontsize=11.5)
fig.savefig(FIG / "story_1_timeline.png")
plt.close(fig)

# Slide version: bars only, large type, three key releases labelled horizontally.
fig, ax = plt.subplots(figsize=(11, 7))
ax.axvspan(CHATGPT, date(2026, 3, 1), color="#f6f3ee", zorder=0, lw=0)
for (d, name), y in zip([(CHATGPT, "ChatGPT launches"), (date(2024, 5, 13), "GPT-4o made free"),
                         (date(2025, 8, 7), "GPT-5")], (54, 54, 47)):
    ax.axvline(d, color=MUTED, lw=1.2, ls=":", zorder=1)
    ax.text(d, y, f" {name}", fontsize=14, color=INK, va="center", ha="left" if name != "GPT-5" else "right")
for s, x, r in zip(SEMS, xs, tl.itertuples()):
    ax.bar(x, r.pct, width=110, color=AI if s in POST else "#b9b8b2", zorder=3, edgecolor="white", lw=1.5)
    ax.errorbar(x, r.pct, yerr=[[r.pct - r.lo], [r.hi - r.pct]], color=MUTED, lw=1.2, capsize=4, zorder=4)
    ax.text(x, r.hi + 1.5, f"{r.pct:.0f}%", ha="center", fontsize=18, fontweight="bold", color=INK, zorder=5)
    ax.text(x, -3.5, f"{r.k}/{r.n}", ha="center", fontsize=12, color=MUTED)
    ax.text(x, -7, LABELS[s].replace(" ", "\n"), ha="center", va="top", fontsize=13, color=INK)
ax.axhline(0, color=MUTED, lw=0.8)
ax.set_ylim(-15, 58)
ax.set_yticks(range(0, 60, 10))
ax.tick_params(labelsize=13)
ax.set_ylabel("% of submissions that look AI-written", fontsize=15)
date_axis(ax)
ax.set_xticks([])
fig.savefig(FIG / "story_1_timeline_slide.png")
plt.close(fig)

# ---------------- 2. Ridgeline of similarity distributions ----------------
grid = np.linspace(-3, 9, 500)
fig, ax = plt.subplots(figsize=(11, 9))
spacing = 0.85
ai_vals = ai.consensus.values
groups = SEMS + ["AI (ChatGPT + Claude)"]
for i, s in enumerate(groups):
    v = ai_vals if s not in SEMS else stu[stu.group == s].consensus.values
    dens = stats.gaussian_kde(v, bw_method=0.25)(grid)
    dens = dens / dens.max() * 1.3
    base = (len(groups) - 1 - i) * spacing
    color = AI if s not in SEMS else SEM_COLOR[s]
    ax.fill_between(grid, base, base + dens, color=color, alpha=0.9 if s not in SEMS else 0.95, zorder=len(groups) - i, lw=0)
    ax.plot(grid, base + dens, color="white", lw=1.4, zorder=len(groups) - i)
    ax.plot(grid, base + dens, color=INK, lw=0.5, zorder=len(groups) - i)
    if s in SEMS:
        flagged = stu[(stu.group == s) & stu.flag].consensus.values
        ax.scatter(flagged, np.full(len(flagged), base + 0.04), marker="|", s=90, color=AI, zorder=40, lw=1.6)
        label = f"{LABELS[s]}   n={int((stu.group == s).sum())}"
    else:
        label = "AI-generated"
    ax.text(-3.15, base + 0.12, label, ha="right", fontsize=9.5, color=INK, fontweight="bold" if s not in SEMS else "normal")
pre_med = stu[stu.group.isin(SEMS[:5])].consensus.median()
ax.axvline(pre_med, color=MUTED, lw=1, ls="--", zorder=50)
ax.text(pre_med, len(groups) * spacing + 0.55, "pre-ChatGPT median", ha="center", fontsize=8, color=MUTED)
ax.axvline(np.median(ai_vals), color=AI, lw=1, ls="--", zorder=50)
ax.text(np.median(ai_vals), len(groups) * spacing + 0.55, "AI median", ha="center", fontsize=8, color=AI)
ax.set_xlim(-3, 9)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Similarity to AI-generated code (SDs above the pre-ChatGPT average, averaged over 6 representations)")
ax.set_title("Each semester's distribution, oldest at the top: a tail grows toward AI after ChatGPT\n"
             "(orange ticks = individual submissions classified AI-like)", loc="left")
fig.savefig(FIG / "story_2_ridgeline.png")
plt.close(fig)

# ---------------- 3. Composition: stacked 100% bars ----------------
comp = pd.DataFrame({name: [((stu.group == s) & (stu.p_ai >= lo) & (stu.p_ai < hi)).sum() / (stu.group == s).sum() * 100
                            for s in SEMS] for name, lo, hi, _ in BANDS}, index=SEMS)
story["composition"] = comp.round(1).to_dict()
fig, ax = plt.subplots(figsize=(12, 5.4))
left = np.zeros(len(SEMS))
ypos = np.arange(len(SEMS))[::-1]
for name, _, _, color in BANDS:
    ax.barh(ypos, comp[name].values, left=left, color=color, edgecolor="white", lw=1.5, height=0.72, label=name)
    for y, l, w in zip(ypos, left, comp[name].values):
        if w >= 4:
            ax.text(l + w / 2, y, f"{w:.0f}%", ha="center", va="center", fontsize=8.5,
                    color="white" if color in ("#d9541c",) else INK)
    left += comp[name].values
ax.set_yticks(ypos)
ax.set_yticklabels([LABELS[s] for s in SEMS])
ax.axhline(ypos[4] - 0.5, color=INK, lw=1.2)
ax.text(101, ypos[4] - 0.5, " ChatGPT", va="center", fontsize=8.5, color=MUTED)
ax.set_xlim(0, 100)
ax.set_xlabel("% of submissions")
ax.grid(axis="y", visible=False)
ax.legend(ncol=4, frameon=False, loc="lower left", bbox_to_anchor=(0, 1.0), fontsize=9)
ax.set_title("What each semester is made of, by classifier probability of AI authorship", loc="left", pad=30)
fig.savefig(FIG / "story_3_composition.png")
plt.close(fig)

# ---------------- 4. Every student as a dot ----------------
fig, ax = plt.subplots(figsize=(12.5, 5.6))
rng = np.random.default_rng(1)
q1, q3 = np.percentile(ai_vals, [25, 75])
ax.axhspan(q1, q3, color=AI, alpha=0.12, lw=0)
ax.axhline(np.median(ai_vals), color=AI, lw=1.2, ls="--")
ax.text(len(SEMS) - 0.45, np.median(ai_vals), "AI median\n(band = middle 50% of AI files)", fontsize=8, color=AI, va="center")
for i, s in enumerate(SEMS):
    sub = stu[stu.group == s]
    x = i + rng.uniform(-0.32, 0.32, len(sub))
    base_color = "#b9b8b2" if s not in POST else SEM_COLOR[s]
    ax.scatter(x[~sub.flag.values], sub.consensus.values[~sub.flag.values], s=13, color=base_color, alpha=0.8,
               edgecolor="white", lw=0.3)
    ax.scatter(x[sub.flag.values], sub.consensus.values[sub.flag.values], s=26, color=AI, edgecolor=INK, lw=0.5, zorder=4)
    ax.plot([i - 0.36, i + 0.36], [sub.consensus.median()] * 2, color=INK, lw=2, zorder=5)
ax.axvline(4.5, color=MUTED, ls="--", lw=1)
ax.text(4.55, 8.3, "ChatGPT released", fontsize=8, color=MUTED, va="top")
ax.set_xticks(range(len(SEMS)))
ax.set_xticklabels([LABELS[s] for s in SEMS])
ax.set_xlim(-0.6, len(SEMS) + 0.9)
ax.set_ylim(-3, 8.5)
ax.set_ylabel("Similarity to AI code (SDs)")
ax.set_title("All 741 submissions. Black line = semester median; orange = classified AI-like.\n"
             "Most students stay put; a growing group lands inside the AI band.", loc="left")
fig.savefig(FIG / "story_4_every_student.png")
plt.close(fig)

# ---------------- 5. Cumulative curves ----------------
fig, ax = plt.subplots(figsize=(10, 5.6))
for s in SEMS:
    v = np.sort(stu[stu.group == s].consensus.values)
    ax.step(v, np.arange(1, len(v) + 1) / len(v) * 100, where="post", color=SEM_COLOR[s], lw=2.2 if s in POST else 1.4,
            label=LABELS[s])
v = np.sort(ai_vals)
ax.step(v, np.arange(1, len(v) + 1) / len(v) * 100, where="post", color=AI, lw=2.2, ls="--", label="AI-generated")
ax.set_xlim(-3, 8)
ax.set_xlabel("Similarity to AI code (SDs)")
ax.set_ylabel("% of submissions at or below this similarity")
ax.set_title("Cumulative distributions move right, toward the AI curve, semester after semester\n"
             "(lighter = older, darker = newer)", loc="left")
ax.legend(frameon=False, fontsize=8.5, loc="center left", bbox_to_anchor=(1.01, 0.5))
fig.savefig(FIG / "story_5_cumulative.png")
plt.close(fig)

# ---------------- 6. Four-metric dashboard on a real timeline ----------------
held = stu[stu.held_out_for_signatures]
panels = [
    ("Submissions classified AI-like (%)", tl.pct.values, (tl.pct - tl.lo).values, (tl.hi - tl.pct).values),
    ("Average similarity to AI (SDs)", tl.sim.values, tl.sim_ci.values, tl.sim_ci.values),
    ("AI 'signature' variable names used per file\n(held-out students only)",
     held.groupby("group").signature_ids.mean().reindex(SEMS).values,
     (1.96 * held.groupby("group").signature_ids.sem()).reindex(SEMS).values,
     (1.96 * held.groupby("group").signature_ids.sem()).reindex(SEMS).values),
    ("Students in AI-dominated clusters (%)\n(unsupervised k-means)",
     pd.Series(res["ai_cluster_share_mean"]).reindex(SEMS).values, None, None),
]
fig, axes = plt.subplots(2, 2, figsize=(14, 8.2), sharex=True)
for ax, (title, vals, lo, hi) in zip(axes.ravel(), panels):
    mark_releases(ax, labels=False)
    ax.plot(xs, vals, color="#9db8de", lw=1.4, zorder=2)
    if lo is not None:
        ax.errorbar(xs, vals, yerr=[lo, hi], fmt="none", ecolor=MUTED, lw=1, capsize=2.5, zorder=3)
    ax.scatter(xs, vals, s=60, c=[SEM_COLOR[s] for s in SEMS], edgecolor=INK, lw=0.6, zorder=4)
    ax.annotate(f"{vals[-1]:.1f}", (xs[-1], vals[-1]), xytext=(8, 0), textcoords="offset points", fontsize=9,
                fontweight="bold", va="center")
    ax.set_title(title, loc="left", fontsize=10.5)
    date_axis(ax)
fig.suptitle("Four independent measures, one direction: semester by semester, 2020 to 2025\n"
             "(shaded = after ChatGPT; dotted lines = ChatGPT, GPT-4, GPT-4o, GPT-4o mini, GPT-4.1, GPT-5, Claude Sonnet 4.5 releases)",
             x=0.07, ha="left", fontweight="bold", fontsize=13)
fig.tight_layout()
fig.savefig(FIG / "story_6_dashboard.png")
plt.close(fig)

# ---------------- 7. Binoculars zero-shot detector ----------------
bfile = ROOT / "binoculars_scores.npz"
if bfile.exists():
    z = np.load(bfile)
    b = pd.DataFrame(z["scores"], columns=["binoculars", "log_ppl", "x_ppl"])
    b["path"] = z["paths"]
    sb = stu.merge(b, on="path")
    ab = b[b.path.str.startswith("data/ai/")].copy()
    ab["variant"] = np.where(ab.path.str.contains("-disguise"), "disguise", "assignment")
    print(f"binoculars: {len(sb)} students, {len(ab)} AI files scored")
    pre = sb[sb.group.isin(SEMS[:5])]
    main_ai_b = ab[ab.variant == "assignment"].binoculars.values
    y = np.r_[np.ones(len(main_ai_b)), np.zeros(len(pre))]
    auc = roc_auc_score(y, -np.r_[main_ai_b, pre.binoculars.values])
    threshold = np.percentile(pre.binoculars, 1)
    sb["b_flag"] = sb.binoculars < threshold
    flag_rates = sb.groupby("group").b_flag.mean().reindex(SEMS) * 100
    tpr = float((main_ai_b < threshold).mean())
    tpr_dis = float((ab[ab.variant == "disguise"].binoculars < threshold).mean())
    rho = stats.spearmanr(sb.binoculars, sb.p_ai)
    agree = pd.crosstab(sb.b_flag, sb.flag)
    story["binoculars"] = {"n_students": len(sb), "n_ai": len(ab), "auc_ai_vs_pre": auc, "threshold_1pct_fpr": threshold,
                           "tpr_at_threshold": tpr, "tpr_disguise": tpr_dis, "pct_flagged": flag_rates.round(1).to_dict(),
                           "spearman_with_classifier": rho.statistic, "spearman_p": rho.pvalue,
                           "mean_by_semester": sb.groupby("group").binoculars.mean().reindex(SEMS).round(4).to_dict(),
                           "both_flag": int(agree.loc[True, True]) if True in agree.index and True in agree.columns else 0,
                           "classifier_only": int(agree.loc[False, True]) if True in agree.columns else 0,
                           "binoculars_only": int(agree.loc[True, False]) if True in agree.index else 0}

    fig, ax = plt.subplots(figsize=(12, 5.4))
    data = [sb[sb.group == s].binoculars.values for s in SEMS] + [main_ai_b, ab[ab.variant == "disguise"].binoculars.values]
    labels = [LABELS[s] for s in SEMS] + ["AI", "AI told to\nlook human"]
    parts = ax.violinplot(data, positions=range(len(data)), showmedians=True, widths=0.8)
    for body, s in zip(parts["bodies"], SEMS + ["ai", "ai2"]):
        body.set_facecolor(SEM_COLOR.get(s, AI) if s in POST or s.startswith("ai") else "#b9b8b2")
        if s.startswith("ai"):
            body.set_facecolor(AI)
        body.set_alpha(0.8)
    for key in ("cmedians", "cmins", "cmaxes", "cbars"):
        parts[key].set_color(MUTED)
        parts[key].set_linewidth(1)
    ax.axhline(threshold, color=INK, ls=":", lw=1)
    ax.text(len(data) - 0.5, threshold, " 1% false-positive\n threshold", fontsize=8, va="center")
    ax.axvline(4.5, color=MUTED, ls="--", lw=1)
    ax.axvline(len(SEMS) - 0.5, color=INK, lw=1)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Binoculars score (lower = more machine-like)")
    ax.set_title(f"Zero-shot Binoculars scores by semester: AI and students overlap heavily (AUC = {auc:.2f}), and no semester shifts",
                 loc="left")
    fig.savefig(FIG / "story_7_binoculars_by_semester.png")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1.3, 1]})
    clf_rates = tl.set_index("sem").pct.reindex(SEMS)
    w = 0.38
    axes[0].bar(np.arange(len(SEMS)) - w / 2, clf_rates.values, w, color=INK, label="Trained classifier (ensemble)")
    axes[0].bar(np.arange(len(SEMS)) + w / 2, flag_rates.values, w, color="#6250d6",
                label=f"Binoculars, zero-shot (catches {tpr:.0%} of AI)")
    axes[0].axvline(4.5, color=MUTED, ls="--", lw=1)
    axes[0].set_xticks(range(len(SEMS)))
    axes[0].set_xticklabels([LABELS[s] for s in SEMS], rotation=30, ha="right")
    axes[0].set_ylabel("% of submissions flagged")
    axes[0].legend(frameon=False, fontsize=8.5, loc="upper left")
    axes[0].set_title("Trained classifier finds the trend; zero-shot Binoculars does not", loc="left")
    for s, c in [(SEMS[:5], "#b9b8b2"), (POST, "#2a78d6")]:
        part = sb[sb.group.isin(s)]
        axes[1].scatter(part.p_ai, part.binoculars, s=12, color=c, alpha=0.7, edgecolor="none",
                        label="pre-ChatGPT" if s == SEMS[:5] else "post-ChatGPT")
    axes[1].axhline(threshold, color=INK, ls=":", lw=1)
    axes[1].axvline(0.5, color=INK, ls=":", lw=1)
    axes[1].set_xlabel("Classifier P(AI)")
    axes[1].set_ylabel("Binoculars score (lower = more machine-like)")
    axes[1].set_title(f"Per-student agreement (Spearman ρ = {rho.statistic:.2f})", loc="left")
    axes[1].legend(frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(FIG / "story_8_binoculars_vs_classifier.png")
    plt.close(fig)

(ROOT / "results_story.json").write_text(json.dumps(story, indent=2, default=float))
print(json.dumps({k: v for k, v in story.items() if k != "timeline"}, indent=1, default=float)[:3000])
