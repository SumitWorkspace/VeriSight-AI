import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "danger";
  children: ReactNode;
};

export function Button({ variant = "secondary", className = "", children, ...props }: ButtonProps) {
  const variants = {
    primary: "border-zinc-950 bg-zinc-950 text-white hover:bg-zinc-800 dark:border-zinc-50 dark:bg-zinc-50 dark:text-zinc-950 dark:hover:bg-zinc-200",
    secondary: "border-zinc-200 bg-white text-zinc-800 hover:bg-zinc-50 dark:border-[#222222] dark:bg-[#111111] dark:text-zinc-100 dark:hover:bg-[#181818]",
    danger: "border-red-200 bg-red-50 text-red-700 hover:bg-red-100 dark:border-red-950 dark:bg-red-950/40 dark:text-red-300 dark:hover:bg-red-950/70"
  };

  return (
    <button
      className={`inline-flex h-9 items-center justify-center gap-2 rounded-md border px-3.5 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50 ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
