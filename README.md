# Project 3 — Multi-Constellation GNSS: One Satellite per System

> **GPS · GLONASS · Galileo · BeiDou · QZSS | Pseudorange & SNR Comparison | 24-Hour | Auckland, NZ**

---

## Overview

While Projects 1 and 2 focused exclusively on GPS, this project opens up the full **multi-GNSS picture**.

Modern receivers track five satellite constellations simultaneously. This project picks the **best-tracked satellite from each system** and compares them side by side — showing how different orbital altitudes, frequencies, and signal designs affect the observables.

| System | Prefix | Country | Orbital Altitude |
|--------|--------|---------|-----------------|
| GPS | `G` | USA 🇺🇸 | ~20,200 km (MEO) |
| GLONASS | `R` | Russia 🇷🇺 | ~19,100 km (MEO) |
| Galileo | `E` | Europe 🇪🇺 | ~23,222 km (MEO) |
| BeiDou | `C` | China 🇨🇳 | ~21,500 km MEO / 36,000 km GEO |
| QZSS | `J` | Japan 🇯🇵 | ~36,000 km (quasi-GEO) |

---

## Output Plots

### Plot 1 — Multi-Constellation Pseudorange Arcs

Each coloured line is one satellite from a different system:
- Higher orbital altitude → larger pseudorange (Galileo > GPS > GLONASS)
- QZSS/BeiDou GEO → nearly flat arc (satellite barely moves)
- Dots mark the closest approach (satellite at peak elevation)

### Plot 2 — Multi-Constellation SNR Heatmap

One row per constellation, colour = signal strength in dB-Hz:
```
Black/Dark   → satellite below horizon
Blue/Purple  → weak signal (low elevation)
Green        → good tracking (SNR > 35 dB-Hz)
Yellow/Orange → excellent signal
```
Each row label is colour-coded to match its constellation.

### Plot 3 — Satellite Availability Timeline

Stacked bar chart showing how many satellites per system are tracked at each epoch,
plus a total count line — demonstrating the power of multi-GNSS receivers.

---

## File Structure

```
project3-multi-constellation/
├── Outputs/
│   ├── plot1_pseudorange.png
│   ├── plot2_snr_heatmap.png
│   └── plot3_availability.png
├── src/
│   ├── config.py            
│   ├── rinex_loader.py      
│   ├── satellite_selection.py 
│   ├── gnss_observables.py       
│   ├── reporting.py         
│   ├── visualization.py     
│   ├── analysis.py
│   └── main.py              
├── requirements.txt                                                       ← Python dependencies
├── LICENSE                                                                ← MIT License
└── README.md                                                              ← This file
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your RINEX file path

Update **Step 2** of the notebook:

```python
obs_path = "/path/to/your/file.rnx"
```

### 3. Run all cells

```bash
jupyter notebook project3_multi_constellation.ipynb
```

The notebook **automatically selects the best satellite per constellation** — no manual configuration needed. It also automatically detects which observable codes are available in your file.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `georinex` | Parse RINEX 3 observation files |
| `xarray` | N-dimensional labelled arrays |
| `pandas` | Time series and DataFrames |
| `numpy` | Numerical computations |
| `matplotlib` | Publication-quality plots |

---

## Observables Used

| Constellation | Pseudorange | SNR |
|--------------|-------------|-----|
| GPS (G) | `C1C` | `S1C` |
| GLONASS (R) | `C1C` / `C1P` | `S1C` / `S1P` |
| Galileo (E) | `C1X` / `C5X` | `S1X` / `S5X` |
| BeiDou (C) | `C1X` / `C2I` | `S1X` / `S2I` |
| QZSS (J) | `C1C` / `C1X` | `S1C` / `S1X` |

The notebook auto-detects the best available code for each satellite.

---

## Technical Note — SNR Heatmap Fix

This project uses `imshow` (not `pcolormesh`) for all heatmaps.  
`pcolormesh` with `shading='auto'` silently drops data on matrices with few rows,  
producing blank plots. `imshow` with `extent=` and `ax.xaxis_date()` renders  
correctly for any matrix size including single-row cases.

---

## Author

**Hakim El Azzouzi**  
MSc Global Navigation Satellite Systems  
Mohammed First University, Oujda, Morocco  
📧 elazzouzihakim10@gmail.com  
🔗 [linkedin.com/in/Hakim-El-Azzouzi](https://linkedin.com/in/Hakim-El-Azzouzi)  
📍 Luxembourg 🇱🇺

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Part of the GNSS RINEX Analysis Series

| # | Project |
|---|---------|
| 1 | Single GPS Satellite — Pseudorange & SNR Heatmap |
| 2 | All GPS Satellites — Fleet Pseudorange & SNR Heatmap |
| **3** | **Multi-Constellation GNSS — One Satellite per System** ← You are here |
| 4 | Pseudorange vs Carrier-Phase Comparison |
| 5 | Constellation Summary — Pie Chart & Histogram |
| 6 | Ionospheric Delay — Geometry-Free Combination |
| 7 | Data Quality Report |
