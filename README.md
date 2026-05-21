## Project Screenshots & Outputs

### 1. AutoValue AI Frontend Interface
![AutoValue AI Frontend Interface](Screenshot%202026-05-22%20003335.jpg)

### 2. FastAPI Swagger UI (Predict Endpoint)
![FastAPI Swagger UI](Screenshot%202026-05-22%20003727.jpg)

### 3. Model Performance Comparison
![Model Performance Comparison](Screenshot%202026-05-22%20003709.jpg)

### 4. Exploratory Data Analysis (EDA)

#### Distribution of Car Prices
![Distribution of Car Prices](Screenshot%202026-05-22%20003718.jpg)

#### Correlation Heatmap of Numerical Features
![Correlation Heatmap](Screenshot%202026-05-22%20003639.jpg)

#### Relationship Between Mileage and Price
![Relationship Between Mileage and Price](Screenshot%202026-05-22%20003628.jpg)

#### Average Car Price Trend by Year (1995 - 2020)
![Average Car Price Trend by Year](Screenshot%202026-05-22%20003649.jpg)

#### 

## If you don't have an environment (do this first)

### 1) Create a virtual environment

From the project root:

```bash
python -m venv .venv
```

### 2) Activate it

Windows (PowerShell):

```bash
.\.venv\Scripts\Activate.ps1
```

macOS/Linux (bash/zsh):

```bash
source .venv/bin/activate
```

### 3) Upgrade pip (recommended)

```bash
python -m pip install --upgrade pip
```

## Artifacts

The trained model and the expected feature columns are saved in `artifacts/`:

- `artifacts/final_model.pkl`
- `artifacts/model_columns.pkl`

These are loaded by the FastAPI service in `main.py`.

## API (FastAPI)

### 1) Install dependencies

If you already have a virtual environment, activate it and install:

```bash
pip install fastapi "uvicorn[standard]" pandas numpy scikit-learn xgboost joblib
```

### 2) Run the server

From the project root:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Swagger UI:

- http://127.0.0.1:8000/docs

Health check:

- http://127.0.0.1:8000/

### 3) Test `/predict`

Example JSON body:

```json
{
  "brand": "Audi",
  "model": "A1",
  "year": 2017,
  "transmission": "Manual",
  "mileage": 15735,
  "fuelType": "Petrol",
  "tax": 150,
  "mpg": 55.4,
  "engineSize": 1.4
}
```

The response is:

```json
{
  "estimated_price": 12651.49,
  "currency": "GBP",
  "model_used": "XGBoost (tuned)"
}
```

## Limitation (Unknown Categories)

The API uses one-hot encoding with a fixed set of columns saved from training. If you send a brand/model/transmission/fuelType that was not seen during training, it will not get a dedicated one-hot column and effectively contributes zeros for those unknown categories. The API still returns a prediction, but accuracy may degrade for truly unseen values.

Average Car Price by Transmission Type
![Average Car Price by Transmission Type](Screenshot%202026-05-22%20003658.jpg)
