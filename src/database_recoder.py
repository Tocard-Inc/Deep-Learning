import itertools
import logging
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
TEAM_OFFSET = 250  # pourquoi faire ?
PRIMARY_COLOR_SLIDER = (290, 290 + TEAM_OFFSET)
SECONDARY_COLOR_SLIDER = (380, 380 + TEAM_OFFSET)

ITEM_X = (200, 450, 700)
ITEM_Y = (300, 580, 860)

NB_STICKERS = [2, 2]
NB_WHEELS = 2
NB_HATS = 2
NB_TEAMS = 2

DELAY = 0.15

NB_PRIMARY_COLORS = 2
NB_SECONDARY_COLORS = 2

NB_HORIZONTAL_ROTATIONS = 3
NB_VERTICAL_ROTATIONS = 3


old_model = None
old_sticker = None
old_wheel = None
old_hat = None
old_primary_color = [None, None]
old_secondary_color = [None, None]
old_team = None


def tap(pos):
    call(["adb", "shell", "input", "tap", str(pos[0]), str(pos[1])])
    #    device.shell(f"input tap {pos[0]} {pos[1]}")


def motion(pos, type):
    call(["adb", "shell", "input", "motionevent", type, str(pos[0]), str(pos[1])])


def selectColor(team: int, primary_color: float, secondary_color: float):

    global old_team
    global old_primary_color
    global old_secondary_color

    tap(COLOR_MENU_BTN)

    # set primary color, if necessary
    if primary_color != old_primary_color[team] or old_team != team:
        motion((COLOR_MIN + 0.5 * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "DOWN")
        motion((COLOR_MIN + primary_color * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "MOVE")
        motion((COLOR_MIN + primary_color * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "UP")

    # set secondary color, if necessary
    if secondary_color != old_secondary_color[team] or old_team != team:
        motion((COLOR_MIN + 0.5 * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "DOWN")
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
        slide = ITEM_Y[0] - ITEM_Y[1]

        motion((ITEM_X[1], ITEM_Y[2]), "DOWN")
        motion((ITEM_X[1], ITEM_Y[1]), "MOVE")
        motion((ITEM_X[1], ITEM_Y[1] + nslide * slide), "MOVE")
        motion((ITEM_X[1], ITEM_Y[1] + nslide * slide), "UP")

        row -= nslide

    tap((ITEM_X[col], ITEM_Y[row]))


def selectModel(model: int):

    global old_model

    if old_model == None:
        global NB_STICKERS

        # go to first model
        for _ in range(len(NB_STICKERS)):
            motion(CENTER, "DOWN")
            motion(np.array(CENTER) + np.array((1000, 0)), "MOVE")
            motion(np.array(CENTER) + np.array((1000, 0)), "UP")
            sleep(1)
        tap(SELECT_CAR_BTN)

        old_model = 0

    n = model - old_model

    if n > 0:
        motion(CENTER, "DOWN")
        motion(np.array(CENTER) + n * np.array((-1700, 0)), "MOVE")
        motion(np.array(CENTER) + n * np.array((-1700, 0)), "UP")
        tap(SELECT_CAR_BTN)
    elif n < 0:
        # because backward is fucked up...
        for _ in range(-n):
            motion(CENTER, "DOWN")
            motion(np.array(CENTER) + np.array((1000, 0)), "MOVE")
            motion(np.array(CENTER) + np.array((1000, 0)), "UP")
            sleep(1)
        tap(SELECT_CAR_BTN)


def newCar(model: int, sticker: int, wheel: int, hat: int, team: int, primary_color: float, secondary_color: float):

    global old_model
    global old_sticker
    global old_wheel
    global old_hat
    global old_primary_color
    global old_secondary_color
    global old_team

    sleep(0.5)

    # goto garage menu
    tap(GARAGE_BTN)
    sleep(DELAY)

    # select new model, if necessary
    if model != old_model:
        selectModel(model)
        old_model = model
        sleep(DELAY)

    # goto loadout editor
    tap(EDIT_LOADOUT_BTN)
    sleep(DELAY)

    # select sticker, if necessary
    if sticker != old_sticker:
        selectItem(STICKER_MENU_BTN, sticker)
        old_sticker = sticker
        sleep(DELAY)

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
    if team != old_team or primary_color != old_primary_color[team] or secondary_color != old_secondary_color[team]:
        selectColor(team, primary_color, secondary_color)
        old_team = team
        old_primary_color[old_team] = primary_color
        old_secondary_color[old_team] = secondary_color
        sleep(DELAY)

    # goto main menu
    tap(BACK_BTN)
    sleep(DELAY)
    tap(BACK_BTN)
    sleep(DELAY)


def generate_loadouts():
    primary_colors = np.linspace(0, 1, NB_PRIMARY_COLORS, endpoint=True)  # pourquoi le endpoint ? (c'est par defaut)
    secondary_colors = np.linspace(0, 1, NB_SECONDARY_COLORS, endpoint=True)

    teams = range(NB_TEAMS)

    # create models and stickers list (as the number of stickers is related to the model)
    models_stickers = []
    for model, n_sticker in enumerate(NB_STICKERS):

        def assemblage(n):
            return model, n

        models_stickers += map(assemblage, range(n_sticker))

    wheels = range(NB_WHEELS)
    hats = range(NB_HATS)

    # create the loadouts iterator
    loadouts = itertools.product(models_stickers, wheels, hats, teams, primary_colors, secondary_colors)
    nb_loadouts = sum(NB_STICKERS) * NB_WHEELS * NB_HATS * NB_PRIMARY_COLORS * NB_SECONDARY_COLORS * NB_TEAMS

    logging.debug(f"number of loadouts: {nb_loadouts}")

    return loadouts


def generate_rotations():
    vertical_rotations = range(NB_VERTICAL_ROTATIONS)
    horizontal_rotations = range(NB_HORIZONTAL_ROTATIONS)

    rotations = itertools.product(vertical_rotations, horizontal_rotations)
    nb_rotations = NB_HORIZONTAL_ROTATIONS * NB_VERTICAL_ROTATIONS

    logging.debug(f"number of rotations: {nb_rotations}")

    return rotations


loadouts = generate_loadouts()
for ((model, sticker), wheel, hat, team, primary_color, secondary_color) in loadouts:
    print(f"next loadout: {((model, sticker), wheel, hat, team, primary_color, secondary_color)}")
    newCar(model, sticker, wheel, hat, team, primary_color, secondary_color)
