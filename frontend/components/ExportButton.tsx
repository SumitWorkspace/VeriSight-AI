import { Download } from "lucide-react";
import type { HistoryItem } from "@/lib/api";

export function ExportButton({ rows }: { rows: HistoryItem[] }) {
  function exportCsv() {
    const header = ["review", "risk_level", "trust_score", "confidence", "sentiment", "created_at"];
    const body = rows.map((row) =>
      [row.review, row.risk_level || row.prediction, row.trust_score, row.confidence, row.sentiment, row.created_at].map((value) => `"${String(value).replaceAll('"', '""')}"`).join(",")
    );
    const blob = new Blob([[header.join(","), ...body].join("\n")], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "trustlens-predictions.csv";
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <button
      type="button"
      onClick={exportCsv}
      disabled={!rows.length}
      className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-white/10 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800"
    >
      <Download className="h-4 w-4" aria-hidden />
      Export
    </button>
  );
}
