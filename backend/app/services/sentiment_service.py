from __future__ import annotations

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentService:
    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> str:
        score = self.analyzer.polarity_scores(text)["compound"]
        if score >= 0.05:
            return "Positive"
        if score <= -0.05:
            return "Negative"
        return "Neutral"
