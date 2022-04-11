import itertools
import logging
import time

import numpy as np

from utils import motion, startup, tap

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

ITEM_X = (200, 450, 700)
ITEM_Y = (300, 580, 860)

NB_STICKERS = (0, 0, 2, 4)
NB_WHEELS = 23
NB_HATS = 23
NB_TEAMS = 2

DELAY = 0.1

NB_PRIMARY_COLORS = 3
NB_SECONDARY_COLORS = 1

old_model = None
old_sticker = None
old_wheel = None
old_hat = None
old_primary_color = [None, None]
old_secondary_color = [None, None]
old_team = None


def selectColor(team: int, primary_color: float, secondary_color: float):

    global old_team
    global old_primary_color
    global old_secondary_color

    tap(COLOR_MENU_BTN)

    # set primary color, if necessary
    if primary_color != old_primary_color[team] or old_team != team:
        if old_primary_color[team] is None:
            motion((COLOR_MIN + 0.5 * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "DOWN")
            motion((COLOR_MIN + 0.1 * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "MOVE")
        else:
            motion((COLOR_MIN + old_primary_color[team] * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "DOWN")
        motion((COLOR_MIN + primary_color * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "MOVE")
        motion((COLOR_MIN + primary_color * COLOR_DIST, PRIMARY_COLOR_SLIDER[team]), "UP")

    # set secondary color, if necessary
    if secondary_color != old_secondary_color[team] or old_team != team:
        if old_primary_color[team] == None:
            motion((COLOR_MIN + 0.5 * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "DOWN")
            motion((COLOR_MIN + 0.1 * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "MOVE")
        else:
            motion((COLOR_MIN + old_secondary_color[team] * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "DOWN")
        motion((COLOR_MIN + secondary_color * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "MOVE")
        motion((COLOR_MIN + secondary_color * COLOR_DIST, SECONDARY_COLOR_SLIDER[team]), "UP")


def rotate(x, y):
    motion(CENTER, "DOWN")
    motion(np.array(CENTER) + np.array((x, y)), "MOVE")
    time.sleep(DELAY)
    motion(np.array(CENTER) + np.array((x, y)), "UP")


def selectItem(kind, i):
    tap(kind)
    time.sleep(DELAY)

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
        for _ in range(len(NB_STICKERS) - 1):
            motion(CENTER, "DOWN")
            motion(np.array(CENTER) + np.array((1000, 0)), "MOVE")
            motion(np.array(CENTER) + np.array((1000, 0)), "UP")
            time.sleep(1)
        tap(SELECT_CAR_BTN)

        old_model = 0

    n = model - old_model

    if n > 0:
        motion(CENTER, "DOWN")
        motion(np.array(CENTER) + n * np.array((-1700, 0)), "MOVE")
        time.sleep(DELAY)
        motion(np.array(CENTER) + n * np.array((-1700, 0)), "UP")
        tap(SELECT_CAR_BTN)
    elif n < 0:
        # because backward is fucked up...
        for _ in range(-n):
            motion(CENTER, "DOWN")
            motion(np.array(CENTER) + np.array((1000, 0)), "MOVE")
            time.sleep(DELAY)
            motion(np.array(CENTER) + np.array((1000, 0)), "UP")
            time.sleep(1)
        tap(SELECT_CAR_BTN)


def newCar(model: int, sticker: int, wheel: int, hat: int, team: int, primary_color: float, secondary_color: float):

    global old_model
    global old_sticker
    global old_wheel
    global old_hat
    global old_primary_color
    global old_secondary_color
    global old_team

    # goto garage menu
    tap(GARAGE_BTN)
    time.sleep(DELAY)

    # select new model, if necessary
    if model != old_model:
        selectModel(model)
        time.sleep(DELAY)

    # goto loadout editor
    tap(EDIT_LOADOUT_BTN)
    time.sleep(DELAY)

    # select sticker, if necessary
    if sticker != old_sticker or model != old_model:
        selectItem(STICKER_MENU_BTN, sticker)
        time.sleep(DELAY)

    # select wheel, if necessary
    if wheel != old_wheel or model != old_model:
        selectItem(WHEEL_MENU_BTN, wheel)
        time.sleep(DELAY)

    # select hat, if necessary
    if hat != old_hat or model != old_model:
        selectItem(HAT_MENU_BTN, hat)
        time.sleep(DELAY)

    # select color, if necessary
    if (
        team != old_team
        or primary_color != old_primary_color[team]
        or secondary_color != old_secondary_color[team]
        or model != old_model
    ):
        selectColor(team, primary_color, secondary_color)
        time.sleep(DELAY)

    # update old values
    old_model = model
    old_sticker = sticker
    old_wheel = wheel
    old_hat = hat
    old_team = team
    old_primary_color[old_team] = primary_color
    old_secondary_color[old_team] = secondary_color

    # goto main menu
    tap(BACK_BTN)
    time.sleep(DELAY)
    tap(BACK_BTN)
    time.sleep(DELAY)
    tap(BACK_BTN)
    tap(BACK_BTN)


def generate_loadouts():
    primary_colors = np.linspace(0, 1, NB_PRIMARY_COLORS)
    secondary_colors = np.linspace(0, 1, NB_SECONDARY_COLORS)

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
    loadouts = itertools.product(wheels, models_stickers, hats, teams, primary_colors, secondary_colors)
    nb_loadouts = sum(NB_STICKERS) * NB_WHEELS * NB_HATS * NB_PRIMARY_COLORS * NB_SECONDARY_COLORS * NB_TEAMS

    logging.debug(f"number of loadouts: {nb_loadouts}")

    return loadouts, nb_loadouts


if __name__ == "__main__":

    startup()
    loadouts, _ = generate_loadouts()
    for (wheel, (model, sticker), hat, team, primary_color, secondary_color) in loadouts:
        print(f"next loadout: {(wheel, (model, sticker), hat, team, primary_color, secondary_color)}")
        newCar(model, sticker, wheel, hat, team, primary_color, secondary_color)
