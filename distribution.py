def create_queue(school, start_period):
    special_courses = ["re", "rk", "wn", "ds"]
    schedules = school.all_schedules
    for per in range(start_period, len(schedules)):
        period = school.all_schedules[per]

        for teacher in school.all_teachers:
            for floor in [teacher.floor, teacher.sub_floor]:
                for class_, room, subject in period:
                    sec = per % 2 != 0
                    group = [class_, room]

                    if len(teacher.queue[per]) < 8:
                        if floor == room.floor and not class_.complete:
                            if sec and group in teacher.queue[per - 1]:
                                continue

                            teacher.queue[per].append(group)
                            if subject not in special_courses:
                                class_.complete = True


def save_result(school, file="result.txt"):
    text = f"Possible amount of tests for each student: {school.std_testkits}\n\n"

    for teacher in school.all_teachers:
        text += teacher.name + "\n"
        for per in range(len(teacher.queue)):
            text += f"{per + 1}: "
            if len(teacher.queue[per]) == 0:
                text += "Free"
            else:
                text += ", ".join([str(loc) for loc in teacher.queue[per]])

            text += "\n"

        text += "\n\n"

    with open(file, 'w+') as f:
        f.write(text)
