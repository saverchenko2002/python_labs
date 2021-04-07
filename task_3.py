from constants_task_3 import *


def random_start():
    [x, y] = np.random.randint(0, size - 1), np.random.randint(0, size - 1)
    while matrix[x, y] != 1:
        [x, y] = np.random.randint(0, size - 1), np.random.randint(0, size - 1)
    return x, y


def user_choice():
    print(choice_question)
    choice = input()
    if choice.lower() == 'y':
        start = random_start()
    elif choice.lower() == 'n':
        print(example_input)
        start = tuple([int(i) for i in input().split(' ')])
        while not (15 > start[0] > -1 and 15 > start[1] > -1):
            print(incorrect_input + " " + bounds_hint + " " + example_input)
            start = tuple([int(i) for i in input().split(' ')])
    else:
        start = "NaN"
    print("Start point = {}".format(start))
    return start


start_point = user_choice()
while start_point == "NaN":
    start_point = user_choice()
