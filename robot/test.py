from smarts import Calculator
from math import tau
import cv2

calculator = Calculator(2, tau / 4.01)
s = 10
while (key := cv2.waitKey(50)) != 32:
    calculator.draw()
    # calculator.beta += 0.01 * tau
    if key == 81:
        calculator.move(-s, 0)
    if key == 82:
        calculator.move(0, -s)
    if key == 83:
        calculator.move(s, 0)
    if key == 84:
        calculator.move(0, s)
