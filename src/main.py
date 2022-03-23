import logging
from time import sleep

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

    device = connect_adb()
    users = get_users(device)
    users = detect_game(device, users)
    start_game(device, users)
    set_notifications(device, False)

    database = connect_to_database("dataset.db")

    loadouts = generate_loadouts()
    NB_ROTATIONS = 3

    while detect_focus(device):
        for (i, loadout) in enumerate(loadouts):
            ((model, sticker), wheel, hat, team, primary_color, secondary_color) = loadout

            logging.debug(f"loadout {i}: {(wheel, hat, team, primary_color, secondary_color)}")
            newCar(model, sticker, wheel, hat, team, primary_color, secondary_color)

            sleep(0.5)
            for x_rotation in range(NB_ROTATIONS):
                rotate(130, 0)
                uuid = take_screenshot(device)
                insert_into_database(database, uuid, loadout, x_rotation, 0)

    set_notifications(device, True)

    database.close()
