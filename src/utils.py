import logging
import re
import subprocess
import time

import ppadb.client
import ppadb.command.serial
import ppadb.device

REGEX_USER: re.Pattern = re.compile(r"UserInfo\{([0-9]*):([a-zA-Z ]*):.*")
REGEX_FOCUS: re.Pattern = re.compile(r"mCurrentFocus.*com.Psyonix.RL2D.*")

PSYONIX_PACKAGE_NAME: str = "com.Psyonix.RL2D"
PSYONIX_ACTIVITY_NAME: str = "com.epicgames.ue4.SplashActivity"

ADB_HOST: str = "127.0.0.1"
ADB_PORT: int = 5037

DETECT_DELAY: int = 1

UserList = list[tuple[int, str]]


def connect_adb() -> ppadb.device.Device:
    client: ppadb.client.Client = ppadb.client.Client(host=ADB_HOST, port=ADB_PORT)
    devices: list[ppadb.device.Device] = client.devices()

    devices_names: list[ppadb.command.serial.Serial] = list(map(lambda d: d.serial, devices))
    logging.debug(f"detected devices: {devices_names}")

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

    logging.debug("game activity started")
    device.shell(f"am start --user {user_id} -n {PSYONIX_PACKAGE_NAME}/{PSYONIX_ACTIVITY_NAME}")
    logging.debug("game activity started")


def set_notifications(device: ppadb.device.Device, enabled: bool) -> None:
    device.shell(f"settings put global heads_up_notifications_enabled {int(enabled)}")

    if enabled:
        logging.debug("enabled heads up notifications")
    else:
        logging.debug("disabled heads up notifications")


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
    set_notifications(device, False)

    while not (detect_zen_mode(device) and detect_focus(device)):
        time.sleep(DETECT_DELAY)

    time.sleep(DETECT_DELAY)

    start_scrpy()
