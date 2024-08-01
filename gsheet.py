import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from gspread_formatting import *
import data_model as dm

# Helper function to convert CellFormat to dictionary
def cell_format_to_dict(cell_format):
    format_dict = {}
    if cell_format.backgroundColor:
        format_dict['backgroundColor'] = {
            'red': cell_format.backgroundColor.red,
            'green': cell_format.backgroundColor.green,
            'blue': cell_format.backgroundColor.blue,
        }
    if cell_format.textFormat:
        format_dict['textFormat'] = {
            'bold': cell_format.textFormat.bold,
            'foregroundColor': {
                'red': cell_format.textFormat.foregroundColor.red,
                'green': cell_format.textFormat.foregroundColor.green,
                'blue': cell_format.textFormat.foregroundColor.blue,
            }
        }
    return format_dict

# Step 1: Create the DataFrame
Volunteers = dm.update()
#Volunteers.sort(key=lambda x: x.get_lastname())

columns = ['First Name', 'Last Name', 'Internal?', 'Tower?'] + Volunteers[0].get_availability().get_times()

data = [[V.get_firstname(), V.get_lastname(), V.get_internal_status(), V.get_tower_status()] + V.get_availability().get_availability() for V in Volunteers]

df = pd.DataFrame(data, columns=columns)

# Step 2: Authorize and retrieve the current sheet data
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("crypto-groove-418105-2d3ac71df114.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open('sample availibility spreadsheet')
sheet = spreadsheet.get_worksheet(0)

# Retrieve current data from the sheet
current_data = sheet.get_all_values()

# Convert current data to a DataFrame for processing
current_df = pd.DataFrame(current_data[1:], columns=current_data[0])
print("Current data in the sheet:")
print(current_df)

# Step 3: Clear the sheet and update with new data
sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())

# Step 4: Apply formatting
# Define cell format for 'Yes' (green), 'No' (red), and changed (yellow)
yes_availibility_format = CellFormat(
    backgroundColor=Color(0, 1, 0),
    textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0))
)

no_availibility_format = CellFormat(
    backgroundColor=Color(1, 0, 0),
    textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0))
)

yes_info_format = CellFormat(
    backgroundColor=Color(185/255, 255/255, 205/255),
    textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0))
)

no_info_format = CellFormat(
    backgroundColor=Color(224/225, 102/255, 102/225),
    textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0))
)

changed_format = CellFormat(
    backgroundColor=Color(1, 1, 0),
    textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0))
)

# Collect batch format requests
requests = []

for row_index, row in df.iterrows():
    for col_index, cell_value in enumerate(row):
        old_value = current_df.iat[row_index, col_index] if row_index < len(current_df) and col_index < len(current_df.columns) else None
        format_dict = cell_format_to_dict(changed_format)
        
        if cell_value != old_value:
            requests.append({
                'repeatCell': {
                    'range': {
                        'sheetId': sheet.id,
                        'startRowIndex': row_index + 1,
                        'endRowIndex': row_index + 2,
                        'startColumnIndex': col_index,
                        'endColumnIndex': col_index + 1,
                    },
                    'cell': {
                        'userEnteredFormat': format_dict,
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })
        else:
            if col_index >= 4:  # Availability columns
                if cell_value == 'Yes':
                    format_dict = cell_format_to_dict(yes_availibility_format)
                elif cell_value == 'No':
                    format_dict = cell_format_to_dict(no_availibility_format)
                else:
                    continue
            elif 2 <= col_index <= 3:  # Internal? and Tower? columns
                if cell_value == 'Yes':
                    format_dict = cell_format_to_dict(yes_info_format)
                elif cell_value == 'No':
                    format_dict = cell_format_to_dict(no_info_format)
                else:
                    continue

            requests.append({
                'repeatCell': {
                    'range': {
                        'sheetId': sheet.id,
                        'startRowIndex': row_index + 1,
                        'endRowIndex': row_index + 2,
                        'startColumnIndex': col_index,
                        'endColumnIndex': col_index + 1,
                    },
                    'cell': {
                        'userEnteredFormat': format_dict,
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })

# Send batch update
batch_update_request = {
    'requests': requests
}

spreadsheet.batch_update(batch_update_request)
