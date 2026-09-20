"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type {
  CandidateMatch,
  EvaluationReport,
  InterviewKit,
} from "@/lib/types";
import { EvidenceChip } from "@/components/EvidenceChip";

export default function InterviewPage() {
  const [candidates, setCandidates] = useState<CandidateMatch[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [kit, setKit] = useState<InterviewKit | null>(null);
  const [notes, setNotes] = useState("");
  const [report, setReport] = useState<EvaluationReport | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api
      .listCandidates()
      .then((r) => setCandidates(r.candidates))
      .catch(() => setCandidates([]));
  }, []);

  async function loadQuestions() {
    if (!selected) return;
    setLoading(true);
    try {
      setKit(await api.questions(selected));
      setReport(null);
    } finally {
      setLoading(false);
    }
  }

  async function evaluate() {
    if (!selected || !notes.trim()) return;
    setLoading(true);
    try {
      setReport(await api.evaluate(selected, notes));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Interview Intelligence</h1>
        <p className="text-slate-400 text-sm">
          Generate questions, capture notes, get a structured evaluation.
        </p>
      </header>

      <div className="flex gap-2 items-center">
        <select
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
          className="rounded-lg border border-slate-700 bg-slate-900/40 px-3 py-2 text-sm"
        >
          <option value="">Select candidate…</option>
          {candidates.map((c) => (
            <option key={c.candidate_id} value={c.candidate_id}>
              {c.candidate_name}
            </option>
          ))}
        </select>
        <button
          onClick={loadQuestions}
          disabled={!selected || loading}
          className="px-4 py-2 rounded-lg bg-indigo-500 hover:bg-indigo-400 text-white text-sm disabled:opacity-50"
        >
          Generate Questions
        </button>
      </div>

      {kit && (
        <section className="rounded-xl border border-slate-800 bg-slate-900/40 p-5 space-y-3">
          <h2 className="font-medium text-slate-200">Interview Kit</h2>
          {kit.questions.map((q, i) => (
            <div key={i} className="border-l-2 border-indigo-500/40 pl-3">
              <div className="text-[10px] uppercase tracking-wide text-indigo-400">
                {q.category} · {q.target_requirement}
              </div>
              <p className="text-slate-200 mt-1">{q.question}</p>
              {q.evidence && (
                <div className="mt-2">
                  <EvidenceChip evidence={q.evidence} />
                </div>
              )}
            </div>
          ))}
        </section>
      )}

      <section className="space-y-3">
        <h2 className="font-medium text-slate-200">Interview Notes</h2>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows={6}
          placeholder="Paste raw interview notes here…"
          className="w-full rounded-lg border border-slate-700 bg-slate-900/40 px-3 py-2 text-sm outline-none focus:border-indigo-500"
        />
        <button
          onClick={evaluate}
          disabled={!selected || !notes.trim() || loading}
          className="px-4 py-2 rounded-lg bg-indigo-500 hover:bg-indigo-400 text-white text-sm disabled:opacity-50"
        >
          Evaluate
        </button>
      </section>

      {report && (
        <section className="rounded-xl border border-slate-800 bg-slate-900/40 p-5 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="font-medium text-slate-200">Evaluation Report</h2>
            <span className="text-xs px-2 py-1 rounded border border-indigo-500/40 text-indigo-300">
              {report.overall_recommendation}
            </span>
          </div>
          <p className="text-slate-300 text-sm">{report.summary}</p>

          <div className="space-y-2 mt-3">
            {report.areas.map((a) => (
              <div
                key={a.requirement_id}
                className="text-sm border-l-2 border-slate-700 pl-3"
              >
                <div className="text-xs text-slate-500">{a.status}</div>
                <div className="text-slate-200">{a.requirement_text}</div>
                {a.notes && (
                  <div className="text-slate-400 text-xs mt-1">{a.notes}</div>
                )}
              </div>
            ))}
          </div>

          {report.unanswered_areas.length > 0 && (
            <div className="mt-4">
              <h3 className="text-sm text-rose-400">Unanswered Areas</h3>
              <ul className="mt-2 space-y-1">
                {report.unanswered_areas.map((u, i) => (
                  <li key={i} className="text-sm text-slate-300">
                    • {u}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}
    </div>
  );
}