from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.linguistic_service import LinguisticFeatures


@dataclass(frozen=True)
class EvidenceProfile:
    strength: str
    evidence_score: int
    specificity_score: int
    context_richness: int
    maturity_score: int
    uncertainty_penalty: int
    trust_ceiling: int
    uncertainty_factors: list[str]


class EvidenceSufficiencyService:
    timing_pattern = re.compile(r"\b(?:\d{1,2}(?::\d{2})?\s?(?:am|pm)|morning|evening|night|weekend|weekday|today|yesterday)\b", re.I)
    numeric_pattern = re.compile(r"\b\d+\b")
    named_entity_pattern = re.compile(r"\b[A-Z][a-z]{2,}\b")
    contrast_pattern = re.compile(r"\b(?:but|although|however|though|except|while|yet)\b", re.I)
    observation_terms = {
        # Lodging / Hotels
        "room", "rooms", "staff", "breakfast", "buffet", "service", "parking", "noise", "bed", "bathroom",
        "location", "music", "ambience", "check-in", "checkout", "lobby", "wifi", "view", "ac", "shower",
        "pool", "gym", "restaurant", "desk", "reception", "manager", "door", "window", "street", "noisy",
        "loud", "quiet", "pillow", "pillows", "sheet", "sheets", "blanket", "blankets", "towel", "towels",
        "soap", "shampoo", "toilet", "elevator", "corridor", "hallway", "balcony", "patio", "stay", "night",
        # Tech / Products
        "screen", "software", "charging", "charger", "ports", "cable", "package", "adapter", "device",
        "devices", "battery", "case", "button", "buttons", "keys", "keyboard", "mouse", "laptop", "phone",
        "tablet", "sound", "bass", "volume", "display", "processor", "memory", "storage", "speed", "tactile",
        "switches", "bluetooth", "unboxing", "box", "packaging", "iphone", "galaxy", "macbook", "protector",
        "hub", "monitor", "stand", "mount", "port", "cleaner",
        # Food / Dining
        "steak", "fries", "cheeseburger", "burger", "tikka", "masala", "naan", "samosas", "curry", "dining",
        "food", "drink", "drinks", "beer", "wine", "menu", "chef", "waiter", "waitress", "table", "sauce",
        "taste", "flavor", "spicy", "sweet", "delicious", "served", "lasagna", "garlic", "knots", "lunch",
        "dinner", "delivery", "shipping", "pizza", "crust", "slice", "sushi", "tuna", "roll", "pasta",
        # Services / General
        "haircut", "salon", "trim", "trimming", "layers", "mechanic", "oil", "brake", "pads", "brakes", "car",
        "wash", "vacuum", "vacuuming", "seat", "seats",
        # Household / Physical observation terms
        "steel", "mesh", "sink", "rust", "water", "flow", "drain", "tool", "material", "plastic", "metal",
        "wood", "size", "weight", "sturdy", "mesh", "clean", "crowded", "price", "value", "cost"
    }
    generic_positive_terms = {
        "good",
        "great",
        "nice",
        "excellent",
        "amazing",
        "perfect",
        "heavenly",
        "friendly",
        "respectful",
        "kindness",
        "clean",
    }

    def analyze(self, review: str, features: LinguisticFeatures, sentiment_score: float) -> EvidenceProfile:
        words = re.findall(r"\b[a-zA-Z'-]+\b", review)
        normalized_words = [word.lower() for word in words]
        word_count = len(normalized_words)
        detail_hits = sum(1 for word in normalized_words if word in self.observation_terms)
        generic_positive_hits = sum(1 for word in normalized_words if word in self.generic_positive_terms)
        timing_hits = len(self.timing_pattern.findall(review))
        numeric_hits = len(self.numeric_pattern.findall(review))
        common_words = {"the", "this", "very", "it", "not", "we", "they", "he", "she", "i", "you", "our", "my", "us", "but", "although", "however", "when", "if", "there", "then", "their", "so", "here", "on", "in", "at", "an", "a", "good", "great", "nice", "excellent", "amazing"}
        named_entity_hits = len([match for match in self.named_entity_pattern.findall(review) if match.lower() not in common_words])
        contrast_hits = len(self.contrast_pattern.findall(review))
        sentence_count = max(1, len([part for part in re.split(r"[.!?]+", review) if part.strip()]))

        detail_density = detail_hits / max(1, word_count)
        
        # 1. Specificity Scoring with Saturation (Requirement 3)
        specificity_score = 0
        specificity_score += min(20, detail_hits * 3) # capped detail observation score
        specificity_score += min(12, timing_hits * 5 + numeric_hits * 3) # capped timing/numeric score
        specificity_score += min(8, named_entity_hits * 3.5) # capped named entity score
        specificity_score += min(16, contrast_hits * 6) # capped contrast score (reward transitions)
        
        if contrast_hits >= 1:
            specificity_score += 5 # structural contrast bonus
            
        if word_count >= 25:
            specificity_score += 8
        elif word_count >= 12:
            specificity_score += 4
            
        if detail_density >= 0.15 and word_count >= 10:
            specificity_score += 6
        specificity_score = min(100, specificity_score)

        # 2. Dedicated Context Richness Scoring (Requirement 4)
        context_richness = 0
        # Environmental detail: lobby, pool, view, room, bed, bathroom, music, ambience, parking, breakfast, buffet
        env_details = sum(1 for w in normalized_words if w in {"lobby", "wifi", "view", "ac", "shower", "pool", "gym", "restaurant", "bed", "bathroom", "music", "ambience", "parking", "breakfast", "buffet"})
        context_richness += min(25, env_details * 5)
        
        # Situational observations: served, crowded, clean, noisy, quiet, etc.
        situational_observations = sum(1 for w in normalized_words if w in {"served", "crowded", "clean", "noisy", "quiet", "handling", "professional", "kindness"})
        context_richness += min(20, situational_observations * 5)
        
        # Experiential depth: sentence variety, sentence count, word count
        depth_score = (word_count * 0.5) + (sentence_count * 3.0)
        context_richness += min(30, depth_score)
        
        # Contextual density: lexical diversity and transitions
        density_score = (features.lexical_diversity * 15.0) + (contrast_hits * 4.0)
        context_richness += min(25, density_score)
        context_richness = min(100, round(context_richness))

        # 3. Review Maturity Scoring (Requirement 2)
        maturity_score = 50 # baseline
        
        # Coherence: penalise repetition
        repetition_penalty = (features.repeated_word_count * 4) + (features.repeated_phrase_count * 8)
        maturity_score -= min(25, repetition_penalty)
        
        # Contextual flow: reward transition / contrast words
        maturity_score += min(15, contrast_hits * 5.0)
        
        # Experiential realism: penalise over-polishing & emotional intensity
        polishing_penalty = 0
        if features.exclamation_count >= 2:
            polishing_penalty += (features.exclamation_count - 1) * 3
        if features.superlative_count >= 3:
            polishing_penalty += (features.superlative_count - 2) * 4
        if features.promotional_phrase_count > 0:
            polishing_penalty += 12
        maturity_score -= min(30, polishing_penalty)
        
        # Narrative quality: lexical richness & sentence diversity
        maturity_score += min(15, features.lexical_diversity * 15.0)
        if sentence_count > 0 and 8 <= (word_count / sentence_count) <= 20: # realistic sentence length
            maturity_score += 8
            
        # Observation richness: specific vs generic
        obs_ratio_bonus = (detail_hits - generic_positive_hits) * 3.0
        if obs_ratio_bonus > 0:
            maturity_score += min(12, obs_ratio_bonus)
        else:
            maturity_score -= min(10, abs(obs_ratio_bonus))
            
        maturity_score = max(15, min(95, round(maturity_score)))

        # 4. Overall Evidence score
        evidence_score = round(specificity_score * 0.42 + context_richness * 0.36 + maturity_score * 0.22)
        
        # Detail Density Bonus
        if detail_density >= 0.20:
            evidence_score += 15
            
        if timing_hits and contrast_hits and detail_hits >= 3:
            evidence_score += 10
            
        evidence_score = min(100, evidence_score)
            
        # 5. Uncertainty Factor Reporting (Requirement 6)
        uncertainty_factors: list[str] = []
        uncertainty_penalty = 0

        if word_count < 12:
            uncertainty_factors.append("Short review length")
            uncertainty_penalty += 24
        elif word_count < 25:
            uncertainty_factors.append("Short review length")
            uncertainty_penalty += 12
            
        if specificity_score < 40:
            uncertainty_factors.append("Limited specificity")
            uncertainty_penalty += 15
            
        if context_richness < 45:
            uncertainty_factors.append("Limited contextual detail")
            uncertainty_penalty += 12
            
        if generic_positive_hits >= 2 and specificity_score < 40:
            uncertainty_factors.append("Generic wording")
            uncertainty_penalty += 10
            
        if specificity_score < 30 or evidence_score < 45:
            uncertainty_factors.append("Weak experiential evidence")
            uncertainty_penalty += 15
            
        if abs(sentiment_score) > 0.82 and contrast_hits == 0:
            uncertainty_factors.append("Strongly one-sided sentiment")
            uncertainty_penalty += 8

        is_low_evidence = (
            (word_count < 20 and contrast_hits == 0) or
            word_count < 15 or
            (specificity_score < 32 and contrast_hits == 0) or
            (specificity_score < 24 and contrast_hits == 0) or
            (specificity_score < 16) or
            (evidence_score < 48 and contrast_hits == 0) or
            (evidence_score < 36)
        )
        if is_low_evidence:
            strength = "Low"
            trust_ceiling = 78
        elif (evidence_score >= 64 and word_count >= 25) or (evidence_score >= 54 and named_entity_hits >= 1 and detail_hits >= 3 and word_count >= 22):
            strength = "Strong"
            trust_ceiling = 98
        else:
            strength = "Moderate"
            trust_ceiling = 90

        return EvidenceProfile(
            strength=strength,
            evidence_score=max(0, min(100, evidence_score)),
            specificity_score=specificity_score,
            context_richness=context_richness,
            maturity_score=maturity_score,
            uncertainty_penalty=min(60, uncertainty_penalty),
            trust_ceiling=trust_ceiling,
            uncertainty_factors=uncertainty_factors,
        )

