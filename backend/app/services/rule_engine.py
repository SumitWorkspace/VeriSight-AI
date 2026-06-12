from __future__ import annotations

from dataclasses import dataclass

from app.services.linguistic_service import LinguisticFeatures


@dataclass(frozen=True)
class RuleSignal:
    label: str
    detail: str
    impact: int
    severity: str
    kind: str


class ReviewRuleEngine:
    def evaluate(self, features: LinguisticFeatures, sentiment_score: float) -> list[RuleSignal]:
        signals: list[RuleSignal] = []

        if features.promotional_phrase_count:
            signals.append(
                RuleSignal(
                    label="Promotional wording",
                    detail=f"Found {features.promotional_phrase_count} promotional phrase(s).",
                    impact=min(24, 9 * features.promotional_phrase_count),
                    severity="medium" if features.promotional_phrase_count < 3 else "high",
                    kind="risk",
                )
            )

        if features.exclamation_count >= 2:
            signals.append(
                RuleSignal(
                    label="Unnatural emotional intensity",
                    detail="The review uses multiple exclamation marks.",
                    impact=min(18, features.exclamation_count * 4),
                    severity="medium" if features.exclamation_count < 5 else "high",
                    kind="risk",
                )
            )

        if features.repeated_word_count or features.repeated_phrase_count:
            signals.append(
                RuleSignal(
                    label="Repetitive wording",
                    detail="Repeated words or short phrases reduce naturalness.",
                    impact=min(18, 8 + features.repeated_word_count * 3 + features.repeated_phrase_count * 4),
                    severity="medium",
                    kind="risk",
                )
            )

        if features.all_caps_count >= 2:
            signals.append(
                RuleSignal(
                    label="Forceful capitalization",
                    detail="Multiple all-caps words can indicate promotional pressure.",
                    impact=min(14, features.all_caps_count * 4),
                    severity="medium",
                    kind="risk",
                )
            )

        if features.generic_recommendation_count and not features.has_specific_details:
            signals.append(
                RuleSignal(
                    label="Generic recommendation language",
                    detail="Recommendation language appears without many concrete details.",
                    impact=8,
                    severity="low",
                    kind="risk",
                )
            )

        if features.superlative_count >= 3 and sentiment_score > 0.6:
            signals.append(
                RuleSignal(
                    label="Excessive superlatives",
                    detail="Many strong positive adjectives appear together.",
                    impact=12,
                    severity="medium",
                    kind="risk",
                )
            )

        if features.review_length_category == "very_short" and not features.has_specific_details:
            signals.append(
                RuleSignal(
                    label="Limited context",
                    detail="The review is very short, so the system keeps the assessment conservative.",
                    impact=5,
                    severity="low",
                    kind="risk",
                )
            )

        if features.has_specific_details:
            signals.append(
                RuleSignal(
                    label="Specific details present",
                    detail="Concrete product or experience details increase trust.",
                    impact=-10,
                    severity="positive",
                    kind="trust",
                )
            )

        if features.exclamation_count <= 1 and features.repeated_word_count == 0 and features.repeated_phrase_count == 0:
            signals.append(
                RuleSignal(
                    label="Natural sentence structure",
                    detail="No strong punctuation or repetition pattern was detected.",
                    impact=-6,
                    severity="positive",
                    kind="trust",
                )
            )

        if 0.35 <= abs(sentiment_score) <= 0.75 and features.superlative_count <= 2:
            signals.append(
                RuleSignal(
                    label="Balanced sentiment intensity",
                    detail="Sentiment is not extreme enough to be suspicious on its own.",
                    impact=-5,
                    severity="positive",
                    kind="trust",
                )
            )

        return signals
