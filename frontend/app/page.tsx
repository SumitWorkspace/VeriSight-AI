import Link from "next/link";
import { ArrowRight, CheckCircle2, Shield, TextSearch } from "lucide-react";
import { PageShell } from "@/components/PageShell";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

const features = [
  {
    title: "Trust scoring",
    description: "Classify reviews as genuine or suspicious with a clear confidence score."
  },
  {
    title: "Explainability",
    description: "Highlight promotional wording, repeated language, and intensity signals directly in the review."
  },
  {
    title: "History",
    description: "Keep a searchable record of reviewed text and model decisions."
  }
];

export default function Home() {
  return (
    <PageShell>
      <section className="grid min-h-[calc(100vh-12rem)] items-center gap-10 py-8 lg:grid-cols-[1fr_0.88fr]">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 rounded-md border border-zinc-200 bg-white px-2.5 py-1 text-xs font-medium text-zinc-600 dark:border-[#222222] dark:bg-[#111111] dark:text-zinc-400">
            <Shield className="h-3.5 w-3.5" aria-hidden />
            Review trust analysis
          </div>
          <h1 className="mt-5 text-4xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-50 sm:text-5xl">
            Analyze online reviews with AI-powered trust scoring.
          </h1>
          <p className="mt-5 max-w-xl text-base leading-7 text-zinc-600 dark:text-zinc-400">
            Identify suspicious language patterns and deceptive review behavior instantly with a focused, explainable review analysis workflow.
          </p>
          <div className="mt-7 flex flex-col gap-3 sm:flex-row">
            <Link href="/analyzer">
              <Button variant="primary">
                Open analyzer
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Button>
            </Link>
          </div>
        </div>

        <Card className="p-4">
          <div className="rounded-md border border-zinc-200 bg-zinc-50 p-4 dark:border-[#222222] dark:bg-[#0a0a0a]">
            <div className="flex items-center justify-between border-b border-zinc-200 pb-3 dark:border-[#222222]">
              <div>
                <p className="text-sm font-medium text-zinc-950 dark:text-zinc-50">Analysis preview</p>
                <p className="mt-1 text-xs text-zinc-500">Example output</p>
              </div>
              <span className="rounded-md border border-emerald-200 bg-emerald-50 px-2 py-1 text-xs font-medium text-emerald-700 dark:border-emerald-950 dark:bg-emerald-950/30 dark:text-emerald-300">
                Low Risk
              </span>
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              {[
                ["Trust", "84/100"],
                ["Confidence", "83.2%"],
                ["Sentiment", "Neutral"]
              ].map(([label, value]) => (
                <div key={label} className="rounded-md border border-zinc-200 bg-white p-3 dark:border-[#222222] dark:bg-[#111111]">
                  <p className="text-xs text-zinc-500">{label}</p>
                  <p className="mt-1 text-sm font-semibold text-zinc-950 dark:text-zinc-50">{value}</p>
                </div>
              ))}
            </div>
            <p className="mt-4 rounded-md border border-zinc-200 bg-white p-3 text-sm leading-6 text-zinc-700 dark:border-[#222222] dark:bg-[#111111] dark:text-zinc-300">
              The product arrived quickly and matched the listing. Battery life was slightly lower than advertised, but performance was consistent.
            </p>
          </div>
        </Card>
      </section>

      <section className="grid gap-4 border-t border-zinc-200 py-10 dark:border-[#222222] md:grid-cols-3">
        {features.map((feature) => (
          <Card key={feature.title} className="p-5">
            <CheckCircle2 className="h-5 w-5 text-emerald-600 dark:text-emerald-400" aria-hidden />
            <h2 className="mt-4 text-sm font-semibold text-zinc-950 dark:text-zinc-50">{feature.title}</h2>
            <p className="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">{feature.description}</p>
          </Card>
        ))}
      </section>

      <section className="border-t border-zinc-200 py-10 dark:border-[#222222]">
        <Card className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-3">
            <TextSearch className="mt-0.5 h-5 w-5 text-zinc-500" aria-hidden />
            <div>
              <h2 className="text-sm font-semibold text-zinc-950 dark:text-zinc-50">Built for review triage</h2>
              <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">No fake metrics, no marketing clutter. Just analysis, explanations, and history.</p>
            </div>
          </div>
          <Link href="/analyzer">
            <Button variant="primary">Try a review</Button>
          </Link>
        </Card>
      </section>
    </PageShell>
  );
}
