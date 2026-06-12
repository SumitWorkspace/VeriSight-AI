from __future__ import annotations

from dataclasses import dataclass

from app.services.evidence_service import EvidenceProfile, EvidenceSufficiencyService
from app.services.linguistic_service import LinguisticFeatures, LinguisticAnalysisService
from app.services.model_service import ModelPrediction, model_service
from app.services.rule_engine import ReviewRuleEngine, RuleSignal
from app.services.sentiment_service import SentimentService
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


@dataclass(frozen=True)
class TrustAnalysis:
    prediction: str
    risk_level: str
    trust_label: str
    trust_score: int
    confidence: float
    evidence_strength: str
    evidence_score: int
    specificity_score: int
    context_richness: int
    maturity_score: int
    uncertainty_penalty: int
    trust_ceiling: int
    confidence_reason: str
    uncertainty_factors: list[str]
    sentiment: str
    sentiment_score: float
    model_prediction: str
    model_confidence: float
    indicators: list[dict[str, object]]
    suspicious_phrases: list[str]
    features: dict[str, object]


class TrustAnalysisService:
    def __init__(self) -> None:
        self.linguistic_service = LinguisticAnalysisService()
        self.evidence_service = EvidenceSufficiencyService()
        self.rule_engine = ReviewRuleEngine()
        self.sentiment_service = SentimentService()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def analyze(self, review: str) -> TrustAnalysis:
        features = self.linguistic_service.analyze(review)
        sentiment = self.sentiment_service.analyze(review)
        sentiment_score = self.sentiment_analyzer.polarity_scores(review)["compound"]
        model_prediction = model_service.predict(review)
        signals = self.rule_engine.evaluate(features, sentiment_score)
        evidence = self.evidence_service.analyze(review, features, sentiment_score)
        trust_score = self._calculate_trust_score(review, features, signals, model_prediction, evidence, sentiment_score)
        risk_level = self._risk_level(trust_score)
        trust_label = self._trust_label(trust_score)
        uncertainty_factors = self._uncertainty_factors(review, features, evidence, signals, model_prediction)
        confidence = self._analysis_confidence(review, features, signals, model_prediction, evidence, uncertainty_factors)
        confidence_reason = self._confidence_reason(evidence, uncertainty_factors, signals)

        return TrustAnalysis(
            prediction=risk_level,
            risk_level=risk_level,
            trust_label=trust_label,
            trust_score=trust_score,
            confidence=confidence,
            evidence_strength=evidence.strength,
            evidence_score=round(evidence.evidence_score),
            specificity_score=round(evidence.specificity_score),
            context_richness=round(evidence.context_richness),
            maturity_score=round(evidence.maturity_score),
            uncertainty_penalty=round(evidence.uncertainty_penalty),
            trust_ceiling=evidence.trust_ceiling,
            confidence_reason=confidence_reason,
            uncertainty_factors=uncertainty_factors,
            sentiment=sentiment,
            sentiment_score=round(sentiment_score, 3),
            model_prediction=model_prediction.prediction,
            model_confidence=model_prediction.confidence,
            indicators=[signal.__dict__ for signal in signals],
            suspicious_phrases=[*features.promotional_phrases, *features.generic_phrases],
            features={
                "word_count": features.word_count,
                "lexical_diversity": features.lexical_diversity,
                "punctuation_intensity": features.exclamation_count,
                "phrase_repetition": features.repeated_phrase_count,
                "repeated_words": features.repeated_word_count,
                "superlatives": features.superlative_count,
                "has_specific_details": features.has_specific_details,
                "evidence_score": evidence.evidence_score,
                "specificity_score": evidence.specificity_score,
                "context_richness": evidence.context_richness,
                "maturity_score": evidence.maturity_score,
                "uncertainty_penalty": evidence.uncertainty_penalty,
                "trust_ceiling": evidence.trust_ceiling,
                "review_length": features.review_length_category,
            },
        )

    def _calculate_trust_score(
        self,
        review: str,
        features: LinguisticFeatures,
        signals: list[RuleSignal],
        model_prediction: ModelPrediction,
        evidence: EvidenceProfile,
        sentiment_score: float,
    ) -> int:
        import re
        base_score = 76.0
        
        # Calculate detail hits and generic flags early
        detail_words = [word for word in re.findall(r"\b[a-zA-Z']+\b", review.lower()) if word in self.evidence_service.observation_terms]
        detail_hits = len(detail_words)
        timing_hits = len(self.evidence_service.timing_pattern.findall(review))
        numeric_hits = len(self.evidence_service.numeric_pattern.findall(review))
        contrast_pattern = re.compile(r"\b(but|although|however|though|except|while|yet)\b", re.I)
        contrast_hits = len(contrast_pattern.findall(review))
        
        category_nouns = {"food", "staff", "room", "rooms", "service", "product", "products", "stay", "item", "items", "place", "experience", "establishment", "quality", "amenities", "value", "price", "cost"}
        all_generic_nouns = all(w in category_nouns for w in detail_words) if detail_words else True
        
        is_generic = (detail_hits <= 1 and timing_hits == 0 and numeric_hits == 0) or all_generic_nouns
        
        # Influence of model prediction (treated as a signal, not absolute truth)
        fake_probability = model_prediction.confidence if model_prediction.prediction == "Fake" else 100 - model_prediction.confidence
        
        # Smooth model prediction oversensitivity for clean reviews
        risk_signal_count = sum(1 for signal in signals if signal.kind == "risk")
        if risk_signal_count == 0 and features.promotional_phrase_count == 0 and features.exclamation_count == 0:
            fake_probability = 50.0 + (fake_probability - 50.0) * 0.7
            
        if fake_probability >= 85:
            base_score -= 18
        elif fake_probability >= 70:
            base_score -= 10
        elif fake_probability >= 58:
            base_score -= 5
        elif fake_probability <= 30:
            base_score += 4

        # Influence of rule engine signals
        for signal in signals:
            if signal.kind == "risk":
                base_score -= signal.impact
            elif signal.kind == "trust":
                base_score += min(2.0, abs(signal.impact) * 0.15)

        # Influence of evidence metrics
        base_score += (evidence.specificity_score - 30) * 0.35
        base_score += (evidence.context_richness - 40) * 0.25
        base_score += (evidence.maturity_score - 50) * 0.10
        base_score += (evidence.evidence_score - 45) * 0.20

        # Penalties for low evidence, specificity, and contextual richness (only for generic reviews)
        if is_generic:
            if evidence.specificity_score < 20:
                base_score -= (20 - evidence.specificity_score) * 0.6
            if evidence.context_richness < 35:
                base_score -= (35 - evidence.context_richness) * 0.5
            if evidence.evidence_score < 45:
                base_score -= (45 - evidence.evidence_score) * 0.5

        # Check for contrast hits and positive words
        # Requirement 7: Balanced Sentiment Bonus
        is_balanced = (contrast_hits >= 1 and 0.15 <= abs(sentiment_score) <= 0.82 and 
                       evidence.specificity_score >= 23)
        # Purely perfect reviews get mild skepticism
        is_purely_one_sided_positive = (sentiment_score > 0.75 and contrast_hits == 0)
        
        if is_balanced:
            base_score += 4.5
        elif is_purely_one_sided_positive:
            base_score -= 3.0
 
        # Requirement 9: Trust Decay for short or low-specificity reviews
        if features.word_count < 12 and evidence.specificity_score < 15:
            base_score -= (12 - features.word_count) * 0.8
        if evidence.specificity_score < 40:
            factor = 0.08 if evidence.specificity_score >= 25 else 0.15
            base_score -= (40 - evidence.specificity_score) * factor
 
        # Requirement 1: Human Variability Analysis
        # 1. Overly uniform positivity penalty
        sentences = [part.strip() for part in re.split(r"[.!?]+", review) if part.strip()]
        if len(sentences) >= 2 and sentiment_score > 0.60 and contrast_hits == 0:
            base_score -= 4.0 if evidence.specificity_score < 35 else 2.0
            
        # 2. Repetitive sentence rhythm penalty
        if len(sentences) >= 3:
            words_per_sentence = [len(re.findall(r"\b[a-zA-Z']+\b", s)) for s in sentences]
            mean_len = sum(words_per_sentence) / len(sentences)
            variance = sum((w - mean_len) ** 2 for w in words_per_sentence) / len(sentences)
            std_dev = variance ** 0.5
            if std_dev < 2.0:
                base_score -= 4.0
                
        # 3. Excessively polished praise penalty
        if (features.promotional_phrase_count > 0 and features.superlative_count >= 2 
            and features.lexical_diversity >= 0.70 and features.word_count >= 12 
            and evidence.specificity_score < 40):
            base_score -= 5.0
 
        # Requirement 3: Compress trust score based on evidence strength & suspicious indicators
        is_ai_style = (features.word_count >= 20 and features.lexical_diversity >= 0.65 and 
                       evidence.specificity_score < 20 and contrast_hits == 0 and sentiment_score > 0.60)

        is_promotional_risk = (features.promotional_phrase_count > 0 and evidence.specificity_score < 22)
        is_suspicious = (risk_signal_count >= 2 or fake_probability >= 78 or 
                         (fake_probability >= 55 and (features.promotional_phrase_count > 0 or features.exclamation_count >= 2)) or
                         is_ai_style or is_promotional_risk)
 
        if is_suspicious:
            # Suspicious review target range: 25-45 (Requirement 3)
            compressed = (
                28.0
                + (evidence.specificity_score - 15) * 0.68
                + (evidence.context_richness - 30) * 1.20
                + (evidence.maturity_score - 45) * 0.02
                + (evidence.evidence_score - 30) * 0.34
                - (evidence.uncertainty_penalty - 58) * 0.36
                - (fake_probability - 60) * 0.18
            )
            trust_score = max(24, min(45, round(compressed)))
        else:
            # Map based on evidence strength
            if evidence.strength == "Low":
                if is_generic:
                    # Generic/Ambiguous target range: 50-61 (fits human ambiguous target 45-70 and Medium Risk)
                    compressed = (
                        57.0
                        + (evidence.specificity_score - 10) * 0.06
                        + (evidence.context_richness - 25) * 0.12
                        + (evidence.maturity_score - 70) * 0.06
                        + (evidence.evidence_score - 30) * 0.26
                        - (evidence.uncertainty_penalty - 54) * 0.38
                        + (base_score - 68.0) * 0.12
                    )
                    trust_score = max(50, min(61, round(compressed)))
                else:
                    # Short-but-specific target range: 74-77 if highly clean, else 65-73 (fits human genuine short target 65-82)
                    is_highly_clean = (risk_signal_count == 0 and fake_probability < 75)
                    if is_highly_clean:
                        compressed = (
                            75.0
                            + (evidence.specificity_score - 24) * 0.60
                            + (evidence.context_richness - 25) * 0.30
                            + (evidence.maturity_score - 80) * 0.32
                            + (evidence.evidence_score - 50) * 0.52
                            - (evidence.uncertainty_penalty - 50) * 0.50
                        )
                        trust_score = max(70, min(78, round(compressed)))
                    else:
                        compressed = (
                            62.5
                            + (evidence.specificity_score - 18) * 0.42
                            + (evidence.context_richness - 22) * 0.16
                            + (evidence.maturity_score - 78) * 0.04
                            + (evidence.evidence_score - 32) * 0.06
                            - (evidence.uncertainty_penalty - 60) * 0.14
                        )
                        trust_score = max(65, min(73, round(compressed)))
            elif evidence.strength == "Moderate":
                # Target range: 72-90
                compressed = (
                    83.0
                    + (base_score - 80.0) * 0.02
                    + (evidence.evidence_score - 50) * 0.30
                    + (evidence.specificity_score - 33) * 0.02
                    + (evidence.context_richness - 30) * 0.60
                    + (evidence.maturity_score - 84) * 0.24
                )
                trust_score = max(72, min(90, round(compressed)))
            else: # Strong
                # Target range: 85-93 (or 94/95)
                is_exceptional = (evidence.specificity_score >= 70 and is_balanced and model_prediction.prediction == "Genuine")
                if is_exceptional:
                    # Exceptional target range: 93-98
                    compressed = 90.5 + (base_score - 80.0) * 0.20
                    trust_score = max(93, min(97, round(compressed)))
                else:
                    compressed = (
                        92.0
                        + (evidence.evidence_score - 70) * 1.04
                        + (base_score - 100.0) * 0.56
                        + (evidence.specificity_score - 55) * 0.26
                        + (evidence.context_richness - 50) * 0.14
                        + (evidence.maturity_score - 88) * 0.22
                    )
                    trust_score = max(83, min(94, round(compressed)))

        # Requirement 2 & 10: Strictly apply evidence ceilings
        ceiling = evidence.trust_ceiling
        if evidence.strength == "Low":
            ceiling = min(ceiling, 78)
        elif evidence.strength == "Moderate":
            ceiling = min(ceiling, 90)
        else:
            ceiling = min(ceiling, 98)

        final_score = min(trust_score, ceiling)
        
        # Requirement 5: Final Probabilistic Calibration Layer (smooth extremes, maintain realistic uncertainty)
        if final_score > 94:
            final_score = 94 + round((final_score - 94) * 0.3)
        elif final_score < 24:
            final_score = 24 - round((24 - final_score) * 0.3)
            
        # Hard caps to avoid extreme values: NEVER return 100 or exactly 98 / 2
        final_score = min(final_score, 97)
        final_score = max(final_score, 24)
        
        return final_score

    @staticmethod
    def _risk_level(score: int) -> str:
        if score >= 70:
            return "Low Risk"
        if score >= 48:
            return "Medium Risk"
        return "High Risk"

    @staticmethod
    def _trust_label(score: int) -> str:
        if score >= 94:
            return "Exceptionally Strong Estimate"
        if score >= 88:
            return "Highly Trustworthy"
        if score >= 70:
            return "Likely Genuine"
        if score >= 48:
            return "Uncertain"
        if score >= 20:
            return "Suspicious"
        return "High Risk"

    @staticmethod
    def _uncertainty_factors(
        review: str,
        features: LinguisticFeatures,
        evidence: EvidenceProfile,
        signals: list[RuleSignal],
        model_prediction: ModelPrediction,
    ) -> list[str]:
        import re
        factors: list[str] = [*evidence.uncertainty_factors]
        risk_signals = [signal for signal in signals if signal.kind == "risk"]
        trust_signals = [signal for signal in signals if signal.kind == "trust"]

        if risk_signals and trust_signals:
            factors.append("Mixed trust indicators detected")
        if 45 <= model_prediction.confidence <= 65:
            factors.append("Model signal is not strongly separated")
            
        # Human Variability factors
        contrast_pattern = re.compile(r"\b(but|although|however|though|except|while|yet)\b", re.I)
        contrast_hits = len(contrast_pattern.findall(review))
        
        sentences = [part.strip() for part in re.split(r"[.!?]+", review) if part.strip()]
        
        # We can analyze sentiment compound for positivity detection
        analyzer = SentimentIntensityAnalyzer()
        sentiment_score = analyzer.polarity_scores(review)["compound"]
        
        if len(sentences) >= 2 and sentiment_score > 0.60 and contrast_hits == 0:
            factors.append("Uniform positivity detected")
            
        if len(sentences) >= 3:
            words_per_sentence = [len(re.findall(r"\b[a-zA-Z']+\b", s)) for s in sentences]
            mean_len = sum(words_per_sentence) / len(sentences)
            variance = sum((w - mean_len) ** 2 for w in words_per_sentence) / len(sentences)
            std_dev = variance ** 0.5
            if std_dev < 2.0:
                factors.append("Repetitive sentence rhythm")
                
        if (features.promotional_phrase_count > 0 and features.superlative_count >= 2 
            and features.lexical_diversity >= 0.70 and features.word_count >= 12 
            and evidence.specificity_score < 40):
            factors.append("Excessively polished praise")

        is_ai_style = (features.word_count >= 20 and features.lexical_diversity >= 0.65 and 
                       evidence.specificity_score < 20 and contrast_hits == 0 and sentiment_score > 0.60)
        if is_ai_style:
            factors.append("Highly polished unspecific narrative (AI style)")

        return list(dict.fromkeys(factors))

    @staticmethod
    def _analysis_confidence(
        review: str,
        features: LinguisticFeatures,
        signals: list[RuleSignal],
        model_prediction: ModelPrediction,
        evidence: EvidenceProfile,
        uncertainty_factors: list[str],
    ) -> float:
        base_confidence = 62.0
        
        # Add values based on evidence quality
        base_confidence += evidence.evidence_score * 0.15
        base_confidence += evidence.maturity_score * 0.08
        
        # Model certainty contribution
        base_confidence += min(5.0, abs(model_prediction.confidence - 50.0) * 0.10)
        
        # Uncertainty factor penalties (dampened stacking)
        num_factors = len(uncertainty_factors)
        factor_penalty = (num_factors ** 0.8) * 2.2
        base_confidence -= factor_penalty
        base_confidence -= evidence.uncertainty_penalty * 0.12
        
        # Decay for short review length
        if features.word_count < 12:
            base_confidence -= (12 - features.word_count) * 1.5
            
        # Calibrate based on evidence strength
        risk_signal_count = sum(1 for s in signals if s.kind == "risk")
        fake_probability = model_prediction.confidence if model_prediction.prediction == "Fake" else 100 - model_prediction.confidence
        
        import re
        contrast_pattern = re.compile(r"\b(but|although|however|though|except|while|yet)\b", re.I)
        contrast_hits = len(contrast_pattern.findall(review))
        
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        sentiment_score = analyzer.polarity_scores(review)["compound"]
        
        is_ai_style = (features.word_count >= 20 and features.lexical_diversity >= 0.65 and 
                       evidence.specificity_score < 20 and contrast_hits == 0 and sentiment_score > 0.60)
        
        is_suspicious = (risk_signal_count >= 2 or fake_probability >= 78 or 
                         (fake_probability >= 55 and (features.promotional_phrase_count > 0 or features.exclamation_count >= 3)) or
                         is_ai_style)
        
        if is_suspicious:
            # We are confident about suspicious reviews if they have clear risk signals
            calibrated = 68.0 + (base_confidence - 60.0) * 0.5
            confidence = max(65.0, min(80.0, calibrated))
        else:
            if evidence.strength == "Low":
                calibrated = 60.0 + (base_confidence - 55.0) * 0.5
                confidence = max(58.0, min(70.0, calibrated))
            elif evidence.strength == "Moderate":
                calibrated = 74.0 + (base_confidence - 65.0) * 0.6
                confidence = max(70.0, min(82.0, calibrated))
            else: # Strong
                calibrated = 83.0 + (base_confidence - 75.0) * 0.5
                confidence = max(75.0, min(90.0, calibrated))
                
        # Absolute hard caps to avoid extreme values
        confidence = min(confidence, 94.0) # Rarely exceed 92, almost never exceed 95
        confidence = max(confidence, 55.0) # Most outputs between 55-82
        
        return round(confidence, 2)

    @staticmethod
    def _confidence_reason(
        evidence: EvidenceProfile,
        uncertainty_factors: list[str],
        signals: list[RuleSignal],
    ) -> str:
        risk_signals = [signal for signal in signals if signal.kind == "risk"]
        trust_signals = [signal for signal in signals if signal.kind == "trust"]
        
        if risk_signals and trust_signals:
            return "Mixed trust indicators reduce certainty."
        
        if "Mixed trust indicators detected" in uncertainty_factors:
            return "Mixed trust indicators reduce certainty."
            
        if evidence.strength == "Low":
            return "Limited evidence available."
            
        if evidence.strength == "Strong" and len(risk_signals) == 0:
            return "Multiple consistent authenticity signals detected."
            
        return "Review contains natural language patterns but limited contextual detail."


trust_analysis_service = TrustAnalysisService()
