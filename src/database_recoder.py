import itertools
import logging
from subprocess import call
from time import sleep

import numpy as np

CENTER = (1000, 500)

GARAGE = (340, 980)

EDIT_LOADOUT_BTN = (1950, 850)
SELECT_CAR_BTN = (1950, 980)

BACK_BTN = (50, 50)

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

# Nsticker = [2, 2]  # [3, 3, 8, 9]
NB_STICKERS = 2
NB_WHEELS = 19
NB_HATS = 22
NB_TEAMS = 2

DELAY = 0.2

NB_PRIMARY_COLORS = 1  # 3
NB_SECONDARY_COLORS = 1  # 3

NB_HORIZONTAL_ROTATIONS = 1  # 3
NB_VERTICAL_ROTATIONS = 1  # 3


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


def newCar(s=-1, w=-1, h=-1, c=-1, p=-1.0, a=-1.0, n=0):
    tap(GARAGE)
    sleep(DELAY)

    if n:
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


# # primary color dicho
# primary_colors = []
# for ip in range(3):
#     ori_p = 1 / 2 ** (ip + 1)
#     dec_p = 1 / 2**ip
#     for jp in range(2**ip):
#         primary_colors.append(ori_p + jp * dec_p)

# # secondary color dicho
# secondary_colors = []
# for ia in range(3):
#     ori_a = 1 / 2 ** (ia + 1)
#     dec_a = 1 / 2**ia
#     for ja in range(2**ia):
#         secondary_colors.append(ori_a + ja * dec_a)

primary_colors = np.linspace(0, 1, 5, endpoint=True)
secondary_colors = np.linspace(0, 1, 5, endpoint=True)

teams = range(NB_TEAMS)

stickers = range(NB_STICKERS)

wheels = range(NB_WHEELS)

hats = range(NB_HATS)

vertical_rotations = range(NB_VERTICAL_ROTATIONS)
horizontal_rotations = range(NB_HORIZONTAL_ROTATIONS)

loadouts = itertools.product(wheels, hats, primary_colors, secondary_colors, teams)
nb_loadouts = (
    len(teams) * len(wheels) * len(hats) * len(primary_colors) * len(secondary_colors)
)  # find something prettier

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)-8s  %(message)s",
    datefmt="(%F %T)",
)

logging.debug(f"number of loadouts: {nb_loadouts}")

for (wheel, hat, primary_color, secondary_color, team) in loadouts:
    logging.debug(f"next loadout: {(team, wheel, hat, primary_color, secondary_color)}")
    newCar(w=wheel, h=hat, p=primary_color, a=secondary_color, c=team)
