import type { Prediction } from "@/lib/api";
import { highlightSuspiciousText } from "@/lib/explainability";
import { Card } from "@/components/ui/Card";

export function AnalyzerResult({ review, result }: { review: string; result: Prediction | null }) {
  if (!result) {
    return (
      <Card className="p-5">
        <p className="text-sm font-medium text-zinc-950 dark:text-zinc-50">No analysis yet</p>
        <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">Submit a review to see trust score, sentiment, and highlighted indicators.</p>
      </Card>
    );
  }

  const trustScore = result.trust_score ?? 50;
  const indicators = result.indicators;
  const phrases = result.suspicious_phrases;
  const evidenceStrength = result.evidence_strength ?? "Low";
  const confidenceReason = result.confidence_reason ?? "Limited evidence available.";
  const uncertaintyFactors = result.uncertainty_factors ?? [];
  const calibrationMetrics = [
    ["Evidence", result.evidence_score],
    ["Specificity", result.specificity_score],
    ["Context", result.context_richness],
    ["Maturity", result.maturity_score],
    ["Penalty", result.uncertainty_penalty],
    ["Ceiling", result.trust_ceiling]
  ].filter(([, value]) => typeof value === "number");

  return (
    <Card className="overflow-hidden">
      <div className="grid border-b border-zinc-200 dark:border-[#222222] sm:grid-cols-4">
        {[
          ["Trust Score", `${trustScore}/100`],
          ["Risk Level", result.risk_level ?? result.prediction],
          ["Confidence", `${result.confidence.toFixed(1)}%`],
          ["Evidence", evidenceStrength]
        ].map(([label, value]) => (
          <div key={label} className="border-b border-zinc-200 p-4 last:border-b-0 dark:border-[#222222] sm:border-b-0 sm:border-r sm:last:border-r-0">
            <p className="text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-500">{label}</p>
            <p className="mt-2 text-lg font-semibold text-zinc-950 dark:text-zinc-50">{value}</p>
          </div>
        ))}
      </div>

      <div className="grid gap-6 p-5 lg:grid-cols-[1fr_0.8fr]">
        <div>
          <h2 className="text-sm font-semibold text-zinc-950 dark:text-zinc-50">Highlighted review</h2>
          <p
            className="mt-3 whitespace-pre-wrap rounded-md border border-zinc-200 bg-zinc-50 p-4 text-sm leading-7 text-zinc-800 dark:border-[#222222] dark:bg-[#0a0a0a] dark:text-zinc-200"
            dangerouslySetInnerHTML={{ __html: highlightSuspiciousText(review, phrases) }}
          />
        </div>

        <div>
          <h2 className="text-sm font-semibold text-zinc-950 dark:text-zinc-50">Suspicious indicators</h2>
          <div className="mt-3 space-y-3">
            {indicators.length ? (
              indicators.map((indicator) => (
                <div key={indicator.label} className="rounded-md border border-zinc-200 p-3 dark:border-[#222222]">
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-sm font-medium text-zinc-950 dark:text-zinc-50">{indicator.label}</p>
                    <span className={`text-xs capitalize ${indicator.kind === "trust" ? "text-emerald-600 dark:text-emerald-400" : "text-zinc-500"}`}>{indicator.severity}</span>
                  </div>
                  <p className="mt-1 text-sm leading-5 text-zinc-600 dark:text-zinc-400">{indicator.detail}</p>
                </div>
              ))
            ) : (
              <p className="rounded-md border border-zinc-200 p-3 text-sm text-zinc-600 dark:border-[#222222] dark:text-zinc-400">No strong risk indicators were detected. Positive sentiment alone is not treated as suspicious.</p>
            )}
          </div>

          <div className="mt-5">
            <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">Confidence reasoning</p>
            <p className="mt-2 rounded-md border border-zinc-200 p-3 text-sm leading-5 text-zinc-600 dark:border-[#222222] dark:text-zinc-400">
              {confidenceReason}
            </p>
            {uncertaintyFactors.length ? (
              <div className="mt-2 flex flex-wrap gap-2">
                {uncertaintyFactors.map((factor) => (
                  <span key={factor} className="rounded-md border border-zinc-200 px-2 py-1 text-xs text-zinc-600 dark:border-[#222222] dark:text-zinc-400">
                    {factor}
                  </span>
                ))}
              </div>
            ) : null}
          </div>

          {calibrationMetrics.length ? (
            <div className="mt-5">
              <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">Calibration metrics</p>
              <div className="mt-2 grid grid-cols-2 gap-2">
                {calibrationMetrics.map(([label, value]) => (
                  <div key={label} className="rounded-md border border-zinc-200 p-2 dark:border-[#222222]">
                    <p className="text-xs text-zinc-500">{label}</p>
                    <p className="text-sm font-semibold text-zinc-950 dark:text-zinc-50">{value}</p>
                  </div>
                ))}
              </div>
            </div>
          ) : null}

          <div className="mt-5">
            <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">Suspicious phrases found</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {(phrases.length ? phrases : ["None"]).map((phrase) => (
                <span key={phrase} className="rounded-md border border-zinc-200 px-2 py-1 text-xs text-zinc-600 dark:border-[#222222] dark:text-zinc-400">
                  {phrase}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}
