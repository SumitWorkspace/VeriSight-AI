import type { ReactNode } from "react";

type PageShellProps = {
  children: ReactNode;
  title?: string;
  description?: string;
};

export function PageShell({ children, title, description }: PageShellProps) {
  return (
    <main className="page-enter mx-auto w-full max-w-6xl px-4 py-8 sm:px-6">
      {title ? (
        <div className="mb-8 max-w-2xl">
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-50 sm:text-3xl">{title}</h1>
          {description ? <p className="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">{description}</p> : null}
        </div>
      ) : null}
      {children}
    </main>
  );
}
