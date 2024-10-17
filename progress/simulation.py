import cv2
import numpy as np
import vector
from math import tau, sin, cos


def vec(x, y):
    return vector.obj(x=x, y=y)


def vecp(rho, phi):
    return vector.obj(rho=rho, phi=phi)


def arrow(img, vec1, vec2):
    return cv2.arrowedLine(
        img, (int(vec1.x), int(vec1.y)), (int(vec2.x), int(vec2.y)), (255, 255, 0), 3
    )


w, h = 1000, 500
anchor = vec(100, 100)
alpha = tau / 4
beta = 0
r0 = 300
r = 200

v = vecp(50, 0)


def draw():
    global alpha, beta

    img = np.zeros((h, w, 3), np.uint8)
    A = vecp(r0, beta) + anchor
    B = vecp(r, alpha) + A
    C = v + B

    img = arrow(img, anchor, A)
    img = arrow(img, A, B)
    img = arrow(img, B, C)

    cv2.imshow("", img)


def move(d=0.000001):
    global alpha, beta

    A = vecp(r0, beta) + anchor
    B = vecp(r, alpha) + A

    x, y = v.x, v.y
    a1, a2 = (-sin(alpha), cos(alpha))
    b1, b2 = (-sin(beta), cos(beta))

    tmp = a1 * b2 - a2 * b1
    a = (b2 * x - b1 * y) / tmp
    b = (a1 * y - a2 * x) / tmp
    alpha += d * a * r0
    beta += d * b * r


while (key := cv2.waitKey(20)) != 32:
    draw()

    if key == 83:
        v.phi += 0.01 * tau
    if key == 81:
        v.phi -= 0.01 * tau
    if key == 82:
        move()
