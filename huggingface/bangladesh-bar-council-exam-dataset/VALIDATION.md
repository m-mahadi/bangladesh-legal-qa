# Release validation

Validated on 2026-07-23 before publication.

## Counts

- 2022 Bangla: 100 questions.
- 2022 English: 100 questions.
- 2023 Bangla: 100 questions.
- 2023 English: 100 questions.
- Total packaged records: 400.

## Parsing and schema

All four JSON files parsed successfully. Every record contains:

- `question_no`
- `question_text`
- `options`
- `correct_answer`
- `correct_answer_text`

## Scope

This repository contains only the 2022-2023 Bangladesh Bar Council evaluation
benchmark. The 2,165-record legal QA and fine-tuning dataset is maintained
separately:

https://huggingface.co/datasets/momahadi/bangladesh-legal-qa-dataset
