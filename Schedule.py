from dataclasses import dataclass
import typing
from enum import Enum, auto
from dataclasses import dataclass

import Role
import Volunteer

class Schedule:
    def __init__(self):
        self.roles: Dict[RoleType, Role] = {}

    def add_role(self, role: Role):
        if role.role_type in self.roles:
            raise ValueError(f"Role {role.role_type} already exists in the schedule")
        self.roles[role.role_type] = role

    def add_volunteer_to_role(self, volunteer: Volunteer):
        if volunteer.role not in self.roles:
            raise ValueError(f"Role {volunteer.role} does not exist in the schedule")
        self.roles[volunteer.role].add_volunteer(volunteer)

    def get_schedule(self):
        schedule = {}
        for role_type, role in self.roles.items():
            schedule[role_type.name] = role.get_volunteer_details()
        return schedule

# Example of creating a schedule and adding roles and volunteers
schedule = Schedule()

# Create roles
role_student = Role(RoleType.STUDENT)
role_staff = Role(RoleType.STAFF)

# Add roles to schedule
schedule.add_role(role_student)
schedule.add_role(role_staff)