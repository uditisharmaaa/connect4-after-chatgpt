"""AI-polishing experiment: give real pre-ChatGPT student files to a chatbot and ask it to fix/clean them.

Answers: what does "student code touched by AI" look like, as opposed to code written by AI from scratch?
Comments are stripped before sending. Output: data/polished/<condition>/<original name>.py (resumable).
Usage: python polish.py <condition> [--n 100] [--budget USD]
"""
import argparse
import concurrent.futures
import json
import random
import threading
from pathlib import Path

from embed import strip_comments
from generate import KEY, extract_code

import requests

ROOT = Path(__file__).parent
CONDITIONS = {
    "gpt4omini-clean": ("openai/gpt-4o-mini-2024-07-18", "clean"),
    "gpt4o-clean": ("openai/gpt-4o-2024-08-06", "clean"),
    "sonnet45-clean": ("anthropic/claude-sonnet-4.5", "clean"),
    "gpt4o-fixonly": ("openai/gpt-4o-2024-08-06", "fixonly"),
}
ASKS = {
    "clean": "Here is my Connect 4 code for my intro CS assignment. Fix any bugs and clean it up so it gets full marks.",
    "fixonly": "Here is my Connect 4 code for my intro CS assignment. Fix only the bugs. Keep my code and my style "
               "exactly as they are otherwise.",
}
PRE = ("old_submissions", "2021_", "2022_")
lock = threading.Lock()
spent = 0.0


def sample(n):
    files = sorted(p for p in (ROOT / "data/students").glob("*.py") if p.name.lower().startswith(PRE))
    return random.Random(0).sample(files, n)


def polish(condition, src, budget):
    global spent
    out = ROOT / "data/polished" / condition / src.name
    if out.exists() or spent > budget:
        return
    model, ask = CONDITIONS[condition]
    prompt = f"{ASKS[ask]}\n\n```python\n{strip_comments(src.read_text(errors='replace'))}\n```\n\nReply with only the full Python code."
    for _ in range(3):
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", timeout=300,
                              headers={"Authorization": f"Bearer {KEY}"},
                              json={"model": model, "messages": [{"role": "user", "content": prompt}],
                                    "usage": {"include": True}, "max_tokens": 8000})
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            break
        except Exception as e:
            err = e
    else:
        print(f"FAIL {condition} {src.name}: {err}")
        return
    out.write_text(extract_code(text).strip() + "\n")
    with lock:
        spent += data.get("usage", {}).get("cost", 0) or 0
        with open(ROOT / "data/polished/metadata.jsonl", "a") as f:
            f.write(json.dumps({"condition": condition, "source": src.name, "cost": data.get("usage", {}).get("cost")}) + "\n")
        print(f"{condition} {src.name} run_total=${spent:.2f}", flush=True)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("condition", choices=CONDITIONS)
    a.add_argument("--n", type=int, default=100)
    a.add_argument("--budget", type=float, default=5.0)
    args = a.parse_args()
    (ROOT / "data/polished" / args.condition).mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda s: polish(args.condition, s, args.budget), sample(args.n)))


if __name__ == "__main__":
    main()
