"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import type { CandidateMatch } from "@/lib/types";
import { EvidenceChip } from "@/components/EvidenceChip";
import { ScoreBadge } from "@/components/ScoreBadge";
import { statusBadge, cn } from "@/lib/utils";

export default function CandidateDetailPage() {
  const params = useParams<{ id: string }>();
  const [match, setMatch] = useState<CandidateMatch | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (!params?.id) return;
    api
      .getCandidate(params.id)
      .then(setMatch)
      .catch((e) => setError(e.message));
  }, [params?.id]);

  if (error) return <p className="text-rose-400">{error}</p>;
  if (!match) return <p className="text-slate-400">Loading…</p>;

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">{match.candidate_name}</h1>
          <p className="text-slate-400 text-sm">{match.summary}</p>
        </div>
        <ScoreBadge score={match.overall_score} />
      </header>

      <section className="space-y-3">
        <h2 className="text-lg font-medium">Requirement Breakdown</h2>
        {match.matched_requirements.map((r) => (
          <div
            key={r.requirement_id}
            className="rounded-xl border border-slate-800 bg-slate-900/40 p-4"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span
                    className={cn(
                      "text-[10px] uppercase tracking-wide px-2 py-0.5 rounded border",
                      statusBadge(r.status)
                    )}
                  >
                    {r.status}
                  </span>
                  <span className="text-[10px] uppercase tracking-wide text-slate-500">
                    {r.category}
                  </span>
                </div>
                <p className="mt-2 text-slate-200">{r.requirement_text}</p>
                <p className="mt-1 text-sm text-slate-400">{r.reasoning}</p>
              </div>
              <span className="text-sm text-slate-400">
                {r.score.toFixed(0)}/100
              </span>
            </div>
            {r.evidence.length > 0 && (
              <div className="mt-3 flex flex-col gap-2">
                {r.evidence.map((e, i) => (
                  <EvidenceChip key={i} evidence={e} />
                ))}
              </div>
            )}
          </div>
        ))}
      </section>

      <section className="grid md:grid-cols-2 gap-4">
        <List title="Strengths" items={match.strengths} tone="emerald" />
        <List
          title="Gaps to Validate"
          items={match.gaps_to_validate}
          tone="amber"
        />
        <List
          title="Missing Requirements"
          items={match.missing_requirements}
          tone="rose"
        />
      </section>
    </div>
  );
}

function List({
  title,
  items,
  tone,
}: {
  title: string;
  items: string[];
  tone: "emerald" | "amber" | "rose";
}) {
  const toneMap = {
    emerald: "border-emerald-500/30 text-emerald-300",
    amber: "border-amber-500/30 text-amber-300",
    rose: "border-rose-500/30 text-rose-300",
  } as const;
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
      <h3 className="font-medium text-slate-200">{title}</h3>
      {items.length === 0 ? (
        <p className="mt-2 text-sm text-slate-500">None</p>
      ) : (
        <ul className="mt-3 space-y-2">
          {items.map((it, i) => (
            <li
              key={i}
              className={cn(
                "text-sm border-l-2 pl-3 py-0.5",
                toneMap[tone]
              )}
            >
              {it}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}