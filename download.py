import gdown
import os
import streamlit as st

@st.cache_resource
def download_data_from_drive():
    """
    The definitive, simple, and robust function to download individual files
    from Google Drive using the 'gdown' library.
    """
    # --- THIS IS THE FINAL, DEFINITIVE CONFIGURATION ---
    # PASTE THE TWO FILE IDs YOU COPIED FROM GOOGLE DRIVE HERE
    
    file_ids = {
        "sachet_main_cases_2M.csv": "1zPxIeFgt2mYfIJIahQ_02oLqJ40gKEef",
        "sachet_sightings_log_2M.csv": "1ZMq5Ds90yZdXc2Q0wUVNugLWY9F-8QJ8"
    }
    
    # --- END OF CONFIGURATION ---

    # Check if BOTH files already exist locally.
    files_to_download = [name for name, _ in file_ids.items() if not os.path.exists(name)]
    
    if files_to_download:
        with st.spinner(f"Downloading required data files... This is a one-time setup."):
            for filename, file_id in file_ids.items():
                if filename in files_to_download:
                    try:
                        # Construct the direct download URL that gdown expects
                        url = f'https://drive.google.com/uc?id={file_id}'
                        
                        print(f"File '{filename}' not found. Downloading...")
                        gdown.download(url, filename, quiet=False)
                        
                        if not os.path.exists(filename):
                            raise Exception(f"Download failed for {filename}")
                            
                        print(f"'{filename}' downloaded successfully.")

                    except Exception as e:
                        st.error(f"FATAL ERROR during data download for {filename}: {e}")
                        st.error("Please double-check the File ID and that sharing is set to 'Anyone with the link'.")
                        st.stop()
    else:
        print("Data files found locally.")





# import gdown
# import os
# import streamlit as st

# @st.cache_resource
# def download_data_from_drive():
#     """
#     The definitive and robust function to download the CONTENTS of a Google Drive folder.
#     Uses the industry-standard 'gdown' library.
#     This version does NOT expect a zip file.
#     """
#     # --- THIS IS THE FINAL, CORRECT CONFIGURATION ---
#     # The shareable link to the FOLDER containing your two CSV files.
#     folder_url = 'https://drive.google.com/drive/folders/10Hwb8Ry0dshr9oVawCUyyO1xhBE9tsTT?usp=sharing'
#     # -----------------------------------------------

#     # The two files we expect to find after the download.
#     cases_csv = 'sachet_main_cases_2M.csv'
#     sightings_csv = 'sachet_sightings_log_2M.csv'
    
#     # Check if BOTH files already exist locally in the Render instance.
#     if not (os.path.exists(cases_csv) and os.path.exists(sightings_csv)):
#         with st.spinner(f"Downloading required data files (~700MB)... This is a one-time setup on the server and will take a few minutes."):
#             try:
#                 print(f"Data files not found. Downloading all files from folder: {folder_url}")
                
#                 # --- THE DEFINITIVE FIX ---
#                 # This command tells gdown to download all files from the folder URL
#                 # directly into the current directory. No zipping involved.
#                 gdown.download_folder(id=folder_url, quiet=False, use_cookies=False)
                
#                 # Verify that the download was successful
#                 if not (os.path.exists(cases_csv) and os.path.exists(sightings_csv)):
#                     st.error("FATAL ERROR: Download seemed to complete, but the required CSV files are still missing.")
#                     st.error("Please double-check your Google Drive folder's sharing permissions. It MUST be set to 'Anyone with the link'.")
#                     st.stop()
                    
#                 print("Download complete. Data files are ready.")

#             except Exception as e:
#                 st.error(f"FATAL ERROR during data download: {e}")
#                 st.error("This may be due to incorrect Google Drive sharing settings or an invalid URL.")
#                 st.stop()
#     else:
#         print("Data files found locally.")
