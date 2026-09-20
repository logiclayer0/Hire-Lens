import clsx, { ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function scoreColor(score: number) {
  if (score >= 75) return "text-emerald-400";
  if (score >= 50) return "text-amber-400";
  return "text-rose-400";
}

export function statusBadge(status: string) {
  switch (status) {
    case "met":
    case "covered":
      return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
    case "partial":
      return "bg-amber-500/10 text-amber-400 border-amber-500/30";
    case "missing":
    case "unanswered":
      return "bg-rose-500/10 text-rose-400 border-rose-500/30";
    default:
      return "bg-slate-500/10 text-slate-300 border-slate-500/30";
  }
}