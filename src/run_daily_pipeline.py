import os
from datetime import datetime
from fetch_data import fetch_macro_data
from build_factors import build_factors

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def main():
    raw = fetch_macro_data(start="2000-01-01")
    factors = build_factors(raw)

    # Save latest full history
    out_dir = os.path.join(BASE_DIR, "data", "processed")
    os.makedirs(out_dir, exist_ok=True)

    factors.to_csv(os.path.join(out_dir, "daily_factors.csv"))

    # Also save a small "latest" JSON for the app
    latest = factors.iloc[-1]
    latest.to_json(os.path.join(out_dir, "latest_factors.json"), orient="index")

if __name__ == "__main__":
    main()
