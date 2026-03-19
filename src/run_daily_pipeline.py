import os
import pandas as pd
from fetch_data import fetch_macro_data
from build_factors import build_factors

# Get absolute path to repo root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data", "processed")

def main():
    print("Fetching macro data...")
    raw = fetch_macro_data(start="2000-01-01")
    print(f"Fetched {len(raw)} rows")
    
    print("Building factors...")
    factors = build_factors(raw)
    print(f"Built factors: {len(factors)} rows")
    
    # Ensure output directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Writing to {DATA_DIR}")
    
    # Save full history
    factors.to_csv(os.path.join(DATA_DIR, "daily_factors.csv"))
    
    # Save latest row as JSON
    latest = factors.iloc[-1].to_dict()
    pd.Series(latest).to_json(os.path.join(DATA_DIR, "latest_factors.json"))
    
    print("Pipeline complete!")
    print(f"Latest sentiment (equal weights): {latest.get('sentiment_0_100_equal', 'N/A'):.1f}")

if __name__ == "__main__":
    main()
