from constants_task_3 import *


class Cell:
    def __init__(self, x, y, value):
        self.routes = {'R': True, 'L': True, 'D': True, 'U': True}
        self.visited = False
        self.value = value

    def __repr__(self):
        return str(self.value)


class Field:
    count = 0
    full_route = list()
    x_current, y_current = 0, 0

    def __init__(self, array):
        self.field = [[Cell(i, j, array[i, j]) for j in range(size)] for i in range(size)]
        self.field = np.asarray(self.field)

    def __repr__(self):
        line = ""
        for i in range(size):
            line += "{}\n".format(self.field[i])
        return line


def random_start():
    [x, y] = np.random.randint(0, size - 1), np.random.randint(0, size - 1)
    while matrix[x, y] != 1:
        [x, y] = np.random.randint(0, size - 1), np.random.randint(0, size - 1)
    return x, y


def user_choice():
    choice = input(choice_question)
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
    return start


def matrix_visualisation(final_matrix):
    print('{}'.format("->".join([str(i) for i in Field.full_route])), sep="")

    final_matrix.field[Field.x_current, Field.y_current].value = 3

    matrix_rotated = matrix_rotate(final_matrix)
    turtle.penup()
    trtl.tracer(0, 0)
    colors = {1: "red", -1: "green", 2: "blue", 3: "black"}
    for r in range(size):
        for c in range(size):
            if matrix_rotated[c, r].value == 0:
                continue
            turtle.goto(c, r)
            turtle.dot(dot_size, colors[matrix_rotated[c, r].value])
    trtl.update()


