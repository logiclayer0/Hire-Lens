"use client";

import { useEffect, useState } from "react";
import { CandidateCard } from "@/components/CandidateCard";
import { api } from "@/lib/api";
import type { CandidateMatch } from "@/lib/types";

export default function CandidatesPage() {
  const [candidates, setCandidates] = useState<CandidateMatch[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .listCandidates()
      .then((r) => setCandidates(r.candidates))
      .catch(() => setCandidates([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Ranked Candidates</h1>
          <p className="text-slate-400 text-sm">
            {candidates.length} candidate(s) · ranked by evidence-backed match
          </p>
        </div>
        <button
          onClick={() => api.match().then(() => window.location.reload())}
          className="px-4 py-2 rounded-lg border border-slate-700 hover:border-indigo-500 text-sm"
        >
          Re-run matching
        </button>
      </header>

      {loading ? (
        <p className="text-slate-400">Loading…</p>
      ) : candidates.length === 0 ? (
        <p className="text-slate-400">
          No candidates yet. Upload resumes first.
        </p>
      ) : (
        <div className="grid gap-4">
          {candidates.map((c) => (
            <CandidateCard key={c.candidate_id} match={c} />
          ))}
        </div>
      )}
    </div>
  );
}