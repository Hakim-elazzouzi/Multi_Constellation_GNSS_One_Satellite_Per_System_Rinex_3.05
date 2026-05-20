"""
Satellite selection module.

Handles grouping satellites by constellation and selecting the
best representative satellite based on observation availability.
"""

import numpy as np

CONSTELLATIONS = ['G', 'R', 'E', 'C', 'J']


def group_satellites(obs):
    """
    Groups satellites by constellation prefix.

    Returns:
        dict: { 'G': [G01, G02, ...], ... }
    """
    all_sv = obs.sv.values
    return {
        p: sorted([s for s in all_sv if s.startswith(p)])
        for p in CONSTELLATIONS
        if any(s.startswith(p) for s in all_sv)
    }


def select_best_satellite(obs, const_config, sats):
    """
    Selects best satellite per constellation based on:
    - maximum valid pseudorange epochs
    - fallback SNR availability

    Returns structured dictionary for plotting + analysis.
    """
    selected = {}

    for prefix, sat_list in sats.items():
        cfg = const_config[prefix]

        best = {
            "sat": None,
            "count": 0,
            "pr_code": None,
            "snr_code": None,
            "pr": None,
            "snr": None,
        }

        for sat in sat_list:
            for pr_code in cfg["pr_codes"]:
                if pr_code not in obs.data_vars:
                    continue

                pr = obs[pr_code].sel(sv=sat).to_series().dropna()

                if len(pr) > best["count"]:
                    snr_series = None
                    snr_code_used = None

                    for snr_code in cfg["snr_codes"]:
                        if snr_code in obs.data_vars:
                            s = obs[snr_code].sel(sv=sat).to_series().dropna()
                            if len(s) > 0:
                                snr_series = s
                                snr_code_used = snr_code
                                break

                    best.update({
                        "sat": sat,
                        "count": len(pr),
                        "pr_code": pr_code,
                        "snr_code": snr_code_used,
                        "pr": pr,
                        "snr": snr_series,
                    })

                break

        if best["sat"]:
            selected[prefix] = best

    return selected
