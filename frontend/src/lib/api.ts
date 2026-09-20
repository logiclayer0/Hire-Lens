import type {
  CandidateMatch,
  CandidateProfile,
  EvaluationReport,
  InterviewKit,
  QueryResponse,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`API ${res.status}: ${detail}`);
  }
  return (await res.json()) as T;
}

export const api = {
  async uploadJD(file: File) {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${BASE}/api/upload/jd`, {
      method: "POST",
      body: form,
    });
    return handle<any>(res);
  },

  async uploadResumes(files: File[]) {
    const form = new FormData();
    files.forEach((f) => form.append("files", f));
    const res = await fetch(`${BASE}/api/upload/resumes`, {
      method: "POST",
      body: form,
    });
    return handle<any>(res);
  },

  async status() {
    const res = await fetch(`${BASE}/api/upload/status`, { cache: "no-store" });
    return handle<{
      jd_loaded: boolean;
      jd_title?: string;
      candidates_loaded: number;
    }>(res);
  },

  async reset() {
    const res = await fetch(`${BASE}/api/upload/reset`, { method: "DELETE" });
    return handle<any>(res);
  },

  async match() {
    const res = await fetch(`${BASE}/api/candidates/match`, { method: "POST" });
    return handle<{ status: string; count: number }>(res);
  },

  async listCandidates() {
    const res = await fetch(`${BASE}/api/candidates`, { cache: "no-store" });
    return handle<{ count: number; candidates: CandidateMatch[] }>(res);
  },

  async getCandidate(id: string) {
    const res = await fetch(`${BASE}/api/candidates/${id}`, {
      cache: "no-store",
    });
    return handle<CandidateMatch>(res);
  },

  async ask(question: string) {
    const res = await fetch(`${BASE}/api/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    return handle<QueryResponse>(res);
  },

  async questions(candidateId: string) {
    const res = await fetch(`${BASE}/api/interview/questions/${candidateId}`, {
      cache: "no-store",
    });
    return handle<InterviewKit>(res);
  },

  async evaluate(candidateId: string, notes: string) {
    const res = await fetch(`${BASE}/api/interview/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ candidate_id: candidateId, notes }),
    });
    return handle<EvaluationReport>(res);
  },
};