"use client";

import { Moon, Sun } from "lucide-react";

type ThemeToggleProps = {
  darkMode: boolean;
  onToggle: () => void;
};

export function ThemeToggle({ darkMode, onToggle }: ThemeToggleProps) {
  return (
    <button
      type="button"
      onClick={onToggle}
      className="inline-flex h-8 w-8 items-center justify-center rounded-md border border-zinc-200 bg-white text-zinc-700 transition hover:bg-zinc-50 dark:border-[#222222] dark:bg-[#111111] dark:text-zinc-300 dark:hover:bg-[#181818]"
      aria-label="Toggle dark mode"
      title="Toggle dark mode"
    >
      {darkMode ? <Sun className="h-4 w-4 transition group-hover:rotate-12" aria-hidden /> : <Moon className="h-4 w-4 transition group-hover:-rotate-12" aria-hidden />}
    </button>
  );
}
