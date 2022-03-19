import logging
import re
from time import sleep

from ppadb.client import Client as AdbClient

REGEX_USER = re.compile(r"UserInfo\{([0-9]*):([a-zA-Z ]*):.*")
REGEX_FOCUS = re.compile(r"mFocused.*com.Psyonix.RL2D.*")

PSYONIX_PACKAGE_NAME = "com.Psyonix.RL2D"
PSYONIX_ACTIVITY_NAME = "com.epicgames.ue4.SplashActivity"

ADB_HOST = "127.0.0.1"
ADB_PORT = 5037

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)-8s  %(message)s",
    datefmt="(%F %T)",
)


def connect_adb():
    client = AdbClient(host=ADB_HOST, port=ADB_PORT)
    devices = client.devices()
    devices_names = list(map(lambda d: d.serial, devices))

    logging.debug(f"devices detected: {devices_names}")

    if len(devices) == 1:
        device = devices[0]
    elif len(devices) == 0:
        print("No device connected")
        exit(1)
    else:
        print("Select a device :")
        # TODO

    logging.debug(f"device selected: {device.serial}")

    return device


def get_users(device):
    device_users = device.shell("pm list users")
    users = REGEX_USER.findall(device_users)

    logging.debug(f"users detected: {users}")
    return users


def detect_game(device, users):
    users = [
        (id, name) for (id, name) in users if "package:" in device.shell(f"pm path --user {id} {PSYONIX_PACKAGE_NAME}")
    ]

    logging.debug(f"playable users: {users}")
    return users


def start_game(device, users):
    if len(users) == 1:
        (user_id, user_name) = users[0]
    elif len(users) == 0:
        print("No Playable users detected")
        exit(1)
    else:
        print("Select a user to game with :")
        # TODO

    logging.debug(f"user selected: {user_name}")
    device.shell(f"am start --user {user_id} -n {PSYONIX_PACKAGE_NAME}/{PSYONIX_ACTIVITY_NAME}")
    logging.debug("game activity started")


def set_notifications(device, enabled: bool):
    device.shell(f"settings put global heads_up_notifications_enabled {int(enabled)}")

    if enabled:
        logging.debug("enabled heads up notificaiton")
    else:
        logging.debug("disabled heads up notificaiton")


def detect_focus(device) -> bool:
    activity_dump = device.shell("dumpsys activity activities")
    result = REGEX_FOCUS.search(activity_dump)
    return result is not None


if __name__ == "__main__":

    device = connect_adb()

    users = get_users(device)

    users = detect_game(device, users)

    start_game(device, users)

    set_notifications(device, False)

    while detect_focus(device):
        sleep(1)

    set_notifications(device, True)
