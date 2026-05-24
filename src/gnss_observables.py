"""
GNSS observable module.

Handles observable selection and visibility calculations
for multi-constellation GNSS analysis.
"""

import pandas as pd


PR_CODE = {
    'G': 'C1C',
    'R': 'C1C',
    'E': 'C1X',
    'C': 'C1X',
    'J': 'C1C'
}


def count_visible_satellites(obs, prefix):
    """
    Counts visible satellites per epoch for a constellation.

    Uses non-NaN pseudorange values as visibility indicator.

    Returns:
        pandas.Series: satellite count over time
    """

    sats = [s for s in obs.sv.values if s.startswith(prefix)]

    if not sats:
        return pd.Series(0, index=pd.to_datetime(obs.time.values))

    code = PR_CODE.get(prefix, 'C1C')

    # Try fallback codes if primary is unavailable
    for c in [code, 'C1X', 'C1C', 'C2I']:

        if c in obs.data_vars:

            return (
                obs[c]
                .sel(sv=sats)
                .count(dim='sv')
                .to_series()
            )

    return pd.Series(0, index=pd.to_datetime(obs.time.values))
