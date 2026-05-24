"""
GNSS analysis module.

Computes numerical statistics and constellation-level
tracking metrics for GNSS observations.
"""

import numpy as np


def compute_constellation_summary(obs, selected):
    """
    Computes numerical summary for each constellation.

    Calculates:
    - pseudorange min/max
    - mean SNR
    - visibility percentage

    Returns:
        dict: constellation statistics
    """

    summary = {}

    total_epochs = len(obs.time)

    for prefix, info in selected.items():

        pr = info['pr']
        snr = info['snr']

        if pr is None or len(pr) == 0:
            continue

        summary[prefix] = {
            'system': info['name'],
            'satellite': info['sat'],
            'pr_min': pr.min() / 1e6,
            'pr_max': pr.max() / 1e6,
            'snr_mean': snr.mean() if snr is not None else np.nan,
            'visible_pct': len(pr) / total_epochs * 100
        }

    return summary


def compute_total_availability(avail):
    """
    Computes total satellite availability across all constellations.

    Returns:
        pandas.Series: total satellites tracked per epoch
    """

    return sum(avail.values())
