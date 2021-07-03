from schedule import get_all_schedules


class School:
    def __init__(self, date, testkits):
        self.rooms = []
        self.date = date

        # Testkits per student
        self.std_testkits = testkits

        self.all_schedules = ([], [], [], [], [], [], [], [], [], [])
        self.all_classes = []
        self.all_rooms = []
        self.all_teachers = []
        self.setup()

    def add_teacher(self, name, floor, sub_floor):
        return self.all_teachers.append(Teacher(name, floor, sub_floor))

    def setup(self):
        schedules = get_all_schedules(self.date)
        for cls in range(len(schedules)):
            class_ = Class(schedules[cls][0])
            self.all_classes.append(class_)
            for table in range(len(schedules[cls][1])):
                schedule = schedules[cls][1]
                for per in range(len(schedule)):
                    for loc in range(len(schedule[per])):
                        subject = str(schedule[per][loc][0]).lower()
                        room_num = str(schedule[per][loc][1]).upper()
                        if room_num not in [r.room_number for r in self.all_rooms]:
                            room = Room(room_num)
                            if room.convert_to_room():
                                self.all_rooms.append(room)

                        room = self.get_room(room_num)
                        group = [class_, room, subject]
                        if room and group not in self.all_schedules[per]:
                            self.all_schedules[per].append(group)

    def get_room(self, number):
        for room in self.all_rooms:
            if room.room_number == str(number).upper():
                return room


class Teacher:
    def __init__(self, name: str, floor: int, sub_floor: int):
        self.name = name
        self.floor = floor
        self.sub_floor = sub_floor

        # Queue consists of 10 lists (periods)
        self.queue = ([], [], [], [], [], [], [], [], [], [])

    def get_period(self, per):
        return self.queue[per]


class Class:
    def __init__(self, class_number):
        self.class_number = class_number
        self.complete = False

    def __repr__(self):
        return self.class_number


class Room:
    def __init__(self, room_number: str):
        self.room_number = str(room_number).upper()
        self.number = self.room_number
        self.floor = -1

    def convert_to_room(self) -> bool:
        # If in the school
        if self.room_number.startswith("R"):
            # Get the floor
            self.floor = int(self.room_number[1])

            # Turn room_number into an integer
            self.number = int(self.room_number[1:4])
            return True

        elif self.room_number == "AULA":
            self.floor = 1
            self.number = 115
            return True

        elif self.room_number == "-":
            self.floor = -1
            self.number = -1

        return False

    # Show as string (orientation purposes)
    def __repr__(self):
        return f"R{self.number}"
