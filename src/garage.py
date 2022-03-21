import itertools
import logging
from curses.ascii import DEL
from subprocess import call
from time import sleep

import numpy as np

CENTER = (1000, 500)

STICKER_MENU_BTN = (220, 60)
WHEEL_MENU_BTN = (330, 60)
HAT_MENU_BTN = (440, 60)
COLOR_MENU_BTN = (660, 60)
GARAGE_BTN = (340, 980)
EDIT_LOADOUT_BTN = (1950, 850)
SELECT_CAR_BTN = (1950, 980)
BACK_BTN = (50, 50)

COLOR_MIN = 375
COLOR_MAX = 715
COLOR_DIST = COLOR_MAX - COLOR_MIN
TEAM_OFFSET = 250
PRIMARY_COLOR_SLIDER = (290, 290 + TEAM_OFFSET)
SECONDARY_COLOR_SLIDER = (380, 380 + TEAM_OFFSET)

itemX = (200, 450, 700)
itemY = (300, 580, 860)

# Nsticker = [2, 2]  # [3, 3, 8, 9]
NB_STICKERS = 2
NB_WHEELS = 19
NB_HATS = 22
NB_TEAMS = 2

DELAY = 0.10

NB_PRIMARY_COLORS = 5
NB_SECONDARY_COLORS = 5

NB_HORIZONTAL_ROTATIONS = 3
NB_VERTICAL_ROTATIONS = 3


old_model = None
old_sticker = None
old_wheel = None
old_hat = None
old_primary_color = 0.5
old_secondary_color = 0.5
old_team = None


def tap(pos):
    call(["adb", "shell", "input", "tap", str(pos[0]), str(pos[1])])
    #    device.shell(f"input tap {pos[0]} {pos[1]}")


def motion(pos, type):
    call(["adb", "shell", "input", "motionevent", type, str(pos[0]), str(pos[1])])


def setColor(team: int, primary_color: float, secondary_color: float):

    global old_primary_color
    global old_secondary_color

    tap(COLOR_MENU_BTN)

    # set primary color, if necessary
    if primary_color != old_primary_color:
        motion((COLOR_MIN + old_primary_color * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "DOWN")
        motion((COLOR_MIN + primary_color * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "MOVE")
        motion((COLOR_MIN + primary_color * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "UP")

    # set secondary color, if necessary
    if secondary_color != old_secondary_color:
        motion((COLOR_MIN + old_secondary_color * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "DOWN")
        motion((COLOR_MIN + secondary_color * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "MOVE")
        motion((COLOR_MIN + secondary_color * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "UP")


def rotate(x, y):
    motion(CENTER, "DOWN")
    motion(np.array(CENTER) + np.array((x, y)), "MOVE")
    sleep(DELAY)
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


# def newCar(model: int, sticker: int, wheel: int, hat: int, team: int, primary_color: float, secondary_color: float):
def newCar(wheel: int, hat: int, team: int, primary_color: float, secondary_color: float):

    global old_model
    global old_sticker
    global old_wheel
    global old_hat
    global old_primary_color
    global old_secondary_color
    global old_team

    # goto garage menu
    sleep(DELAY)
    tap(GARAGE_BTN)

    # # select new model, if necessary
    # if model != old_model:
    #     nextModel(model)
    #     old_model = model
    #     sleep(DELAY)

    # goto loadout editor
    sleep(DELAY)
    tap(EDIT_LOADOUT_BTN)

    # # select sticker, if necessary
    # if sticker != old_sticker:
    #     selectItem(STICKER_MENU_BTN, sticker)
    #     old_sticker = sticker
    #     sleep(DELAY)

    # select wheel, if necessary
    if wheel != old_wheel:
        selectItem(WHEEL_MENU_BTN, wheel)
        old_wheel = wheel
        sleep(DELAY)

    # select hat, if necessary
    if hat != old_hat:
        selectItem(HAT_MENU_BTN, hat)
        old_hat = hat
        sleep(DELAY)

    # select color, if necessary
    if team != old_team or primary_color != old_primary_color or secondary_color != old_secondary_color:
        setColor(team, primary_color, secondary_color)
        old_team = team
        old_primary_color = primary_color
        old_secondary_color = secondary_color
        sleep(DELAY)

    # goto main menu
    sleep(DELAY)
    tap(BACK_BTN)
    sleep(DELAY)
    tap(BACK_BTN)


def generate_loadouts():
    primary_colors = np.linspace(0, 1, NB_PRIMARY_COLORS, endpoint=True)
    secondary_colors = np.linspace(0, 1, NB_SECONDARY_COLORS, endpoint=True)

    teams = range(NB_TEAMS)
    # stickers = range(NB_STICKERS)
    wheels = range(NB_WHEELS)
    hats = range(NB_HATS)

    loadouts = itertools.product(wheels, hats, teams, primary_colors, secondary_colors)
    nb_loadouts = NB_WHEELS * NB_HATS * NB_PRIMARY_COLORS * NB_SECONDARY_COLORS * NB_TEAMS

    logging.debug(f"number of loadouts: {nb_loadouts}")

    return loadouts
