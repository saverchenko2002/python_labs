from constants_task_3 import *


class Cell:
    def __init__(self, x, y, value):
        self.routes = {'R': True, 'L': True, 'D': True, 'U': True}
        self.visited = False
        self.value = value

    def __repr__(self):
        return str(self.value)


class Field:
    end = - 1
    count = 0
    full_route = list()
    x_current, y_current = 0, 0

    @classmethod
    def clear(cls):
        cls.count = 0
        cls.x_current = 0
        cls.y_current = 0
        cls.end = -1
        cls.full_route.clear()

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


def matrix_visualisation(a):
    print('{}'.format("->".join([str(i) for i in Field.full_route])), sep="")

    a.field[Field.x_current, Field.y_current].value = 3

    matrix1 = rotate90Clockwise(a)
    # matrix[Field.full_route[0][1], Field.full_route[0][0]].value = 3
    # matrix = a.field
    turtle.penup()
    trtl.tracer(0, 0)
    colors = {1: "red", -1: "HotPink", 2: "blue", 3: "black"}
    for r in range(size):
        for c in range(size):
            if matrix1[c, r].value == 0:
                continue
            turtle.goto(c, r)
            turtle.dot(dot_size, colors[matrix1[c, r].value])
    trtl.update()


def rotate90Clockwise(matrix2):
    A = matrix2.field
    N = len(A[0])
    for i in range(N // 2):
        for j in range(i, N - i - 1):
            temp = A[i][j]
            A[i][j] = A[N - 1 - j][i]
            A[N - 1 - j][i] = A[N - 1 - i][N - 1 - j]
            A[N - 1 - i][N - 1 - j] = A[j][N - 1 - i]
            A[j][N - 1 - i] = temp
    return np.asarray(A)


def matrix_flip(a, b):
    temp = []
    a = a.tolist()
    for i in range(len(a)):
        temp = temp + [a[i][:]]
    if b == 'h':

        for i in range(len(temp)):
            temp[i].reverse()
            i = i + 1
        return np.asarray(temp)
    elif b == 'v':
        temp.reverse()
        return np.asarray(temp)


def bounds(work_field):
    if work_field.full_route[Field.count][0] == 0:
        work_field.field[Field.full_route[Field.count]].routes['U'] = False
    if work_field.full_route[Field.count][0] == size - 1:
        work_field.field[Field.full_route[Field.count]].routes['D'] = False
    if work_field.full_route[Field.count][1] == 0:
        work_field.field[Field.full_route[Field.count]].routes['L'] = False
    if work_field.full_route[Field.count][1] == size - 1:
        work_field.field[Field.full_route[Field.count]].routes['R'] = False


def search_algorithm(PW):
    # start_point = user_choice()
    # while start_point == "NaN":
    #     start_point = user_choice()
    start_point = PW
    print("{}->".format(PW), end='')
    matrix_new = np.asarray(matrix.tolist())
    matrix_new[start_point] = 1
    work_field = Field(matrix_new)
    Field.x_current, Field.y_current = start_point

    Field.full_route.append(start_point)

    while work_field.end == -1:
        if Field.full_route[0] == Field.full_route[len(Field.full_route) - 1] and len(Field.full_route) != 1:
            print("Route exists")
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
                for i in work_field.field[Field.x_current,
                         Field.full_route[Field.count - 1][1] + 1:Field.full_route[Field.count][1]]:
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
                    work_field.field[Field.full_route[Field.count]].routes['L'] and not work_field.field[
                Field.x_current, Field.y_current].visited:
                Field.full_route.append((Field.x_current, Field.y_current))
                work_field.field[Field.x_current, Field.y_current].visited = True
                work_field.field[Field.full_route[Field.count]].routes['L'] = False
                Field.count += 1
                work_field.field[Field.full_route[Field.count]].routes['R'] = False
                work_field.field[Field.x_current, Field.y_current].value = 2
                for i in work_field.field[Field.x_current,
                         Field.full_route[Field.count][1] + 1:Field.full_route[Field.count - 1][1]]:
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
            if work_field.field[Field.x_current, Field.y_current].value == -1 or work_field.field[
                Field.x_current, Field.y_current].visited \
                    or not work_field.field[Field.full_route[Field.count]].routes['D']:
                Field.x_current = Field.full_route[Field.count][0]
                work_field.field[Field.full_route[Field.count]].routes['D'] = False
                break
            elif work_field.field[Field.x_current, Field.y_current].value > 0 and \
                    work_field.field[Field.full_route[Field.count]].routes['D'] and not work_field.field[
                Field.x_current, Field.y_current].visited:
                Field.full_route.append((Field.x_current, Field.y_current))
                work_field.field[Field.x_current, Field.y_current].visited = True
                work_field.field[Field.full_route[Field.count]].routes['D'] = False
                Field.count += 1
                work_field.field[Field.full_route[Field.count]].routes['U'] = False
                work_field.field[Field.x_current, Field.y_current].value = 2
                for i in work_field.field[Field.full_route[Field.count - 1][0] + 1:Field.full_route[Field.count][0],
                         Field.y_current]:
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
                    work_field.field[Field.full_route[Field.count]].routes['U'] and not work_field.field[
                Field.x_current, Field.y_current].visited:
                Field.full_route.append((Field.x_current, Field.y_current))
                work_field.field[Field.x_current, Field.y_current].visited = True
                work_field.field[Field.full_route[Field.count]].routes['U'] = False
                Field.count += 1
                work_field.field[Field.full_route[Field.count]].routes['D'] = False
                work_field.field[Field.x_current, Field.y_current].value = 2
                for i in work_field.field[Field.full_route[Field.count][0] + 1:Field.full_route[Field.count - 1][0],
                         Field.y_current]:
                    i.value = -1
                break
            elif Field.x_current == 0 and work_field.field[Field.x_current, Field.y_current].value != 1:
                Field.x_current = Field.full_route[Field.count][0]
                work_field.field[Field.full_route[Field.count]].routes['U'] = False
                break
        # for i in range (len(Field.full_route))
        #print('{}'.format("->".join([str(i) for i in Field.full_route])), sep="")

        if prev_count == Field.count:
            #print("TUPIK")
            work_field.field[Field.x_current, Field.y_current].visited = False
            Field.count -= 1
            Field.x_current = Field.full_route[Field.count][0]
            Field.y_current = Field.full_route[Field.count][1]
            x, y = Field.full_route.pop()
            # print(work_field.field[Field.full_route[0]].routes)
            #print('{}'.format("->".join([str(i) for i in Field.full_route])), sep="")
            #print(Field.x_current, Field.y_current)
            #print(Field.count)
            #print(work_field.field[Field.x_current, Field.y_current].routes.values())
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
                #print("chmo")
                if x > Field.full_route[Field.count][0]:
                    for i in work_field.field[Field.full_route[Field.count][0] + 1:x, y]:
                        i.value = 0
                        #print("chmo1")
                if x < Field.full_route[Field.count][0]:
                    for i in work_field.field[x + 1:Field.full_route[Field.count][0], y]:
                        i.value = 0
                        #print("chmo2")
            work_field.field[x, y] = Cell(x, y, 1)

    return work_field


for i  in range(size):
    for j in range(size):
        search_algorithm((i,j))
        Field.clear()

