import os
import pandas as pd
from fredapi import Fred

FRED_API_KEY = os.getenv("FRED_API_KEY")

def fetch_macro_data(start="2000-01-01"):
    fred = Fred(api_key=FRED_API_KEY)

    series_ids = {
        "cli_oecd": "OECDLOLITONOSTSAM",   # OECD CLI normalized (example)[web:65]
        "unemp_rate": "UNRATE",            # US unemployment rate
        "baa_spread": "BAA10Y",            # BAA corp - 10Y Treasury (example)[web:74]
        "term_spread": "T10Y2Y",           # 10y-2y Treasury
        # add more series here...
    }

    dfs = []
    for name, sid in series_ids.items():
        s = fred.get_series(sid, observation_start=start)
        df = s.to_frame(name=name)
        dfs.append(df)

    data = pd.concat(dfs, axis=1)
    data.index.name = "date"
    return data
