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

MODELS_PATH = '../models'
MODEL_FILENAME = 'rot_25e'

# Load model
model = models.load_model(MODELS_PATH + '/' + MODEL_FILENAME)

utils.startup(need_focus=False)

running = True

while running:
    utils.screenshot(filename='live', folder=MODELS_PATH)
    
    # Lecture de l'image
    img = PIL.Image.open(MODELS_PATH + '/live')

    # Redimensionnement de l'image
    img = img.resize(RESIZED_SIZE[:-1], PIL.Image.ANTIALIAS)

    X = np.asarray(img)

    Y = model.evaluate(X)
    
    print(f"Model detected : {LABELS[Y]}")
