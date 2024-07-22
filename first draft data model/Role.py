from dataclasses import dataclass
import typing
from enum import Enum, auto
from dataclasses import dataclass

from Volunteer import Volunteer

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

class Role:
    def __init__(self, role_type: RoleType):
        self.role_type = role_type
        self.volunteers: List[Volunteer] = []

    def add_volunteer(self, volunteer: Volunteer):
        if volunteer.role == self.role_type:
            self.volunteers.append(volunteer)
        else:
            raise ValueError(f"Volunteer role {volunteer.role} does not match role {self.role_type}")

    def get_volunteer_details(self):
        details = []
        for volunteer in self.volunteers:
            volunteer_detail = {
                "response_id": volunteer.response_id,
                "first_name": volunteer.first_name,
                "last_name": volunteer.last_name,
                "year": volunteer.year.name,
                "phone_number": volunteer.phone_number,
                "email": volunteer.email,
                "first_aid_certification": volunteer.first_aid_certification.name,
                "first_aid_level": volunteer.first_aid_level,
                "dietary_restrictions": volunteer.dietary_restrictions.name,
                "dietary_description": volunteer.dietary_description,
                "volunteer_hours": volunteer.volunteer_hours,
                "additional_info": volunteer.additional_info,
                "interested_in_tower": volunteer.interested_in_tower.name,
                "previous_tower_experience": volunteer.previous_tower_experience.name,
                "own_wetsuit": volunteer.own_wetsuit.name,
                "availability": volunteer.availability,
            }
            details.append(volunteer_detail)
        return details