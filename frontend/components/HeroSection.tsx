import { ArrowRight, BadgeCheck, BrainCircuit, Radar } from "lucide-react";
import { FeatureCard } from "@/components/FeatureCard";

export function HeroSection() {
  return (
    <section className="relative overflow-hidden rounded-lg border border-white/60 bg-white/58 p-6 shadow-soft backdrop-blur-2xl dark:border-white/10 dark:bg-slate-900/58 sm:p-8">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_10%,rgba(20,184,166,0.20),transparent_28rem),radial-gradient(circle_at_80%_30%,rgba(99,102,241,0.16),transparent_24rem)]" />
      <div className="relative grid gap-8 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
        <div>
          <span className="inline-flex items-center gap-2 rounded-full border border-teal-200 bg-teal-50 px-3 py-1 text-xs font-semibold text-teal-700 dark:border-teal-500/20 dark:bg-teal-500/10 dark:text-teal-200">
            <BadgeCheck className="h-3.5 w-3.5" aria-hidden />
            RoBERTa model loaded
          </span>
          <h1 className="mt-5 max-w-3xl text-4xl font-semibold tracking-normal text-slate-950 dark:text-white sm:text-5xl">
            AI review intelligence for product trust teams.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600 dark:text-slate-300">
            Analyze English reviews with transformer classification, sentiment context, confidence scoring, and history built for a portfolio-ready SaaS demo.
          </p>
          <a
            href="#analyzer"
            className="mt-6 inline-flex items-center gap-2 rounded-lg bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-950/20 transition duration-300 hover:-translate-y-0.5 hover:bg-slate-800 dark:bg-teal-300 dark:text-slate-950 dark:hover:bg-teal-200"
          >
            Analyze review
            <ArrowRight className="h-4 w-4" aria-hidden />
          </a>
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          <FeatureCard icon={BrainCircuit} title="Transformer verdicts" description="Fine-tuned RoBERTa classification with saved model metrics." />
          <FeatureCard icon={Radar} title="Explainable heuristics" description="Trace specific risk features like repeated language, context richness, and sentiment contrast." />
        </div>
      </div>
    </section>
  );
}
