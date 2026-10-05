"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.

import os
import pandas as pd
import joblib


DEFAULT_MODEL_PATH = "../model/wine_quality_classifier.joblib"


def load_wine_quality_model(path):
    return joblib.load(path)

def infer_wine_quality(X, model=None):
    if model is None:
        model = load_wine_quality_model()

    return model.predict(X)
    