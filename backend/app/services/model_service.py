from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from app.core.config import settings


@dataclass
class ModelPrediction:
    prediction: str
    confidence: float


class BaselineClassifier:
    """Deterministic fallback used before the transformer model is trained."""

    suspicious_terms = {
        "life changing",
        "best ever",
        "perfect",
        "must buy",
        "five stars",
        "amazing product",
        "highly recommend",
        "unbelievable",
    }

    def predict(self, review: str) -> ModelPrediction:
        normalized = re.sub(r"\s+", " ", review.lower()).strip()
        exclamation_count = normalized.count("!")
        all_caps_words = len(re.findall(r"\b[A-Z]{3,}\b", review))
        suspicious_hits = sum(term in normalized for term in self.suspicious_terms)
        score = min(0.95, 0.25 + suspicious_hits * 0.18 + exclamation_count * 0.05 + all_caps_words * 0.04)
        if score >= 0.5:
            return ModelPrediction("Fake", round(score * 100, 2))
        return ModelPrediction("Genuine", round((1 - score) * 100, 2))


class ModelService:
    def __init__(self) -> None:
        self.model_loaded = False
        self.classifier = self._load_classifier()

    def _load_classifier(self):
        model_dir = Path(settings.model_dir)
        if model_dir.exists() and (model_dir / "config.json").exists():
            root = Path(__file__).resolve().parents[3]
            model_package = root / "model"
            if str(model_package) not in sys.path:
                sys.path.append(str(model_package))
            from inference import FakeReviewClassifier

            self.model_loaded = True
            return FakeReviewClassifier(model_dir)
        return BaselineClassifier()

    def predict(self, review: str) -> ModelPrediction:
        result = self.classifier.predict(review)
        if hasattr(result, "label"):
            return ModelPrediction(prediction=result.label, confidence=result.confidence)
        return result


model_service = ModelService()
