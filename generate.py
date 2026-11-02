"""Generate AI Connect 4 solutions via OpenRouter, one folder per model.

Usage: python generate.py <model_short> <count> [--budget USD]
Resumable: existing files are skipped. Stops once the run's spend passes --budget.
"""
import argparse
import concurrent.futures
import json
import os
import re
import threading
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")
KEY = os.environ["OPENROUTER_API_KEY"]

MODELS = {
    "gpt35": {"id": "openai/gpt-3.5-turbo-0613"},
    "gpt4": {"id": "openai/gpt-4"},
    "gpt4o": {"id": "openai/gpt-4o-2024-08-06"},
    "gpt5": {"id": "openai/gpt-5", "reasoning": {"effort": "low"}},
    "sonnet45": {"id": "anthropic/claude-sonnet-4.5"},
    "gemini25": {"id": "google/gemini-2.5-flash"},
    "deepseek": {"id": "deepseek/deepseek-chat-v3-0324"},
    "gpt4omini": {"id": "openai/gpt-4o-mini-2024-07-18"},
    "llama31": {"id": "meta-llama/llama-3.1-70b-instruct"},
    "gpt41": {"id": "openai/gpt-4.1"},
    "haiku45": {"id": "anthropic/claude-haiku-4.5"},
}

SHORT_PROMPT = (
    "write a connect 4 game in python for my intro cs class. 6 rows 7 columns, columns labeled A-G, "
    "2 to 5 players (X O V H M) set by constants, pick a random first player, validate input, "
    "check wins and draws, use os.system('clear'). {style}"
)
DISGUISE_SUFFIX = (
    "Write it the way a real first-year student would, so it doesn't look AI-generated: "
    "no docstrings, few comments, simple variable names, nothing fancy."
)

STYLES = [
    "",
    "Keep it simple, like a beginner would write it.",
    "Add comments explaining the code.",
    "Make the code clean and readable.",
    "Use functions to organize the code.",
    "Keep it short.",
    "Only use basic Python a first-year student would know.",
    "Make sure it gets full marks on the rubric.",
]

PROMPT = (
    "I'm a first-year computer science student. Here is my programming assignment:\n\n"
    + (ROOT / "assignment_prompt.txt").read_text()
    + "\nWrite the complete Python solution. {style}\n"
    "Reply with only the Python code."
)

lock = threading.Lock()
spent = 0.0


def extract_code(text):
    fenced = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.S)
    return max(fenced, key=len) if fenced else text


def build_prompt(variant, style):
    if variant == "short":
        return SHORT_PROMPT.format(style=style)
    if variant == "disguise":
        return PROMPT.format(style=DISGUISE_SUFFIX)
    return PROMPT.format(style=style)


def generate(short, i, budget, variant):
    global spent
    folder = short if variant == "assignment" else f"{short}-{variant}"
    out = ROOT / "data" / "ai" / folder / f"{folder}_{i:04d}.py"
    if out.exists() or spent > budget:
        return
    style = STYLES[i % len(STYLES)]
    body = {
        "model": MODELS[short]["id"],
        "messages": [{"role": "user", "content": build_prompt(variant, style)}],
        "usage": {"include": True},
        "max_tokens": 12000,
    }
    if "reasoning" in MODELS[short]:
        body["reasoning"] = MODELS[short]["reasoning"]
    for attempt in range(3):
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                              headers={"Authorization": f"Bearer {KEY}"}, json=body, timeout=300)
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            break
        except Exception as e:
            err = e
    else:
        print(f"FAIL {short} {i}: {err}")
        return
    code = extract_code(text).strip() + "\n"
    cost = data.get("usage", {}).get("cost", 0) or 0
    out.write_text(code)
    with lock:
        spent += cost
        with open(ROOT / "data" / "ai" / "metadata.jsonl", "a") as f:
            f.write(json.dumps({"file": str(out.relative_to(ROOT)), "model": MODELS[short]["id"],
                                "variant": variant, "style": style, "cost": cost,
                                "usage": data.get("usage")}) + "\n")
        print(f"{short} {i} lines={code.count(chr(10))} cost=${cost:.4f} run_total=${spent:.2f}", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("model", choices=MODELS)
    p.add_argument("count", type=int)
    p.add_argument("--budget", type=float, default=5.0)
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--prompt", choices=["assignment", "short", "disguise"], default="assignment")
    a = p.parse_args()
    folder = a.model if a.prompt == "assignment" else f"{a.model}-{a.prompt}"
    (ROOT / "data" / "ai" / folder).mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda i: generate(a.model, i, a.budget, a.prompt), range(a.count)))


if __name__ == "__main__":
    main()
