import subprocess

import numpy as np
import PIL
import ppadb.client
import ppadb.command.serial
import ppadb.device
import tensorflow
from keras import models

import utils

RESIZED_SIZE = (100, 50, 3)
LABELS = ['octane', 'werewolf', 'breakout', 'aftershock']

# Load model
model = models.load_model('../models/model')

utils.startup(need_focus=False)

running = True

while running:
    utils.screenshot(filename='live', folder='../models')
    
    # Lecture de l'image
    img = PIL.Image.open('../models/live')

    # print(f"img.size = {img.size}")

    # Redimensionnement de l'image
    img = img.resize(RESIZED_SIZE[:-1], PIL.Image.ANTIALIAS)

    # print(f"img.size = {img.size}")

    X = np.asarray(img)

    Y = model.evaluate(X)
    
    print(f"Model detected : {LABELS[Y]}")
