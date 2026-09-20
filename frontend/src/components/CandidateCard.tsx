"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { CandidateMatch } from "@/lib/types";
import { ScoreBadge } from "./ScoreBadge";
import { statusBadge, cn } from "@/lib/utils";

export function CandidateCard({ match }: { match: CandidateMatch }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5 hover:border-indigo-500/40 transition">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/30">
              Rank #{match.rank}
            </span>
            <h3 className="text-lg font-semibold text-slate-100">
              {match.candidate_name}
            </h3>
          </div>
          <p className="mt-1 text-sm text-slate-400">{match.summary}</p>
        </div>
        <ScoreBadge score={match.overall_score} />
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3 text-xs">
        <Stat label="Strengths" value={match.strengths.length} tone="emerald" />
        <Stat label="To Validate" value={match.gaps_to_validate.length} tone="amber" />
        <Stat label="Missing" value={match.missing_requirements.length} tone="rose" />
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {match.matched_requirements.slice(0, 4).map((r) => (
          <span
            key={r.requirement_id}
            className={cn(
              "text-xs px-2 py-1 rounded-md border",
              statusBadge(r.status)
            )}
          >
            {r.requirement_text.slice(0, 40)}
          </span>
        ))}
      </div>

      <div className="mt-5 flex justify-end">
        <Link
          href={`/candidates/${match.candidate_id}`}
          className="text-sm text-indigo-400 hover:text-indigo-300"
        >
          View evidence →
        </Link>
      </div>
    </div>
  );
}

function Stat({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: "emerald" | "amber" | "rose";
}) {
  const toneMap = {
    emerald: "text-emerald-400",
    amber: "text-amber-400",
    rose: "text-rose-400",
  } as const;
  return (
    <div className="rounded-md border border-slate-800 bg-slate-950/40 px-3 py-2">
      <div className={`text-lg font-semibold ${toneMap[tone]}`}>{value}</div>
      <div className="text-slate-500">{label}</div>
    </div>
  );
}