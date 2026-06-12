import { Loader2 } from "lucide-react";

type LoadingOverlayProps = {
  show: boolean;
  label?: string;
};

export function LoadingOverlay({ show, label = "Analyzing review signals" }: LoadingOverlayProps) {
  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-slate-950/20 p-4 backdrop-blur-sm dark:bg-slate-950/45">
      <div className="w-full max-w-sm rounded-lg border border-white/60 bg-white/86 p-6 text-center shadow-2xl backdrop-blur-2xl dark:border-white/10 dark:bg-slate-900/90">
        <div className="mx-auto grid h-14 w-14 place-items-center rounded-lg bg-gradient-to-br from-teal-300 to-cyan-500 text-slate-950">
          <Loader2 className="h-7 w-7 animate-spin" aria-hidden />
        </div>
        <p className="mt-4 font-semibold text-slate-950 dark:text-white">{label}</p>
        <div className="mt-4 space-y-2">
          <div className="h-2 animate-pulse rounded-full bg-slate-200 dark:bg-slate-700" />
          <div className="mx-auto h-2 w-2/3 animate-pulse rounded-full bg-slate-200 dark:bg-slate-700" />
        </div>
      </div>
    </div>
  );
}
