import logging
from time import sleep

import init
from database import connect_to_database, insert_into_database, take_screenshot
from garage import generate_loadouts, newCar, rotate
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

logging.getLogger("PIL.PngImagePlugin").setLevel(logging.ERROR)

if __name__ == "__main__":

    connect_adb()
    users = get_users(init.device)
    users = detect_game(init.device, users)
    start_game(init.device, users)
    set_notifications(init.device, False)

    database = connect_to_database("dataset.db")

    loadouts = generate_loadouts()
    NB_ROTATIONS = 1
    N_START = 9984
    N_STOP = 1e10
    
    for (i, loadout) in enumerate(loadouts):
        # Sauter les N premiers
        if i < N_START:
            continue

        if i >= N_STOP:
            exit(0)

        ((model, sticker), wheel, hat, team, primary_color, secondary_color) = loadout

        logging.debug(f"loadout {i}: {((model, sticker), wheel, hat, team, primary_color, secondary_color)}")
        newCar(model, sticker, wheel, hat, team, primary_color, secondary_color)

        sleep(0.5)
        for x_rotation in range(NB_ROTATIONS):
            uuid = take_screenshot(init.device)
            insert_into_database(database, uuid, loadout, x_rotation, 0)
            rotate(130, 0)

    set_notifications(init.device, True)

    database.close()
