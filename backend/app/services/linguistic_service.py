from __future__ import annotations

import re
from dataclasses import dataclass


PROMOTIONAL_PHRASES = (
    "best ever",
    "must buy",
    "five stars",
    "worth every penny",
    "worth every single penny",
    "life changing",
    "everyone must",
    "highly recommend to everyone",
    "changed my life",
    "absolutely amazing",
    "simply flawless",
    "outstanding quality",
    "unbelievable price",
    "do not hesitate",
    "don't hesitate",
    "book them today",
    "book now",
    "buy it right now",
    "buy now",
    "won't regret",
    "wont regret",
    "hands down",
    "best service ever",
    "unbelievable quality",
    "perfect support",
    "amazing product",
    "incredible and perfect",
    "perfect service",
    "magical and perfect",
    "unbelievable service",
    "best customer support",
    "best hotel ever",
)

GENERIC_RECOMMENDATIONS = (
    "highly recommend",
    "recommend to everyone",
    "must try",
    "don't miss",
    "highly recommend this",
    "recommend it to everyone",
)

SUPERLATIVES = {
    "best",
    "perfect",
    "flawless",
    "unbelievable",
    "amazing",
    "magical",
    "outstanding",
    "excellent",
    "incredible",
}


@dataclass(frozen=True)
class LinguisticFeatures:
    word_count: int
    lexical_diversity: float
    exclamation_count: int
    all_caps_count: int
    repeated_word_count: int
    repeated_phrase_count: int
    promotional_phrase_count: int
    generic_recommendation_count: int
    superlative_count: int
    has_specific_details: bool
    review_length_category: str
    promotional_phrases: list[str]
    generic_phrases: list[str]


class LinguisticAnalysisService:
    detail_patterns = (
        r"\b\d+\b",
        r"\b(room|rooms|staff|breakfast|buffet|service|parking|noise|bed|bathroom|location|music|ambience|check-in|checkout|lobby|wifi|view|ac|shower|pool|gym|restaurant|desk|reception|manager|door|window|street|noisy|loud|quiet|pillow|pillows|sheet|sheets|blanket|blankets|towel|towels|soap|shampoo|toilet|elevator|corridor|hallway|balcony|patio|stay|night|screen|software|charging|charger|ports|cable|package|adapter|device|devices|battery|case|button|buttons|keys|keyboard|mouse|laptop|phone|tablet|sound|bass|volume|display|processor|memory|storage|speed|tactile|switches|bluetooth|unboxing|box|packaging|hub|monitor|stand|mount|port|cleaner|steak|fries|cheeseburger|burger|tikka|masala|naan|samosas|curry|dining|food|drink|drinks|beer|wine|menu|chef|waiter|waitress|table|sauce|taste|flavor|spicy|sweet|delicious|served|lasagna|garlic|knots|lunch|dinner|delivery|shipping|pizza|crust|slice|sushi|tuna|roll|pasta|haircut|salon|trim|trimming|layers|mechanic|oil|brake|pads|brakes|car|wash|vacuum|vacuuming|seat|seats|steel|mesh|sink|rust|water|flow|drain|tool|material|plastic|metal|wood|size|weight|sturdy|clean|crowded)\b",
    )

    def analyze(self, review: str) -> LinguisticFeatures:
        normalized = re.sub(r"\s+", " ", review.lower()).strip()
        words = re.findall(r"\b[a-zA-Z']+\b", normalized)
        word_count = len(words)
        unique_words = len(set(words))
        lexical_diversity = round(unique_words / word_count, 3) if word_count else 0.0
        exclamation_count = review.count("!")
        all_caps_count = len(re.findall(r"\b[A-Z]{3,}\b", review))
        repeated_word_count = self._count_repeated_words(words)
        repeated_phrase_count = self._count_repeated_phrases(words)
        promotional_phrases = [phrase for phrase in PROMOTIONAL_PHRASES if phrase in normalized]
        generic_phrases = [phrase for phrase in GENERIC_RECOMMENDATIONS if phrase in normalized]
        superlative_count = sum(1 for word in words if word in SUPERLATIVES)
        has_specific_details = any(re.search(pattern, normalized) for pattern in self.detail_patterns)

        if word_count < 8:
            length_category = "very_short"
        elif word_count < 25:
            length_category = "short"
        elif word_count > 180:
            length_category = "long"
        else:
            length_category = "normal"

        return LinguisticFeatures(
            word_count=word_count,
            lexical_diversity=lexical_diversity,
            exclamation_count=exclamation_count,
            all_caps_count=all_caps_count,
            repeated_word_count=repeated_word_count,
            repeated_phrase_count=repeated_phrase_count,
            promotional_phrase_count=len(promotional_phrases),
            generic_recommendation_count=len(generic_phrases),
            superlative_count=superlative_count,
            has_specific_details=has_specific_details,
            review_length_category=length_category,
            promotional_phrases=promotional_phrases,
            generic_phrases=generic_phrases,
        )

    @staticmethod
    def _count_repeated_words(words: list[str]) -> int:
        repeated = 0
        for previous, current in zip(words, words[1:]):
            if previous == current and len(current) > 2:
                repeated += 1
        return repeated

    @staticmethod
    def _count_repeated_phrases(words: list[str]) -> int:
        if len(words) < 6:
            return 0
        phrases = [" ".join(words[index : index + 3]) for index in range(len(words) - 2)]
        seen: set[str] = set()
        repeated: set[str] = set()
        for phrase in phrases:
            if phrase in seen:
                repeated.add(phrase)
            seen.add(phrase)
        return len(repeated)
