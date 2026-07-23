# Year-wise Scoring Report

## Table 1: Majority Rule (2 out of 3)
Model: Qwen 3.5 2B Finetuned

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 50/100 (50.00%) | 31/100 (31.00%) | 37/100 (37.00%) | 27/100 (27.00%) | 36.25% |
| Vector RAG | 52/100 (52.00%) | 32/100 (32.00%) | 38/100 (38.00%) | 25/100 (25.00%) | 36.75% |
| Zero Shot | 43/100 (43.00%) | 28/100 (28.00%) | 28/100 (28.00%) | 25/100 (25.00%) | 31.00% |

## Table 2: Strict Rule (3 out of 3)
Model: Qwen 3.5 2B Finetuned

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 32/100 (32.00%) | 13/100 (13.00%) | 24/100 (24.00%) | 19/100 (19.00%) | 22.00% |
| Vector RAG | 26/100 (26.00%) | 12/100 (12.00%) | 28/100 (28.00%) | 9/100 (9.00%) | 18.75% |
| Zero Shot | 18/100 (18.00%) | 13/100 (13.00%) | 11/100 (11.00%) | 9/100 (9.00%) | 12.75% |

## Table 3: Paper Score = Average of 3 Run Scores
Model: Qwen 3.5 2B Finetuned

Formula per paper: (Run 1 score + Run 2 score + Run 3 score) / 3

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Paper Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 50.67% | 34.00% | 39.67% | 32.00% | 39.08% |
| Vector RAG | 47.67% | 31.67% | 40.67% | 29.67% | 37.42% |
| Zero Shot | 45.67% | 33.33% | 34.00% | 26.67% | 34.92% |
