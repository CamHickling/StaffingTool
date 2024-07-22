import requests
import json
import time
import pandas as pd
from io import BytesIO
import zipfile
import io


def get_auth():
    with open('qualtrics_access.json', 'r') as json_file:
        data = json.load(json_file)
    return data['API Token'], data['Survey ID'], data['User Datacenter ID']

def make_request(api_token, survey_id, data_center):
    export_url = f"https://{data_center}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": api_token
    }
    
    payload = {
        "format": "json"
    }
    
    try:
        response = requests.post(export_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        progress_id = response_data['result']['progressId']
        
        # Check the progress
        progress_url = f"https://{data_center}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses/{progress_id}"
        while True:
            response = requests.get(progress_url, headers=headers)
            response.raise_for_status()
            progress_data = response.json()
            status = progress_data['result']['status']
            if status == 'complete':
                file_id = progress_data['result']['fileId']
                break
            elif status == 'failed':
                print("Export failed")
                return None
            else:
                print("Export in progress...")
                time.sleep(5)
        
        # Download the file
        download_url = f"https://{data_center}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses/{file_id}/file"
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def retrieve_data():
    api_token, survey_id, data_center = get_auth()
    data = make_request(api_token, survey_id, data_center)
    if data:
        # Decompress the ZIP file
        with zipfile.ZipFile(io.BytesIO(data), 'r') as zip_ref:
            # Assuming there is only one file in the ZIP
            file_name = zip_ref.namelist()[0]
            with zip_ref.open(file_name) as json_file:
                json_data = json_file.read()
                data_dict = json.loads(json_data)
                
                '''
                # Convert JSON data to DataFrame
                if isinstance(data_dict, list):
                    df = pd.json_normalize(data_dict)
                else:
                    df = pd.json_normalize([data_dict])
                
                # Print the DataFrame
                print(df.head())
                '''

                # Path to the JSON file
                json_file_path = 'data.json'

                # Save the dictionary to the JSON file
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(data_dict, f, indent=4)

                print("Data export successful!")

                return data_dict



if __name__ == "__main__":
    retrieve_data()
