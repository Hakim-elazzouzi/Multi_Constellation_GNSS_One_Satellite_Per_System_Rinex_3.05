# src/visualization.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap

from config import (
    FIGURE_FACE,
    AX_FACE,
    GRID_COLOR,
    SPINE_COLOR,
    TICK_COLOR,
    TEXT_COLOR,
    CONST_COLORS_MAP,
    CONST_NAMES
)

# ─────────────────────────────────────────────────────────────
# Plot 1 — Multi-Constellation Pseudorange
# ─────────────────────────────────────────────────────────────

def plot_multi_constellation_pseudorange(selected):
    """
    Plots pseudorange arcs for one representative satellite
    from each GNSS constellation.

    Compares orbital geometry and satellite distance behaviour
    between GPS, GLONASS, Galileo, BeiDou, and QZSS systems.
    """

    fig, ax = plt.subplots(figsize=(16, 7), facecolor=FIGURE_FACE)
    ax.set_facecolor(AX_FACE)

    ax.set_title(
        'Multi-Constellation Pseudorange — One Satellite per System\n'
        'AUCK00NZL | Auckland, New Zealand | 2026-01-01',
        fontsize=13,
        fontweight='bold',
        color="#ffffff"
    )

    for prefix, info in selected.items():

        pr = info["pr"]

        if pr is None or len(pr) == 0:
            continue

        ax.plot(
            pr.index,
            pr.values / 1e6,
            color=info["color"],
            lw=2.0,
            alpha=0.9,
            label=f"{info['name']} {info['sat']} [{info['pr_code']}]"
        )

        if len(pr) > 10:
            idx_min = pr.idxmin()

            ax.scatter(
                idx_min,
                pr[idx_min] / 1e6,
                color=info["color"],
                s=50,
                zorder=5
            )

    ax.set_ylabel(
        'Pseudorange [Mm = million metres]',
        fontsize=11,
        color=TICK_COLOR
    )

    ax.set_xlabel(
        'UTC Time (HH:MM)',
        fontsize=11,
        color=TICK_COLOR
    )

    ax.tick_params(colors=TICK_COLOR)

    ax.grid(True, color=GRID_COLOR, linewidth=0.5)

    for spine in ax.spines.values():
        spine.set_edgecolor(SPINE_COLOR)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

    plt.xticks(rotation=30, color=TICK_COLOR)

    legend = ax.legend(
        fontsize=10,
        loc='upper right',
        framealpha=0.3,
        facecolor="#1a1a2e",
        edgecolor="#444444"
    )

    for text in legend.get_texts():
        text.set_color("white")

    plt.tight_layout()

    plt.savefig(
        'plot1_multi_constellation_pseudorange.png',
        dpi=150,
        bbox_inches='tight',
        facecolor=fig.get_facecolor()
    )

    plt.show()


# ─────────────────────────────────────────────────────────────
# Plot 2 — Multi-Constellation SNR Heatmap
# ─────────────────────────────────────────────────────────────

def plot_multi_constellation_heatmap(obs, selected):
    """
    Creates a multi-constellation SNR heatmap.

    Each row represents one satellite from a different GNSS
    constellation, allowing comparison of signal quality
    and satellite visibility over time.
    """

    time_index = pd.to_datetime(obs.time.values)

    n_epochs = len(time_index)

    ordered = ['G', 'R', 'E', 'C', 'J']

    rows_data = []

    row_labels = []

    row_colors = []

    for prefix in ordered:

        if prefix not in selected:
            continue

        info = selected[prefix]

        sat = info["sat"]

        snr_code = info["snr_code"]

        if snr_code is None:

            snr_arr = np.full(n_epochs, np.nan)

        else:

            snr_full = obs[snr_code].sel(sv=sat).to_series()

            snr_arr = snr_full.reindex(time_index).values

        rows_data.append(snr_arr)

        row_labels.append(f"{info['name']}\n{sat}")

        row_colors.append(info["color"])

    n_rows = len(rows_data)

    snr_matrix = np.array(rows_data)

    snr_display = np.where(np.isnan(snr_matrix), 5, snr_matrix)

    gnss_cmap = LinearSegmentedColormap.from_list(
        "gnss_snr",
        [
            "#0d1117",
            "#1a0533",
            "#2c3e8c",
            "#0099cc",
            "#00e676",
            "#ffeb3b",
            "#ff6f00",
        ],
        N=256
    )

    fig, ax = plt.subplots(figsize=(16, 5), facecolor=FIGURE_FACE)

    ax.set_facecolor(FIGURE_FACE)

    ax.imshow(
        snr_display,
        aspect='auto',
        cmap=gnss_cmap,
        vmin=15,
        vmax=55,
        extent=[
            mdates.date2num(time_index[0]),
            mdates.date2num(time_index[-1]),
            -0.5,
            n_rows - 0.5
        ],
        origin='upper'
    )

    ax.xaxis_date()

    sm = plt.cm.ScalarMappable(
        cmap=gnss_cmap,
        norm=plt.Normalize(vmin=15, vmax=55)
    )

    sm.set_array([])

    cbar = plt.colorbar(sm, ax=ax, pad=0.01)

    cbar.set_label(
        'SNR [dB-Hz]',
        color=TEXT_COLOR,
        fontsize=11
    )

    cbar.ax.yaxis.set_tick_params(color=TICK_COLOR)

    plt.setp(
        cbar.ax.get_yticklabels(),
        color=TICK_COLOR
    )

    ax.set_yticks(range(n_rows))

    ax.set_yticklabels(
        row_labels,
        fontsize=10,
        fontweight='bold'
    )

    for tick_label, color in zip(ax.get_yticklabels(), row_colors):
        tick_label.set_color(color)

    ax.set_title(
        'Multi-Constellation SNR Heatmap — One Satellite per System\n'
        'AUCK00NZL | Auckland, New Zealand | 2026-01-01\n'
        'Green/Yellow = strong signal | Blue/Purple = weak | Black = not visible',
        fontsize=12,
        fontweight='bold',
        color="#ffffff"
    )

    ax.set_xlabel(
        'UTC Time (HH:MM)',
        fontsize=11,
        color=TEXT_COLOR
    )

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

    plt.xticks(rotation=30, color=TICK_COLOR)

    for y in np.arange(0.5, n_rows, 1):

        ax.axhline(y, color=SPINE_COLOR, lw=0.8)

    for spine in ax.spines.values():

        spine.set_edgecolor(SPINE_COLOR)

    plt.tight_layout()

    plt.savefig(
        'plot2_multi_constellation_snr_heatmap.png',
        dpi=150,
        bbox_inches='tight',
        facecolor=fig.get_facecolor()
    )

    plt.show()


