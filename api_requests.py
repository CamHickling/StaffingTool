import requests
import time
import zipfile
import io
import pandas as pd

# Pull in the API token, survey ID, and data center from a JSON file
with open('qualtrics_access.json', 'r') as json_file:
    data = json.load(json_file)
    api_token = data['API Token']
    survey_id = data['Survey ID']
    data_center = data['User Datacenter ID']

# Set the headers
headers = {
    "Content-Type": "application/json",
    "X-API-TOKEN": api_token
}

# Step 1: Start the Export Job
export_url = f"https://{data_center}/API/v3/surveys/{survey_id}/export-responses"
payload = {
    "format": "json"
}

response = requests.post(export_url, json=payload, headers=headers)
response_json = response.json()
if response.status_code != 200:
    print(f"Error: {response_json}")
    exit()

progress_id = response_json['result']['progressId']

# Step 2: Check Export Job Progress
progress_url = f"https://{data_center}/API/v3/surveys/{survey_id}/export-responses/{progress_id}"

while True:
    response = requests.get(progress_url, headers=headers)
    response_json = response.json()
    
    if response.status_code != 200:
        print(f"Error: {response_json}")
        exit()
    
    status = response_json['result']['status']
    if status == 'complete':
        file_id = response_json['result']['fileId']
        break
    elif status == 'failed':
        print(f"Export job failed: {response_json}")
        exit()
    
    time.sleep(1)  # Wait for 1 second before checking again

# Step 3: Download the Data File
download_url = f"https://{data_center}/API/v3/surveys/{survey_id}/export-responses/{file_id}/file"
response = requests.get(download_url, headers=headers)

if response.status_code != 200:
    print(f"Error: {response.json()}")
    exit()

# Unzip the file and read the JSON data
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    for filename in z.namelist():
        with z.open(filename) as f:
            data = pd.read_json(f)
            print(data.head())  # Display the first few rows of the dataframe

# Now the data in a pandas dataframe and can process it as needed