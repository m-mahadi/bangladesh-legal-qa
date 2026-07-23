# Year-wise Scoring Report

## Table 1: Majority Rule (2 out of 3)
Model: Qwen 3.5 4B Finetuned

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 59/100 (59.00%) | 37/100 (37.00%) | 52/100 (52.00%) | 43/100 (43.00%) | 47.75% |
| Vector RAG | 63/100 (63.00%) | 30/100 (30.00%) | 53/100 (53.00%) | 38/100 (38.00%) | 46.00% |
| Zero Shot | 45/100 (45.00%) | 35/100 (35.00%) | 42/100 (42.00%) | 36/100 (36.00%) | 39.50% |

## Table 2: Strict Rule (3 out of 3)
Model: Qwen 3.5 4B Finetuned

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 36/100 (36.00%) | 21/100 (21.00%) | 37/100 (37.00%) | 24/100 (24.00%) | 29.50% |
| Vector RAG | 45/100 (45.00%) | 10/100 (10.00%) | 34/100 (34.00%) | 19/100 (19.00%) | 27.00% |
| Zero Shot | 23/100 (23.00%) | 16/100 (16.00%) | 19/100 (19.00%) | 14/100 (14.00%) | 18.00% |

## Table 3: Paper Score = Average of 3 Run Scores
Model: Qwen 3.5 4B Finetuned

Formula per paper: (Run 1 score + Run 2 score + Run 3 score) / 3

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Paper Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 57.67% | 41.00% | 55.00% | 43.00% | 49.17% |
| Vector RAG | 62.67% | 33.00% | 54.33% | 38.67% | 47.17% |
| Zero Shot | 47.00% | 37.67% | 41.33% | 34.67% | 40.17% |
