from smarts_for_stupids import Calculator

from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)

from math import tau


def run(moves, scale, r, alpha, ev3):
    PAPER_TURNER_PORT = "A"
    PAPER_TURNER_GEARS = [1, 40]
    PEN_TURNER_PORT = "B"
    PEN_TURNER_GEARS = [8, 40]
    MOVES_PER_SECOND = 5

    paper_turner = Motor(
        PAPER_TURNER_PORT,
        positive_direction=Direction.CLOCKWISE,
        gears=PAPER_TURNER_GEARS,
    )
    pen_turner = Motor(
        PEN_TURNER_PORT, positive_direction=Direction.CLOCKWISE, gears=PEN_TURNER_GEARS
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
