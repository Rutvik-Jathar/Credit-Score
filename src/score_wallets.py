import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
from feature_engineering import extract_wallet_features
from scoring_model import score_all_wallets

def main():
    parser = argparse.ArgumentParser(description='Aave V2 DeFi Credit Scoring')
    parser.add_argument('--input', required=True, help='Path to input JSON file')
    parser.add_argument('--output', required=True, help='Path to output CSV file')
    args = parser.parse_args()

    # Load data
    try:
        df = pd.read_json(args.input)
    except Exception as e:
        print(f"Failed to load input file: {e}")
        df = pd.DataFrame()

    # Try to extract features
    features_df = extract_wallet_features(df)
    if features_df.empty:
        print("No valid wallet activity found in input file.")
        scores_df = pd.DataFrame({'wallet': [], 'score': []})
    else:
        scores_df = score_all_wallets(features_df)
        print(f"Scored {len(scores_df)} wallets.")
    # Save scores
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    scores_df.to_csv(args.output, index=False)
    # Plot distribution
    if not scores_df.empty:
        bins = list(range(0, 1100, 100))
        plt.figure(figsize=(8,5))
        plt.hist(scores_df['score'], bins=bins, edgecolor='black')
        plt.title('Aave V2 Credit Score Distribution')
        plt.xlabel('Score')
        plt.ylabel('Number of Wallets')
        plt.xticks(bins)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('outputs/score_distribution.png')
        print("Score distribution plot saved to outputs/score_distribution.png")

if __name__ == '__main__':
    main() 