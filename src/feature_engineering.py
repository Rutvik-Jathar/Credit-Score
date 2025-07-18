import pandas as pd
import numpy as np
from typing import Dict, Any

def extract_wallet_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts wallet-level features from raw transaction data.
    Returns a DataFrame indexed by wallet with feature columns.
    """
    if df.empty:
        return pd.DataFrame()

    # Normalize columns
    df = df.copy()
    # Use 'userWallet' as wallet address
    if 'wallet' not in df.columns and 'userWallet' in df.columns:
        df['wallet'] = df['userWallet']
    # Extract action from 'action' or 'actionData.type'
    if 'action' not in df.columns and 'actionData' in df.columns:
        df['action'] = df['actionData'].apply(lambda x: x.get('type', '').lower() if isinstance(x, dict) else '')
    else:
        df['action'] = df['action'].str.lower()
    # Extract amount from 'actionData.amount' (convert to float)
    if 'amount' not in df.columns and 'actionData' in df.columns:
        def parse_amount(x):
            if isinstance(x, dict) and 'amount' in x:
                try:
                    return float(x['amount']) / 1e6  # USDC/USDT/DAI decimals
                except Exception:
                    return 0.0
            return 0.0
        df['amount'] = df['actionData'].apply(parse_amount)
    # Extract token from 'actionData.assetSymbol'
    if 'token' not in df.columns and 'actionData' in df.columns:
        df['token'] = df['actionData'].apply(lambda x: x.get('assetSymbol', '') if isinstance(x, dict) else '')

    features = []
    grouped = df.groupby('wallet')
    for wallet, group in grouped:
        actions = group['action'].unique()
        n_actions = len(actions)
        n_liquidations = (group['action'] == 'liquidationcall').sum()
        total_deposit = group.loc[group['action'] == 'deposit', 'amount'].sum()
        total_borrow = group.loc[group['action'] == 'borrow', 'amount'].sum()
        total_repay = group.loc[group['action'] == 'repay', 'amount'].sum()
        repay_ratio = total_repay / total_borrow if total_borrow > 0 else 0.0
        borrow_to_deposit = total_borrow / total_deposit if total_deposit > 0 else np.nan
        features.append({
            'wallet': wallet,
            'n_actions': n_actions,
            'n_liquidations': n_liquidations,
            'total_deposit': total_deposit,
            'total_borrow': total_borrow,
            'total_repay': total_repay,
            'repay_ratio': repay_ratio,
            'borrow_to_deposit': borrow_to_deposit,
        })
    return pd.DataFrame(features).set_index('wallet') 