export type SuspiciousIndicator = {
  label: string;
  detail: string;
  severity: "low" | "medium" | "high" | "positive";
};

const promotionalPhrases = [
  "best ever",
  "must buy",
  "perfect",
  "life changing",
  "highly recommend",
  "unbelievable",
  "five stars",
  "amazing product",
  "worth every penny"
];

export function getSuspiciousPhrases(review: string): string[] {
  const normalized = review.toLowerCase();
  return promotionalPhrases.filter((phrase) => normalized.includes(phrase));
}

export function getSuspiciousIndicators(review: string): SuspiciousIndicator[] {
  const phrases = getSuspiciousPhrases(review);
  const exclamationCount = (review.match(/!/g) ?? []).length;
  const repeatedWords = review.toLowerCase().match(/\b(\w+)\b(?=.*\b\1\b)/g) ?? [];
  const indicators: SuspiciousIndicator[] = [];

  if (phrases.length) {
    indicators.push({
      label: "Promotional wording",
      detail: `${phrases.length} phrase${phrases.length === 1 ? "" : "s"} commonly seen in exaggerated reviews.`,
      severity: phrases.length > 2 ? "high" : "medium"
    });
  }

  if (exclamationCount >= 2) {
    indicators.push({
      label: "Emotional intensity",
      detail: "Multiple exclamation marks may indicate inflated enthusiasm.",
      severity: exclamationCount > 4 ? "high" : "medium"
    });
  }

  if (new Set(repeatedWords).size >= 5) {
    indicators.push({
      label: "Repeated language",
      detail: "The review repeats several terms, which can reduce naturalness.",
      severity: "low"
    });
  }

  return indicators;
}

export function getTrustScore(prediction: string, confidence: number, explicitScore?: number | null): number {
  if (typeof explicitScore === "number") {
    // Hard cap all scores at 97 to avoid deterministic perfect certitude (Requirement 1)
    return Math.min(97, Math.max(21, explicitScore));
  }
  // Calibrated fallbacks that compress extremes and avoid 0, 100, 98, 2 (Requirement 3)
  if (prediction === "High Risk" || prediction === "Fake") {
    return Math.max(23, Math.min(47, Math.round(50 - confidence * 0.25)));
  }
  if (prediction === "Low Risk" || prediction === "Genuine") {
    return Math.max(72, Math.min(85, Math.round(70 + confidence * 0.15)));
  }
  return 65; // Realistic neutral middle value
}

export function highlightSuspiciousText(review: string, backendPhrases: string[] = []): string {
  let output = review;
  const phrases = Array.from(new Set([...getSuspiciousPhrases(review), ...backendPhrases]));
  for (const phrase of phrases) {
    const regex = new RegExp(`(${phrase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`, "gi");
    output = output.replace(regex, '<mark class="review-highlight">$1</mark>');
  }
  return output;
}
