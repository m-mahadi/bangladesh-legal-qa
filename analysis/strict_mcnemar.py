from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "final push" / "results"
OUT = Path(__file__).resolve().parent
FIGURE_TEX = OUT.parent / "figures" / "src" / "fig-significance.tex"

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

MODES = {
    "None": "zero",
    "BM25": "bm25",
    "FAISS": "rag",
}

EXAMS = {
    "2022 English": "bar_exam_2022_english_fixed",
    "2022 Bangla": "bar_exam_2022_clean",
    "2023 English": "bar_exam_2023_english",
    "2023 Bangla": "bar_exam_2023_clean",
}


def mode_dir(root: Path, token: str) -> Path:
    matches = [p for p in root.iterdir() if p.is_dir() and token in p.name.lower()]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {token!r} directory under {root}, found {matches}")
    return matches[0]


def load_runs(root: Path, mode: str, exam_stem: str) -> list[list[bool]]:
    folder = mode_dir(root, MODES[mode])
    run_dirs = sorted(p for p in folder.iterdir() if p.is_dir() and p.name.lower().startswith("run"))
    if len(run_dirs) != 3:
        raise RuntimeError(f"Expected three runs under {folder}, found {run_dirs}")

    runs: list[list[dict]] = []
    for run_dir in run_dirs:
        files = list(run_dir.glob(f"*{exam_stem}*results.json"))
        if len(files) != 1:
            raise RuntimeError(f"Expected one {exam_stem} result in {run_dir}, found {files}")
        runs.append(json.loads(files[0].read_text(encoding="utf-8-sig")))

    if any(len(run) != 100 for run in runs):
        raise RuntimeError(f"Expected 100 questions in every run: {folder}, {exam_stem}")

    keys = [(item.get("question_no"), item.get("correct_answer")) for item in runs[0]]
    for run in runs[1:]:
        if [(item.get("question_no"), item.get("correct_answer")) for item in run] != keys:
            raise RuntimeError(f"Question alignment differs across runs: {folder}, {exam_stem}")

    return [[bool(item.get("is_correct")) for item in run] for run in runs]


def strict_vector(root: Path, mode: str, exam_stem: str) -> list[bool]:
    runs = load_runs(root, mode, exam_stem)
    return [all(run[i] for run in runs) for i in range(100)]


def mcnemar_exact(losses: int, wins: int) -> float:
    discordant = losses + wins
    if discordant == 0:
        return 1.0
    tail = sum(math.comb(discordant, k) for k in range(min(losses, wins) + 1)) / (2**discordant)
    return min(1.0, 2.0 * tail)


def holm_adjust(p_values: list[float]) -> list[float]:
    order = sorted(range(len(p_values)), key=p_values.__getitem__)
    adjusted = [1.0] * len(p_values)
    running = 0.0
    count = len(p_values)
    for rank, idx in enumerate(order):
        running = max(running, (count - rank) * p_values[idx])
        adjusted[idx] = min(1.0, running)
    return adjusted


def exact_cluster_signflip(differences: list[int]) -> float:
    """Exact paired randomization test with one label flip per exam question."""
    observed = abs(sum(differences))
    counts = {0: 1}
    for difference in differences:
        if difference == 0:
            continue
        magnitude = abs(difference)
        next_counts: dict[int, int] = defaultdict(int)
        for total, count in counts.items():
            next_counts[total + magnitude] += count
            next_counts[total - magnitude] += count
        counts = next_counts
    return sum(count for total, count in counts.items() if abs(total) >= observed) / sum(counts.values())


def analyze() -> list[dict]:
    rows: list[dict] = []
    for scale, roots in MODELS.items():
        for exam, exam_stem in EXAMS.items():
            for mode in MODES:
                base = strict_vector(roots["base"], mode, exam_stem)
                ft = strict_vector(roots["ft"], mode, exam_stem)
                losses = sum(b and not f for b, f in zip(base, ft))
                wins = sum(f and not b for b, f in zip(base, ft))
                rows.append(
                    {
                        "scale": scale,
                        "exam": exam,
                        "retrieval": mode,
                        "base_strict": sum(base),
                        "ft_strict": sum(ft),
                        "delta": sum(ft) - sum(base),
                        "ft_wins": wins,
                        "base_wins": losses,
                        "discordant": wins + losses,
                        "p_exact": mcnemar_exact(losses, wins),
                    }
                )

    adjusted = holm_adjust([row["p_exact"] for row in rows])
    for row, q_value in zip(rows, adjusted):
        row["p_holm"] = q_value
        row["significant_05"] = q_value < 0.05
    return rows


