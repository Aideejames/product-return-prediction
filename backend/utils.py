"""Preprocessing helpers — mirror the notebook pipeline 1:1."""
import numpy as np
import pandas as pd


def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    """Same two engineered features as Task 5 in the notebook."""
    out = data.copy()

    # 1. Combined support-contact signal
    out["total_support_contacts"] = (
        out["customer_support_calls"] + out["chat_interactions"]
    )
    out = out.drop(columns=["customer_support_calls", "chat_interactions"])

    # 2. Log-transformed price
    out["log_price"] = np.log1p(out["product_price"])
    out = out.drop(columns=["product_price"])

    return out


def preprocess_raw_order(raw: dict, bundle: dict) -> pd.DataFrame:
    """
    Convert a single raw order (dict from the API) into the exact
    model-ready feature vector used during training.
    """
    df = pd.DataFrame([raw])

    # Drop identifier if present — the model never saw it
    df = df.drop(columns=["order_id"], errors="ignore")

    # Feature engineering (same as notebook)
    df = engineer_features(df)

    # Median imputation using values stored in the bundle
    cols_to_impute = bundle["numeric_features"] + bundle["binary_flags"]
    df[cols_to_impute] = df[cols_to_impute].fillna(bundle["train_medians"])

    # Standard scaling (transform-only, using the fitted scaler)
    df[bundle["numeric_features"]] = bundle["scaler"].transform(
        df[bundle["numeric_features"]]
    )

    # One-hot encode categoricals
    df = pd.get_dummies(
        df, columns=bundle["categorical_features"], dtype=int
    )

    # Align columns to what the model expects
    df = df.reindex(columns=bundle["model_columns"], fill_value=0)

    return df