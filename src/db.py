import sqlite3
import uuid
from fileinput import filename

DATA_FOLDER = "data/"

con = sqlite3.connect("dataset.db")

from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)
device = client.device("13231FDD4003UE")

filename = uuid.uuid1()
result = device.screencap()
with open(f"{DATA_FOLDER}/{filename}.png", "wb") as fp:
    fp.write(result)
    con.execute(f"INSERT INTO data VALUES ('{filename}',{0},{0},{0.5},{0.5},{0},{0},{0},{0},{0})")
    con.commit()

con.close()
