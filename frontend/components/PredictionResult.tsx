import { Gauge, ShieldAlert, ShieldCheck, Smile } from "lucide-react";
import type { Prediction } from "@/lib/api";

export function PredictionResult({ result }: { result: Prediction | null }) {
  if (!result) {
    return (
      <section className="rounded-lg border border-dashed border-slate-300 bg-white/64 p-6 text-slate-500 dark:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400">
        Awaiting analysis
      </section>
    );
  }

  const isFake = result.prediction === "Fake";

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-soft dark:border-slate-700 dark:bg-slate-900">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Prediction</p>
          <div className="mt-2 flex items-center gap-3">
            {isFake ? (
              <ShieldAlert className="h-8 w-8 text-rose-500" aria-hidden />
            ) : (
              <ShieldCheck className="h-8 w-8 text-emerald-500" aria-hidden />
            )}
            <p className="text-3xl font-semibold text-slate-950 dark:text-white">{result.prediction}</p>
          </div>
        </div>
        <span className={`rounded-full px-3 py-1 text-sm font-semibold ${isFake ? "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-200" : "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-200"}`}>
          {result.confidence.toFixed(1)}%
        </span>
      </div>

      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        <div className="flex items-center gap-3 rounded-lg bg-slate-100 p-4 dark:bg-slate-800">
          <Gauge className="h-5 w-5 text-cyan-600 dark:text-cyan-300" aria-hidden />
          <div>
            <p className="text-xs font-medium uppercase text-slate-500 dark:text-slate-400">Confidence</p>
            <p className="font-semibold text-slate-900 dark:text-white">{result.confidence.toFixed(2)}%</p>
          </div>
        </div>
        <div className="flex items-center gap-3 rounded-lg bg-slate-100 p-4 dark:bg-slate-800">
          <Smile className="h-5 w-5 text-amber-600 dark:text-amber-300" aria-hidden />
          <div>
            <p className="text-xs font-medium uppercase text-slate-500 dark:text-slate-400">Sentiment</p>
            <p className="font-semibold text-slate-900 dark:text-white">{result.sentiment}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
