"""Embed students + main ChatGPT/Claude generations with hosted code-embedding models via OpenRouter.

Comments are stripped before sending (from AI and student files alike), so names or notes in comments
never leave this machine; lexical/AST/style features still see the full files locally.
Cached per file in embeddings/<encoder>.npz; reruns only embed new files.
Usage: python embed.py <encoder> [<encoder> ...]
"""
import concurrent.futures
import io
import os
import sys
import time
import tokenize
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent
OUT = ROOT / "embeddings"
OUT.mkdir(exist_ok=True)
load_dotenv(ROOT / ".env")

ENCODERS = {
    "openai3large": "openai/text-embedding-3-large",
    "voyagecode": "voyageai/voyage-code-4",
    "codestral": "mistralai/codestral-embed-2505",
    "qwen3emb": "qwen/qwen3-embedding-8b",
}
EMBEDDED_MODELS = ["gpt35", "gpt4", "gpt4o", "gpt4omini", "gpt41", "gpt5", "sonnet45", "haiku45"]
MAX_CHARS = 20000
CHAR_LIMIT = {"openai3large": 12000, "codestral": 12000}


def all_files():
    ai = [p for m in EMBEDDED_MODELS for p in (ROOT / "data/ai" / m).glob("*.py")]
    return sorted(str(p.relative_to(ROOT)) for p in list((ROOT / "data/students").glob("*.py")) + ai)


def strip_comments(code, limit=MAX_CHARS):
    try:
        kept = [t for t in tokenize.generate_tokens(io.StringIO(code).readline) if t.type != tokenize.COMMENT]
        code = tokenize.untokenize(kept)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        code = "\n".join(line.split("#")[0] for line in code.splitlines())
    return "\n".join(line.rstrip() for line in code.splitlines() if line.strip())[:limit]


def embed_batch(name, texts):
    err = None
    for attempt in range(8):
        if attempt:
            time.sleep(2 ** min(attempt, 5))
        try:
            r = requests.post("https://openrouter.ai/api/v1/embeddings", timeout=180,
                              headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                              json={"model": ENCODERS[name], "input": texts})
            data = r.json()["data"]
            return [d["embedding"] for d in sorted(data, key=lambda d: d["index"])]
        except Exception as e:
            err = e
    raise RuntimeError(f"{name}: {err}")


def run(name):
    cache = OUT / f"{name}.npz"
    have = {}
    if cache.exists():
        z = np.load(cache)
        have = dict(zip(z["paths"], z["vecs"]))
    todo = [f for f in all_files() if f not in have]
    print(f"{name}: {len(have)} cached, {len(todo)} to embed", flush=True)
    batches = [todo[i:i + 16] for i in range(0, len(todo), 16)]
    texts = lambda b: [strip_comments((ROOT / f).read_text(errors="replace"), CHAR_LIMIT.get(name, MAX_CHARS)) for f in b]
    with concurrent.futures.ThreadPoolExecutor(6) as ex:
        for batch, vecs in zip(batches, ex.map(lambda b: embed_batch(name, texts(b)), batches)):
            have.update(zip(batch, np.array(vecs, dtype=np.float32)))
    keys = sorted(have)
    np.savez(cache, paths=np.array(keys), vecs=np.vstack([have[k] for k in keys]))
    print(f"{name}: saved {len(keys)}", flush=True)


if __name__ == "__main__":
    for name in sys.argv[1:]:
        run(name)
