import type { ReactNode } from "react";

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <section className={`rounded-lg border border-zinc-200 bg-white dark:border-[#222222] dark:bg-[#111111] ${className}`}>{children}</section>;
}
