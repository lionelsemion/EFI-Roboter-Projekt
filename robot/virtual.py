import cv2
from smarts import Calculator


def run(moves, scale, r, alpha, b=None):
    calculator = Calculator(r, alpha)

    for move in moves:
        calculator.move(move[0] * scale, move[1] * scale)
        calculator.draw()
        cv2.waitKey(30)

    cv2.waitKey()
    cv2.destroyAllWindows()
