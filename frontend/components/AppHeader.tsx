"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ShieldCheck } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useTheme } from "@/hooks/useTheme";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/analyzer", label: "Analyzer" },
  { href: "/settings", label: "Settings" }
];

export function AppHeader() {
  const pathname = usePathname();
  const { darkMode, setDarkMode } = useTheme();

  return (
    <header className="sticky top-0 z-40 border-b border-zinc-200 bg-white/85 backdrop-blur-xl dark:border-[#222222] dark:bg-[#0a0a0a]/85">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="flex h-14 items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <span className="grid h-8 w-8 place-items-center rounded-md border border-zinc-200 bg-zinc-950 text-white dark:border-[#222222] dark:bg-[#111111]">
              <ShieldCheck className="h-4 w-4" aria-hidden />
            </span>
            <span className="text-sm font-semibold tracking-tight text-zinc-950 dark:text-zinc-50">VeriSight AI</span>
          </Link>

          <nav className="hidden items-center gap-1 rounded-md border border-zinc-200 bg-zinc-50 p-1 dark:border-[#222222] dark:bg-[#111111] sm:flex">
            {navItems.map((item) => {
              const active = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`rounded px-3 py-1.5 text-sm transition ${
                    active
                      ? "bg-white text-zinc-950 shadow-sm dark:bg-[#1a1a1a] dark:text-zinc-50"
                      : "text-zinc-600 hover:text-zinc-950 dark:text-zinc-400 dark:hover:text-zinc-100"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>

          <ThemeToggle darkMode={darkMode} onToggle={() => setDarkMode((value) => !value)} />
        </div>

        <nav className="flex gap-1 overflow-x-auto border-t border-zinc-200 py-2 dark:border-[#222222] sm:hidden">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`shrink-0 rounded px-3 py-1.5 text-sm transition ${
                  active ? "bg-zinc-950 text-white dark:bg-zinc-50 dark:text-zinc-950" : "text-zinc-600 dark:text-zinc-400"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
