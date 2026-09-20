"use client";

import { useState } from "react";
import { Quote, ChevronDown } from "lucide-react";
import type { Evidence } from "@/lib/types";
import { cn } from "@/lib/utils";

export function EvidenceChip({ evidence }: { evidence: Evidence }) {
  const [open, setOpen] = useState(false);
  if (!evidence?.text) return null;
  return (
    <div className="inline-block w-full">
      <button
        onClick={() => setOpen((v) => !v)}
        className={cn(
          "flex items-center gap-2 text-xs px-2 py-1 rounded-md border transition",
          "border-indigo-500/30 bg-indigo-500/10 text-indigo-300 hover:bg-indigo-500/20"
        )}
      >
        <Quote size={12} />
        <span>Evidence</span>
        <ChevronDown
          size={12}
          className={cn("transition", open && "rotate-180")}
        />
      </button>
      {open && (
        <div className="mt-2 text-xs p-3 rounded-md border border-slate-700 bg-slate-900/60">
          <p className="text-slate-200 italic">&ldquo;{evidence.text}&rdquo;</p>
          <p className="mt-2 text-slate-500">
            {evidence.source}
            {evidence.page ? ` · page ${evidence.page}` : ""}
            {evidence.line ? ` · line ${evidence.line}` : ""}
          </p>
        </div>
      )}
    </div>
  );
}