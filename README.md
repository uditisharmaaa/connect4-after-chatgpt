# Connect 4 After ChatGPT

Senior capstone, NYU Abu Dhabi (Uditi Sharma). Has intro-CS student code become more similar to AI-generated code since ChatGPT, semester by semester?

The study compares 741 student submissions of CS-UH 1001 Assignment 2 (Connect 4) from nine semesters (2020 to Fall 2025) with 4,100 AI-generated solutions to the same assignment, using six code representations and a battery of statistical tests.

## Headline results

- Similarity to AI code grows every post-ChatGPT semester: Cohen's d = 0.78, 1.01, 1.35, 1.49 vs pre-ChatGPT students (all p < 0.001).
- A second, AI-like group of submissions appears only after ChatGPT: one population in every pre-ChatGPT semester, two in every post-ChatGPT semester.
- Submissions classified AI-like: 1 of 401 before ChatGPT vs 35 of 340 after (Fisher p = 1e-11); 16.5% in Fall 2024 and 20.3% in Fall 2025.
- AI-polished student code lands where the typical 2024-25 student sits and is rarely flagged, so 20% is a floor on AI involvement.
- Every representation analysed on its own (incl. Jina Code v2) shows the jump: 0-2.5% of students in AI-dominated clusters before ChatGPT, 19-39% in Fall 2025 (`results_per_embedding.json`).
- Part of the drift in the *average* student predates ChatGPT; the causal claim rests on the new AI-like group.

All numbers are in `results.json`, `results_baseline2021.json`, `results_extra.json` and `results_story.json`.

## What is in this repo

| Path | Contents |
| --- | --- |
| `data/ai/<model>/` | AI solutions: 300 each from GPT-3.5, GPT-4, GPT-4o, GPT-4o mini, GPT-4.1, GPT-5, Claude Sonnet 4.5, Claude Haiku 4.5, Gemini 2.5 Flash, DeepSeek V3, Llama 3.1 70B; 100 each of "short prompt" and "look human" variants |
| `data/ai/metadata.jsonl` | Model, style instruction, token usage and cost per generation |
| `data/ai_excluded/` | Generations left out of the analysis (extras beyond 300, a broken-provider model, partial variants) |
| `figures/`, `figures_baseline2021/` | Every chart; the second folder is the sensitivity run without the Pre-2021 archive |
| `results*.json`, `ai_scores.csv` | Aggregate results per semester and per-AI-file scores |

## What is not in this repo

- **Student submissions** and everything derived from them (AI-polished copies, per-student scores, feature and embedding caches). They belong to the course instructor and are analysed only in aggregate.
- **The assignment text** (`assignment_prompt.txt`), which the course asks not to be published.
- **`.env`** with the OpenRouter API key.

To rerun everything, place the instructor's submission files in `data/students/` (named like `2023_Fall_296.py`, `Old_Submissions_69.py`), the assignment text in `assignment_prompt.txt`, and `OPENROUTER_API_KEY=...` plus `JINA_API_KEY=...` in `.env`.

## Pipeline

```bash
python generate.py gpt5 300                 # AI solutions via OpenRouter (resumable, budget-capped)
python generate.py gpt5 100 --prompt short  # prompt variants: short | disguise
python features.py                          # lexical TF-IDF, AST and style features
python embed.py openai3large voyagecode codestral qwen3emb jina   # code embeddings (comments stripped; Jina needs JINA_API_KEY)
python analyze.py                           # main analysis -> figures/ + results.json
BASELINE=2021 python analyze.py             # sensitivity run without Pre-2021
python polish.py gpt4o-clean                # AI-polishing experiment (4 conditions)
python extra_analysis.py                    # per-semester table, two-group test, polishing, attribution
python per_embedding.py                     # each representation alone: PCA cluster maps, cluster share, own classifier
python binoculars.py && python semester_charts.py   # zero-shot detector + presentation charts
```

Python 3.12, packages in `requirements.txt`. Cost: about $67 for generations, about $7 for embeddings and the polishing experiment.

## Notes

- Semesters: Spring = January-May, Fall = September-December. ChatGPT launched 30 November 2022, so Fall 2022 is pre-ChatGPT.
- The Pre-2021 archive follows an older spec without the 2-5 player requirement; every key result is repeated without it.
- "AI-like" describes code style at the group level. It is not evidence that any individual student used AI.
