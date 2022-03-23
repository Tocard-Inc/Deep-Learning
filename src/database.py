import io
import logging
import sqlite3
import uuid

from PIL import Image

DATA_FOLDER = "data/"


def take_screenshot(device):
    result = device.screencap()
    logging.debug("screenshot taken")
    image = Image.open(io.BytesIO(result))
    image = image.crop((0, 160, 2200, 860))
    image.thumbnail((150, 150))
    logging.debug("screenshot converted")
    # image = image.resize((150, 150), Image.ANTIALIAS)

    filename = uuid.uuid1()
    image.save(f"{DATA_FOLDER}/{filename}.png")
    logging.debug("screenshot saved")

    return filename


def connect_to_database(filename):
    return sqlite3.connect(filename)


def insert_into_database(database, uuid, loadout, x_rotation, y_rotation):
    ((model, sticker), wheel, hat, team, primary_color, secondary_color) = loadout
    database.execute(
        f"INSERT INTO data VALUES ('{uuid}',{model},{team},{primary_color},{secondary_color},{hat},{sticker},{wheel},{x_rotation},{y_rotation})"
    )
    database.commit()
