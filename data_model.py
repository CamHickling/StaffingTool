import csv
import api_requests
import json
import re
import random
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# roles
# volunteers

#steps:
# 1. model volunteer and their availability
# 2. model roles and their scheduling needs
# 3. print both models to csv

class Volunteer:
    def __init__(self, firstname, lastname, availability, internal_status, tower_status):
        self.firstname = firstname
        self.lastname = lastname
        self.availability = availability
        self.internal_status = internal_status
        self.tower_status = tower_status

    def __str__(self):
        return f'{self.name}, {self.availability}'

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname
    
    def get_availability(self):
        return self.availability
    
    def get_internal_status(self):
        return self.internal_status
    
    def get_tower_status(self):
        return self.tower_status

class Role: 
    def __init__(self, name, availability):
        self.name = name
        self.availability = availability

    def __str__(self):
        return f'{self.name}, {self.schedule}'

class Availability:
    def __init__(self):
        self.times = sorted(['{:02d}:00:00'.format(i) for i in range(9, 18)] + ['{:02d}:30:00'.format(i) for i in range(9, 18)])
        self.availability = [random.choice(["Yes", "No"]) for time in self.times]

    def __str__(self):
        return f'{self.name}, {self.times}'

    def get_times(self):
        return self.times

    def get_availability(self):
        return self.availability


def update():
    with open('data.json') as f:
        data = json.load(f)
        
        volunteers = []

        for response in data["responses"]:
            values = response["values"]
            labels = response["labels"]

            firstname = values.get("QID1_TEXT", "")
            lastname = values.get("QID2_TEXT", "")
            internal = "Yes" if labels.get("QID3", "UBC Student") == "Current Intramural Staff" or labels.get("QID3", "UBC Student") == "Intramural Staff Alumni" else "No" 
            tower = labels.get("QID10", "No") 

            '''
            try:
                availq = [labels["QID17"], labels["QID18"]]
            except KeyError:
                availq= [labels["QID13"], labels["QID14"]]
            
            availq = [availq[0], availq[1]]

            a_temp = []

            for a in availq:
                print(a)

                # Regular expression pattern to match times
                pattern = r'(\d{1,2}:\d{2}[APM]{2})\s*-\s*(\d{1,2}:\d{2}[APM]{2})'

                # Search for the pattern in the string
                match = re.search(pattern, a)

                if match:
                    start_time = match.group(1)
                    end_time = match.group(2)

                start_int = int(start_time.split(":")[0])
                end_int = int(end_time.split(":")[0])

                for i in range(start_int, end_int):
                    a_temp.append(i)
            
            availq = a_temp
            '''
           
            A = Availability()
            V = Volunteer(firstname, lastname, A, internal, tower)
            volunteers.append(V)
            
        return volunteers

if __name__ == "__main__":
    print(update())