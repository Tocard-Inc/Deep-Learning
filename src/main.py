import logging
from time import sleep
from tkinter import VERTICAL

from garage import generate_loadouts, generate_rotations, newCar, rotate
from init import (
    connect_adb,
    detect_focus,
    detect_game,
    get_users,
    set_notifications,
    start_game,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
    datefmt="(%F %T)",
)

if __name__ == "__main__":

    device = connect_adb()

    users = get_users(device)
    users = detect_game(device, users)
    start_game(device, users)
    set_notifications(device, False)

    loadouts = generate_loadouts()
    rotations = generate_rotations()

    while detect_focus(device):
        for (wheel, hat, team, primary_color, secondary_color) in loadouts:
            logging.debug(f"next loadout: {(wheel, hat, team, primary_color, secondary_color)}")
            newCar(wheel, hat, team, primary_color, secondary_color)

            # for (horizontal_rotation, vertical_rotation) in rotations:
            #     rotate(horizontal_rotation, vertical_rotation)

    set_notifications(device, True)
