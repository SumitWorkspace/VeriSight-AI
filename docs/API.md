# API Documentation

Base URL: `http://localhost:8000`

## Health

`GET /health`

```json
{
  "status": "ok",
  "model_loaded": true
}
```

## Predict

`POST /predict`

Request:

```json
{
  "review": "The product arrived quickly and works as expected."
}
```

Response:

```json
{
  "prediction": "Low Risk",
  "risk_level": "Low Risk",
  "trust_label": "Likely Genuine",
  "trust_score": 76,
  "confidence": 62.4,
  "evidence_strength": "Moderate",
  "evidence_score": 63,
  "specificity_score": 58,
  "context_richness": 61,
  "maturity_score": 72,
  "uncertainty_penalty": 12,
  "trust_ceiling": 90,
  "confidence_reason": "Review contains natural language patterns but limited contextual detail.",
  "uncertainty_factors": [
    "Short review length"
  ],
  "sentiment": "Positive",
  "sentiment_score": 0.42,
  "model_prediction": "Genuine",
  "model_confidence": 78.1,
  "indicators": [],
  "suspicious_phrases": [],
  "features": {
    "word_count": 8,
    "specificity_score": 2,
    "review_length": "short"
  }
}
```

## Batch Predict

`POST /batch-predict`

Upload a CSV file using multipart form data. The file must contain a review column named `review`, `text`, `review_text`, or `content`.

## Dashboard

`GET /dashboard`

Returns total analyzed reviews, fake/genuine percentages, and recent predictions.
