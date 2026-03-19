import pandas as pd
from utils import compute_zscore, rescale_to_0_100

def build_factors(raw_df: pd.DataFrame):
    df = raw_df.copy().sort_index()

    # Compute z-scores per series
    z = pd.DataFrame(index=df.index)
    for col in df.columns:
        z[col] = compute_zscore(df[col])

    # Align direction: positive = risk-supportive
    # Example:
    # - higher CLI -> positive, keep as is
    # - higher unemployment -> negative, flip sign
    # - higher spreads -> negative, flip sign
    z_adj = z.copy()
    z_adj["unemp_rate"] = -z["unemp_rate"]
    z_adj["baa_spread"] = -z["baa_spread"]

    # Block definitions (simple averages, you can refine)
    macro_block = z_adj[["cli_oecd", "unemp_rate"]].mean(axis=1)
    policy_block = z_adj[["term_spread"]].mean(axis=1)   # add policy rate, CB BS later
    risk_block = z_adj[["baa_spread"]].mean(axis=1)

    factors = pd.DataFrame({
        "macro_block": macro_block,
        "policy_block": policy_block,
        "risk_block": risk_block
    })

    # Also keep individual z-scores for drilldown
    for col in z_adj.columns:
        factors[f"z_{col}"] = z_adj[col]

    # Optionally precompute a default 0–100 index with equal weights
    equal_z = (factors["macro_block"] +
               factors["policy_block"] +
               factors["risk_block"]) / 3.0
    factors["sentiment_0_100_equal"] = rescale_to_0_100(equal_z)

    return factors
