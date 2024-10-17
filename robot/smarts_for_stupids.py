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
