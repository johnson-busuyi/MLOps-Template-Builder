
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.pkl"

model = None

SPECIES = ["setosa", "versicolor", "virginica"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
    yield
    model = None


app = FastAPI(
    title="MLOps Prediction API",
    description="Random Forest Iris classification API",
    version="1.0.0",
    lifespan=lifespan
)


class IrisInput(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


@app.get("/")
def home():
    return {"message": "MLOps Prediction API is running"}


@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: IrisInput):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Train the model first."
        )

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = int(model.predict(features)[0])

    return {
        "prediction": prediction,
        "species": SPECIES[prediction]
    }
