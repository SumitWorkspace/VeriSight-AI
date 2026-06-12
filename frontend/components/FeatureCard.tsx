import type { LucideIcon } from "lucide-react";

type FeatureCardProps = {
  icon: LucideIcon;
  title: string;
  description: string;
};

export function FeatureCard({ icon: Icon, title, description }: FeatureCardProps) {
  return (
    <section className="group rounded-lg border border-white/60 bg-white/64 p-5 shadow-sm backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:bg-white/82 hover:shadow-soft dark:border-white/10 dark:bg-slate-900/58 dark:hover:bg-slate-900/82">
      <div className="grid h-10 w-10 place-items-center rounded-lg bg-slate-950 text-white transition duration-300 group-hover:scale-105 dark:bg-teal-300 dark:text-slate-950">
        <Icon className="h-5 w-5" aria-hidden />
      </div>
      <h3 className="mt-4 font-semibold text-slate-950 dark:text-white">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{description}</p>
    </section>
  );
}
