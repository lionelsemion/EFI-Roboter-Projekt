import cv2
import numpy as np
from math import tau, sin, cos, atan2, sqrt


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


def arrow(img, vec1, vec2):
    return cv2.arrowedLine(
        img,
        (int(vec1.x), int(vec1.y)),
        (int(vec2.x), int(vec2.y)),
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )


def line(img, vec1, vec2):
    return cv2.line(
        img,
        (int(vec1.x), int(vec1.y)),
        (int(vec2.x), int(vec2.y)),
        (127, 127, 127),
        1,
        cv2.LINE_AA,
    )


class Calculator:

    def __init__(self, r, alpha, precision=0.0000001) -> None:
        self.r0 = 400 / ((1 / r) + 1)  # Distance of the two centers of rotation
        self.r = 400 / (
            r + 1
        )  # The distance of the two centers of rotation, divided by the pen arm length
        self.alpha = tau / 2 - alpha  # Angle between the pen arm and the paper rotator
        self.precision = precision  # Max numerical step width

        self.anchor = vec(50, 50)
        self.w, self.h = 1000, 500
        self.beta = 0

        self.painting = np.zeros((self.h, self.w, 3), np.uint8)
        margin = 10
        self.painting = cv2.circle(
            self.painting,
            (self.anchor.x, self.anchor.y),
            400 - margin,
            (64, 64, 64),
            -1,
            cv2.LINE_AA,
        )
        self.painting = cv2.circle(
            self.painting,
            (self.anchor.x, self.anchor.y),
            int(self.r0 - self.r + margin),
            (0, 0, 0),
            -1,
            cv2.LINE_AA,
        )

        A = vecp(self.r0, self.beta) + self.anchor
        self.oldB = vecp(self.r, self.alpha) + A

    def draw(self):
        A = vecp(self.r0, self.beta) + self.anchor
        B = vecp(self.r, self.alpha) + A

        if self.oldB != B:
            self.painting = line(self.painting, self.oldB, B)
            self.oldB = B

        img = np.copy(self.painting)

        img = arrow(img, self.anchor, A)
        img = arrow(img, A, B)

        cv2.imshow("", img)

    def _nanomove(self, v):
        v = v.copy()

        A = vecp(self.r0, self.beta) + self.anchor
        B = vecp(self.r, self.alpha) + A

        x, y = v.x, v.y
        a1, a2 = (-sin(self.alpha), cos(self.alpha))
        b1, b2 = (-sin(self.beta), cos(self.beta))

        tmp = a1 * b2 - a2 * b1
        a = (b2 * x - b1 * y) / tmp
        b = (a1 * y - a2 * x) / tmp
        self.alpha += a * self.r0
        self.beta += b * self.r

        return vec(a * self.r0, b * self.r)

    def move(self, dx, dy):
        d_angles = vec(0, 0)

        v = vec(dx, dy)
        r = v.rho
        v.rho = self.precision
        for _ in range(int(r / self.precision)):
            d_angles += self._nanomove(v)
        if r % self.precision > 0:
            v.rho = r % self.precision
        d_angles += self._nanomove(v)

        return d_angles.x, d_angles.y
