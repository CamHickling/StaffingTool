import csv

# roles
# volunteers

#steps:
# 1. model volunteer and their availability
# 2. model roles and their scheduling needs
# 3. print both models to csv

class Volunteer:
    def __init__(self, name, availability: Availability):
        self.name = name
        self.availability = availability

class Role: 
    def __init__(self, name, schedule: Availability):
        self.name = name
        self.schedule = schedule

class Availability:
    def __init__(self, day, time):
        self.day = day
        self.time = time

def to_csv():
    pass