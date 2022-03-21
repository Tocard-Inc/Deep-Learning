import logging
from time import sleep

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
    NB_ROTATIONS = 20

    while detect_focus(device):
        for (i, (wheel, hat, team, primary_color, secondary_color)) in enumerate(loadouts):
            logging.debug(f"loadout {i}: {(wheel, hat, team, primary_color, secondary_color)}")
            newCar(wheel, hat, team, primary_color, secondary_color)

            sleep(0.5)
            for _ in range(NB_ROTATIONS):
                rotate(130, 0)

    set_notifications(device, True)
