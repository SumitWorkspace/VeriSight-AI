"use client";

import { ChangeEvent, FormEvent } from "react";
import { FileUp, Loader2, Search, Wand2 } from "lucide-react";

type ReviewInputProps = {
  review: string;
  loading: boolean;
  batchLoading: boolean;
  error: string;
  onReviewChange: (value: string) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onFileChange: (event: ChangeEvent<HTMLInputElement>) => void;
};

export function ReviewInput({ review, loading, batchLoading, error, onReviewChange, onSubmit, onFileChange }: ReviewInputProps) {
  const reviewLength = review.trim().length;

  return (
    <form id="analyzer" onSubmit={onSubmit} className="rounded-lg border border-white/60 bg-white/78 p-6 shadow-soft backdrop-blur-2xl dark:border-white/10 dark:bg-slate-900/78">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Wand2 className="h-5 w-5 text-teal-500" aria-hidden />
            <label htmlFor="review" className="text-lg font-semibold text-slate-950 dark:text-white">Review Analyzer</label>
          </div>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Paste an English product or hotel review.</p>
        </div>
        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">{reviewLength}/5000</span>
      </div>

      <textarea
        id="review"
        value={review}
        onChange={(event) => onReviewChange(event.target.value)}
        rows={10}
        maxLength={5000}
        className="mt-5 w-full resize-none rounded-lg border border-slate-200/80 bg-white/90 p-4 text-base leading-7 text-slate-900 shadow-inner outline-none transition duration-300 placeholder:text-slate-400 focus:border-teal-400 focus:ring-4 focus:ring-teal-400/15 dark:border-white/10 dark:bg-slate-950/80 dark:text-white"
        placeholder="Paste a review to analyze..."
      />

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <button
          type="submit"
          disabled={loading || reviewLength < 5}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-950/20 transition duration-300 hover:-translate-y-0.5 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-teal-300 dark:text-slate-950 dark:hover:bg-teal-200"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : <Search className="h-4 w-4" aria-hidden />}
          Analyze Review
        </button>

        <label className="inline-flex cursor-pointer items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 shadow-sm transition duration-300 hover:-translate-y-0.5 hover:bg-slate-50 dark:border-white/10 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800">
          {batchLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : <FileUp className="h-4 w-4" aria-hidden />}
          Upload CSV
          <input type="file" accept=".csv" className="sr-only" onChange={onFileChange} />
        </label>
      </div>

      {error ? <p className="mt-4 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700 dark:border-rose-500/20 dark:bg-rose-500/10 dark:text-rose-200">{error}</p> : null}
    </form>
  );
}
