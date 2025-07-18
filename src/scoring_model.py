import numpy as np
import pandas as pd

def score_wallet(features: pd.Series) -> int:
    score = 600
    # +100 if repay covers >80% of borrowed
    if features['repay_ratio'] > 0.8:
        score += 100
    # -150 if wallet was ever liquidated
    if features['n_liquidations'] > 0:
        score -= 150
    # +50 for 3+ distinct actions
    if features['n_actions'] >= 3:
        score += 50
    # Penalize if borrowed > deposited
    if features['borrow_to_deposit'] > 1:
        score -= 100
    # Clamp to 0-1000
    score = int(np.clip(score, 0, 1000))
    return score

def score_all_wallets(features_df: pd.DataFrame) -> pd.DataFrame:
    if features_df.empty:
        return pd.DataFrame(columns=['wallet', 'score'])
    scores = features_df.apply(score_wallet, axis=1)
    return pd.DataFrame({'wallet': features_df.index, 'score': scores}) 