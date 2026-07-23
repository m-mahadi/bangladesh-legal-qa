---
language:
- bn
- en
license: cc-by-4.0
task_categories:
- question-answering
- text-generation
tags:
- legal
- legal-nlp
- bangladesh
- bangladesh-law
- bangladesh-legal-qa-dataset
- bangladesh-legal-dataset
- bangladesh-law-dataset
- bangladesh-legal-corpus
- bilingual
- bangla
- bengali
- english
- bangla-legal-qa
- bengali-legal-nlp
- legal-question-answering
- legal-qa-dataset
- fine-tuning-dataset
- instruction-tuning
- supervised-fine-tuning
- llm-fine-tuning
- irac
- retrieval-augmented-generation
- rag
- low-resource-languages
- law
pretty_name: "Bangladesh Legal QA Dataset: Bangla-English Law and Fine-Tuning"
size_categories:
- 1K<n<10K
configs:
- config_name: audit
  data_files:
  - split: train
    path: "sft/finetune_dataset_2165.json"
  default: true
- config_name: direct_answer
  data_files:
  - split: train
    path: "sft/finetune_answer_only_2165.jsonl"
- config_name: irac
  data_files:
  - split: train
    path: "sft/finetune_irac_answer_2165.jsonl"
---

# Bangladesh Legal QA Dataset: Bangla-English Law and Fine-Tuning

The **Bangladesh Legal QA Dataset** is a bilingual Bangla-English dataset for
Bangladesh law question answering, legal NLP, LLM fine-tuning, instruction
tuning, and retrieval-augmented generation (RAG). It provides 2,165
context-grounded legal QA records, direct-answer and IRAC chat-format training
data, and structured statutory text from six Bangladesh Acts and three
schedules.

This is the **2,165-record paper-aligned release** used for the associated
small-language-model legal QA study. It does not include the separate, later
3,519-record dataset family.

Associated paper: *Do Small Models Use the Law You Give Them?
Context-Injected Fine-Tuning for Legal QA in Bangladesh*. The arXiv link will
be added after the preprint is posted.

## Separate Bangladesh Bar Council benchmark

The 400-question 2022-2023 Bangladesh Bar Council evaluation benchmark is
published separately:

