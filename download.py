


import gdown
import os
import streamlit as st

@st.cache_resource # This is the key to making it download only once
def download_required_files():
    """
    The definitive, simple, and robust function to download individual files
    from Google Drive using 'gdown'. This runs only if the files are not
    already present on the server's disk.
    """
    # --- THIS IS THE ONLY PART YOU NEED TO EDIT ---
    # PASTE THE TWO FILE IDs YOU COPIED FROM GOOGLE DRIVE HERE
    files_to_download = {
        "sachet_main_cases_2M.csv": "1zPxIeFgt2mYfIJIahQ_02oLqJ40gKEef",
        "sachet_sightings_log_2M.csv": "1ZMq5Ds90yZdXc2Q0wUVNugLWY9F-8QJ8"
    }
    # --- END OF EDITING SECTION ---

    with st.spinner("Performing one-time data setup... This may take several minutes."):
        for filename, file_id in files_to_download.items():
            if not os.path.exists(filename):
                try:
                    print(f"File '{filename}' not found. Downloading from cloud...")
                    
                    # You MUST replace the placeholder above, or this will fail.
                    if 'YOUR_ID' in file_id:
                        st.error(f"FATAL ERROR: You must replace the placeholder File ID for '{filename}' in download.py.")
                        st.stop()

                    output_path = gdown.download(id=file_id, output=filename, quiet=False)

                    if not output_path or not os.path.exists(output_path):
                        raise Exception(f"gdown download failed for {filename}")

                    print(f"'{filename}' downloaded successfully.")

                except Exception as e:
                    st.error(f"FATAL ERROR during data download for '{filename}': {e}")
                    st.error("Please double-check the File ID and that sharing for this specific file is set to 'Anyone with the link'.")
                    st.stop()
    print("All required data files are present.")
