from Distribution import improved_queue, save_to_text
from School import *


sufficient, amount = check_tests()

# Enough tests
if sufficient:
    print("Give all")
    print("Amount of tests for each student:", amount)

    improved_queue()

    for teacher in TEACHERS:
        print(teacher.name)
        for per in range(len(teacher.queue)):
            print("Period -", per + 1)
            print(teacher.queue[per])

        print()

    save_to_text("result.txt")

# Not enough tests
else:
    print("Wait for tests")
