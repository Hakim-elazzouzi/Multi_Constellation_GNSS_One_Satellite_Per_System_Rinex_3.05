import georinex as gr
import numpy as np
import pandas as pd

from config import CONST_CONFIG

from satellite_selection import (
    group_satellites,
    select_best_satellites,
    compute_availability
)

from visualization import (
    plot_multi_constellation_pseudorange,
    plot_multi_constellation_heatmap,
    plot_constellation_availability
)

from reporting import (
    print_constellation_selection_table,
    print_constellation_summary,
    print_availability_stats
)
# Main pipeline

def main():

    # Step 1 — Load RINEX
    obs_path = "/AUCK00NZL_R_20260010000_01D_30S_MO.rnx"

    print("FILE HEADER")
    print("=" * 60)

    header = gr.rinexheader(obs_path)
    for k, v in header.items():
        print(f"{k:<25}: {v}")

    print("\nLoading observation data (this may take 1–2 minutes)...")
    obs = gr.load(obs_path, interval=30)
    print("Data loaded successfully\n")

    # Step 2 — Satellite grouping
    constellations = group_satellites(obs)

    # Step 3 — Select best satellite per system
    selected = select_best_satellites(
        constellations,
        CONST_CONFIG,
        obs
    )

    # Choose pseudorange for availability analysis (standard GPS)
    pr_code = "C1C" if "C1C" in obs.data_vars else "C1X"

    avail, total_per_epoch = compute_availability(
        obs,
        pr_code,
        constellations
    )

    # Step 4 — Reporting (ALL prints centralized)
    print_constellation_selection_table(selected)

    print_availability_stats(total_per_epoch, avail)

    print_constellation_summary(
        obs,
        selected,
        total_per_epoch,
        CONST_CONFIG
    )

    # Step 5 — Visualizations
    plot_multi_constellation_pseudorange(selected)

    plot_multi_constellation_heatmap(obs, selected)

    plot_constellation_availability(avail, total_per_epoch)


# Entry point

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
