import joblib
import os
import logging
from src.config import MODEL_PATH

logger = logging.getLogger(__name__)

def load_model():
    """Loads the trained pipeline."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}.")
    return joblib.load(MODEL_PATH)

def predict_on_time(model, X):
    """Returns probability array."""
    # Returns [Prob_Class_0, Prob_Class_1] -> [Prob_Late, Prob_OnTime]
    return model.predict_proba(X)