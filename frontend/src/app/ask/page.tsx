"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import type { QueryResponse } from "@/lib/types";

const SUGGESTIONS = [
  "Which candidates have led teams and worked on payments?",
  "Who has experience with Kubernetes?",
  "Which candidates are missing AWS experience?",
  "Who has the most backend experience?",
];

export default function AskPage() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function ask(q: string) {
    if (!q.trim()) return;
    setLoading(true);
    setError("");
    try {
      setResult(await api.ask(q));
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Ask the Pool</h1>
        <p className="text-slate-400 text-sm">
          Natural-language queries across all indexed candidates.
        </p>
      </header>

      <div className="flex gap-2">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && ask(question)}
          placeholder="Ask about skills, experience, gaps…"
          className="flex-1 rounded-lg border border-slate-700 bg-slate-900/40 px-4 py-2.5 text-sm outline-none focus:border-indigo-500"
        />
        <button
          onClick={() => ask(question)}
          disabled={loading}
          className="px-5 py-2.5 rounded-lg bg-indigo-500 hover:bg-indigo-400 text-white text-sm font-medium disabled:opacity-50"
        >
          {loading ? "…" : "Ask"}
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => {
              setQuestion(s);
              ask(s);
            }}
            className="text-xs px-3 py-1.5 rounded-full border border-slate-700 text-slate-400 hover:border-indigo-500 hover:text-indigo-300 transition"
          >
            {s}
          </button>
        ))}
      </div>

      {error && <p className="text-rose-400 text-sm">{error}</p>}

      {result && (
        <div className="space-y-4">
          <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
            <h2 className="text-sm uppercase tracking-wide text-indigo-400">
              Answer
            </h2>
            <p className="mt-2 text-slate-200">{result.answer}</p>
          </div>

          {result.sources.length > 0 && (
            <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
              <h2 className="text-sm uppercase tracking-wide text-slate-400">
                Sources
              </h2>
              <ul className="mt-3 space-y-3">
                {result.sources.map((s, i) => (
                  <li
                    key={i}
                    className="text-sm border-l-2 border-indigo-500/40 pl-3"
                  >
                    <div className="text-indigo-300 text-xs">
                      {s.candidate_name} · {s.source}
                    </div>
                    <p className="text-slate-300 italic mt-1">
                      &ldquo;{s.snippet}&rdquo;
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}