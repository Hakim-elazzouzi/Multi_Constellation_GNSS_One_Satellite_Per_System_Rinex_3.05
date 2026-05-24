import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')   # save-to-file backend; swap to 'TkAgg' for interactive window

import georinex as gr
import xarray as xr
import numpy as np
import pandas as pd

from config import CONST_CONFIG, OBS_PATH

from satellite_selection import select_best_constellations

from visualization import (
    plot_multi_constellation_pseudorange,
    plot_multi_constellation_heatmap,
    plot_constellation_availability,
)

from reporting import (
    print_constellation_selection_table,
    print_constellation_summary,
    print_availability_stats,
)


# ─────────────────────────────────────────────
# Main pipeline
# ─────────────────────────────────────────────

def load_obs(obs_path):
    """
    Load RINEX by constellation to avoid memory/timeout issues
    with large mixed-constellation files, then merge.
    """
    print("FILE HEADER")
    print("=" * 60)
    header = gr.rinexheader(obs_path)
    for k, v in header.items():
        print(f"{k:<25}: {v}")

    print("\nLoading observation data (one constellation at a time)...")
    parts = []
    for use in ['G', 'R', 'E', 'C', 'J']:
        print(f"  Loading {use}...", flush=True)
        parts.append(gr.load(obs_path, interval=30, use=use))

    obs = xr.merge(parts)
    print(f"Data loaded: {len(obs.sv)} SVs | {len(obs.time)} epochs\n")
    return obs


def main():

    # ── 1. Load RINEX ────────────────────────
    obs = load_obs(OBS_PATH)

    # ── 2. Satellite selection + availability ─
    selected, avail, total_per_epoch = select_best_constellations(obs)

    # ── 3. Reporting ──────────────────────────
    print_constellation_selection_table(selected)
    print_availability_stats(total_per_epoch, avail)
    print_constellation_summary(obs, selected, total_per_epoch, CONST_CONFIG)

    # ── 4. Visualization ──────────────────────
    plot_multi_constellation_pseudorange(selected)
    plot_multi_constellation_heatmap(obs, selected)
    plot_constellation_availability(avail, total_per_epoch)

    print("\nAll plots saved successfully.")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()
