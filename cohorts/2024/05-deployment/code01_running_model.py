import pickle

import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer


def open_pickle(model_file):
    model = None
    with open(model_file, 'rb') as f_in:
        model = pickle.load(f_in)
    return model


MODEL_FILEPATH = "homework/model1.bin"
DV_FILEPATH = "homework/dv.bin"


model1 = open_pickle(MODEL_FILEPATH)
dv = open_pickle(DV_FILEPATH)


X = {"job": "management", "duration": 400, "poutcome": "success"}

X_transformed = dv.transform(X)
y_predict = model1.predict_proba(X_transformed)

print(y_predict[0, 1])

