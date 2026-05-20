"""
Satellite selection module.

Handles grouping satellites by constellation and selecting the
best representative satellite based on observation availability.
"""

import numpy as np

def group_satellites(obs):
    """
    Groups satellites by constellation prefix.
    Returns: dict: { 'g': [g01, g02, ...], ... }
    """
    all_sv = obs.sv.values
    constellations = {}
    
    # Extract unique first letters from all satellite names
    prefixes = sorted(list(set(s[0] for s in all_sv if s)))
    
    for prefix in prefixes:
        # Gather and sort all satellites matching this prefix
        sats = sorted([s for s in all_sv if s.startswith(prefix)])
        constellations[prefix] = sats
        
    return constellations

def select_best_satellite(obs, const_config, sats):
    """
    Selects best satellite per constellation based on:
    - maximum valid pseudorange epochs
    - fallback SNR availability

    Returns structured dictionary for plotting + analysis.
    """
   import numpy as np

def select_best_satellites(constellations, CONST_CONFIG, obs):
    """
    Selects the satellite with the most valid epochs for each constellation.
    
    Returns:
        dict: The 'selected' dictionary containing the best satellite data per prefix.
    """
    selected = {}   # will hold: prefix → {sat, pr_code, snr_code, pr_data, snr_data}

    for prefix, sats in constellations.items():
        cfg = CONST_CONFIG[prefix]
        best_sat = None
        best_pr_code = None
        best_snr_code = None
        best_count = 0
        best_pr = None
        best_snr = None

        for sat in sats:
            # Try each pseudorange code
            for pr_code in cfg['pr_codes']:
                if pr_code not in obs.data_vars:
                    continue
                pr = obs[pr_code].sel(sv=sat).to_series().dropna()
                if len(pr) > best_count:
                    # Also find SNR
                    snr = None
                    snr_code_used = None
                    for snr_code in cfg['snr_codes']:
                        if snr_code in obs.data_vars:
                            s = obs[snr_code].sel(sv=sat).to_series().dropna()
                            if len(s) > 0:
                                snr = s
                                snr_code_used = snr_code
                                break
                    best_count = len(pr)
                    best_sat = sat
                    best_pr_code = pr_code
                    best_snr_code = snr_code_used
                    best_pr = pr
                    best_snr = snr
                break  # use first working code

        if best_sat:
            selected[prefix] = {
                'sat': best_sat,
                'pr_code': best_pr_code,
                'snr_code': best_snr_code,
                'pr': best_pr,
                'snr': best_snr,
                'color': cfg['color'],
                'name': cfg['name'],
            }

    return selected
