import pandas as pd
import numpy as np
from utils import compute_zscore, rescale_to_0_100

def build_factors(raw_df: pd.DataFrame):
    df = raw_df.copy().sort_index()
    
    # Compute z-scores per series (skip if all NaN)
    z_adj = pd.DataFrame(index=df.index)
    for col in df.columns:
        if df[col].notna().sum() > 100:  # only if >100 valid points
            z = compute_zscore(df[col])
            # Align direction (customize these)
            if col in ["unemp_rate", "baa_spread"]:
                z = -z  # higher = worse
            z_adj[col] = z
        else:
            print(f"Skipping {col}: insufficient data")
    
    print(f"Using {len(z_adj.columns)} series for factors")
    
    # Define blocks (only using available columns)
    macro_cols = [c for c in ["cli_oecd", "unemp_rate"] if c in z_adj.columns]
    policy_cols = [c for c in ["term_spread"] if c in z_adj.columns]
    risk_cols = [c for c in ["baa_spread"] if c in z_adj.columns]
    
    macro_block = z_adj[macro_cols].mean(axis=1) if macro_cols else pd.Series(0, index=z_adj.index)
    policy_block = z_adj[policy_cols].mean(axis=1) if policy_cols else pd.Series(0, index=z_adj.index)
    risk_block = z_adj[risk_cols].mean(axis=1) if risk_cols else pd.Series(0, index=z_adj.index)
    
    factors = pd.DataFrame({
        "macro_block": macro_block,
        "policy_block": policy_block,
        "risk_block": risk_block
    })
    
    # Add individual z-scores
    for col in z_adj.columns:
        factors[f"z_{col}"] = z_adj[col]
    
    # Drop only rows where ALL blocks are NaN
    factors = factors.dropna(subset=["macro_block", "policy_block", "risk_block"])
    
    # Equal weight sentiment
    equal_z = (factors["macro_block"] + factors["policy_block"] + factors["risk_block"]) / 3.0
    factors["sentiment_0_100_equal"] = rescale_to_0_100(equal_z)
    
    print(f"Final factors shape: {factors.shape}")

    if len(factors) > 0:
        print(f"Date range: {factors.index[0].date()} to {factors.index[-1].date()}")
    else:
        print("No valid factor rows were produced.")

    print("Preview of z_adj:")
    print(z_adj.head())

    print("Preview of factor blocks:")
    print(factors[["macro_block", "policy_block", "risk_block"]].head(10))

    print("Non-null counts by factor block before filtering:")
    print(factors[["macro_block", "policy_block", "risk_block"]].notna().sum())

    
    return factors
