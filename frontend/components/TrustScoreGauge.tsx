type TrustScoreGaugeProps = {
  score: number;
  label?: string;
};

export function TrustScoreGauge({ score, label = "Trust score" }: TrustScoreGaugeProps) {
  const clamped = Math.min(Math.max(score, 0), 100);

  return (
    <div className="relative grid place-items-center">
      <div
        className="grid h-36 w-36 place-items-center rounded-full transition duration-700"
        style={{
          background: `conic-gradient(#14b8a6 ${clamped * 3.6}deg, rgba(148, 163, 184, 0.22) 0deg)`
        }}
      >
        <div className="grid h-28 w-28 place-items-center rounded-full bg-white/95 shadow-inner dark:bg-slate-950/95">
          <div className="text-center">
            <p className="text-3xl font-semibold text-slate-950 dark:text-white">{Math.round(clamped)}</p>
            <p className="text-xs font-medium text-slate-500 dark:text-slate-400">{label}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
