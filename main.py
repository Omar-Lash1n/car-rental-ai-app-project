from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Car Price Prediction API")

MODEL_USED = "XGBoost (tuned)"

# Load artifacts
ARTIFACT_DIR = Path("artifacts")
MODEL_PATH = ARTIFACT_DIR / "final_model.pkl"
COLUMNS_PATH = ARTIFACT_DIR / "model_columns.pkl"

try:
    model = joblib.load(MODEL_PATH)
    model_columns = joblib.load(COLUMNS_PATH)
except Exception as e:
    raise RuntimeError(
        f"Failed to load artifacts. Ensure {MODEL_PATH} and {COLUMNS_PATH} exist. Error: {e}"
    )


class CarInput(BaseModel):
    brand: str
    model: str
    year: int = Field(..., le=datetime.now().year)
    transmission: str
    mileage: float = Field(..., ge=0)
    fuelType: str
    tax: float
    mpg: float
    engineSize: float = Field(..., gt=0)


class PredictResponse(BaseModel):
    estimated_price: float
    currency: str = "GBP"
    model_used: str


def preprocess_input(input_dict: dict, columns: list[str]) -> pd.DataFrame:
    df = pd.DataFrame([input_dict])

    # Clean strings (avoid issues like leading/trailing spaces)
    for col in ["brand", "model", "transmission", "fuelType"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)
    return df


@app.post("/predict")
def predict_price(car: CarInput):
    try:
        # Pydantic v2 uses model_dump(); v1 uses dict()
        if hasattr(car, "model_dump"):
            data = car.model_dump()
        else:
            data = car.dict()

        processed = preprocess_input(data, model_columns)
        prediction = model.predict(processed)[0]
        return PredictResponse(
            estimated_price=round(float(prediction), 2),
            currency="GBP",
            model_used=MODEL_USED,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def health_check():
    return {"status": "API is running"}
