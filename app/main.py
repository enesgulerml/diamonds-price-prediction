# app/main.py

import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os


from app.schemas import DiamondFeatures, PredictionResponse
from src.config import CUT_ORDER, COLOR_ORDER, CLARITY_ORDER

# Global Model
models = {}
MODEL_DIR = "app/model_files"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Initializing API... Target: {MODEL_DIR}")
    try:
        models["regressor"] = mlflow.pyfunc.load_model(MODEL_DIR)
        print(f"✅Model loaded successfully!")
    except Exception as e:
        print(f"❌ Model Loading Error: {e}")
        models["regressor"] = None
    yield
    models.clear()


app = FastAPI(title="Diamonds Price API", lifespan=lifespan)


def preprocess_input(data: DiamondFeatures) -> pd.DataFrame:
    df = pd.DataFrame([data.model_dump()])
    try:
        df['cut'] = CUT_ORDER.index(df['cut'][0])
        df['color'] = COLOR_ORDER.index(df['color'][0])
        df['clarity'] = CLARITY_ORDER.index(df['clarity'][0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Category error: {e}")

    expected_cols = ["carat", "depth", "table", "x", "y", "z", "cut", "color", "clarity"]
    df = df[expected_cols].astype(float)
    return df


@app.get("/")
def health_check():
    status = "Active" if models["regressor"] else "Inactive"
    return {"status": status}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: DiamondFeatures):
    if not models["regressor"]:
        raise HTTPException(status_code=503, detail="The model is out of service.")

    processed_df = preprocess_input(features)
    prediction = models["regressor"].predict(processed_df)

    return {
        "predicted_price": round(float(prediction[0]), 2),
        "model_version": "Embedded V2"
    }