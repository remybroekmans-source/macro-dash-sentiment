import os
import pandas as pd
import numpy as np

def compute_zscore(series, window=756):  # ~3 years of daily data if daily
    # rolling z-score
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    z = (series - rolling_mean) / rolling_std
    return z

def rescale_to_0_100(z, clip=2.5):
    # map z-score to 0–100 linearly between -clip and +clip
    z_clipped = z.clip(-clip, clip)
    return 50 + (z_clipped / clip) * 50  # -clip -> 0, 0 -> 50, +clip -> 100
