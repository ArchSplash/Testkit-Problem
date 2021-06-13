"""
FLOW CHART:
https://lucid.app/lucidchart/30eacef3-fe8c-4182-b1e0-a889130f4838/edit?beaconFlowId=C1E680E67C0D6F2F&page=0_0#
Only works for user (me)
"""

from Schedule import get_all_schedules
from SortTestkits import TESTKIT_AMOUNT
from time import strftime


# Teacher Class
class Teacher:
    def __init__(self, name: str, floor: int, sub_floor: int):
        self.name = name
        self.floor = floor
        self.sub_floor = sub_floor

    # Queue consists of 10 lists (periods)
        self.queue = [[], [], [], [], [], [], [], [], [], []]

    def get_period(self, per):
        return self.queue[per]


# Class "Class"
class Class:
    def __init__(self, name, schedule):
        self.name = name
        self.complete = False
        self.schedule = schedule

        for per in range(len(self.schedule)):
            for tm in range(len(self.schedule[per])):
                schedule[per][tm][1] = Room(self.schedule[per][tm][1])

    # Show as string (orientation purposes)
    def __repr__(self):
        return self.name

    def get_period(self, per):
        return self.schedule[per]


# Room Class
class Room:
    def __init__(self, room_number: str):
        self.room_number = str(room_number).upper()
        self.number = self.room_number
        self.floor = -1

        # If in the school
        if self.room_number.startswith("R"):
            # Get the floor
            self.floor = int(self.room_number[1])

            # Turn room_number into an integer
            self.number = int(self.room_number[1:4])

        elif self.room_number == "AULA":
            self.floor = 1
            self.number = 115

        elif self.room_number == "-":
            self.floor = -1
            self.number = -1

    # Show as string (orientation purposes)
    def __repr__(self):
        return f"R{self.number}"


# Convert from strings to their respective objects: Class
def converted_classes(date: str):
    if check_tests()[0]:
        classes = get_all_schedules(date)
        for i in range(len(classes)):
            classes[i] = Class(classes[i][0], classes[i][1])

        return classes


# Check if enough tests are there
def check_tests():
    sufficient = TOTAL_STUDENTS <= TESTKIT_AMOUNT
    return sufficient, TESTKIT_AMOUNT // TOTAL_STUDENTS if sufficient else 0


# Get classes and students
TOTAL_STUDENTS = int(input("Total Students: "))  # SENIOR_STUDENTS + JUNIOR_STUDENTS
date_ = input(f"Date (e.g. {strftime('%Y-%m-%d')}): ")
START_PERIOD = int(input("When should it start: ")) - 1

CLASSES = converted_classes(date_)

# Declare and create Teacher objects
FLOORS = [0, 1, 2, 3]
TEACHERS = [Teacher("Rabe", FLOORS[1], FLOORS[0]), Teacher("Wetzel", FLOORS[2], FLOORS[3])]
