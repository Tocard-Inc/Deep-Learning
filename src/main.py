import datetime
import logging
import sqlite3
import time

import garage
import utils

NB_ETA = 25

NB_ROTATIONS = 10

N_START = 0
N_STOP = 0

DELAY_TRANSITION = 0.3

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
    datefmt="(%F %T)",
)

logging.getLogger("PIL.PngImagePlugin").setLevel(logging.ERROR)

if __name__ == "__main__":

    # mise en place de l'environnement de travail
    utils.startup()

    # connection à la base de données sqlite3
    db = sqlite3.connect("dataset.db")

    # génération des configurations des voitures
    loadouts, nb_loadouts = garage.generate_loadouts()
    digits_loadout = len(str(nb_loadouts))

    # initialisation de la liste au calcul de l'ETA
    eta_list = [10.0 for _ in range(NB_ETA)]

    # boucle principale sur les loadouts
    for (i, loadout) in enumerate(loadouts):

        # Sauter les N_START premiers
        if N_START and i <= N_START:
            continue

        # Skip après N_STOP loadouts
        if N_STOP and i >= N_STOP:
            break

        # tic
        elapsed = time.time()

        # unpacking du loadout
        (wheel, (model, sticker), hat, team, primary_color, secondary_color) = loadout

        # modification de la voiture dans le garage
        garage.newCar(model, sticker, wheel, hat, team, primary_color, secondary_color)

        # transition du garage au menu principale
        time.sleep(DELAY_TRANSITION)

        # boucle des rotations
        for x_rotation in range(NB_ROTATIONS):
            uuid = utils.screenshot()
            utils.insert(db, uuid, loadout, x_rotation, 0)
            garage.rotate(265, 0)

        # tac
        elapsed = time.time() - elapsed
        eta_list[i % NB_ETA] = elapsed
        estimation = int((nb_loadouts - i) * sum(eta_list) / NB_ETA)
        formated_estimation = datetime.timedelta(seconds=estimation)
        percentage_done = i / nb_loadouts * 100

        logging.debug(
            f"loadout {str(i).zfill(digits_loadout)}/{nb_loadouts} ({percentage_done:02.02f}%) ({elapsed:.02f}s, ETA: {formated_estimation}): {loadout}"
        )

    # fermeture de la db sqlite3
    db.close()
