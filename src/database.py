import io
import sqlite3
import uuid

from PIL import Image, ImageOps

DATA_FOLDER = "data/"

con = sqlite3.connect("dataset.db")

from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)
device = client.device("13231FDD4003UE")

filename = uuid.uuid1()
result = device.screencap()

image = Image.open(io.BytesIO(result))
image = image.crop((0, 160, 2200, 860))
image = image.resize((150, 150), Image.ANTIALIAS)

image.save("data/test.png")
image.rotate(90).save("data/test90.png")
image.rotate(180).save("data/test180.png")
image.rotate(-90).save("data/test-90.png")
ImageOps.mirror(image).save("data/testmirror.png")

con.execute(f"INSERT INTO data VALUES ('{filename}',{0},{0},{0.5},{0.5},{0},{0},{0},{0},{0})")
con.commit()

con.close()
