from School import *


# Create queue for teacher
def create_queue(teacher: Teacher, floor, per):
    special_courses = ["re", "rk", "wn", "ds"]

    # Get "per" (period) from all classes
    for class_ in CLASSES:
        assert isinstance(class_, Class)
        schedule = class_.get_period(per)

        # Check teacher's floor
        # Normal class
        if len(schedule) == 1 and not class_.complete:
            if len(teacher.queue[per]) < 8:
                lesson = schedule[0][0]
                room = schedule[0][1]

                # Special courses like dsp
                specials = list(map(lambda course: lesson.lower().startswith(course), special_courses))
                if any(specials):

                    # If room is on the same floor as the teacher
                    if floor == room.floor and room.number not in [r.number for r in teacher.queue[per]]:
                        if (per + 1) % 2 == 0 and room.number not in [r.number for r in teacher.queue[per - 1]] or \
                                (per + 1) % 2 != 0:
                            teacher.queue[per].append(room)

                # Normal class / lesson
                else:

                    # If room is on the same floor as the teacher
                    if floor == room.floor:

                        # Every 2 periods
                        if (per + 1) % 2 == 0 and room.number not in [r.number for r in teacher.queue[per - 1]] or \
                                (per + 1) % 2 != 0:
                            teacher.queue[per].append(room)
                            class_.complete = True

        # Courses
        else:

            # If class is not done yet / not been distributed
            if not class_.complete:

                # For each ongoing lesson from class
                for les in schedule:

                    # If teacher has less than 8 rooms in queue
                    if len(teacher.queue[per]) < 8:
                        lesson = les[0]
                        room = les[1]

                        # If room is on the same floor as teacher
                        if floor == room.floor and room.number not in [r.number for r in teacher.queue[per]]:

                            # If double lesson
                            if (per + 1) % 2 == 0 and room.number not in [r.number for r in teacher.queue[per - 1]] or \
                                    (per + 1) % 2 != 0:
                                if not class_.complete:
                                    teacher.queue[per].append(room)

                                    # Detect class cancellation
                                    if len(schedule) % 2 == 0:
                                        if lesson not in special_courses and -1 in [l_[1].number for l_ in schedule]:
                                            class_.complete = True


def improved_queue():
    # Create queue for all teachers
    list(map(lambda i_: list(map(lambda t: create_queue(t, t.floor, i_), TEACHERS)), range(START_PERIOD, 10)))

    # if less than 8 classes --> Change floor temporarily to 0th or 3rd
    for i in range(START_PERIOD, 10):
        for teacher in TEACHERS:
            period = teacher.get_period(i)
            if len(period) < 8:
                create_queue(teacher, teacher.sub_floor, i)

    # Print classes that the teachers could not complete
    print("\nIncomplete Classes")
    for class_ in CLASSES:
        if not class_.complete:
            print(class_.name)
    print()


def save_to_text(file_name: str):
    text = f"Amount of tests for each student: {check_tests()[1]}\n\n"

    # For each teacher
    for teacher in TEACHERS:
        queue = teacher.queue

        # Write teacher's name
        text += teacher.name + "\n"

        for i in range(len(queue)):
            period = queue[i]

            text += str(i + 1) + ": "

            # If queue for period is not empty
            if period:

                # Add queue to text
                text += ", ".join([f"R{room.number}" for room in period if period]) + "\n"

            # Free time if empty
            else:
                text += "Free time\n"

        # Add newline to text
        text += "\n"

    # Write text to file
    with open(file_name, "w+") as f:
        f.write(text)
