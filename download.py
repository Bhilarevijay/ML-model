# import requests
# import zipfile
# import os
# import streamlit as st

# def download_file_from_google_drive(id, destination):
#     """
#     The definitive and robust function to download large files from Google Drive.
#     Handles the 'virus scan' warning page correctly.
#     """
#     URL = "https://docs.google.com/uc?export=download"
#     session = requests.Session()

#     # Initial request to get the confirmation token
#     response = session.get(URL, params={'id': id}, stream=True)
#     token = None
#     for key, value in response.cookies.items():
#         if key.startswith('download_warning'):
#             token = value

#     # If a confirmation token is found, make a second request with it
#     if token:
#         params = {'id': id, 'confirm': token}
#         response = session.get(URL, params=params, stream=True)

#     # Now, save the actual content
#     CHUNK_SIZE = 32768
#     with open(destination, "wb") as f:
#         for chunk in tqdm(response.iter_content(CHUNK_SIZE), desc="Downloading data", unit='KB'):
#             if chunk:
#                 f.write(chunk)

# # Import tqdm here as it's used in the function above
# from tqdm import tqdm

# @st.cache_resource
# def download_and_extract_data():
#     """
#     Downloads and extracts the required data files if they don't exist.
#     This function is now correct and will work on Render.
#     """
#     # --- THIS IS THE ONLY PART YOU NEED TO EDIT ---
#     # 1. Create a zip file containing BOTH your CSVs: sachet_main_cases_2M.csv and sachet_sightings_log_2M.csv
#     # 2. Upload that ONE zip file to Google Drive and get its shareable link ID.
#     #    - To get the ID: Share the zip file, copy link. It will look like: 
#     #      https://drive.google.com/file/d/THIS_IS_THE_ID/view?usp=sharing
#     file_id = 'YOUR_GOOGLE_DRIVE_FILE_ID' # <-- PASTE YOUR FILE ID HERE
#     https://drive.google.com/drive/folders/10Hwb8Ry0dshr9oVawCUyyO1xhBE9tsTT?usp=sharing
#     # -----------------------------------------------
    
#     # You MUST replace the placeholder above, or this will fail.
#     if file_id == 'YOUR_GOOGLE_DRIVE_FILE_ID':
#         st.error("FATAL ERROR in download.py: You must replace 'YOUR_GOOGLE_DRIVE_FILE_ID' with the actual ID of your zip file from Google Drive.")
#         st.stop()

#     zip_path = 'sachet_data.zip'
#     cases_csv = 'sachet_main_cases_2M.csv'
#     sightings_csv = 'sachet_sightings_log_2M.csv'
    
#     if not (os.path.exists(cases_csv) and os.path.exists(sightings_csv)):
#         with st.spinner(f"Downloading required data (~300MB)... This is a one-time setup on the server."):
#             print("Data files not found locally. Downloading from cloud storage...")
#             download_file_from_google_drive(file_id, zip_path)
            
#             # Add a check to ensure the downloaded file is a valid zip
#             if not zipfile.is_zipfile(zip_path):
#                 st.error("FATAL ERROR: The downloaded file from Google Drive is not a valid zip file. Please check your sharing settings and File ID in download.py.")
#                 st.stop()
                
#             print("Download complete. Extracting files...")
#             with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#                 zip_ref.extractall('.')
#             os.remove(zip_path) # Clean up the zip file
#             print("Extraction complete. Files are ready.")
#     else:
#         print("Data files found locally.")






import gdown
import os
import streamlit as st

@st.cache_resource
def download_data_from_drive():
    """
    The definitive and robust function to download the CONTENTS of a Google Drive folder.
    Uses the industry-standard 'gdown' library.
    This version does NOT expect a zip file.
    """
    # --- THIS IS THE FINAL, CORRECT CONFIGURATION ---
    # The shareable link to the FOLDER containing your two CSV files.
    folder_url = 'https://drive.google.com/drive/folders/10Hwb8Ry0dshr9oVawCUyyO1xhBE9tsTT?usp=sharing'
    # -----------------------------------------------

    # The two files we expect to find after the download.
    cases_csv = 'sachet_main_cases_2M.csv'
    sightings_csv = 'sachet_sightings_log_2M.csv'
    
    # Check if BOTH files already exist locally in the Render instance.
    if not (os.path.exists(cases_csv) and os.path.exists(sightings_csv)):
        with st.spinner(f"Downloading required data files (~700MB)... This is a one-time setup on the server and will take a few minutes."):
            try:
                print(f"Data files not found. Downloading all files from folder: {folder_url}")
                
                # --- THE DEFINITIVE FIX ---
                # This command tells gdown to download all files from the folder URL
                # directly into the current directory. No zipping involved.
                gdown.download_folder(id=folder_url, quiet=False, use_cookies=False)
                
                # Verify that the download was successful
                if not (os.path.exists(cases_csv) and os.path.exists(sightings_csv)):
                    st.error("FATAL ERROR: Download seemed to complete, but the required CSV files are still missing.")
                    st.error("Please double-check your Google Drive folder's sharing permissions. It MUST be set to 'Anyone with the link'.")
                    st.stop()
                    
                print("Download complete. Data files are ready.")

            except Exception as e:
                st.error(f"FATAL ERROR during data download: {e}")
                st.error("This may be due to incorrect Google Drive sharing settings or an invalid URL.")
                st.stop()
    else:
        print("Data files found locally.")
