OBS_PATH = "/AUCK00NZL_R_20260010000_01D_30S_MO.rnx" 

# GNSS CONFIGURATION FILE

CONSTELLATIONS = ['G', 'R', 'E', 'C', 'J']

# Constellation configuration
# Each system uses different observable codes depending on the receiver
CONST_CONFIG = {
    'G': {'name': 'GPS',     'color': '#2196F3', 'pr_codes': ['C1C', 'C2W'], 'snr_codes': ['S1C', 'S2W']},
    'R': {'name': 'GLONASS', 'color': '#F44336', 'pr_codes': ['C1C', 'C1P'], 'snr_codes': ['S1C', 'S1P']},
    'E': {'name': 'Galileo', 'color': '#4CAF50', 'pr_codes': ['C1X', 'C5X'], 'snr_codes': ['S1X', 'S5X']},
    'C': {'name': 'BeiDou',  'color': '#FF9800', 'pr_codes': ['C2I', 'C1X'], 'snr_codes': ['S1X', 'S2I']},
    'J': {'name': 'QZSS',     'color': '#9C27B0', 'pr_codes': ['C1C', 'C1X'], 'snr_codes': ['S1C', 'S1X']},
}

PSEUDORANGE_PRIORITY = {
    'G': ['C1C', 'C1W', 'C2W'],
    'R': ['C1C', 'C1P'],
    'E': ['C1X', 'C5X', 'C7X'],
    'C': ['C2I', 'C1X', 'C6I'],
    'J': ['C1C', 'C1X']
}

SNR_PRIORITY = {
    'G': ['S1C', 'S1W'],
    'R': ['S1C', 'S1P'],
    'E': ['S1X', 'S5X'],
    'C': ['S1X', 'S2I'],
    'J': ['S1C', 'S1X']
}

PLOT_STYLE = {
    "figure_dpi": 120,
    "dark_bg": "#0d1117",
    "axes_bg": "#111827",
    "grid_color": "#222222",
    "text_color": "#aaaaaa",
    "spine_color": "#333333",
}

SNR_THRESHOLDS = {
    "poor": 25,
    "good": 35,
    "excellent": 40
}

CONST_CONFIG = {
    'G': {'name': 'GPS',     'color': '#2196F3', 'pr_codes': ['C1C', 'C2W'], 'snr_codes': ['S1C', 'S2W']},
    'R': {'name': 'GLONASS', 'color': '#F44336', 'pr_codes': ['C1C', 'C1P'], 'snr_codes': ['S1C', 'S1P']},
    'E': {'name': 'Galileo', 'color': '#4CAF50', 'pr_codes': ['C1X', 'C5X'], 'snr_codes': ['S1X', 'S5X']},
    'C': {'name': 'BeiDou',  'color': '#FF9800', 'pr_codes': ['C1X', 'C2I'], 'snr_codes': ['S1X', 'S2I']},
    'J': {'name': 'QZSS',   'color': '#9C27B0', 'pr_codes': ['C1C', 'C1X'], 'snr_codes': ['S1C', 'S1X']},
}
