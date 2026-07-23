"""Correlation between fine-tuned thinking-mode leakage and the
fine-tuned-minus-base strict-consistency delta, per evaluation cell.

For each of the 36 cells (scale x exam file x retrieval mode) computes the
fine-tuned model's <think>-leakage rate over its 300 outputs and the
strict-consistency delta (fine-tuned minus base, out of 100), then reports
Pearson r and Spearman rho. Cited in the Discussion section.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "final push" / "results"
ROOTS = {
    "qwen3.5-0.8b-base-aII": ("0.8B", "base"),
    "qwen 3.5 0.8b finetuned all": ("0.8B", "ft"),
    "qwen3.5-2b-base-aII": ("2B", "base"),
    "qwen 3.5 2b finetuned all": ("2B", "ft"),
    "qwen3.5-4b-base-aII": ("4B", "base"),
    "qwen 3.5-4b-finetuned-all": ("4B", "ft"),
}


def main() -> None:
    cells: dict = defaultdict(
        lambda: {
            "leak": 0,
            "n": 0,
            "runs": {"base": defaultdict(list), "ft": defaultdict(list)},
        }
    )
    for root, (scale, variant) in ROOTS.items():
        for fp in (RESULTS / root).rglob("*results.json"):
            head = str(fp).lower().split("run")[0]
            mode = (
                "zero" if "zero" in head else ("bm25" if "bm25" in head else "rag")
            )
            exam = fp.name.split("bar_exam_")[-1].replace("-results.json", "")
            key = (scale, exam, mode)
            for i, r in enumerate(json.loads(fp.read_text(encoding="utf-8"))):
                if variant == "ft":
                    cells[key]["leak"] += "<think>" in (r["model_output"] or "")
                    cells[key]["n"] += 1
                cells[key]["runs"][variant][i].append(
                    r["predicted_answer"] == r["correct_answer"]
                )
    xs, ys = [], []
    for key in sorted(cells):
        c = cells[key]
        leak = 100 * c["leak"] / c["n"]
        sc = {
            v: sum(all(w) for w in c["runs"][v].values() if len(w) == 3)
            for v in ("base", "ft")
        }
        xs.append(leak)
        ys.append(sc["ft"] - sc["base"])
        print(f"{key[0]:5} {key[1]:24} {key[2]:5} leak={leak:5.1f}%  "
              f"delta={sc['ft'] - sc['base']:+3d}")

    def pearson(a: list, b: list) -> float:
        n = len(a)
        ma, mb = sum(a) / n, sum(b) / n
        cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        sa = sum((x - ma) ** 2 for x in a) ** 0.5
        sb = sum((y - mb) ** 2 for y in b) ** 0.5
        return cov / (sa * sb)

    def ranks(v: list) -> list:
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0] * len(v)
        for rank, i in enumerate(order):
            out[i] = rank
        return out

    print(f"\ncells: {len(xs)}")
    print(f"Pearson r    = {pearson(xs, ys):.3f}")
    print(f"Spearman rho = {pearson(ranks(xs), ranks(ys)):.3f}")


if __name__ == "__main__":
    main()
