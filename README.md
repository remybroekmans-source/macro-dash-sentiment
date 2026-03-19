macro-dashboard-sentiment/
├─ data/
│  ├─ raw/          # raw API pulls (optional, for debugging)
│  └─ processed/    # daily aggregated, z-scored factors, etc.
├─ src/
│  ├─ fetch_data.py         # pulls macro & market data
│  ├─ build_factors.py      # computes z-scores, sub-indices
│  ├─ run_daily_pipeline.py # orchestrator script
│  └─ utils.py              # helper functions
├─ app/
│  └─ app.py        # Streamlit or Dash app (interactive weights)
├─ .github/
│  └─ workflows/
│       └─ daily-pipeline.yml  # GitHub Actions workflow
├─ requirements.txt
├─ README.md
└─ LICENSE
