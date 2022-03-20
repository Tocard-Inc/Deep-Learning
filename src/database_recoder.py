import logging
from subprocess import call
from time import sleep

import numpy as np

CENTER = (1000, 500)

GARAGE = (340, 980)

EDIT_LOADOUT_BTN = (1950, 850)
SELECT_CAR_BTN = (1950, 980)

BACK_BTN = (70, 60)

itemX = (200, 450, 700)
itemY = (300, 580, 860)

STICKER_MENU_BTN = (220, 60)
WHEEL_MENU_BTN = (330, 60)
HAT_MENU_BTN = (440, 60)
COLOR_MENU_BTN = (660, 60)

PRIMARY_COLOR_SLIDER = (290, 542)
SECONDARY_COLOR_SLIDER = (380, 632)

color_min = 366
color_max = 708
color_center = (color_min + color_max) / 2
color_dist = color_max - color_min

Nsticker = [2, 2]  # [3, 3, 8, 9]
Nwheel = 19
Nhat = 22

DELAY = 0.5

Ncolor_p = 1  # 3
Ncolor_a = 1  # 3

Nrot_h = 1  # 3
Nrot_v = 1  # 3


def tap(pos):
    call(["adb", "shell", "input", "tap", str(pos[0]), str(pos[1])])
    #    device.shell(f"input tap {pos[0]} {pos[1]}")


def motion(pos, type):
    call(["adb", "shell", "input", "motionevent", type, str(pos[0]), str(pos[1])])


def setColor(c: int, p: float, a: float):
    tap(COLOR_MENU_BTN)

    # set principal color
    motion((color_center, PRIMARY_COLOR_SLIDER[c]), "DOWN")
    motion((color_min + 100, PRIMARY_COLOR_SLIDER[c]), "MOVE")
    motion((color_min + p * color_dist, PRIMARY_COLOR_SLIDER[c]), "MOVE")
    motion((color_min + p * color_dist, PRIMARY_COLOR_SLIDER[c]), "UP")

    # set accent color
    motion((color_center, SECONDARY_COLOR_SLIDER[c]), "DOWN")
    motion((color_min + 100, SECONDARY_COLOR_SLIDER[c]), "MOVE")
    motion((color_min + a * color_dist, SECONDARY_COLOR_SLIDER[c]), "MOVE")
    motion((color_min + a * color_dist, SECONDARY_COLOR_SLIDER[c]), "UP")


def rotate(x, y):
    sleep(2)
    motion(CENTER, "DOWN")
    motion(CENTER, "MOVE")
    motion(np.array(CENTER) + np.array((x, y)), "MOVE")
    motion(np.array(CENTER) + np.array((x, y)), "UP")


def selectItem(kind, i):
    tap(kind)
    sleep(DELAY)

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
    motion(CENTER, "DOWN")
    motion(CENTER, "MOVE")
    motion(np.array(CENTER) + np.array((n * -1700, 0)), "MOVE")
    motion(np.array(CENTER) + np.array((n * -1700, 0)), "UP")
    tap(SELECT_CAR_BTN)


def newCar(s=-1, w=-1, h=-1, c=-1, p=-1.0, a=-1.0, n=-1):
    tap(GARAGE)
    sleep(DELAY)

    if n != 0:
        nextModel(n)
        sleep(DELAY)

    tap(EDIT_LOADOUT_BTN)
    sleep(DELAY)

    if s >= 0:
        selectItem(STICKER_MENU_BTN, s)
        sleep(DELAY)

    if w >= 0:
        selectItem(WHEEL_MENU_BTN, w)
        sleep(DELAY)

    if h >= 0:
        selectItem(HAT_MENU_BTN, h)
        sleep(DELAY)

    if c >= 0:
        setColor(c, p, a)
        sleep(DELAY)

    tap(BACK_BTN)
    sleep(DELAY)

    tap(BACK_BTN)
    sleep(DELAY)


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
                        logging.debug("model")
                        newCar(-1, -1, -1, c, p, a, 0)

                        # sticker
                        for s in range(ns):
                            logging.debug("sticker")
                            newCar(s, -1, -1, -1, 0.0, 0.0, 0)

                            # wheel
                            for w in range(Nwheel):
                                logging.debug("wheel")
                                newCar(-1, w, -1, -1, 0.0, 0.0, 0)

                                # hat
                                for h in range(Nhat):
                                    logging.debug("hat")
                                    newCar(-1, -1, h, -1, 0.0, 0.0, 0)

                                    # rotate
                                    for i in range(Nrot_v):
                                        for j in range(Nrot_h):
                                            rotate(1200, 0)
                                            logging.debug("rotation")
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
