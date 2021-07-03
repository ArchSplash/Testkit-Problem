from testkits import sort_testkits
from school import *
from distribution import *
from time import strftime


# Get classes and students
TOTAL_STUDENTS = int(input("Total Students: "))  # SENIOR_STUDENTS + JUNIOR_STUDENTS
DATE = input(f"Date (e.g. {strftime('%Y-%m-%d')}): ")
START_PERIOD = int(input("When should it start: ")) - 1

TESTKITS_AMOUNT = sort_testkits()

if TOTAL_STUDENTS <= TESTKITS_AMOUNT:
    # Declare and create objects
    school = School(DATE, TESTKITS_AMOUNT // TOTAL_STUDENTS)
    FLOORS = [0, 1, 2, 3]
    school.all_teachers = [Teacher("Rabe", FLOORS[1], FLOORS[0]), Teacher("Wetzel", FLOORS[2], FLOORS[3])]

    # Enough tests
    print("Give all")
    print("Possible amount of tests for each student:", school.std_testkits)

    create_queue(school, START_PERIOD)

    for teacher in school.all_teachers:
        print(teacher.name)
        for per in range(len(teacher.queue)):
            print("Period -", per + 1)
            print(teacher.queue[per])
        print()

    for cls in school.all_classes:
        if not cls.complete:
            print(cls)

    save_result(school)

# Not enough tests
else:
    print("Wait for tests")
