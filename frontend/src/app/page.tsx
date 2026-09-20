import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-10">
      <section className="pt-8">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
          Hiring intelligence that{" "}
          <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            shows its work.
          </span>
        </h1>
        <p className="mt-4 text-slate-400 max-w-2xl">
          HireLens reads job descriptions and resumes, ranks candidates with
          evidence, and generates interview questions — every insight traceable
          to a source line.
        </p>
        <div className="mt-6 flex gap-3">
          <Link
            href="/upload"
            className="px-5 py-2.5 rounded-lg bg-indigo-500 hover:bg-indigo-400 text-white text-sm font-medium transition"
          >
            Get Started
          </Link>
          <Link
            href="/candidates"
            className="px-5 py-2.5 rounded-lg border border-slate-700 hover:border-slate-500 text-sm transition"
          >
            View Candidates
          </Link>
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-4">
        {features.map((f) => (
          <div
            key={f.title}
            className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
          >
            <h3 className="font-semibold text-slate-100">{f.title}</h3>
            <p className="mt-2 text-sm text-slate-400">{f.body}</p>
          </div>
        ))}
      </section>
    </div>
  );
}

const features = [
  {
    title: "Evidence-first",
    body: "Every score links back to the exact resume sentence it came from.",
  },
  {
    title: "Gap detection",
    body: "HireLens flags what's missing and what needs validation in interviews.",
  },
  {
    title: "Interview ready",
    body: "Generates role-specific questions and evaluates post-interview notes.",
  },
];