"use client";

import { FormEvent, useState } from "react";
import { Loader2, RotateCcw, Sparkles, Trash2 } from "lucide-react";
import { AnalyzerResult } from "@/components/AnalyzerResult";
import { PageShell } from "@/components/PageShell";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Prediction, predictReview } from "@/lib/api";

const exampleReview = "Perfect product, best ever! I highly recommend this to everyone. Five stars and worth every penny!";

export default function AnalyzerPage() {
  const [review, setReview] = useState("");
  const [result, setResult] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyze(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await predictReview(review);
      setResult(data);
      if (typeof window !== "undefined") {
        sessionStorage.setItem("verisight_last_analysis", JSON.stringify({ review, ...data }));
      }
    } catch (caught) {
      console.error(caught);
      const message = caught instanceof Error ? caught.message : "";
      if (message.toLowerCase().includes("failed to fetch") || message.toLowerCase().includes("network error") || message.toLowerCase().includes("fetch failed")) {
        setError("Unable to connect to the VeriSight AI backend. If the backend is hosted on a free tier (like Render), it may be waking up from sleep. Please wait 45-60 seconds and try again.");
      } else {
        setError(message || "Unable to analyze review. An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  }

  function clear() {
    setReview("");
    setResult(null);
    setError("");
  }

  return (
    <PageShell title="Analyzer" description="Paste an English review to generate a calibrated trust score, risk level, and explainability highlights.">
      <div className="grid gap-6 lg:grid-cols-[0.85fr_1.15fr]">
        <Card className="p-5">
          <form onSubmit={analyze}>
            <div className="flex items-center justify-between gap-4">
              <label htmlFor="review" className="text-sm font-semibold text-zinc-950 dark:text-zinc-50">
                Review text
              </label>
              <span className="text-xs text-zinc-500">{review.trim().length}/5000</span>
            </div>
            <textarea
              id="review"
              value={review}
              onChange={(event) => setReview(event.target.value)}
              maxLength={5000}
              rows={14}
              className="mt-3 w-full resize-none rounded-md border border-zinc-200 bg-zinc-50 p-3 text-sm leading-6 text-zinc-950 outline-none transition focus:border-zinc-400 focus:bg-white dark:border-[#222222] dark:bg-[#0a0a0a] dark:text-zinc-50 dark:focus:border-zinc-600"
              placeholder="Paste a review here..."
            />
            <div className="mt-4 flex flex-wrap gap-2">
              <Button variant="primary" type="submit" disabled={loading || review.trim().length < 5}>
                {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : <Sparkles className="h-4 w-4" aria-hidden />}
                Analyze
              </Button>
              <Button type="button" onClick={() => setReview(exampleReview)}>
                <RotateCcw className="h-4 w-4" aria-hidden />
                Example
              </Button>
              <Button type="button" onClick={clear}>
                <Trash2 className="h-4 w-4" aria-hidden />
                Clear
              </Button>
            </div>
            {error ? <p className="mt-4 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700 dark:border-red-950 dark:bg-red-950/30 dark:text-red-300">{error}</p> : null}
          </form>
        </Card>

        <AnalyzerResult review={review} result={result} />
      </div>
    </PageShell>
  );
}
