import os
import time

import matplotlib.pyplot as plt
import numpy as np
import PIL
import ppadb.command.serial
import ppadb.device
import tensorflow as tf
from keras import models

import utils


def make_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(last_conv_layer_name).output, model.output])

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

    return heatmap.numpy()


def make_gradcam(img, heatmap, alpha=0.5):
    # convert img to float32 to support alpha blending
    img = tf.image.convert_image_dtype(img, dtype=tf.float32)

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = plt.get_cmap("jet")

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = tf.keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = tf.keras.preprocessing.image.img_to_array(jet_heatmap)
    jet_heatmap = jet_heatmap / 255

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + img * (1 - alpha)
    superimposed_img = tf.keras.preprocessing.image.array_to_img(superimposed_img)

    # Display Grad CAM
    return superimposed_img


RESIZED_SIZE = (100, 50, 3)
LABELS = ["octane", "werewolf", "breakout", "aftershock"]

MODELS_PATH = "models"
MODEL_FILENAME = "full_aug_5e"

last_conv_layer_name = "C2D_last"

# Load model
model = models.load_model(MODELS_PATH + "/" + MODEL_FILENAME)

utils.startup(need_focus=False)
utils.screenshot(filename="live", folder=MODELS_PATH)

# Attendre que la première image soit créée
time.sleep(10)

running = True

X = np.zeros((1, RESIZED_SIZE[1], RESIZED_SIZE[0], RESIZED_SIZE[2]))

plt.ion()
plt.show()

while running:

    utils.screenshot(filename="live", folder=MODELS_PATH)

    # Lecture de l'image
    img = PIL.Image.open(MODELS_PATH + "/live.jpg")

    # Redimensionnement de l'image
    img = img.resize(RESIZED_SIZE[:-1], PIL.Image.ANTIALIAS)

    X[0] = np.asarray(img)

    preds = model.predict(X)
    index = np.argmax(preds)

    os.system("clear")
    print(f"Model detected : {LABELS[index]}")
    for i in range(len(LABELS)):
        print(f"\t- {LABELS[i]} {preds[0,i]:.03f}")

    plt.subplot(1, 5, 1)
    plt.imshow(img)
    plt.title(f"prediction: {LABELS[index]}")

    for i in range(4):
        # generate class activation heatmap
        heatmap = make_heatmap(X, model, last_conv_layer_name, pred_index=i)
        # generate gradmap
        gradcam = make_gradcam(img, heatmap)

        plt.subplot(1, 5, i + 2)
        plt.imshow(gradcam)
        plt.title(f"{LABELS[i]} ({preds[0][i]:.4f})")

    plt.tight_layout()
    plt.draw()
    plt.pause(0.001)
