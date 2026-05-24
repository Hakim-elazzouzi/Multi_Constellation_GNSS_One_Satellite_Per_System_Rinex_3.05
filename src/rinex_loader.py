# Install georinex if not already installed
# Uncomment the line below if you are running this for the first time:
# !pip install --upgrade georinex
import georinex as gr

def load_rinex(obs_path, interval=30):
    """
    Loads RINEX observation file and extracts metadata and measurements.

    Reads the RINEX header for station and receiver information, then loads
    observation data at the specified sampling interval.
    Returns both parsed data and header information for GNSS processing.
    """
    print("Reading RINEX header...")  
    header = gr.rinexheader(obs_path)     # Read the file header first (fast — no data loaded yet)

    print("FILE HEADER")
    print("=" * 60)
    for key, value in header.items():
        print(f"{key:<25}: {value}")

    print("Loading observation data...")
    obs = gr.load(obs_path, interval=30, use='G')  # Load GPS only (much faster)

    print("Data Loaded successfully")
    return obs, header
