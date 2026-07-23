# Context-Injected Fine-Tuning for Bangladeshi Legal QA

Public artifacts for the paper **"Do Small Models Use the Law You Give Them?
Context-Injected Fine-Tuning for Legal QA in Bangladesh"** (Moniruzzaman
Mahadi, Abrar Mohammed Tanzim Alam, Sayma Siddika Monalisa, Mir Mohammad Asif
Abdullah, Mahina Rahman Deya; supervised by Swakkhar Shatabda, BRAC
University, and Md Adnan Arefeen, North South University).

Everything referenced by the paper's Reproducibility Inventory appendix is in
this repository. All data is public statutory and examination text; there is
no personal data.

## Links

- **Main dataset (Hugging Face):** https://huggingface.co/datasets/momahadi/bangladesh-legal-qa-dataset — 2,165 paper-aligned QA/SFT records + law corpus (CC BY 4.0).
- **Bar Council exam benchmark (Hugging Face):** https://huggingface.co/datasets/momahadi/bangladesh-bar-council-exam-dataset — the separate 400-question 2022/2023 evaluation set.
- **Paper (arXiv):** link added once the preprint is posted.
- **License:** CC BY 4.0 for the release team's original contributions; see [`LICENSE.md`](LICENSE.md) for the statutory-source and benchmark carve-outs.

## Contents

```
corpus/       Structured bilingual law corpus (15 JSON files)
qa-dataset/   The 2,165-record bilingual legal QA dataset (6 splits)
sft/          Chat-format fine-tuning files (2 JSONL variants)
evaluation/   The four Bar Council exam benchmark files
results/      Per-question model outputs for all 12 evaluated systems
analysis/     Statistics and audit scripts + their outputs
```

## 1. corpus/ — structured law corpus

Six Bangladeshi acts plus three schedules from the Bar Council syllabus, in
Bangla and English, as one JSON file per act/schedule, preserving section
hierarchy (act, section/order/rule, text, summaries where available).
Loading them with the normalization used in the paper yields 2,519
deduplicated sections. The exact loader (key fallbacks, display format,
dedup) appears in every evaluation notebook and in the corpus-loading cell
reproduced by `analysis/pair_validate.py`'s data expectations.

Note: this corpus covers the Bar Council syllabus, not the full body of
Bangladeshi statute law.

## 2. qa-dataset/ — 2,165 QA records

Six splits by format and language (counts in parentheses):

| File | Records |
|---|---|
| `singlehop bangla.json` (493) | single-section factual QA, Bangla |
| `singlehop english.json` (302) | single-section factual QA, English |
| `advanced selection bangla.json` (407) | multi-option selection, Bangla |
| `advanced selection english.json` (305) | multi-option selection, English |
| `bar exam style bangla.json` (311) | exam-style MCQ, Bangla |
| `bar exam style english.json` (347) | exam-style MCQ, English |

Each record carries the question, options/answer, and the governing
statutory section(s) — the "context injection" of the paper's title. The
2022/2023 benchmark exams below were withheld from generation of these
records (see the paper's leakage discussion in Section 3).

## 3. sft/ — fine-tuning files

- `finetune_answer_only.jsonl` — 2,165 chat-format examples, direct-answer
  style. **This is the variant used for every model in the paper.**
- `finetune_irac_answer.jsonl` — 2,165 examples, IRAC-reasoning style
  (released for completeness; not used in the reported experiments).

Format: one JSON object per line with `messages` (system / user with
question + injected "Retrieved Sections" / assistant answer). The paper's
90/10 train/validation split (1,948/217) is generated at runtime with seed
42; it is not persisted as separate files.

## 4. evaluation/ — the benchmark

Four 100-question files from the 2022 and 2023 Bangladesh Bar Council MCQ
examinations:

- `bar_exam_2022_clean.json`, `bar_exam_2023_clean.json` — Bangla originals.
- `bar_exam_2022_english_fixed.json`, `bar_exam_2023_english.json` — machine
  translations (no independent legal review; see Limitations).

Fields: `question_no`, `question_text`, `options` (dict), `correct_answer`,
`correct_answer_text`.

## 5. results/ — per-question model outputs

One folder per system (base and fine-tuned Qwen3.5 at 0.8B, 2B, 4B). Inside
each: one directory per retrieval condition (zero-shot / BM25 / FAISS
"rag"), each with `run1..run3` (seeds 42, 456, 2024), each holding one
results JSON per exam file. Every record preserves the full raw
`model_output` alongside `predicted_answer` and `is_correct`, so all paper
numbers can be recomputed from scratch — 21,600 outputs in total.

## 6. analysis/ — reproduce the paper's numbers

Run from inside a checkout where `results/` sits at
`<repo>/final push/results` (or edit the `RESULTS` path constant at the top
of each script; they contain no other configuration):

- `strict_mcnemar.py` — the paired significance analysis (Table 5, Appendix
  C): question-clustered exact randomization tests and 36 cell-level exact
  McNemar tests, Holm-corrected. Outputs `strict_mcnemar_holm.csv`,
  `scale_level_significance.csv`.
- `pair_validate.py` — the parser audit (Appendix D): re-validates every
  stored prediction against the letter+text answer contract. Outputs
  `pair_validate_audit.csv`.
- `error_prevalence.py` — the failure-prevalence table (Appendix D): parse
  failures, thinking-mode leakage, language drift. Outputs
  `error_prevalence.csv`.
- `leakage_correlation.py` — the per-cell correlation between fine-tuned
  think-leakage rate and the fine-tuned-minus-base strict delta (Spearman
  rho = -0.47) cited in the Discussion.
- `language_drift_significance.py` - the paired language-drift analysis on
  Bangla outputs. It preserves all nine outputs for each original question as
  one cluster, runs 200,000 two-sided randomizations, and applies Holm
  correction across the three model scales. Its output is
  `language_drift_significance.csv`.

The committed CSVs are the exact outputs used in the paper; rerunning the
scripts on `results/` must reproduce them.

Python 3.10+; no third-party dependencies (standard library only).

## Models

Fine-tuned model weights (merged F16 GGUF) and LoRA adapters are hosted
separately; training configuration is fully specified in the paper
(Section 4 and Appendix A). Base models are the public Qwen3.5 releases.

## License and citation

Statutory text is Bangladeshi public law; exam questions are from public
Bar Council examinations. The QA dataset and SFT files are released for
research use. Please cite the paper when using any component. These
artifacts are research materials, not legal advice.
