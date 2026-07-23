"""Question-clustered paired test of Bangla-to-English language drift."""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
from pathlib import Path

CHAT = re.compile(r"<\|im_(?:start|end)\|>|<\|endoftext\|>")
THINK = re.compile(r"<think\b[^>]*>.*?(?:</think\s*>|\Z)", re.S | re.I)
MODELS = {
    "0.8B": ("qwen3.5-0.8b-base-aII", "qwen 3.5 0.8b finetuned all"),
    "2B": ("qwen3.5-2b-base-aII", "qwen 3.5 2b finetuned all"),
    "4B": ("qwen3.5-4b-base-aII", "qwen 3.5-4b-finetuned-all"),
}
MODES = ("zero", "bm25", "rag")
EXAMS = ("bar_exam_2022_clean", "bar_exam_2023_clean")


def mode_dir(root: Path, token: str) -> Path:
    matches = [p for p in root.iterdir() if p.is_dir() and token in p.name.lower()]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {token!r} directory under {root}: {matches}")
    return matches[0]


def load_runs(root: Path, mode: str, exam: str) -> list[list[dict]]:
    folder = mode_dir(root, mode)
    run_dirs = sorted(p for p in folder.iterdir() if p.is_dir() and p.name.lower().startswith("run"))
    if len(run_dirs) != 3:
        raise RuntimeError(f"Expected three runs under {folder}: {run_dirs}")
    runs = []
    for run_dir in run_dirs:
        hits = list(run_dir.glob(f"*{exam}*results.json"))
        if len(hits) != 1:
            raise RuntimeError(f"Expected one {exam} result in {run_dir}: {hits}")
        runs.append(json.loads(hits[0].read_text(encoding="utf-8-sig")))
    keys = [[(r.get("question_no"), r.get("correct_answer")) for r in run] for run in runs]
    if any(len(run) != 100 for run in runs) or keys[1:] != keys[:1] * 2:
        raise RuntimeError(f"Question alignment differs under {folder}, {exam}")
    return runs


def classify(record: dict) -> tuple[int, int]:
    visible = THINK.sub("", CHAT.sub("", record.get("model_output") or ""))
    letters = [c for c in visible if c.isalpha()]
    if not letters:
        return 0, 0
    bangla = sum("\u0980" <= c <= "\u09ff" for c in letters)
    return int(bangla / len(letters) < 0.5), 1


def clusters(root: Path) -> tuple[list[tuple[int, int]], list[tuple]]:
    out, keys = [], []
    for exam in EXAMS:
        loaded = [load_runs(root, mode, exam) for mode in MODES]
        for question in range(100):
            records = [run[question] for mode_runs in loaded for run in mode_runs]
            out.append(tuple(map(sum, zip(*(classify(r) for r in records)))))
            keys.append((exam, records[0].get("question_no"), records[0].get("correct_answer")))
    return out, keys


def randomization_p(base: list[tuple[int, int]], ft: list[tuple[int, int]], permutations: int, seed: int) -> float:
    bd, bv = map(sum, zip(*base))
    fd, fv = map(sum, zip(*ft))
    observed = fd / fv - bd / bv
    deltas = [(f[0] - b[0], f[1] - b[1]) for b, f in zip(base, ft)]
    rng, extreme = random.Random(seed), 0
    for _ in range(permutations):
        swap_d = swap_v = 0
        bits = rng.getrandbits(len(deltas))
        for i, (dd, dv) in enumerate(deltas):
            if bits >> i & 1:
                swap_d += dd
                swap_v += dv
        permuted = (fd - swap_d) / (fv - swap_v) - (bd + swap_d) / (bv + swap_v)
        extreme += abs(permuted) >= abs(observed) - 1e-15
    return (extreme + 1) / (permutations + 1)


def holm(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    adjusted, running = [1.0] * len(values), 0.0
    for rank, index in enumerate(order):
        running = max(running, (len(values) - rank) * values[index])
        adjusted[index] = min(1.0, running)
    return adjusted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--permutations", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=20260720)
    args = parser.parse_args()
    results = args.repo / "final push" / "results"
    rows = []
    for offset, (scale, names) in enumerate(MODELS.items()):
        base, base_keys = clusters(results / names[0])
        ft, ft_keys = clusters(results / names[1])
        if base_keys != ft_keys:
            raise RuntimeError(f"Base and fine-tuned questions differ at {scale}")
        bd, bv = map(sum, zip(*base))
        fd, fv = map(sum, zip(*ft))
        rows.append({
            "scale": scale,
            "question_clusters": len(base),
            "outputs_per_variant": 1800,
            "base_drift_n": bd,
            "base_visible_n": bv,
            "base_drift_pct": 100 * bd / bv,
            "ft_drift_n": fd,
            "ft_visible_n": fv,
            "ft_drift_pct": 100 * fd / fv,
            "delta_pp": 100 * (fd / fv - bd / bv),
            "p_clustered": randomization_p(base, ft, args.permutations, args.seed + offset),
        })
    for row, p_adj in zip(rows, holm([r["p_clustered"] for r in rows])):
        row["p_holm"] = p_adj
    assert [(r["scale"], round(r["base_drift_pct"], 1), round(r["ft_drift_pct"], 1)) for r in rows] == [
        ("0.8B", 53.2, 0.7), ("2B", 44.0, 0.2), ("4B", 44.7, 0.7)
    ]
    out = Path(__file__).with_name("language_drift_significance.csv")
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