def analyze_scale_level() -> list[dict]:
    rows: list[dict] = []
    for scale, roots in MODELS.items():
        strict_differences: list[int] = []
        answer_differences: list[int] = []
        for year in ("2022", "2023"):
            stems = [stem for exam, stem in EXAMS.items() if exam.startswith(year)]
            base_conditions = [load_runs(roots["base"], mode, stem) for stem in stems for mode in MODES]
            ft_conditions = [load_runs(roots["ft"], mode, stem) for stem in stems for mode in MODES]
            for question in range(100):
                strict_differences.append(
                    sum(
                        all(ft[run][question] for run in range(3))
                        - all(base[run][question] for run in range(3))
                        for base, ft in zip(base_conditions, ft_conditions)
                    )
                )
                answer_differences.append(
                    sum(
                        ft[run][question] - base[run][question]
                        for base, ft in zip(base_conditions, ft_conditions)
                        for run in range(3)
                    )
                )
        rows.append(
            {
                "scale": scale,
                "question_clusters": 200,
                "strict_outcomes_per_variant": 1200,
                "strict_delta": sum(strict_differences),
                "strict_delta_pp": 100 * sum(strict_differences) / 1200,
                "strict_p": exact_cluster_signflip(strict_differences),
                "answers_per_variant": 3600,
                "answer_delta": sum(answer_differences),
                "answer_delta_pp": 100 * sum(answer_differences) / 3600,
                "answer_p": exact_cluster_signflip(answer_differences),
            }
        )

    for prefix in ("strict", "answer"):
        adjusted = holm_adjust([row[f"{prefix}_p"] for row in rows])
        for row, value in zip(rows, adjusted):
            row[f"{prefix}_p_holm"] = value
    return rows


def write_outputs(rows: list[dict], scale_rows: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "strict_mcnemar_holm.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    with (OUT / "scale_level_significance.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scale_rows[0]))
        writer.writeheader()
        writer.writerows(scale_rows)

    summary = {
        scale: {
            "significant_cells": sum(row["significant_05"] for row in rows if row["scale"] == scale),
            "positive_significant": sum(
                row["significant_05"] and row["delta"] > 0 for row in rows if row["scale"] == scale
            ),
            "negative_significant": sum(
                row["significant_05"] and row["delta"] < 0 for row in rows if row["scale"] == scale
            ),
        }
        for scale in MODELS
    }
    summary["scale_level"] = {row["scale"]: row for row in scale_rows}
    (OUT / "strict_mcnemar_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def write_figure_tex(rows: list[dict]) -> None:
    lookup = {(row["scale"], row["exam"], row["retrieval"]): row for row in rows}
    vmax = max(abs(row["delta"]) for row in rows)
    lines = [
        r"\documentclass[border=3pt]{standalone}",
        r"\usepackage{tikz}",
        r"\definecolor{teal}{HTML}{2A7F78}",
        r"\definecolor{gold}{HTML}{B07C24}",
        r"\definecolor{navy}{HTML}{18324A}",
        r"\begin{document}",
        r"\begin{tikzpicture}[x=1.55cm,y=0.82cm,font=\rmfamily]",
    ]

    for panel, scale in enumerate(MODELS):
        offset = panel * 4.25
        lines.append(rf"\node[font=\bfseries] at ({offset + 1.5},1.0) {{{scale}}};")
        for column, mode in enumerate(MODES):
            lines.append(rf"\node[font=\scriptsize] at ({offset + column + 0.5},0.35) {{{mode}}};")
        for row_index, exam in enumerate(EXAMS):
            y = -row_index - 0.5
            if panel == 0:
                lines.append(rf"\node[anchor=east,font=\scriptsize] at ({offset - 0.08},{y}) {{{exam}}};")
            for column, mode in enumerate(MODES):
                result = lookup[(scale, exam, mode)]
                intensity = 12 + round(60 * abs(result["delta"]) / vmax)
                fill = "teal" if result["delta"] >= 0 else "gold"
                star = r"\textsuperscript{*}" if result["significant_05"] else ""
                p_text = r"<.001" if result["p_holm"] < 0.001 else f"={result['p_holm']:.3f}".lstrip("0")
                x = offset + column
                lines.extend(
                    [
                        rf"\filldraw[fill={fill}!{intensity},draw=white,line width=.7pt] ({x},{y - 0.5}) rectangle ({x + 1},{y + 0.5});",
                        rf"\node[align=center,font=\scriptsize] at ({x + 0.5},{y}) {{{result['delta']:+d}{star}\\[-1pt]{{\tiny $p_{{\rm adj}}{p_text}$}}}};",
                    ]
                )

    lines.extend(
        [
            r"\fill[teal!45] (2.2,-5.45) rectangle (2.55,-5.15);",
            r"\node[anchor=west,font=\scriptsize] at (2.62,-5.30) {fine-tuned higher};",
            r"\fill[gold!45] (5.0,-5.45) rectangle (5.35,-5.15);",
            r"\node[anchor=west,font=\scriptsize] at (5.42,-5.30) {base higher};",
            r"\node[anchor=west,font=\scriptsize] at (7.35,-5.30) {darker $=$ larger $|\Delta|$; * $p_{\rm adj}<.05$};",
            r"\end{tikzpicture}",
            r"\end{document}",
        ]
    )
    FIGURE_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def self_check(rows: list[dict], scale_rows: list[dict]) -> None:
    assert len(rows) == 36
    assert len(scale_rows) == 3
    expected = {"0.8B": (169, 261), "2B": (94, 226), "4B": (-25, -28)}
    assert {row["scale"]: (row["strict_delta"], row["answer_delta"]) for row in scale_rows} == expected
    assert mcnemar_exact(0, 0) == 1.0
    assert exact_cluster_signflip([1]) == 1.0


if __name__ == "__main__":
    analysis = analyze()
    scale_analysis = analyze_scale_level()
    self_check(analysis, scale_analysis)
    write_outputs(analysis, scale_analysis)
    write_figure_tex(analysis)
    print(json.dumps(json.loads((OUT / "strict_mcnemar_summary.json").read_text()), indent=2))
