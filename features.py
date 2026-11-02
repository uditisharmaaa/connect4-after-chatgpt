"""Load student + AI files; compute lexical TF-IDF, AST TF-IDF and style features (embeddings live in embed.py)."""
import ast
import io
import re
import tokenize
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings("ignore")
ROOT = Path(__file__).parent

SEMESTERS = ["Pre-2021", "Spring 2021", "Fall 2021", "Spring 2022", "Fall 2022", "Spring 2023", "Fall 2023",
             "Spring 2024", "Fall 2024", "Spring 2025", "Fall 2025", "Spring 2026"]
FIRST_AI_SEMESTER = "Spring 2023"
MODEL_NAMES = {"gpt35": "GPT-3.5", "gpt4": "GPT-4", "gpt4o": "GPT-4o", "gpt4omini": "GPT-4o mini",
               "gpt41": "GPT-4.1", "gpt5": "GPT-5", "sonnet45": "Claude Sonnet 4.5", "haiku45": "Claude Haiku 4.5",
               "gemini25": "Gemini 2.5 Flash", "deepseek": "DeepSeek V3", "llama31": "Llama 3.1 70B"}
MAIN_MODELS = ["gpt35", "gpt4", "gpt4o", "gpt4omini", "gpt41", "gpt5", "sonnet45", "haiku45"]
OTHER_MODELS = ["gemini25", "deepseek", "llama31"]
FAMILY = {m: "Claude" if m in ("sonnet45", "haiku45") else "Other" if m in OTHER_MODELS else "ChatGPT" for m in MODEL_NAMES}
MODEL_RELEASE = {"gpt35": "Nov 2022", "gpt4": "Mar 2023", "gpt4o": "May 2024", "gpt4omini": "Jul 2024",
                 "gpt41": "Apr 2025", "gpt5": "Aug 2025", "sonnet45": "Sep 2025", "haiku45": "Oct 2025",
                 "gemini25": "Jun 2025", "deepseek": "Mar 2025", "llama31": "Jul 2024"}
AVAILABLE_FROM = {"gpt35": "Spring 2023", "gpt4": "Spring 2023", "gpt4o": "Fall 2024", "gpt4omini": "Fall 2024",
                  "gpt41": "Fall 2025", "gpt5": "Fall 2025", "sonnet45": "Fall 2025", "haiku45": "Spring 2026",
                  "gemini25": "Fall 2025", "deepseek": "Fall 2025", "llama31": "Fall 2024"}
ERA_MODEL = {"Spring 2023": "gpt35", "Fall 2023": "gpt35", "Fall 2024": "gpt4o", "Fall 2025": "gpt5"}


def semester_of(name):
    if name.lower().startswith("old_submissions"):
        return "Pre-2021"
    year, term = name.split("_")[:2]
    return f"{term.capitalize()} {year}"


def load():
    rows = []
    for f in sorted((ROOT / "data/students").glob("*.py")):
        rows.append(dict(path=str(f.relative_to(ROOT)), source="student", group=semester_of(f.name), model="", variant=""))
    for f in sorted((ROOT / "data/ai").glob("*/*.py")):
        model, _, variant = f.parent.name.partition("-")
        rows.append(dict(path=str(f.relative_to(ROOT)), source="ai", group=f.parent.name, model=model, variant=variant or "assignment"))
    df = pd.DataFrame(rows)
    df["code"] = [(ROOT / p).read_text(errors="replace") for p in df.path]
    df["post_chatgpt"] = df.group.map(lambda g: g in SEMESTERS and SEMESTERS.index(g) >= SEMESTERS.index(FIRST_AI_SEMESTER))
    return df


def code_tokens(code):
    """Python tokens with comments dropped, strings -> STR, numbers -> NUM."""
    out = []
    try:
        for t in tokenize.generate_tokens(io.StringIO(code).readline):
            if t.type == tokenize.COMMENT or t.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                                                       tokenize.DEDENT, tokenize.ENDMARKER):
                continue
            out.append("STR" if t.type == tokenize.STRING else "NUM" if t.type == tokenize.NUMBER else t.string)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        out = re.findall(r"[A-Za-z_]\w*|\S", re.sub(r"#.*", "", code))
    return " ".join(out)


def ast_nodes(code):
    try:
        return " ".join(type(n).__name__ for n in ast.walk(ast.parse(code)))
    except Exception:
        return ""


def style_features(code):
    lines = code.splitlines()
    nonblank = [l for l in lines if l.strip()]
    n = max(len(nonblank), 1)
    try:
        tree = ast.parse(code)
        nodes = list(ast.walk(tree))
        funcs = [x for x in nodes if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))]
        docstrings = sum(ast.get_docstring(x) is not None for x in funcs + [tree])
        typed = sum(x.returns is not None or any(a.annotation for a in x.args.args) for x in funcs)
        names = [x.id for x in nodes if isinstance(x, ast.Name)] + [x.name for x in funcs]
        parses = 1
    except Exception:
        funcs, docstrings, typed, names, nodes, parses = [], 0, 0, [], [], 0
    return {
        "parses": parses,
        "lines": n,
        "comment_ratio": sum(l.strip().startswith("#") for l in lines) / n,
        "functions": len(funcs),
        "docstrings": docstrings,
        "type_hints": typed,
        "fstrings": len(re.findall(r"\bf[\"']", code)),
        "main_guard": int("__name__" in code and "__main__" in code),
        "avg_name_len": float(np.mean([len(x) for x in names])) if names else 0.0,
        "snake_case": float(np.mean(["_" in x for x in names])) if names else 0.0,
        "global_stmts": len(re.findall(r"^\s*global\s", code, re.M)),
        "enumerate": code.count("enumerate("),
        "range_len": code.count("range(len("),
        "comprehensions": sum(isinstance(x, (ast.ListComp, ast.GeneratorExp)) for x in nodes),
        "try_except": sum(isinstance(x, ast.Try) for x in nodes),
        "avg_line_len": float(np.mean([len(l) for l in nonblank])) if nonblank else 0.0,
        "spec_five_checkers": int(all(re.search(rf"[\"']{c}[\"']", code) for c in "VHM")),
        "spec_clear": int("clear" in code and "system" in code),
        "spec_random": int("random" in code),
    }


def main():
    df = load()
    print(df.groupby(["source", "group"]).size())
    lexical = TfidfVectorizer(token_pattern=r"\S+", ngram_range=(1, 3), min_df=2, sublinear_tf=True)
    X_lex = lexical.fit_transform(df.code.map(code_tokens))
    structural = TfidfVectorizer(token_pattern=r"\S+", ngram_range=(1, 3), min_df=2, sublinear_tf=True)
    X_ast = structural.fit_transform(df.code.map(ast_nodes))
    style = pd.DataFrame([style_features(c) for c in df.code])
    meta = pd.concat([df.drop(columns="code"), style], axis=1)
    meta.to_csv(ROOT / "features.csv", index=False)
    import scipy.sparse as sp
    sp.save_npz(ROOT / "lexical.npz", X_lex)
    sp.save_npz(ROOT / "ast.npz", X_ast)
    import json
    (ROOT / "vocab.json").write_text(json.dumps({"lexical": lexical.get_feature_names_out().tolist(),
                                                 "ast": structural.get_feature_names_out().tolist()}))


if __name__ == "__main__":
    main()
