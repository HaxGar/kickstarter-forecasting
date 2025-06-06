# pip install google-cloud-storage

import glob
import os
import time
import pickle

from sklearn.naive_bayes import MultinomialNB
# from tensorflow import keras
from google.cloud import storage

from kickstarter_predictor.params import *

def save_full_registry(model, model_type: str, params: dict = None, metrics: dict = None) -> None:
    assert model is not None, "No model provided"

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{model_type}.pkl"
    registry_path = os.path.join(PROJECT_ROOT, "models", filename)
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)

    registry_dict = {
        "model": model,
        "model_type": model_type,
        "params": params,
        "metrics": metrics
    }

    with open(registry_path, "wb") as file:
        pickle.dump(registry_dict, file)

    print("✅ Full registry (model, model_type, params, metrics) saved locally")
    return registry_path


def load_model(model_name : str = None):
    """
    Return a dictionnary with the followig keys :
    model, model_type, params, metrics
    """

    model = None

    registry_dir = os.path.join(PROJECT_ROOT, "models")
    registry_files = sorted(
        [f for f in os.listdir(registry_dir) if f.endswith(".pkl")]
    )

    if model_name is None:
        latest_path = os.path.join(registry_dir, registry_files[-1])
        with open(latest_path, "rb") as file:
            model = pickle.load(file)

    else :
        model_path = os.path.join(registry_dir, model_name)
        with open (model_path, "rb") as file:
            model = pickle.load(file)

    assert "model" in model.keys()
    assert "model_type" in model.keys()
    assert "params" in model.keys()
    assert "metrics" in model.keys()

    return model
