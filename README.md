# Aave V2 DeFi Credit Scoring

This project analyzes DeFi wallet activity on Aave V2 and generates a credit score (0–1000) for each wallet based on historical transaction behavior.

## Project Structure
- `data/user-wallet-transactions.json` — Raw transaction data
- `src/feature_engineering.py` — Extracts wallet-level features
- `src/scoring_model.py` — Rule-based credit scoring logic
- `src/score_wallets.py` — CLI script to generate scores and plot distribution
- `outputs/scores.csv` — Wallet-to-score output
- `outputs/score_distribution.png` — Histogram of scores
- `README.md` — Project overview and instructions
- `analysis.md` — Score distribution and behavioral insights
- `requirements.txt` — Python dependencies
- `.gitignore` — Ignore outputs and Python cache

## Feature Engineering
Features are extracted per wallet from raw Aave V2 transactions:
- Number of distinct actions
- Number of liquidations
- Total deposited, borrowed, and repaid
- Repay-to-borrow ratio
- Borrow-to-deposit ratio

## Scoring Approach
A rule-based model assigns a score (0–1000):
- Start at 600
- +100 if repay covers >80% of borrowed
- -150 if ever liquidated
- +50 for 3+ distinct actions
- -100 if borrowed > deposited
- Clamp to 0–1000
- If no activity, score is 0

## Architecture & Data Flow
1. **Raw Data**: `user-wallet-transactions.json`
2. **Feature Extraction**: `feature_engineering.py`
3. **Scoring**: `scoring_model.py`
4. **CLI Script**: `score_wallets.py` — runs the full pipeline and outputs results

## Usage
Install dependencies:
```bash
pip install -r requirements.txt
```
Run scoring pipeline:
```bash
python src/score_wallets.py --input data/user-wallet-transactions.json --output outputs/scores.csv
```
Outputs:
- `outputs/scores.csv`: Wallet scores
- `outputs/score_distribution.png`: Score histogram 