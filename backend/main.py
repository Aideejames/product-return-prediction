"""FastAPI backend for the Product Return Prediction model."""
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from utils import preprocess_raw_order

# ── Load the persisted bundle once at startup ───────────────
ARTIFACT_PATH = Path(__file__).parent / "artifacts" / "model_data.joblib"
bundle = joblib.load(ARTIFACT_PATH)

app = FastAPI(
    title="Product Return Prediction API",
    description=(
        "Predicts the probability that a pre-shipment order will be returned. "
        "Trained for Ibong and Sons e-commerce."
    ),
    version="1.0.0",
)

# Allow the frontend (any origin during dev) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request schema — mirrors the raw CSV columns ────────────
class OrderFeatures(BaseModel):
    product_category: str
    sub_category: str
    brand: str
    product_price: float = Field(..., gt=0)
    discount_percent: float
    product_rating: float
    review_count: float
    fragile_item: int = Field(..., ge=0, le=1)
    warranty_available: int = Field(..., ge=0, le=1)
    product_return_rate: float
    category_return_rate: float
    brand_return_rate: float
    defect_rate: float
    seller_rating: float
    seller_return_rate: float
    fulfillment_type: str
    payment_method: str
    quantity: int
    shipping_distance_km: float
    delayed_delivery: int = Field(..., ge=0, le=1)
    wishlist_before_purchase: int = Field(..., ge=0, le=1)
    product_page_views: int
    customer_support_calls: int
    chat_interactions: int


class PredictionResponse(BaseModel):
    return_probability: float
    predicted_returned: int
    threshold: float
    model_name: str


# ── Routes ──────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Product Return Prediction API",
        "model": bundle["model_name"],
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/model-info")
def model_info():
    return {
        "model_name": bundle["model_name"],
        "metrics": bundle["metrics"],
        "feature_count": len(bundle["model_columns"]),
        "top_features": bundle["feature_importance"][:10],
        "threshold": bundle["threshold"],
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(order: OrderFeatures):
    try:
        X = preprocess_raw_order(order.model_dump(), bundle)
        proba = float(bundle["model"].predict_proba(X)[:, 1][0])
        predicted = int(proba >= bundle["threshold"])

        return PredictionResponse(
            return_probability=round(proba, 4),
            predicted_returned=predicted,
            threshold=bundle["threshold"],
            model_name=bundle["model_name"],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))