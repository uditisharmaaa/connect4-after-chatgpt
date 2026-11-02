"""Zero-shot AI-code detection with the Binoculars score (Hans et al., 2024), using a small open model pair (SmolLM2-360M base + Instruct).

score = log-perplexity under the observer / cross-perplexity between observer and performer.
Lower = more machine-like. No training on our data. Scores cached per file in binoculars_scores.npz.
Usage: python binoculars.py [--limit N]   (N = files to score this run, for benchmarking)
"""
import argparse
import os
import time
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).parent
CACHE = ROOT / "binoculars_scores.npz"
OBSERVER, PERFORMER = "HuggingFaceTB/SmolLM2-360M", "HuggingFaceTB/SmolLM2-360M-Instruct"
MAX_TOKENS = 768
MAIN_MODELS = ["gpt35", "gpt4", "gpt4o", "gpt4omini", "gpt41", "gpt5", "sonnet45", "haiku45"]
DISGUISE = ["gpt35-disguise", "gpt4o-disguise", "gpt5-disguise", "sonnet45-disguise"]
torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "8")))


def files():
    """All students, 50 files per main model, 25 per 'look human' variant (fixed, reproducible picks)."""
    picks = sorted((ROOT / "data/students").glob("*.py"))
    for m in MAIN_MODELS:
        picks += sorted((ROOT / "data/ai" / m).glob("*.py"))[:50]
    for m in DISGUISE:
        picks += sorted((ROOT / "data/ai" / m).glob("*.py"))[:25]
    return [str(p.relative_to(ROOT)) for p in picks]


def score(code, tok, obs, perf):
    ids = tok(code, return_tensors="pt", truncation=True, max_length=MAX_TOKENS)["input_ids"]
    with torch.no_grad():
        lo = obs(ids).logits[0, :-1].float()
        lp = perf(ids).logits[0, :-1].float()
    target = ids[0, 1:]
    log_p_obs = torch.log_softmax(lo, -1)
    log_ppl = torch.nn.functional.nll_loss(log_p_obs, target).item()
    x_ppl = (-(torch.softmax(lp, -1) * log_p_obs).sum(-1)).mean().item()
    return log_ppl / x_ppl, log_ppl, x_ppl


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--limit", type=int, default=None)
    args = a.parse_args()
    tok = AutoTokenizer.from_pretrained(OBSERVER)
    obs = AutoModelForCausalLM.from_pretrained(OBSERVER, dtype=torch.float32).eval()
    perf = AutoModelForCausalLM.from_pretrained(PERFORMER, dtype=torch.float32).eval()
    have = {}
    if CACHE.exists():
        z = np.load(CACHE)
        have = {p: row for p, row in zip(z["paths"], z["scores"])}
    todo = [f for f in files() if f not in have][:args.limit]
    print(f"{len(have)} cached, {len(todo)} to score", flush=True)
    start = time.time()
    for k, f in enumerate(todo, 1):
        have[f] = np.array(score((ROOT / f).read_text(errors="replace"), tok, obs, perf))
        if k % 50 == 0 or k == len(todo):
            keys = sorted(have)
            np.savez(CACHE, paths=np.array(keys), scores=np.vstack([have[p] for p in keys]))
            print(f"{k}/{len(todo)}  {(time.time() - start) / k:.2f}s/file", flush=True)


if __name__ == "__main__":
    main()
