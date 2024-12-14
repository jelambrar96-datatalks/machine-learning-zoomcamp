#!/usr/bin/env python
# coding: utf-8

from io import BytesIO
from urllib import request

import numpy as np

from PIL import Image
import tflite_runtime.interpreter as tflite


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_input(X):
    temp_array = np.array(X, dtype=np.float32)
    temp_array = (temp_array / 255.0 * 2) - 1
    return temp_array


interpreter = tflite.Interpreter(model_path='bees-wasps-v2.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


classes = [
    'dress',
    'hat',
    'longsleeve',
    'outwear',
    'pants',
    'shirt',
    'shoes',
    'shorts',
    'skirt',
    't-shirt'
]

# url = 'http://bit.ly/mlbookcamp-pants'

def predict(url):

    img = download_image(url)
    img = np.array(prepare_image(img, (150, 150)))

    x = img.reshape((1, *img.shape))
    x = preprocess_input(x)

    interpreter.set_tensor(input_index, x)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    return preds.tolist()


def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result
