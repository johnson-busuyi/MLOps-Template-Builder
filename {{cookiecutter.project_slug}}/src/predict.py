
from pathlib import Path

import joblib


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.pkl"


def predict(features):
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([features])
    return int(prediction[0])


if __name__ == "__main__":
    sample = [5.1, 3.5, 1.4, 0.2]
    result = predict(sample)
    print(f"Prediction: {result}")
