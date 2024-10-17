#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from math import tau, sin, cos, atan2, sqrt


############ Constants ############


PAPER_TURNER_PORT = "A"
PAPER_TURNER_GEARS = [1, 40]
PEN_TURNER_PORT = "B"
PEN_TURNER_GEARS = [8, 40]
MOVES_PER_SECOND = 5
INVERT_PAPER_TURNER = False
INVERT_PEN_TURNER = False


############ Patterns and Curves ############


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


############ Maths ############


class Vec:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @property
    def rho(self):
        return sqrt(self.x * self.x + self.y * self.y)

    @rho.setter
    def rho(self, value):
        scale = value / self.rho
        self.x *= scale
        self.y *= scale

    @property
    def phi(self):
        return atan2(self.y, self.x)

    @phi.setter
    def phi(self, value):
        self.x, self.y = self.rho * cos(value), self.rho * sin(value)

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __sub__(self, other):
        return self + -other

    def __repr__(self) -> str:
        return f"{self.x} {self.y}"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def copy(self):
        return Vec(self.x, self.y)


def vec(x, y):
    return Vec(x, y)


def vecp(rho, phi):
    return Vec(rho * cos(phi), rho * sin(phi))


class Calculator:

    def __init__(self, r, alpha, precision=1e-2) -> None:
        self.r0 = 400 / ((1 / r) + 1)  # Distance of the two centers of rotation
        self.r = 400 / (
            r + 1
        )  # The distance of the two centers of rotation, divided by the pen arm length
        self.alpha = tau / 2 - alpha  # Angle between the pen arm and the paper rotator
        self.precision = precision  # Max numerical step width

        self.beta = 0

        A = vecp(self.r0, self.beta)

        self.target_B = vecp(self.r, self.alpha + self.beta) + A
        self.d_alpha = 0
        self.d_beta = 0

    def _loss(self):
        aA = vecp(self.r0, self.d_beta + self.beta)
        aB = vecp(self.r, self.d_alpha + self.alpha + self.d_beta + self.beta) + aA

        return (aB - self.target_B).rho ** 2

    def move(self, dx, dy):
        self.target_B += Vec(dx, dy)

        p = self.precision

        self.d_alpha = self.d_beta = 0

        loss = self._loss()

        w = 1e-15
        while loss > p:
            self.d_alpha += w
            m_alpha = (self._loss() - loss) / w
            self.d_alpha -= 0.0000001 * m_alpha + w
            loss = self._loss()
            self.d_beta += w
            m_beta = (self._loss() - loss) / w
            self.d_beta -= 0.0000001 * m_beta + w
            loss = self._loss()

        self.alpha += self.d_alpha
        self.beta += self.d_beta

        return self.d_alpha, self.d_beta


############ Driver ############


def run(moves, scale, r, alpha, ev3):
    paper_turner = Motor(
        PAPER_TURNER_PORT,
        positive_direction=(
            Direction.COUNTERCLOCKWISE if INVERT_PAPER_TURNER else Direction.CLOCKWISE
        ),
        gears=PAPER_TURNER_GEARS,
    )
    pen_turner = Motor(
        PEN_TURNER_PORT,
        positive_direction=(
            Direction.COUNTERCLOCKWISE if INVERT_PEN_TURNER else Direction.CLOCKWISE
        ),
        gears=PEN_TURNER_GEARS,
    )

    calculator = Calculator(r, alpha)

    angle_changes = []

    for move in moves:
        d_alpha, d_beta = calculator.move(move[0] * scale, move[1] * scale)
        angle_changes.append((d_alpha * 360 / tau, d_beta * 360 / tau))

    ev3.light(Color.BLUE)
    ev3.speaker.beep()

    i = 0
    for d_alpha, d_beta in angle_changes:
        i += 0
        ev3.display.text(f"{round(i/len(angle_changes)*100)}%")
        pen_turner.run_angle(
            d_alpha * MOVES_PER_SECOND * 1.1, d_alpha, then=Stop.HOLD, wait=False
        )
        paper_turner.run_angle(
            d_beta * MOVES_PER_SECOND * 1.1, d_beta, then=Stop.HOLD, wait=False
        )
        wait(1000 / MOVES_PER_SECOND)

    ev3.display.text(f"Done.")
    ev3.speaker.beep()
    wait(1000)
    ev3.display.text(f"Reset pen before starting again")
    wait(1000)


############ Main ############


ev3 = EV3Brick()


while 1:
    ev3.light(Color.GREEN)

    selected_curve = 0
    ev3.display.text(f"< {CURVES[selected_curve]} >")
    while True:
        b = ev3.buttons()
        if Button.LEFT in b:
            selected_curve = (selected_curve - 1) % len(CURVES)
            ev3.display.text(f"< {CURVES[selected_curve]} >")
            while Button.LEFT in b:
                pass

        elif Button.RIGHT in b:
            selected_curve = (selected_curve + 1) % len(CURVES)
            ev3.display.text(f"< {CURVES[selected_curve]} >")
            while Button.RIGHT in b:
                pass

        elif Button.CENTER in b:
            ev3.display.text(f"{CURVES[selected_curve]}\nCalculating...")
            break

    ev3.speaker.beep()
    ev3.light(Color.YELLOW)
    draw_curve(CURVES[selected_curve], run, 1, ev3)
