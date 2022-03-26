import logging
import re
import sqlite3
import subprocess
import time
import uuid

import ppadb.client
import ppadb.command.serial
import ppadb.device

REGEX_USER: re.Pattern = re.compile(r"UserInfo\{([0-9]*):([a-zA-Z ]*):.*")
REGEX_FOCUS: re.Pattern = re.compile(r"mCurrentFocus.*com.Psyonix.RL2D.*")

PSYONIX_PACKAGE_NAME: str = "com.Psyonix.RL2D"
PSYONIX_ACTIVITY_NAME: str = "com.epicgames.ue4.SplashActivity"

ADB_HOST: str = "127.0.0.1"
ADB_PORT: int = 5037

DELAY_DETECT: int = 1

DATA_FOLDER = "data/"

UserList = list[tuple[int, str]]


def tap(pos):
    device.shell(f"input tap {pos[0]} {pos[1]}")


def motion(pos, type):
    device.shell(f"input motionevent {type} {pos[0]} {pos[1]}")


def connect_adb() -> ppadb.device.Device:
    client: ppadb.client.Client = ppadb.client.Client(host=ADB_HOST, port=ADB_PORT)
    devices: list[ppadb.device.Device] = client.devices()

    devices_names: list[ppadb.command.serial.Serial] = list(map(lambda d: d.serial, devices))
    logging.debug(f"detected devices: {devices_names}")

    global device
    if len(devices) == 1:
        device = devices[0]
    elif len(devices) == 0:
        print("No device connected")
        exit(1)
    else:
        print("Select a device :")
        raise NotImplementedError  # TODO

    logging.debug(f"selected device: {device.serial}")

    return device


def get_users(device: ppadb.device.Device) -> UserList:
    device_users: str = device.shell("pm list users")
    users: UserList = REGEX_USER.findall(device_users)

    logging.debug(f"detected users: {users}")

    return users


def detect_game(device: ppadb.device.Device, users: UserList) -> UserList:
    playable_users: UserList = list()
    for (id, name) in users:
        if "package:" in device.shell(f"pm path --user {id} {PSYONIX_PACKAGE_NAME}"):
            playable_users.append((id, name))

    logging.debug(f"playable users: {playable_users}")

    return playable_users


def start_game(device: ppadb.device.Device, users: UserList) -> None:
    if len(users) == 1:
        (user_id, user_name) = users[0]
    elif len(users) == 0:
        print("No Playable users detected")
        exit(1)
    else:
        print("Select a user to game with :")
        raise NotImplementedError  # TODO

    logging.debug(f"selected user: {user_name}")

    device.shell(f"am start --user {user_id} -n {PSYONIX_PACKAGE_NAME}/{PSYONIX_ACTIVITY_NAME}")
    logging.debug("game activity started")


def detect_zen_mode(device: ppadb.device.Device) -> bool:
    return device.shell("settings get global zen_mode") != "1\n"


def detect_focus(device: ppadb.device.Device) -> bool:
    activity_dump = device.shell("dumpsys activity activities")
    result = REGEX_FOCUS.search(activity_dump)

    return result is not None


def start_scrpy() -> None:
    subprocess.Popen(
        "scrcpy --crop=700:1830:160:200 --v4l2-sink=/dev/video2 --disable-screensaver -N -m 250".split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def startup() -> None:
    device = connect_adb()
    users = get_users(device)
    users = detect_game(device, users)
    start_game(device, users)

    while not (detect_zen_mode(device) or detect_focus(device)):
        time.sleep(DELAY_DETECT)

    time.sleep(DELAY_DETECT)

    start_scrpy()


def screenshot() -> uuid.UUID:
    filename = uuid.uuid1()

    subprocess.Popen(
        f"ffmpeg -f video4linux2 -i /dev/video2 -frames:v 1 {DATA_FOLDER}/{filename}.jpg".split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    return filename


def insert(database: sqlite3.Connection, uuid: uuid.UUID, loadout: tuple, x_rotation: int, y_rotation: int) -> None:
    ((model, sticker), wheel, hat, team, primary_color, secondary_color) = loadout
    database.execute(
        f"INSERT INTO data VALUES ('{uuid}',{model},{team},{primary_color},{secondary_color},{hat},{sticker},{wheel},{x_rotation},{y_rotation})"
    )
    database.commit()