def matrix_rotate(array):
    work_matrix = array.field
    length = len(work_matrix[0])
    for i in range(length // 2):
        for j in range(i, length - i - 1):
            temp = work_matrix[i][j]
            work_matrix[i][j] = work_matrix[length - 1 - j][i]
            work_matrix[length - 1 - j][i] = work_matrix[length - 1 - i][length - 1 - j]
            work_matrix[length - 1 - i][length - 1 - j] = work_matrix[j][length - 1 - i]
            work_matrix[j][length - 1 - i] = temp
    return np.asarray(work_matrix)


def bounds(work_field):
    if work_field.full_route[Field.count][0] == 0:
        work_field.field[Field.full_route[Field.count]].routes['U'] = False
    if work_field.full_route[Field.count][0] == size - 1:
        work_field.field[Field.full_route[Field.count]].routes['D'] = False
    if work_field.full_route[Field.count][1] == 0:
        work_field.field[Field.full_route[Field.count]].routes['L'] = False
    if work_field.full_route[Field.count][1] == size - 1:
        work_field.field[Field.full_route[Field.count]].routes['R'] = False


def search_algorithm():
    start_point = user_choice()
    while start_point == "NaN":
        start_point = user_choice()

    matrix[start_point] = 1
    work_field = Field(matrix)
    Field.x_current, Field.y_current = start_point
    Field.full_route.append(start_point)

    while True:
        if Field.full_route[0] == Field.full_route[len(Field.full_route) - 1] and len(Field.full_route) != 1:
            print(successful_route, end='')
            break

        prev_count = Field.count

        while 0 <= Field.y_current < size - 1:
            bounds(work_field)
            if Field.full_route[0] == Field.full_route[len(Field.full_route) - 1] and len(Field.full_route) != 1:
                break
            Field.y_current += 1
            if work_field.field[Field.x_current, Field.y_current].value == -1 or \
                    work_field.field[Field.x_current, Field.y_current].visited \
                    or not work_field.field[Field.full_route[Field.count]].routes['R']:
                Field.y_current = Field.full_route[Field.count][1]
                work_field.field[Field.full_route[Field.count]].routes['R'] = False
                break
            elif work_field.field[Field.x_current, Field.y_current].value > 0 and \
                    work_field.field[Field.full_route[Field.count]].routes['R'] and not \
                    work_field.field[Field.x_current, Field.y_current].visited:
                Field.full_route.append((Field.x_current, Field.y_current))
                work_field.field[Field.x_current, Field.y_current].visited = True
                work_field.field[Field.full_route[Field.count]].routes['R'] = False
                Field.count += 1
                work_field.field[Field.x_current, Field.y_current].value = 2
                work_field.field[Field.full_route[Field.count]].routes['L'] = False
                for i in work_field.field[Field.x_current, Field.full_route[Field.count - 1][1] + 1:Field.full_route[Field.count][1]]:
                    i.value = -1
                break
            elif Field.y_current == size - 1 and work_field.field[Field.x_current, Field.y_current].value != 1:
                Field.y_current = Field.full_route[Field.count][1]
                work_field.field[Field.full_route[Field.count]].routes['R'] = False
                break

        while 0 < Field.y_current <= size - 1:
            bounds(work_field)
            if Field.full_route[0] == Field.full_route[len(Field.full_route) - 1] and len(Field.full_route) != 1:
                break
            Field.y_current -= 1
            if work_field.field[Field.x_current, Field.y_current].value == -1 or work_field.field[
                Field.x_current, Field.y_current].visited \
                    or not work_field.field[Field.full_route[Field.count]].routes['L']:
                Field.y_current = Field.full_route[Field.count][1]
                work_field.field[Field.full_route[Field.count]].routes['L'] = False
                break
            elif work_field.field[Field.x_current, Field.y_current].value > 0 and \
                    work_field.field[Field.full_route[Field.count]].routes['L'] and not work_field.field[Field.x_current, Field.y_current].visited:
                Field.full_route.append((Field.x_current, Field.y_current))
                work_field.field[Field.x_current, Field.y_current].visited = True
                work_field.field[Field.full_route[Field.count]].routes['L'] = False
                Field.count += 1
                work_field.field[Field.full_route[Field.count]].routes['R'] = False
                work_field.field[Field.x_current, Field.y_current].value = 2
                for i in work_field.field[Field.x_current, Field.full_route[Field.count][1] + 1:Field.full_route[Field.count - 1][1]]:
                    i.value = -1
                break
            elif Field.y_current == 0 and work_field.field[Field.x_current, Field.y_current].value != 1:
                work_field.field[Field.full_route[Field.count]].routes['L'] = False
                Field.y_current = Field.full_route[Field.count][1]
                break

        while 0 <= Field.x_current < size - 1:
            bounds(work_field)
            if Field.full_route[0] == Field.full_route[len(Field.full_route) - 1] and len(Field.full_route) != 1:
                break
            Field.x_current += 1
            if work_field.field[Field.x_current, Field.y_current].value == -1 \
                    or work_field.field[Field.x_current, Field.y_current].visited \
                    or not work_field.field[Field.full_route[Field.count]].routes['D']:
                Field.x_current = Field.full_route[Field.count][0]
                work_field.field[Field.full_route[Field.count]].routes['D'] = False
                break
            elif work_field.field[Field.x_current, Field.y_current].value > 0 and \
                    work_field.field[Field.full_route[Field.count]].routes['D'] and not work_field.field[Field.x_current, Field.y_current].visited:
                Field.full_route.append((Field.x_current, Field.y_current))
                work_field.field[Field.x_current, Field.y_current].visited = True
                work_field.field[Field.full_route[Field.count]].routes['D'] = False
                Field.count += 1
                work_field.field[Field.full_route[Field.count]].routes['U'] = False
                work_field.field[Field.x_current, Field.y_current].value = 2
                for i in work_field.field[Field.full_route[Field.count - 1][0] + 1:Field.full_route[Field.count][0], Field.y_current]:
                    i.value = -1
                break
            elif Field.x_current == size - 1 and work_field.field[Field.x_current, Field.y_current].value != 1:
                Field.x_current = Field.full_route[Field.count][0]
                work_field.field[Field.full_route[Field.count]].routes['D'] = False
                break

        while 0 < Field.x_current <= size - 1:
            bounds(work_field)
            if Field.full_route[0] == Field.full_route[len(Field.full_route) - 1] and len(Field.full_route) != 1:
                break
            Field.x_current -= 1
            if work_field.field[Field.x_current, Field.y_current].value == -1 \
                    or work_field.field[Field.x_current, Field.y_current].visited \
                    or not work_field.field[Field.full_route[Field.count]].routes['U']:
                Field.x_current = Field.full_route[Field.count][0]
                work_field.field[Field.full_route[Field.count]].routes['U'] = False
                break
            elif work_field.field[Field.x_current, Field.y_current].value > 0 and \
                    work_field.field[Field.full_route[Field.count]].routes['U'] and not work_field.field[Field.x_current, Field.y_current].visited:
                Field.full_route.append((Field.x_current, Field.y_current))
                work_field.field[Field.x_current, Field.y_current].visited = True
                work_field.field[Field.full_route[Field.count]].routes['U'] = False
                Field.count += 1
                work_field.field[Field.full_route[Field.count]].routes['D'] = False
                work_field.field[Field.x_current, Field.y_current].value = 2
                for i in work_field.field[Field.full_route[Field.count][0] + 1:Field.full_route[Field.count - 1][0], Field.y_current]:
                    i.value = -1
                break
            elif Field.x_current == 0 and work_field.field[Field.x_current, Field.y_current].value != 1:
                Field.x_current = Field.full_route[Field.count][0]
                work_field.field[Field.full_route[Field.count]].routes['U'] = False
                break

        if prev_count == Field.count:

            work_field.field[Field.x_current, Field.y_current].visited = False
            Field.count -= 1
            Field.x_current = Field.full_route[Field.count][0]
            Field.y_current = Field.full_route[Field.count][1]
            x, y = Field.full_route.pop()

            if not any(work_field.field[Field.x_current, Field.y_current].routes.values()) and Field.count == -1:
                print(false_point)
                break
            if x == Field.full_route[Field.count][0]:
                if y > Field.full_route[Field.count][1]:
                    for i in work_field.field[x, Field.full_route[Field.count][1] + 1:y]:
                        i.value = 0
                if y < Field.full_route[Field.count][1]:
                    for i in work_field.field[x, y + 1:Field.full_route[Field.count][1]]:
                        i.value = 0

            if y == Field.full_route[Field.count][1]:
                if x > Field.full_route[Field.count][0]:
                    for i in work_field.field[Field.full_route[Field.count][0] + 1:x, y]:
                        i.value = 0
                if x < Field.full_route[Field.count][0]:
                    for i in work_field.field[x + 1:Field.full_route[Field.count][0], y]:
                        i.value = 0
            work_field.field[x, y] = Cell(x, y, 1)

    return work_field


matrix_visualisation(search_algorithm())
screen.mainloop()