**[Bangladesh Bar Council Exam QA Dataset](https://huggingface.co/datasets/momahadi/bangladesh-bar-council-exam-dataset)**

The separation keeps the open license for this research dataset clear while
allowing the exam repository to carry its own source-rights notice. Files named
`bar_exam_style_*` in this repository are researcher-created QA training
subsets, not the raw Bar Council examination files.

## What the dataset contains

| Component | Size | What it is for |
| --- | ---: | --- |
| Audit-friendly legal QA dataset | 2,165 records | Questions, answers, legal context, Act and section metadata, and provenance |
| Direct-answer chat SFT | 2,165 records | Supervised fine-tuning and instruction tuning |
| IRAC-answer chat SFT | 2,165 records | Legal reasoning experiments using Issue, Rule, Application, and Conclusion structure |
| QA source splits | 6 files | Bangla and English single-hop, advanced-selection, and bar-exam-style training subsets |
| Bangladesh law corpus | 6 Acts + 3 schedules | Retrieval and context-grounded legal QA experiments |

### QA record breakdown

| Dimension | Records |
| --- | ---: |
| Total | 2,165 |
| Bangla/Bengali | 1,211 |
| English | 954 |
| Single-hop | 795 |
| Advanced selection | 712 |
| Bar-exam style | 658 |

## Repository structure

```text
.
|-- sft/
|   |-- finetune_dataset_2165.json
|   |-- finetune_answer_only_2165.jsonl
|   `-- finetune_irac_answer_2165.jsonl
|-- qa-splits/
|-- law-corpus/
|   |-- english/
|   |-- bangla/
|   `-- schedules/
|-- CONTRIBUTORS.md
|-- CITATION.bib
|-- LICENSE.md
`-- VALIDATION.md
```

## Files

### SFT data

| File | Records | Purpose |
| --- | ---: | --- |
| `sft/finetune_dataset_2165.json` | 2,165 | Audit-friendly source records with legal context and metadata |
| `sft/finetune_answer_only_2165.jsonl` | 2,165 | Chat messages with direct answers |
| `sft/finetune_irac_answer_2165.jsonl` | 2,165 | Chat messages with IRAC-formatted answers |

### QA splits

| File | Records |
| --- | ---: |
| `qa-splits/single_hop_bangla.json` | 493 |
| `qa-splits/single_hop_english.json` | 302 |
| `qa-splits/advanced_selection_bangla.json` | 407 |
| `qa-splits/advanced_selection_english.json` | 305 |
| `qa-splits/bar_exam_style_bangla.json` | 311 |
| `qa-splits/bar_exam_style_english.json` | 347 |
| **Total** | **2,165** |

## Loading the data

```python
from datasets import load_dataset

repo = "momahadi/bangladesh-legal-qa-dataset"

audit_records = load_dataset(repo, "audit", split="train")
answer_only = load_dataset(repo, "direct_answer", split="train")
irac = load_dataset(repo, "irac", split="train")
```

Load the separate examination benchmark with:

```python
bar_repo = "momahadi/bangladesh-bar-council-exam-dataset"
bar_2022_bn = load_dataset(bar_repo, "bar_council", split="test_2022_bn")
```

## Dataset fields

The audit-friendly JSON contains fields for dataset ID, language, question
type, Act and section metadata, candidate legal sections, question, answer,
IRAC reasoning, quality metadata, and source-file provenance. Some fields are
present only for particular question types.

Each JSONL training record has one `messages` array using the standard
system/user/assistant chat structure.

## Intended uses

- Bangladesh legal NLP and bilingual Bangla-English legal QA;
- supervised fine-tuning and instruction-tuning experiments;
- IRAC-formatted legal-answer generation;
- retrieval-augmented and context-grounded legal QA;
- controlled evaluation of small language models;
- low-resource-language and cross-lingual legal AI research.

## Limitations

- This is a research dataset, not legal advice.
- Answers and legal references may contain errors and should be independently
  verified before high-stakes use.
- The records cover a limited set of statutes, schedules, years, languages,
  and question types.
- The 2,165-record release must not be merged silently with the later
  3,519-record dataset family.

## Provenance

The bundle was assembled from the paper-aligned research artifacts:

- structured legal context from six Bangladesh Acts and three schedules;
- final QA splits for single-hop, advanced-selection, and bar-exam-style
  questions;
- final direct-answer and IRAC SFT variants.

Model-result files and score tables are not included.

## Contributors and research supervision

The repository is maintained under a personal Hugging Face account, but credit
is attached to the dataset itself. The ordered release list is:

1. Moniruzzaman Mahadi - dataset author and corresponding maintainer
2. Abrar Mohammed Tanzim Alam - dataset contributor
3. Sayma Siddika Monalisa - dataset contributor
4. Mir Mohammad Asif Abdullah - dataset contributor
5. Mahina Rahman Deya - dataset contributor
6. Swakkhar Shatabda - research supervisor
7. Md Adnan Arefeen - research supervisor

Correspondence: [momahadi9664@gmail.com](mailto:momahadi9664@gmail.com)

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md) and [`CITATION.bib`](CITATION.bib).
More detailed CRediT roles can be added after confirmation by the team.

## Citation

This BibTeX entry cites the **dataset release itself**, not the unpublished
research paper. A paper citation can be added separately after publication.

```bibtex
@dataset{mahadi2026bangladeshlegalqa,
  title     = {Bangladesh Legal QA Dataset: Bangla-English Law and Fine-Tuning Data},
  author    = {{Moniruzzaman Mahadi} and
               {Abrar Mohammed Tanzim Alam} and
               {Sayma Siddika Monalisa} and
               {Mir Mohammad Asif Abdullah} and
               {Mahina Rahman Deya} and
               {Swakkhar Shatabda} and
               {Md Adnan Arefeen}},
  year      = {2026},
  version   = {1.1.0},
  publisher = {Hugging Face},
  keywords  = {Bangladesh legal QA, Bangla legal NLP, Bengali legal question answering, legal LLM fine-tuning, Bangladesh law corpus},
  url       = {https://huggingface.co/datasets/momahadi/bangladesh-legal-qa-dataset}
}
```

## License and source rights

The release team's original dataset contributions are licensed under the
**Creative Commons Attribution 4.0 International license (CC BY 4.0)**. This
includes the original questions, answers, annotations, metadata, selection,
arrangement, and researcher-produced translations to the extent the release
team holds rights in them.

Official statutory text is source material and was not authored by the release
team. The team does not claim ownership of that text or purport to relicense
rights it does not hold. See [`LICENSE.md`](LICENSE.md) for the exact scope and
attribution requirements.
