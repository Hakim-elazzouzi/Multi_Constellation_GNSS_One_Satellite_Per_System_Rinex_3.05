"""
Satellite selection module.

Handles grouping satellites by constellation and selecting the
best representative satellite based on observation availability.
Also computes per-constellation satellite availability timeseries.
"""

import numpy as np
import pandas as pd

from config import CONST_CONFIG
from gnss_observables import count_visible_satellites


def group_satellites(obs):
    """
    Groups satellites by constellation prefix.

    Returns:
        dict: { 'G': ['G01', 'G02', ...], 'R': [...], ... }
    """
    all_sv = obs.sv.values
    constellations = {}

    prefixes = sorted(set(s[0] for s in all_sv if s))

    for prefix in prefixes:
        sats = sorted([s for s in all_sv if s.startswith(prefix)])
        constellations[prefix] = sats

    return constellations


def select_best_satellites(constellations, obs):
    """
    Selects the satellite with the most valid pseudorange epochs
    for each constellation.

    Returns:
        dict: prefix → {sat, pr_code, snr_code, pr, snr, color, name}
    """
    selected = {}

    for prefix, sats in constellations.items():

        # Only process constellations we have config for
        if prefix not in CONST_CONFIG:
            continue

        cfg = CONST_CONFIG[prefix]
        best_sat      = None
        best_pr_code  = None
        best_snr_code = None
        best_count    = 0
        best_pr       = None
        best_snr      = None

        for sat in sats:
            for pr_code in cfg['pr_codes']:
                if pr_code not in obs.data_vars:
                    continue

                pr = obs[pr_code].sel(sv=sat).to_series().dropna()

                if len(pr) > best_count:
                    # Find the best available SNR code for this satellite
                    snr          = None
                    snr_code_used = None

                    for snr_code in cfg['snr_codes']:
                        if snr_code in obs.data_vars:
                            s = obs[snr_code].sel(sv=sat).to_series().dropna()
                            if len(s) > 0:
                                snr           = s
                                snr_code_used = snr_code
                                break

                    best_count    = len(pr)
                    best_sat      = sat
                    best_pr_code  = pr_code
                    best_snr_code = snr_code_used
                    best_pr       = pr
                    best_snr      = snr

                # Move to next satellite once a working code is found
                break

        if best_sat:
            selected[prefix] = {
                'sat':      best_sat,
                'pr_code':  best_pr_code,
                'snr_code': best_snr_code,
                'pr':       best_pr,
                'snr':      best_snr,
                'color':    cfg['color'],
                'name':     cfg['name'],
            }

    return selected


def compute_availability(obs):
    """
    Counts visible satellites per epoch for every constellation.

    Returns:
        avail (dict):           prefix → pd.Series (count per epoch)
        total_per_epoch (Series): sum across all constellations
    """
    prefixes = ['G', 'R', 'E', 'C', 'J']

    avail = {p: count_visible_satellites(obs, p) for p in prefixes}

    total_per_epoch = sum(avail.values())

    return avail, total_per_epoch


def select_best_constellations(obs):
    """
    Top-level entry point called by main.py.

    Returns:
        selected        (dict)   – best satellite info per prefix
        avail           (dict)   – visible satellite count per epoch per prefix
        total_per_epoch (Series) – total satellites tracked per epoch
    """
    constellations  = group_satellites(obs)
    selected        = select_best_satellites(constellations, obs)
    avail, total_per_epoch = compute_availability(obs)

    return selected, avail, total_per_epoch