# ─────────────────────────────────────────────────────────────
# Plot 3 — Satellite Availability Timeline
# ─────────────────────────────────────────────────────────────

def plot_constellation_availability(avail, total_per_epoch):
    """
    Visualises satellite availability for each GNSS constellation.

    Displays stacked constellation counts and total tracked
    satellites over time to demonstrate the benefit of
    multi-GNSS positioning.
    """

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(16, 8),
        sharex=True,
        facecolor=FIGURE_FACE
    )

    fig.suptitle(
        'Multi-Constellation Satellite Availability — AUCK00NZL | 2026-01-01\n'
        'How many satellites from each system are tracked per epoch',
        fontsize=13,
        fontweight='bold',
        color="#ffffff"
    )

    for ax in axes:

        ax.set_facecolor(AX_FACE)

        ax.tick_params(colors=TICK_COLOR)

        ax.grid(True, color=GRID_COLOR, linewidth=0.5)

        for spine in ax.spines.values():

            spine.set_edgecolor(SPINE_COLOR)

    t = avail['G'].index

    bottom = np.zeros(len(t))

    for prefix in ['G', 'R', 'E', 'C', 'J']:

        vals = avail[prefix].values.astype(float)

        axes[0].bar(
            t,
            vals,
            bottom=bottom,
            color=CONST_COLORS_MAP[prefix],
            alpha=0.85,
            width=pd.Timedelta('30s'),
            label=CONST_NAMES[prefix],
            edgecolor='none'
        )

        bottom += vals

    axes[0].axhline(
        4,
        color="#F44336",
        ls='--',
        lw=1.2,
        alpha=0.7,
        label='Min for standalone GPS positioning (4 sats)'
    )

    axes[0].set_ylabel(
        'Satellites Tracked',
        color=TICK_COLOR,
        fontsize=11
    )

    axes[0].set_title(
        'Satellites per epoch — stacked by constellation',
        fontsize=10,
        color="#ffffff"
    )

    legend = axes[0].legend(
        ncol=6,
        fontsize=9,
        loc='upper right',
        framealpha=0.3,
        facecolor="#1a1a2e",
        edgecolor="#444444"
    )

    for text in legend.get_texts():

        text.set_color("white")

    axes[1].plot(
        t,
        total_per_epoch.values,
        color="#ffffff",
        lw=1.5,
        label='Total all constellations'
    )

    axes[1].fill_between(
        t,
        total_per_epoch.values,
        color="#ffffff",
        alpha=0.08
    )

    axes[1].axhline(
        4,
        color="#F44336",
        ls='--',
        lw=1.2,
        alpha=0.7,
        label='Min GPS-only (4)'
    )

    axes[1].axhline(
        total_per_epoch.mean(),
        color="#FFEB3B",
        ls='--',
        lw=1.2,
        label=f'Daily mean ({total_per_epoch.mean():.0f} sats)'
    )

    axes[1].set_ylabel(
        'Total Satellites',
        color=TICK_COLOR,
        fontsize=11
    )

    axes[1].set_xlabel(
        'UTC Time (HH:MM)',
        color=TICK_COLOR,
        fontsize=11
    )

    axes[1].set_title(
        'Total multi-GNSS satellite count — why multi-constellation matters',
        fontsize=10,
        color="#ffffff"
    )

    legend2 = axes[1].legend(
        fontsize=9,
        framealpha=0.3,
        facecolor="#1a1a2e",
        edgecolor="#444444"
    )

    for text in legend2.get_texts():

        text.set_color("white")

    axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    axes[1].xaxis.set_major_locator(mdates.HourLocator(interval=2))

    plt.xticks(rotation=30, color=TICK_COLOR)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    plt.savefig(
        'plot3_constellation_availability.png',
        dpi=150,
        bbox_inches='tight',
        facecolor=fig.get_facecolor()
    )

    plt.show()
