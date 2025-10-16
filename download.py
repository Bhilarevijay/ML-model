import requests
import zipfile
import os
import streamlit as st

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

@st.cache_resource
def download_and_extract_data():
    """Downloads and extracts the required data files if they don't exist."""
    # --- THIS IS THE ONLY PART YOU NEED TO EDIT ---
    # 1. Create a zip file containing BOTH your CSVs: sachet_main_cases_2M.csv and sachet_sightings_log_2M.csv
    # 2. Upload that ONE zip file to Google Drive and get its shareable link ID.
    #    - To get the ID: Share the zip file, copy the link, it will be like '.../d/FILE_ID/view?usp=sharing'
    file_id = '10Hwb8Ry0dshr9oVawCUyyO1xhBE9tsTT' # <-- PASTE YOUR FILE ID HERE
    # -----------------------------------------------

    zip_path = 'sachet_data.zip'
    cases_csv = 'sachet_main_cases_2M.csv'
    sightings_csv = 'sachet_sightings_log_2M.csv'
    
    # If the files don't already exist, download and extract them.
    if not (os.path.exists(cases_csv) and os.path.exists(sightings_csv)):
        with st.spinner(f"Downloading required data files (~200-300MB)... This is a one-time setup."):
            print("Data files not found. Downloading from cloud storage...")
            download_file_from_google_drive(file_id, zip_path)
            print("Download complete. Extracting files...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('.')
            os.remove(zip_path) # Clean up the zip file
            print("Extraction complete. Files are ready.")
    else:
        print("Data files found locally.")
