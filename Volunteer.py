from dataclasses import dataclass
import typing
from enum import Enum, auto
from dataclasses import dataclass

class Year(Enum):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()
    FOURTH = auto()
    FIFTH = auto()

class Role(Enum):
    STUDENT = auto()
    STAFF = auto()
    ALUMNI = auto()
    OTHER = auto()

class YesNo(Enum):
    YES = auto()
    NO = auto()

@dataclass
class Volunteer:
    response_id: str
    first_name: str
    last_name: str
    year: Year
    role: Role
    phone_number: str
    email: str
    first_aid_certification: YesNo
    first_aid_level: str  # If yes, what level
    dietary_restrictions: YesNo
    dietary_description: str  # If yes, please describe
    volunteer_hours: int
    additional_info: str
    interested_in_tower: YesNo
    previous_tower_experience: YesNo
    own_wetsuit: YesNo
    availability: [] # list of availibility on event days (of which days are lists by the half hour)

# Generates for free:
# __init__()
# __repr__()
# __eq__()

# Example of creating an instance of the Volunteer dataclass with enums
volunteer_example = Volunteer(
    response_id="12345",
    first_name="John",
    last_name="Doe",
    year=Year.SENIOR,
    role=Role.STUDENT,
    phone_number="555-1234",
    email="john.doe@example.com",
    first_aid_certification=YesNo.YES,
    first_aid_level="Level 2",
    dietary_restrictions=YesNo.YES,
    dietary_description="Vegetarian",
    volunteer_hours=10,
    additional_info="None",
    interested_in_tower=YesNo.YES,
    previous_tower_experience=YesNo.NO,
    own_wetsuit=YesNo.YES,
    availability="Weekends"
)

print(volunteer_example)