# HireLens — 5-Minute Demo Script

## 0:00 — Hook (30s)

"Recruiters spend 23 hours screening per hire. Worse, most AI screening tools
are black boxes — they give a score, but no explanation.

HireLens does the first pass AND shows its work. Every score links back to
the exact resume sentence it came from."

## 0:30 — Upload (30s)

- Open http://localhost:3000/upload
- Drag in `data/samples/sample_jd.txt`
- Drag in `resume_1.txt`, `resume_2.txt`, `resume_3.txt`
- Click "Upload & Analyze"

Say: "JD is parsed into atomic requirements. Each resume is parsed into a
structured profile with evidence."

## 1:00 — Ranked Candidates (60s)

- Open /candidates
- Point out the ranked list: Rahul #1, Priya #2, Amit #3
- Click Rahul → show requirement-by-requirement breakdown
- Open an Evidence chip → show the exact quoted line from his resume

Say: "Notice: nothing here is a black box. Each match cites the source line."

## 2:00 — Ask the Pool (90s)

- Open /ask
- Type: "Which candidates have led teams and worked on payments?"
- Show instant answer + cited snippets

Say: "Recruiters can query the entire pool in plain English. Every answer
includes the source snippets used to produce it."

## 3:30 — Interview Kit (60s)

- Open /interview
- Select Rahul → Generate Questions
- Show verify + probe-gap + depth questions
- Paste fake interview notes → Evaluate
- Show report with unanswered areas flagged

Say: "Interviewers get role-specific questions and a structured evaluation —
including what they still need to probe."

## 4:30 — Close (30s)

"HireLens removes busywork. Every insight is auditable. Humans stay in
control — AI just shows them where to look."

## Backup

If live demo fails, play recorded video: `assets/demo.mp4`.