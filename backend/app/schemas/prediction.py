from __future__ import annotations

from datetime import datetime

import json

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PredictionRequest(BaseModel):
    review: str = Field(..., min_length=5, max_length=5000)


class PredictionResponse(BaseModel):
    prediction: str
    risk_level: str | None = None
    trust_label: str | None = None
    trust_score: int | None = None
    confidence: float
    evidence_strength: str | None = "Low"
    evidence_score: int | None = 0
    specificity_score: int | None = 0
    context_richness: int | None = 0
    maturity_score: int | None = 0
    uncertainty_penalty: int | None = 0
    trust_ceiling: int | None = 78
    confidence_reason: str | None = "Limited evidence available."
    uncertainty_factors: list[str] = Field(default_factory=list)
    sentiment: str
    sentiment_score: float = 0.0
    model_prediction: str = "Unknown"
    model_confidence: float = 0.0
    indicators: list[dict[str, object]] = Field(default_factory=list)
    suspicious_phrases: list[str] = Field(default_factory=list)
    features: dict[str, object] = Field(default_factory=dict)

    @field_validator("indicators", mode="before")
    @classmethod
    def parse_indicators(cls, value: object) -> list[dict[str, object]]:
        if value is None:
            return []
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                return []
        return value

    @field_validator("uncertainty_factors", mode="before")
    @classmethod
    def parse_uncertainty_factors(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                return []
        return value




class BatchPredictionItem(PredictionResponse):
    review: str


class BatchPredictionResponse(BaseModel):
    count: int
    predictions: list[BatchPredictionItem]
