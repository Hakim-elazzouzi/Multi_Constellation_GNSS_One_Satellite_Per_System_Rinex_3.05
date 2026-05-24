import georinex as gr
import numpy as np
import pandas as pd

from satellite_selection import select_best_constellations
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

from config import CONST_CONFIG


# Main pipeline

def main():

    # Load RINEX
    obs_path = "/AUCK00NZL_R_20260010000_01D_30S_MO.rnx"

    print("FILE HEADER")
    print("=" * 60)

    header = gr.rinexheader(obs_path)
    for k, v in header.items():
        print(f"{k:<25}: {v}")

    print("\nLoading observation data...")
    obs = gr.load(obs_path, interval=30)
    print("Data loaded successfully\n")

    # Satellite selection
    selected, avail, total_per_epoch = select_best_constellations(obs)

    # Reporting (ALL prints centralized here)
    print_constellation_selection_table(selected)

    print_availability_stats(total_per_epoch, avail)

    print_constellation_summary(
        obs,
        selected,
        total_per_epoch,
        CONST_CONFIG
    )

    # Visualization
    plot_multi_constellation_pseudorange(selected)

    plot_multi_constellation_heatmap(obs, selected)

    plot_constellation_availability(avail, total_per_epoch)


# Entry point

if __name__ == "__main__":
    main()
