# Fraud Detection Dashboard

Interactive bilingual (Arabic/English) dashboard for IEEE-CIS Fraud Detection analysis.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Data Files

Copy the exported files from your Google Drive `streamlit_app/` folder:

| Source Path | Destination |
|---|---|
| `data/model_metrics.json` | `data/model_metrics.json` |
| `data/fraud_stats.json` | `data/fraud_stats.json` |
| `data/eda_summary.json` | `data/eda_summary.json` |
| `data/hourly_fraud.csv` | `data/hourly_fraud.csv` |
| `data/amt_distribution.csv` | `data/amt_distribution.csv` |
| `data/productcd_fraud.csv` | `data/productcd_fraud.csv` |
| `data/feature_importance.csv` | `data/feature_importance.csv` |
| `data/confusion_matrix.csv` | `data/confusion_matrix.csv` |
| `data/sample_transactions.csv` | `data/sample_transactions.csv` |
| `data/model_input_samples.parquet` | `data/model_input_samples.parquet` |
| `artifacts/feature_schema.json` | `artifacts/feature_schema.json` |
| `model/final_model_xgb.json` | `artifacts/final_model_xgb.json` |

## Docker

```bash
docker build -t fraud-dashboard .
docker run --rm -p 8501:8501 fraud-dashboard
```

## Streamlit Community Cloud

1. Push this repository to GitHub
2. Create a new app on share.streamlit.io
3. Set `app.py` as the entrypoint
4. Deploy

## Tests

```bash
pytest tests/ -v
```
