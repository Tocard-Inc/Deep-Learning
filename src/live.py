import subprocess
import time

import numpy as np
import PIL
import ppadb.client
import ppadb.command.serial
import ppadb.device
import tensorflow
from keras import models

import utils

RESIZED_SIZE = (100, 50, 3)
LABELS = ["octane", "werewolf", "breakout", "aftershock"]

MODELS_PATH = "models"
MODEL_FILENAME = "rot_25e"

# Load model
model = models.load_model(MODELS_PATH + "/" + MODEL_FILENAME)

utils.startup(need_focus=False)

running = True

X = np.zeros((1, RESIZED_SIZE[1], RESIZED_SIZE[0], RESIZED_SIZE[2]))

while running:
    utils.screenshot(filename="live", folder=MODELS_PATH)

    time.sleep(1)

    # Lecture de l'image
    img = PIL.Image.open(MODELS_PATH + "/live.jpg")

    # Redimensionnement de l'image
    img = img.resize(RESIZED_SIZE[:-1], PIL.Image.ANTIALIAS)

    X[0] = np.asarray(img)

    Y = model.predict(X)

    index = int(np.dot(Y, np.array([0, 1, 2, 3]).T))

    print()
    print()
    print(f"Model detected : {LABELS[index]}")
    for i in range(len(LABELS)):
        print(f"\t- {LABELS[i]} {Y[0,i]:.03f}")
