export type Prediction = {
  prediction: string;
  risk_level?: "Low Risk" | "Medium Risk" | "High Risk" | null;
  trust_label?: string | null;
  trust_score?: number | null;
  confidence: number;
  evidence_strength?: "Low" | "Moderate" | "Strong" | null;
  evidence_score?: number | null;
  specificity_score?: number | null;
  context_richness?: number | null;
  maturity_score?: number | null;
  uncertainty_penalty?: number | null;
  trust_ceiling?: number | null;
  confidence_reason?: string | null;
  uncertainty_factors?: string[];
  sentiment: "Positive" | "Negative" | "Neutral";
  sentiment_score: number;
  model_prediction: string;
  model_confidence: number;
  indicators: Array<{
    label: string;
    detail: string;
    impact: number;
    severity: string;
    kind: string;
  }>;
  suspicious_phrases: string[];
  features: Record<string, string | number | boolean>;
};
export type HistoryItem = Prediction & {
  review: string;
  created_at: string;
};

export type BatchPrediction = {
  count: number;
  predictions: Array<Prediction & { review: string }>;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail ?? "Request failed");
  }
  return response.json() as Promise<T>;
}

export async function predictReview(review: string): Promise<Prediction> {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ review })
  });
  return parseResponse<Prediction>(response);
}



export async function uploadBatch(file: File): Promise<BatchPrediction> {
  const data = new FormData();
  data.append("file", file);
  const response = await fetch(`${API_BASE_URL}/batch-predict`, {
    method: "POST",
    body: data
  });
  return parseResponse<BatchPrediction>(response);
}
