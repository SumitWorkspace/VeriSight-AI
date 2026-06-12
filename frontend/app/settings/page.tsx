"use client";

import { useState } from "react";
import { PageShell } from "@/components/PageShell";
import { Card } from "@/components/ui/Card";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useTheme } from "@/hooks/useTheme";

export default function SettingsPage() {
  const { darkMode, setDarkMode } = useTheme();
  const [profileName, setProfileName] = useState("Review Analyst");

  return (
    <PageShell title="Settings">
      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="p-5">
          <h2 className="text-sm font-semibold text-zinc-950 dark:text-zinc-50">Theme</h2>
          <div className="mt-4 flex items-center justify-between rounded-md border border-zinc-200 p-3 dark:border-[#222222]">
            <div>
              <p className="text-sm text-zinc-950 dark:text-zinc-50">Dark mode</p>
              <p className="mt-1 text-sm text-zinc-500">Use a near-black interface.</p>
            </div>
            <ThemeToggle darkMode={darkMode} onToggle={() => setDarkMode((value) => !value)} />
          </div>
        </Card>

        <Card className="p-5">
          <h2 className="text-sm font-semibold text-zinc-950 dark:text-zinc-50">Profile</h2>
          <label htmlFor="profile" className="mt-4 block text-xs font-medium uppercase tracking-wide text-zinc-500">
            Display name
          </label>
          <input
            id="profile"
            value={profileName}
            onChange={(event) => setProfileName(event.target.value)}
            className="mt-2 h-9 w-full rounded-md border border-zinc-200 bg-zinc-50 px-3 text-sm text-zinc-950 outline-none dark:border-[#222222] dark:bg-[#0a0a0a] dark:text-zinc-50"
          />
        </Card>
      </div>
    </PageShell>
  );
}
