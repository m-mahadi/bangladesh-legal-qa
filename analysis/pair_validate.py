"""Letter+text pairing audit for stored predictions.

Design rationale (from the authors): fine-tuned models were trained to state
the option letter TOGETHER with the option text ("Therefore, (C) Property
only is correct.", "সুতরাং সঠিক উত্তর হলো **(ক) সম্পত্তি বা অফিস**।"), and base
models were instructed to end with "Answer: (X) full option text". A stored
prediction is therefore verifiable: the predicted letter should appear in the
output immediately followed by (a prefix of) that letter's option text. A
letter inside a legal citation is never followed by the option text, so this
check cannot be fooled by citations.

For every record we compute:
  pair_pred  = letter of the LAST letter+text-validated pair in the output
  agreement  = does pair_pred match the stored legacy predicted_answer?

Outputs pair_validate_audit.csv per (scale, variant, exam, mode) with
agreement counts, and prints overall stats plus the cells with most
disagreement for manual inspection.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "final push" / "results"
OUT = Path(__file__).resolve().parent / "pair_validate_audit.csv"

MODELS = {
    "0.8B": {
        "base": RESULTS / "qwen3.5-0.8b-base-aII",
        "ft": RESULTS / "qwen 3.5 0.8b finetuned all",
    },
    "2B": {
        "base": RESULTS / "qwen3.5-2b-base-aII",
        "ft": RESULTS / "qwen 3.5 2b finetuned all",
    },
    "4B": {
        "base": RESULTS / "qwen3.5-4b-base-aII",
        "ft": RESULTS / "qwen 3.5-4b-finetuned-all",
    },
}
MODES = {"None": "zero", "BM25": "bm25", "FAISS": "rag"}
EXAMS = {
    "2022 English": "bar_exam_2022_english_fixed",
    "2022 Bangla": "bar_exam_2022_clean",
    "2023 English": "bar_exam_2023_english",
    "2023 Bangla": "bar_exam_2023_clean",
}

_THINK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL)


def clean(text: str) -> str:
    for m in ["<|im_end|>", "<|im_start|>", "<|endoftext|>"]:
        if m in text:
            text = text.split(m)[0]
    return _THINK_RE.sub("", text)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", str(s)).lower()
    return re.sub(r"[\s\*\.\,\।\(\)\[\]\"'“”‘’:;\-–—]+", "", s)


def pair_predict(raw: str, options: dict) -> str | None:
    """Letter of the LAST occurrence where a key is followed by its option
    text (normalized prefix match within the next 80 raw chars)."""
    text = clean(str(raw or ""))
    best_pos, best_key = -1, None
    for k, opt_text in options.items():
        k = str(k).strip()
        tgt = norm(opt_text)
        if not k or not tgt:
            continue
        prefix = tgt[: min(len(tgt), 10)]
        for m in re.finditer(re.escape(k), text):
            window = norm(text[m.end() : m.end() + 80])
            if window.startswith(prefix):
                if m.start() > best_pos:
                    best_pos, best_key = m.start(), k
    return best_key


def mode_dir(root: Path, token: str) -> Path:
    matches = [p for p in root.iterdir() if p.is_dir() and token in p.name.lower()]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {token!r} dir under {root}: {matches}")
    return matches[0]


def run_files(root: Path, mode: str, exam_stem: str) -> list[Path]:
    folder = mode_dir(root, MODES[mode])
    run_dirs = sorted(
        p for p in folder.iterdir() if p.is_dir() and p.name.lower().startswith("run")
    )
    if len(run_dirs) != 3:
        raise RuntimeError(f"Expected three runs under {folder}: {run_dirs}")
    out = []
    for rd in run_dirs:
        hits = list(rd.glob(f"*{exam_stem}*results.json"))
        if len(hits) != 1:
            raise RuntimeError(f"Expected one {exam_stem} result in {rd}: {hits}")
        out.append(hits[0])
    return out


def main() -> None:
    rows = []
    tot = agree = both_null = legacy_only = pair_only = differ = 0
    for scale, variants in MODELS.items():
        for variant, root in variants.items():
            for exam_label, exam_stem in EXAMS.items():
                for mode in MODES:
                    c_agree = c_lonly = c_ponly = c_diff = c_bnull = 0
                    legacy_sc = pair_sc = 0
                    runs = []
                    for fp in run_files(root, mode, exam_stem):
                        recs = json.loads(fp.read_text(encoding="utf-8"))
                        run = []
                        for r in recs:
                            tot += 1
                            l = r.get("predicted_answer")
                            p = pair_predict(r.get("model_output"), r["options"])
                            run.append((r["correct_answer"], l, p))
                            if l == p:
                                if l is None:
                                    c_bnull += 1
                                    both_null += 1
                                else:
                                    c_agree += 1
                                    agree += 1
                            elif p is None:
                                c_lonly += 1
                                legacy_only += 1
                            elif l is None:
                                c_ponly += 1
                                pair_only += 1
                            else:
                                c_diff += 1
                                differ += 1
                        runs.append(run)
                    n = len(runs[0])
                    legacy_sc = sum(
                        all(run[i][1] == run[i][0] for run in runs) for i in range(n)
                    )
                    pair_sc = sum(
                        all(run[i][2] == run[i][0] for run in runs) for i in range(n)
                    )
                    rows.append(
                        {
                            "scale": scale,
                            "variant": variant,
                            "exam": exam_label,
                            "mode": mode,
                            "agree_nonnull": c_agree,
                            "both_null": c_bnull,
                            "legacy_only": c_lonly,
                            "pair_only": c_ponly,
                            "letter_differs": c_diff,
                            "legacy_strictcons": legacy_sc,
                            "pair_strictcons": pair_sc,
                        }
                    )
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"outputs audited: {tot}")
    print(f"  letter agrees (non-null):        {agree} ({agree/tot:.1%})")
    print(f"  both unparsed/unvalidated:       {both_null} ({both_null/tot:.1%})")
    print(f"  legacy has letter, pair cannot validate: {legacy_only} ({legacy_only/tot:.1%})")
    print(f"  pair validates, legacy null:     {pair_only} ({pair_only/tot:.1%})")
    print(f"  DIFFERENT letters (worst case):  {differ} ({differ/tot:.1%})")
    print()
    worst = sorted(rows, key=lambda r: -r["letter_differs"])[:8]
    print("cells with most letter-level conflicts:")
    for r in worst:
        print(
            f"  {r['scale']} {r['variant']:4s} {r['exam']:12s} {r['mode']:5s} "
            f"differs={r['letter_differs']} legacy_only={r['legacy_only']} "
            f"strictcons legacy={r['legacy_strictcons']} pair={r['pair_strictcons']}"
        )


if __name__ == "__main__":
    main()
