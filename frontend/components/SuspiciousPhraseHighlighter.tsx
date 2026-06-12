const suspiciousPhrases = ["best ever", "must buy", "perfect", "life changing", "highly recommend", "unbelievable", "five stars", "amazing product"];

export function SuspiciousPhraseHighlighter({ text }: { text: string }) {
  const matches = suspiciousPhrases.filter((phrase) => text.toLowerCase().includes(phrase));

  return (
    <section className="rounded-lg border border-white/60 bg-white/70 p-5 shadow-sm backdrop-blur-2xl dark:border-white/10 dark:bg-slate-900/70">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h3 className="font-semibold text-slate-950 dark:text-white">Suspicious phrase scan</h3>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Pattern hints used for analyst context</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-200">{matches.length}</span>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {(matches.length ? matches : ["No obvious phrase spikes"]).map((item) => (
          <span key={item} className="rounded-full border border-teal-200 bg-teal-50 px-3 py-1 text-xs font-semibold text-teal-700 dark:border-teal-500/20 dark:bg-teal-500/10 dark:text-teal-200">
            {item}
          </span>
        ))}
      </div>
    </section>
  );
}
