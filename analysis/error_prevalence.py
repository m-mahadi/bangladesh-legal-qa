"""Error-prevalence statistics from the preserved per-question outputs.

Computes, per (scale, variant, exam language) aggregated over years, runs,
and retrieval modes (n = 1,800 outputs per row):

  null_pct   : stored predicted_answer is null (parse failure).
  think_pct  : output contains a model-emitted <think> block (thinking-mode
               leakage; the training data disabled thinking).
  novis_pct  : no visible alphabetic text remains once think content and chat
               markers are removed (the model never produced a readable
               answer outside its reasoning).
  drift_pct  : Bangla exams only; among outputs WITH visible text, the share
               whose visible text is majority non-Bangla script (the model
               answered a Bangla question in English).

Writes error_prevalence.csv (per-mode and aggregate rows) next to this file.
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "final push" / "results"
OUT = Path(__file__).resolve().parent / "error_prevalence.csv"

ROOTS = {
    "qwen3.5-0.8b-base-aII": ("0.8B", "base"),
    "qwen 3.5 0.8b finetuned all": ("0.8B", "ft"),
    "qwen3.5-2b-base-aII": ("2B", "base"),
    "qwen 3.5 2b finetuned all": ("2B", "ft"),
    "qwen3.5-4b-base-aII": ("4B", "base"),
    "qwen 3.5-4b-finetuned-all": ("4B", "ft"),
}
CHAT = re.compile(r"<\|im_(?:start|end)\|>|<\|endoftext\|>")
THINK = re.compile(r"<think\b[^>]*>.*?(?:</think\s*>|\Z)", re.S | re.I)


def bangla_fraction(text: str) -> float | None:
    alpha = [c for c in text if c.isalpha()]
    if not alpha:
        return None
    return sum(1 for c in alpha if "ঀ" <= c <= "৿") / len(alpha)


def main() -> None:
    stats: dict = defaultdict(
        lambda: {"n": 0, "null": 0, "think": 0, "novis": 0, "drift": 0, "vis": 0}
    )
    for root, (scale, variant) in ROOTS.items():
        for fp in (RESULTS / root).rglob("*results.json"):
            head = str(fp.relative_to(RESULTS / root)).lower().split("run")[0]
            mode = "zero" if "zero" in head else ("bm25" if "bm25" in head else "rag")
            lang = "Bangla" if "clean" in fp.name else "English"
            for key in [(scale, variant, lang, mode), (scale, variant, lang, "all")]:
                s = stats[key]
                for r in json.loads(fp.read_text(encoding="utf-8")):
                    s["n"] += 1
                    s["null"] += r["predicted_answer"] is None
                    raw = CHAT.sub("", r.get("model_output") or "")
                    s["think"] += "<think>" in raw
                    frac = bangla_fraction(THINK.sub("", raw))
                    if frac is None:
                        s["novis"] += 1
                    else:
                        s["vis"] += 1
                        if lang == "Bangla" and frac < 0.5:
                            s["drift"] += 1
    rows = []
    for (scale, variant, lang, mode), s in sorted(stats.items()):
        rows.append(
            {
                "scale": scale,
                "variant": variant,
                "language": lang,
                "mode": mode,
                "n": s["n"],
                "null_pct": round(100 * s["null"] / s["n"], 2),
                "think_pct": round(100 * s["think"] / s["n"], 2),
                "novis_pct": round(100 * s["novis"] / s["n"], 2),
                "drift_pct": round(100 * s["drift"] / s["vis"], 2)
                if lang == "Bangla" and s["vis"]
                else "",
            }
        )
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows -> {OUT.name}")
    print(f"{'scale':5} {'var':4} {'lang':7} {'null%':>6} {'think%':>7} {'novis%':>7} {'drift%':>7}")
    for r in rows:
        if r["mode"] == "all":
            print(
                f"{r['scale']:5} {r['variant']:4} {r['language']:7} "
                f"{r['null_pct']:6} {r['think_pct']:7} {r['novis_pct']:7} "
                f"{r['drift_pct'] if r['drift_pct'] != '' else '-':>7}"
            )


if __name__ == "__main__":
    main()
