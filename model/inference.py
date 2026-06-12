from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from preprocess import clean_review_text


@dataclass
class Prediction:
    label: str
    confidence: float


class FakeReviewClassifier:
    """Loads a saved transformer model and predicts fake-review probability."""

    def __init__(self, model_dir: str | Path, max_length: int = 256) -> None:
        self.model_dir = Path(model_dir)
        self.max_length = max_length
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_dir)
        self.model.to(self.device)
        self.model.eval()

    def predict(self, review: str) -> Prediction:
        cleaned = clean_review_text(review)
        encoded = self.tokenizer(
            cleaned,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=self.max_length,
        )
        encoded = {key: value.to(self.device) for key, value in encoded.items()}
        with torch.no_grad():
            logits = self.model(**encoded).logits
            probabilities = torch.softmax(logits, dim=-1).squeeze(0)
        predicted_index = int(torch.argmax(probabilities).item())
        label = "Fake" if predicted_index == 1 else "Genuine"
        confidence = round(float(probabilities[predicted_index].item()) * 100, 2)
        return Prediction(label=label, confidence=confidence)
