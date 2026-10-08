# 🛒 Product Return Prediction — Ibong and Sons

A production-ready ML service that predicts, **before an order ships**, whether
it will be returned. Built as a capstone project on a 12,000-order e-commerce
dataset.

**🔗 Live demo:** https://your-deployed-url.com *(replace once deployed)*

## Highlights

| | |
|---|---|
| **Model** | Logistic Regression (`class_weight='balanced'`) |
| **Recall (returned)** | **86.2%** — catches 4 of every 5 returns |
| **Precision** | 71.9% |
| **ROC-AUC** | 0.85 |
| **Features** | 85 (14 numeric, 4 binary, 67 one-hot) |
| **Training rows** | 9,597 (after leakage-safe outlier removal) |

## Why recall over accuracy

Missing a return costs a full refund + reverse-logistics; a false alarm costs
only a retention nudge. The business prioritises **recall** — the model catches
**86% of actual returns**.

## Stack

- **Backend:** FastAPI + Uvicorn
- **Frontend:** Vanilla HTML/CSS/JS
- **Model:** scikit-learn, serialised with `joblib`
- **Deployment:** Render (backend) + GitHub Pages (frontend)

## Project structure

```
.
├── backend/
│   ├── main.py               FastAPI app
│   ├── utils.py              Preprocessing (mirrors notebook)
│   ├── requirements.txt
│   └── artifacts/
│       └── model_data.joblib Trained bundle (model + scaler + metadata)
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

## Run locally

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs at http://127.0.0.1:8000/docs

### 2. Frontend

Open `frontend/index.html` in a browser — it calls the local API.

## API

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{ "product_category": "Electronics", ... }'
```

Response:

```json
{
  "return_probability": 0.741,
  "predicted_returned": 1,
  "threshold": 0.5,
  "model_name": "Logistic Regression"
}
```

## Notebook

The full modelling notebook is at [`notebooks/product_return_prediction.ipynb`](notebooks/).

## License

MIT — see [LICENSE](LICENSE).