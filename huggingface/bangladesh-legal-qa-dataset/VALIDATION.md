# Release validation

Validated on 2026-07-23 before packaging.

## Counts

- Audit-friendly SFT source: 2,165 records.
- Direct-answer JSONL: 2,165 records.
- IRAC-answer JSONL: 2,165 records.
- Languages: 1,211 Bangla and 954 English.
- Question types: 795 single-hop, 712 advanced-selection, and 658
  bar-exam-style researcher-created records.
- Dataset IDs: 2,165 unique values, with no missing IDs.
- Quality flags: all 2,165 final records have `quality_flag: false`.

## Parsing

All JSON and JSONL files in the release folder parsed successfully.

## Secret scan

A strict email-address scan found no email addresses inside the JSON or JSONL
data files. No credentials were added to the release folder.

## SHA-256

```text
finetune_dataset_2165.json
f82e6e681d25e2ccfb20d2d1e69274e311fe50c51dd72126bd03b216dee35109

finetune_answer_only_2165.jsonl
9bea8a6650c72c4d1238bbecdfae6330fe09f57b1c214e193242a519c3ca3d1b

finetune_irac_answer_2165.jsonl
0ffcc2bdee0bc090363bf9bd6b1f074916da58390b94c542927416f6242f9cc2
```

## Scope boundary

This folder contains the paper-aligned 2,165-record dataset. The separate
3,519-record direct/IRAC/IRARC family was not copied into this release.

The four raw 2022-2023 Bangladesh Bar Council evaluation files are excluded by
design and published in a separate benchmark repository:

https://huggingface.co/datasets/momahadi/bangladesh-bar-council-exam-dataset
