from math import tau, sin, cos


moves = []

direction = 0


def l():
    moves.append([-1, 0])


def u():
    moves.append([0, -1])


def r():
    moves.append([1, 0])


def d():
    moves.append([0, 1])


def rotate(phi):
    global direction
    direction += phi / 360 * tau


def forward(r=1):
    global moves
    global direction
    moves.append([cos(direction) * r, sin(direction) * r])


def hilbert(iteration):
    global direction, moves
    moves = []

    def A(depth):
        if depth > 0:
            D(depth - 1)
            u()
            A(depth - 1)
            r()
            A(depth - 1)
            d()
            B(depth - 1)

    def B(depth):
        if depth > 0:
            C(depth - 1)
            l()
            B(depth - 1)
            d()
            B(depth - 1)
            r()
            A(depth - 1)

    def C(depth):
        if depth > 0:
            B(depth - 1)
            d()
            C(depth - 1)
            l()
            C(depth - 1)
            u()
            D(depth - 1)

    def D(depth):
        if depth > 0:
            A(depth - 1)
            r()
            D(depth - 1)
            u()
            D(depth - 1)
            l()
            C(depth - 1)

    A(iteration)

    return moves


def gosper(iteration):
    global direction, moves
    moves = []

    def A(depth):
        if depth > 0:
            A(depth - 1)
            rotate(-60)
            B(depth - 1)
            rotate(-60)
            rotate(-60)
            B(depth - 1)
            rotate(60)
            A(depth - 1)
            rotate(60)
            rotate(60)
            A(depth - 1)
            A(depth - 1)
            rotate(60)
            B(depth - 1)
            rotate(-60)
        else:
            forward()

    def B(depth):
        if depth > 0:
            rotate(60)
            A(depth - 1)
            rotate(-60)
            B(depth - 1)
            B(depth - 1)
            rotate(-60)
            rotate(-60)
            B(depth - 1)
            rotate(-60)
            A(depth - 1)
            rotate(60)
            rotate(60)
            A(depth - 1)
            rotate(60)
            B(depth - 1)
        else:
            forward()

    A(iteration)

    return moves


def euler():
    global direction, moves
    moves = []

    for a in range(-180, 181, 1):
        forward(0.3)
        rotate(a)

    return moves


def spiral(turns):
    global direction, moves
    moves = []

    for a in range(1, 100 * turns):
        forward(a / (10 * turns))
        rotate(3.6)

    return moves


def greek(iteration):
    global direction, moves
    moves = []

    def A(depth):
        if depth > 0:
            rotate(90)
            B(depth - 1)
            forward()
            B(depth - 1)
            forward()
            rotate(-90)
            A(depth - 1)
            forward()
            A(depth - 1)
            forward()
            A(depth - 1)
            rotate(-90)
            forward()
            rotate(-90)
            A(depth - 1)
            forward()
            rotate(90)
            B(depth - 1)
            forward()
            B(depth - 1)
            rotate(90)
            forward()
            A(depth - 1)

    def B(depth):
        if depth > 0:
            rotate(-90)
            A(depth - 1)
            forward()
            A(depth - 1)
            forward()
            rotate(90)
            B(depth - 1)
            forward()
            B(depth - 1)
            forward()
            B(depth - 1)
            rotate(90)
            forward()
            rotate(90)
            B(depth - 1)
            forward()
            rotate(-90)
            A(depth - 1)
            forward()
            A(depth - 1)
            rotate(-90)
            forward()
            B(depth - 1)

    rotate(230)
    A(iteration)

    return moves


def squares(subdiv, count):
    global direction, moves
    moves = []

    for _ in range(count * 4 - 1):
        for _ in range(subdiv):
            forward(1 / subdiv)
        rotate(90 + 90 / (count * 4 - 1))

    return moves


def grid(iterations):
    global direction, moves
    moves = []

    for i in range(iterations):
        for j in range(4):
            for _ in range(iterations - (j == 3) - i):
                forward()
                rotate(-90 if i % 2 else 90)
                forward()
                rotate(90 if i % 2 else -90)
            forward()
            rotate(90 if i % 2 else -90)

    forward()
    rotate(90 if iterations % 2 else -90)
    forward()
    if not iterations % 2:
        rotate(90 if iterations % 2 else -90)
        forward()
        rotate(90 if iterations % 2 else -90)
        forward()

    for i in range((iterations + 1) // 2):
        rotate(90 if iterations % 2 else -90)
        forward()
        rotate(90 if iterations % 2 else -90)
        forward()
        rotate(-90 if iterations % 2 else 90)
        forward()
        rotate(-90 if iterations % 2 else 90)
        forward()

    return moves


start_angle = tau / 4

CURVES = [
    "TRIANGLE",
    "SQUARES",
    "GRID",
    "SPIRAL",
    "EULER",
    "HILBERT",
    "GOSPER",
    "GREEK",
]


def draw_curve(name, run, centers_distance=1, brick=None):
    global direction

    if name == "TRIANGLE":
        direction = tau / 2
        moves = squares(20, 1)
        run(moves, 100, centers_distance, start_angle, brick)

    if name == "SQUARES":
        direction = tau / 2
        moves = squares(20, 4)
        run(moves, 100, centers_distance, start_angle, brick)

    if name == "GRID":
        direction = tau / 2
        moves = grid(5)
        run(moves, 15, centers_distance, start_angle, brick)

    if name == "SPIRAL":
        direction = 0
        moves = spiral(5)
        run(moves, 0.5, centers_distance, start_angle, brick)

    if name == "EULER":
        direction = 0
        moves = euler()
        run(moves, 20, centers_distance, start_angle, brick)

    if name == "HILBERT":
        moves = hilbert(4)
        run(moves, 7, centers_distance, start_angle, brick)

    if name == "GOSPER":
        direction = 0
        moves = gosper(3)
        run(moves, 10, centers_distance, start_angle, brick)

    if name == "GREEK":
        direction = 0
        moves = greek(3)
        run(moves, 6.5, centers_distance, start_angle, brick)
