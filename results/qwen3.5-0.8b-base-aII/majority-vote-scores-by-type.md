# Year-wise Scoring Report

## Table 1: Majority Rule (2 out of 3)
Model: Qwen 3.5 0.8B Base

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 30/100 (30.00%) | 18/100 (18.00%) | 24/100 (24.00%) | 22/100 (22.00%) | 23.50% |
| Vector RAG | 32/100 (32.00%) | 17/100 (17.00%) | 26/100 (26.00%) | 14/100 (14.00%) | 22.25% |
| Zero Shot | 35/100 (35.00%) | 22/100 (22.00%) | 23/100 (23.00%) | 12/100 (12.00%) | 23.00% |

## Table 2: Strict Rule (3 out of 3)
Model: Qwen 3.5 0.8B Base

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 4/100 (4.00%) | 3/100 (3.00%) | 0/100 (0.00%) | 0/100 (0.00%) | 1.75% |
| Vector RAG | 2/100 (2.00%) | 1/100 (1.00%) | 0/100 (0.00%) | 2/100 (2.00%) | 1.25% |
| Zero Shot | 7/100 (7.00%) | 0/100 (0.00%) | 3/100 (3.00%) | 0/100 (0.00%) | 2.50% |

## Table 3: Paper Score = Average of 3 Run Scores
Model: Qwen 3.5 0.8B Base

Formula per paper: (Run 1 score + Run 2 score + Run 3 score) / 3

| Type | 2022 English | 2022 Bangla | 2023 English | 2023 Bangla | Average Paper Score |
|---|---:|---:|---:|---:|---:|
| BM25 RAG | 37.00% | 23.00% | 29.67% | 22.33% | 28.00% |
| Vector RAG | 34.67% | 22.00% | 30.00% | 22.67% | 27.33% |
| Zero Shot | 36.00% | 23.67% | 28.67% | 21.33% | 27.42% |
