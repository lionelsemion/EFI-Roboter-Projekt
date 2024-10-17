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


from patterns import draw_curve, CURVES
from physical import run


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
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
