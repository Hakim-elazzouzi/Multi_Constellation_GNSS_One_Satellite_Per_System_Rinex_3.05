import numpy as np


# Satellite selection report

def print_constellation_selection_table(selected):
    """
    Prints best satellite selection per constellation.
    Shows PR code, SNR code, valid epochs, and mean SNR.
    """

    print("\nSelecting best satellite per constellation:\n")

    print(f"{'System':<12} {'Satellite':<10} {'PR Code':<8} "
          f"{'SNR Code':<9} {'Valid Epochs':>12} {'Mean SNR':>12}")
    print("-" * 65)

    for prefix, info in selected.items():

        sat = info['sat']
        pr_code = info['pr_code']
        snr_code = info['snr_code']

        pr = info['pr']
        snr = info['snr']

        valid_epochs = len(pr) if pr is not None else 0
        mean_snr = snr.mean() if snr is not None and len(snr) > 0 else np.nan

        snr_str = f"{mean_snr:.1f} dB-Hz" if not np.isnan(mean_snr) else "N/A"

        print(f"  {info['name']:<10} {sat:<10} {pr_code:<8} "
              f"{str(snr_code):<9} {valid_epochs:>12} {snr_str:>12}")


# Availability summary

def print_constellation_summary(obs, selected, total_per_epoch, const_names):
    """
    Prints final numerical comparison per constellation.

    Includes:
    - pseudorange range
    - mean SNR
    - visibility percentage
    """

    print("\nMULTI-CONSTELLATION SUMMARY")
    print("=" * 80)

    print(f"{'System':<10} {'Satellite':<10} {'PR [Mm] min–max':<22} "
          f"{'SNR mean':>12} {'Visible %':>10}")
    print("-" * 80)

    total_epochs = len(obs.time)

    for prefix in ['G', 'R', 'E', 'C', 'J']:

        if prefix not in selected:
            print(f"  {const_names[prefix]:<8}  — not in file")
            continue

        info = selected[prefix]

        pr = info['pr']
        snr = info['snr']

        if pr is None or len(pr) == 0:
            print(f"  {info['name']:<8}  — no pseudorange data")
            continue

        pr_range = f"{pr.min()/1e6:.2f} – {pr.max()/1e6:.2f} Mm"

        snr_mean = (
            f"{snr.mean():.1f} dB-Hz"
            if snr is not None and len(snr) > 0
            else "N/A"
        )

        visible_pct = f"{len(pr) / total_epochs * 100:.1f}%"

        print(
            f"  {info['name']:<8}  {info['sat']:<10} "
            f"{pr_range:<22} {snr_mean:>12} {visible_pct:>10}"
        )


# Availability stats helper (optional reuse)

def print_availability_stats(total_per_epoch, avail):
    """
    Prints global GNSS availability metrics.
    """

    print("\nGLOBAL SATELLITE AVAILABILITY")
    print("=" * 60)

    print(f"Mean total satellites per epoch : {total_per_epoch.mean():.1f}")
    print(f"Max satellites tracked          : {total_per_epoch.max():.0f}")
    print(f"Min satellites tracked          : {total_per_epoch.min():.0f}")

    if 'G' in avail:
        print(f"GPS-only mean satellites       : {avail['G'].mean():.1f}")

    print(f"Epochs analyzed                : {len(total_per_epoch)}")
