"use client";

import { useEffect, useState } from "react";
import { FileUploader } from "@/components/FileUploader";
import { api } from "@/lib/api";

export default function UploadPage() {
  const [jd, setJD] = useState<File[]>([]);
  const [resumes, setResumes] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<any>(null);
  const [message, setMessage] = useState<string>("");

  async function refresh() {
    try {
      setStatus(await api.status());
    } catch {
      setStatus(null);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleUpload() {
    if (!jd.length || !resumes.length) {
      setMessage("Please upload 1 JD and at least 1 resume.");
      return;
    }
    setLoading(true);
    setMessage("Uploading JD…");
    try {
      await api.uploadJD(jd[0]);
      setMessage("Parsing resumes…");
      await api.uploadResumes(resumes);
      setMessage("Running matching…");
      await api.match();
      setMessage("✅ Ready. Go to Candidates.");
      setJD([]);
      setResumes([]);
      await refresh();
    } catch (e: any) {
      setMessage(`❌ ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleReset() {
    await api.reset();
    setMessage("Reset done.");
    await refresh();
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Upload</h1>
        <p className="text-slate-400 text-sm">
          Job description + candidate resumes.
        </p>
      </header>

      {status && (
        <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-4 text-sm text-slate-300">
          JD loaded:{" "}
          <span className="text-indigo-300">
            {status.jd_loaded ? status.jd_title : "no"}
          </span>{" "}
          · Candidates:{" "}
          <span className="text-indigo-300">{status.candidates_loaded}</span>
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        <FileUploader label="Job Description (PDF/TXT)" files={jd} onChange={setJD} />
        <FileUploader
          label="Resumes (multiple)"
          multiple
          files={resumes}
          onChange={setResumes}
        />
      </div>

      <div className="flex items-center gap-3">
        <button
          disabled={loading}
          onClick={handleUpload}
          className="px-5 py-2.5 rounded-lg bg-indigo-500 hover:bg-indigo-400 text-white text-sm font-medium disabled:opacity-50"
        >
          {loading ? "Processing…" : "Upload & Analyze"}
        </button>
        <button
          onClick={handleReset}
          className="px-4 py-2.5 rounded-lg border border-slate-700 hover:border-rose-500 text-sm"
        >
          Reset
        </button>
        {message && <span className="text-sm text-slate-300">{message}</span>}
      </div>
    </div>
  );
}