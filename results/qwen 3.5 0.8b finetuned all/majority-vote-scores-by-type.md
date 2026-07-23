# Year-wise Scoring Report

## Table 1: Majority Rule (2 out of 3)
Model: Qwen 3.5 0.8B Finetuned

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 45/100 (45.00%) | 24/100 (24.00%) | 39/100 (39.00%) | 33/100 (33.00%) | 35.25% |
| Vector RAG | 53/100 (53.00%) | 25/100 (25.00%) | 39/100 (39.00%) | 23/100 (23.00%) | 35.00% |
| Zero Shot | 40/100 (40.00%) | 18/100 (18.00%) | 27/100 (27.00%) | 27/100 (27.00%) | 28.00% |

## Table 2: Strict Rule (3 out of 3)
Model: Qwen 3.5 0.8B Finetuned

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 25/100 (25.00%) | 10/100 (10.00%) | 25/100 (25.00%) | 19/100 (19.00%) | 19.75% |
| Vector RAG | 34/100 (34.00%) | 8/100 (8.00%) | 21/100 (21.00%) | 7/100 (7.00%) | 17.50% |
| Zero Shot | 22/100 (22.00%) | 2/100 (2.00%) | 10/100 (10.00%) | 8/100 (8.00%) | 10.50% |

## Table 3: Paper Score = Average of 3 Run Scores
Model: Qwen 3.5 0.8B Finetuned

Formula per paper: (Run 1 score + Run 2 score + Run 3 score) / 3

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Paper Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 43.67% | 25.67% | 41.33% | 33.33% | 36.00% |
| Vector RAG | 52.67% | 29.00% | 38.67% | 28.00% | 37.08% |
| Zero Shot | 42.33% | 23.00% | 30.33% | 30.00% | 31.42% |
