---
language:
- bn
- en
license: other
task_categories:
- question-answering
tags:
- legal
- legal-nlp
- bangladesh
- bangladesh-law
- bangladesh-bar-council
- bangladesh-bar-exam
- bar-exam
- bar-exam-dataset
- multiple-choice-question-answering
- legal-question-answering
- evaluation
- benchmark
- bilingual
- bangla
- bengali
- english
- low-resource-languages
pretty_name: "Bangladesh Bar Council Exam QA Dataset: 2022-2023 Bangla-English"
size_categories:
- n<1K
configs:
- config_name: bar_council
  data_files:
  - split: test_2022_bn
    path: "evaluation/bar_exam_2022_bangla.json"
  - split: test_2022_en
    path: "evaluation/bar_exam_2022_english.json"
  - split: test_2023_bn
    path: "evaluation/bar_exam_2023_bangla.json"
  - split: test_2023_en
    path: "evaluation/bar_exam_2023_english.json"
  default: true
---

# Bangladesh Bar Council Exam QA Dataset: 2022-2023 Bangla-English

The **Bangladesh Bar Council Exam QA Dataset** is a 400-question bilingual
Bangla-English legal question-answering benchmark compiled from the 2022 and
2023 Bangladesh Bar Council examination materials. It is intended for legal
NLP evaluation, multiple-choice question answering, retrieval experiments, and
Bangladesh law language-model research.

This repository contains the examination benchmark only. The larger
fine-tuning dataset is published separately:

**[Bangladesh Legal QA Dataset](https://huggingface.co/datasets/momahadi/bangladesh-legal-qa-dataset)**

## Contents

| Split | File | Questions |
| --- | --- | ---: |
| 2022 Bangla | `evaluation/bar_exam_2022_bangla.json` | 100 |
| 2022 English | `evaluation/bar_exam_2022_english.json` | 100 |
| 2023 Bangla | `evaluation/bar_exam_2023_bangla.json` | 100 |
| 2023 English | `evaluation/bar_exam_2023_english.json` | 100 |
| **Total** |  | **400** |

The English files contain machine-translated versions used in the associated
research. Each record includes:

- `question_no`
- `question_text`
- `options`
- `correct_answer`
- `correct_answer_text`

## Loading

```python
from datasets import load_dataset

repo = "momahadi/bangladesh-bar-council-exam-dataset"

bar_2022_bn = load_dataset(repo, "bar_council", split="test_2022_bn")
bar_2022_en = load_dataset(repo, "bar_council", split="test_2022_en")
bar_2023_bn = load_dataset(repo, "bar_council", split="test_2023_bn")
bar_2023_en = load_dataset(repo, "bar_council", split="test_2023_en")
```

## Intended uses

- Bangladesh Bar Council examination QA evaluation;
- bilingual Bangla-English legal NLP benchmarking;
- multiple-choice legal question answering;
- retrieval and context-use evaluation;
- reproducible comparison with the associated research paper.

## Important limitations

- The release team compiled and structured the benchmark but did not author the
  underlying examination questions.
- The English files contain machine-translated material.
- Answer keys and translations may contain errors and should be independently
  checked before high-stakes use.
- Multiple-choice exam performance is a narrow measure of legal capability.
- This is a research benchmark, not study advice or legal advice.

## Source rights

This repository uses the Hugging Face `other` license tag. The release team
does not claim copyright in the underlying Bangladesh Bar Council examination
questions and does not grant rights it does not hold. See
[`LICENSE.md`](LICENSE.md).

Separating this benchmark from the CC BY 4.0 fine-tuning dataset prevents the
exam material from making the main dataset's license ambiguous.

## Contributors and research supervision

The ordered release list is:

1. Moniruzzaman Mahadi - dataset compiler and corresponding maintainer
2. Abrar Mohammed Tanzim Alam - dataset contributor
3. Sayma Siddika Monalisa - dataset contributor
4. Mir Mohammad Asif Abdullah - dataset contributor
5. Mahina Rahman Deya - dataset contributor
6. Swakkhar Shatabda - research supervisor
7. Md Adnan Arefeen - research supervisor

Correspondence: [momahadi9664@gmail.com](mailto:momahadi9664@gmail.com)

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md) and [`CITATION.bib`](CITATION.bib).

## Citation

This citation is for the compiled and structured benchmark release. It does not
represent the release team as authors of the underlying examination questions.

```bibtex
@dataset{mahadi2026bangladeshbarexamqa,
  title     = {Bangladesh Bar Council Exam QA Dataset: 2022--2023 Bangla-English Benchmark},
  author    = {{Moniruzzaman Mahadi} and
               {Abrar Mohammed Tanzim Alam} and
               {Sayma Siddika Monalisa} and
               {Mir Mohammad Asif Abdullah} and
               {Mahina Rahman Deya} and
               {Swakkhar Shatabda} and
               {Md Adnan Arefeen}},
  year      = {2026},
  version   = {1.0.0},
  publisher = {Hugging Face},
  note      = {Compiled and structured benchmark release; underlying examination questions are not authored by the release team},
  url       = {https://huggingface.co/datasets/momahadi/bangladesh-bar-council-exam-dataset}
}
```
