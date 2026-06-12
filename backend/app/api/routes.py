from __future__ import annotations

from io import BytesIO

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.prediction import (
    BatchPredictionItem,
    BatchPredictionResponse,
    PredictionRequest,
    PredictionResponse,
)
from app.services.model_service import model_service
from app.services.trust_service import trust_analysis_service


router = APIRouter()


def _predict_review(review: str) -> PredictionResponse:
    analysis = trust_analysis_service.analyze(review)
    return PredictionResponse(
        prediction=analysis.prediction,
        risk_level=analysis.risk_level,
        trust_label=analysis.trust_label,
        trust_score=analysis.trust_score,
        confidence=analysis.confidence,
        evidence_strength=analysis.evidence_strength,
        evidence_score=analysis.evidence_score,
        specificity_score=analysis.specificity_score,
        context_richness=analysis.context_richness,
        maturity_score=analysis.maturity_score,
        uncertainty_penalty=analysis.uncertainty_penalty,
        trust_ceiling=analysis.trust_ceiling,
        confidence_reason=analysis.confidence_reason,
        uncertainty_factors=analysis.uncertainty_factors,
        sentiment=analysis.sentiment,
        sentiment_score=analysis.sentiment_score,
        model_prediction=analysis.model_prediction,
        model_confidence=analysis.model_confidence,
        indicators=analysis.indicators,
        suspicious_phrases=analysis.suspicious_phrases,
        features=analysis.features,
    )


@router.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "model_loaded": model_service.model_loaded}


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    return _predict_review(payload.review)


@router.post("/batch-predict", response_model=BatchPredictionResponse)
async def batch_predict(file: UploadFile = File(...)) -> BatchPredictionResponse:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file.")

    content = await file.read()
    try:
        frame = pd.read_csv(BytesIO(content))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not parse CSV file.") from exc

    review_column = next((column for column in frame.columns if column.lower() in {"review", "text", "review_text", "content"}), None)
    if review_column is None:
        raise HTTPException(status_code=400, detail="CSV must contain a review, text, review_text, or content column.")

    predictions: list[BatchPredictionItem] = []
    for raw_review in frame[review_column].dropna().astype(str).head(200):
        cleaned = raw_review.strip()
        if len(cleaned) < 5 or len(cleaned) > 5000:
            continue  # Skip invalid length reviews to protect resources
        response = _predict_review(cleaned)
        predictions.append(BatchPredictionItem(review=cleaned, **response.model_dump()))
    return BatchPredictionResponse(count=len(predictions), predictions=predictions)


