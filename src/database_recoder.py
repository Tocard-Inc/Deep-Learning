from subprocess import call
from time import sleep
import numpy as np


center = (1000, 500)

garage = (340, 980)

edit = (1950, 850)
select = (1950, 980)

back = (70, 60)

itemX = (200, 450, 700)
itemY = (300, 580, 860)

sticker = (220, 60)
wheel = (330, 60)
hat = (440, 60)
color = (660, 60)

principale = (290, 542)
accent = (380, 632)

color_min = 366
color_max = 708
color_center = (color_min + color_max) / 2
color_dist = color_max - color_min

Nsticker = [2, 2]  # [3, 3, 8, 9]
Nwheel = 2  # 19
Nhat = 2  # 22

delay = 0.08

Ncolor_p = 1  # 3
Ncolor_a = 1  # 3

Nrot_h = 1  # 3
Nrot_v = 1  # 3


def tap(pos):
    call(["adb", "shell", "input", "tap", str(pos[0]), str(pos[1])])


def motion(pos, type):
    call(["adb", "shell", "input", "motionevent", type, str(pos[0]), str(pos[1])])


def setColor(c: int, p: float, a: float):
    tap(color)

    # set principal color
    motion((color_center, principale[c]), "DOWN")
    motion((color_min + 100, principale[c]), "MOVE")
    motion((color_min + p * color_dist, principale[c]), "MOVE")
    motion((color_min + p * color_dist, principale[c]), "UP")

    # set accent color
    motion((color_center, accent[c]), "DOWN")
    motion((color_min + 100, accent[c]), "MOVE")
    motion((color_min + a * color_dist, accent[c]), "MOVE")
    motion((color_min + a * color_dist, accent[c]), "UP")


def rotate(x, y):
    motion(center, "DOWN")
    motion(center, "MOVE")
    motion(np.array(center) + np.array((x, y)), "MOVE")
    motion(np.array(center) + np.array((x, y)), "UP")


def selectItem(kind, i):
    tap(kind)
    sleep(delay)

    col = i % 3
    row = i // 3

    # slide up item list
    if row > 2:
        nslide = row - 2
        slide = itemY[0] - itemY[1]

        motion((itemX[1], itemY[2]), "DOWN")
        motion((itemX[1], itemY[1]), "MOVE")
        motion((itemX[1], itemY[1] + nslide * slide), "MOVE")
        motion((itemX[1], itemY[1] + nslide * slide), "UP")

        row -= nslide

    tap((itemX[col], itemY[row]))


def nextModel(n):
    motion(center, "DOWN")
    motion(center, "MOVE")
    motion(np.array(center) + np.array((n * -1700, 0)), "MOVE")
    motion(np.array(center) + np.array((n * -1700, 0)), "UP")
    tap(select)


def newCar(s: int, w: int, h: int, c: int, p: float, a: float, n: int):
    tap(garage)
    sleep(delay)

    if n != 0:
        nextModel(n)
        sleep(delay)

    tap(edit)
    sleep(delay)

    if s >= 0:
        selectItem(sticker, s)
        sleep(delay)

    if w >= 0:
        selectItem(wheel, w)
        sleep(delay)

    if h >= 0:
        selectItem(hat, h)
        sleep(delay)

    if c >= 0:
        setColor(c, p, a)
        sleep(delay)

    tap(back)
    sleep(delay)

    tap(back)
    sleep(delay)


# principal color dicho
for ip in range(3):
    ori_p = 1 / 2 ** (ip + 1)
    dec_p = 1 / 2**ip
    for jp in range(2**ip):
        p = ori_p + jp * dec_p

        # accent color dicho
        for ia in range(3):
            ori_a = 1 / 2 ** (ia + 1)
            dec_a = 1 / 2**ia
            for ja in range(2**ia):
                a = ori_a + ja * dec_a

                # blue/orange
                for c in range(2):

                    # model
                    for nm, ns in enumerate(Nsticker):
                        newCar(-1, -1, -1, c, p, a, 0)

                        # sticker
                        for s in range(ns):
                            newCar(s, -1, -1, -1, 0.0, 0.0, 0)

                            # wheel
                            for w in range(Nwheel):
                                newCar(-1, w, -1, -1, 0.0, 0.0, 0)

                                # hat
                                for h in range(Nhat):
                                    newCar(-1, -1, h, -1, 0.0, 0.0, 0)

                                    # rotate
                                    for i in range(Nrot_v):
                                        for j in range(Nrot_h):
                                            rotate(1200, 0)
                                        rotate(0, 100)
                        # next model
                        newCar(
                            -1,
                            -1,
                            -1,
                            -1,
                            -1,
                            -1,
                            1 if nm != len(Nsticker) - 1 else 1 - len(Nsticker),
                        )
