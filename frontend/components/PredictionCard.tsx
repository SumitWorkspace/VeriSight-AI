import { ShieldAlert, ShieldCheck, Sparkles } from "lucide-react";
import type { Prediction } from "@/lib/api";
import { ConfidenceMeter } from "@/components/ConfidenceMeter";
import { TrustScoreGauge } from "@/components/TrustScoreGauge";

export function PredictionCard({ result }: { result: Prediction | null }) {
  if (!result) {
    return (
      <section className="rounded-lg border border-dashed border-slate-300/80 bg-white/55 p-6 text-slate-500 shadow-sm backdrop-blur-2xl dark:border-white/10 dark:bg-slate-900/55 dark:text-slate-400">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-lg bg-slate-100 dark:bg-slate-800">
            <Sparkles className="h-5 w-5 text-teal-500" aria-hidden />
          </div>
          <div>
            <p className="font-semibold text-slate-800 dark:text-slate-100">Awaiting analysis</p>
            <p className="mt-1 text-sm">Submit an English review to generate an AI authenticity report.</p>
          </div>
        </div>
      </section>
    );
  }

  const isFake = result.prediction === "Fake";
  const trustScore = isFake ? 100 - result.confidence : result.confidence;

  return (
    <section className="overflow-hidden rounded-lg border border-white/60 bg-white/78 p-6 shadow-soft backdrop-blur-2xl dark:border-white/10 dark:bg-slate-900/78">
      <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">AI verdict</p>
          <div className="mt-3 flex items-center gap-3">
            <div className={`grid h-12 w-12 place-items-center rounded-lg ${isFake ? "bg-rose-100 text-rose-600 dark:bg-rose-950 dark:text-rose-200" : "bg-emerald-100 text-emerald-600 dark:bg-emerald-950 dark:text-emerald-200"}`}>
              {isFake ? <ShieldAlert className="h-6 w-6" aria-hidden /> : <ShieldCheck className="h-6 w-6" aria-hidden />}
            </div>
            <div>
              <p className="text-3xl font-semibold tracking-normal text-slate-950 dark:text-white">{result.prediction}</p>
              <p className="text-sm text-slate-500 dark:text-slate-400">Sentiment: {result.sentiment}</p>
            </div>
          </div>
        </div>
        <TrustScoreGauge score={trustScore} />
      </div>
      <div className="mt-6">
        <ConfidenceMeter value={result.confidence} />
      </div>
    </section>
  );
}
