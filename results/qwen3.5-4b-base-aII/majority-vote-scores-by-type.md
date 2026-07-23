# Year-wise Scoring Report

## Table 1: Majority Rule (2 out of 3)
Model: Qwen 3.5 4B Base

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 58/100 (58.00%) | 36/100 (36.00%) | 53/100 (53.00%) | 37/100 (37.00%) | 46.00% |
| Vector RAG | 59/100 (59.00%) | 28/100 (28.00%) | 50/100 (50.00%) | 32/100 (32.00%) | 42.25% |
| Zero Shot | 47/100 (47.00%) | 27/100 (27.00%) | 47/100 (47.00%) | 38/100 (38.00%) | 39.75% |

## Table 2: Strict Rule (3 out of 3)
Model: Qwen 3.5 4B Base

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 44/100 (44.00%) | 16/100 (16.00%) | 40/100 (40.00%) | 23/100 (23.00%) | 30.75% |
| Vector RAG | 46/100 (46.00%) | 14/100 (14.00%) | 38/100 (38.00%) | 12/100 (12.00%) | 27.50% |
| Zero Shot | 32/100 (32.00%) | 15/100 (15.00%) | 29/100 (29.00%) | 14/100 (14.00%) | 22.50% |

## Table 3: Paper Score = Average of 3 Run Scores
Model: Qwen 3.5 4B Base

Formula per paper: (Run 1 score + Run 2 score + Run 3 score) / 3

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Paper Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 58.67% | 40.33% | 56.00% | 41.67% | 49.17% |
| Vector RAG | 61.33% | 33.00% | 53.67% | 34.33% | 45.58% |
| Zero Shot | 51.67% | 35.67% | 50.00% | 39.00% | 44.08% |
