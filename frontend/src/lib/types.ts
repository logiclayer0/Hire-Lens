export type Evidence = {
  text: string;
  source: string;
  page?: number | null;
  line?: number | null;
};

export type SkillItem = {
  skill: string;
  evidence: Evidence;
  confidence: "high" | "medium" | "low";
};

export type CandidateProfile = {
  candidate_id: string;
  name: string;
  email: string;
  phone: string;
  location: string;
  total_experience_years: number;
  summary: string;
  skills: SkillItem[];
  experiences: any[];
  projects: any[];
  education: any[];
  resume_filename: string;
};

export type RequirementMatch = {
  requirement_id: string;
  requirement_text: string;
  category: string;
  status: "met" | "partial" | "missing";
  score: number;
  reasoning: string;
  evidence: Evidence[];
  confidence: "high" | "medium" | "low";
};

export type CandidateMatch = {
  candidate_id: string;
  candidate_name: string;
  overall_score: number;
  rank: number;
  matched_requirements: RequirementMatch[];
  missing_requirements: string[];
  gaps_to_validate: string[];
  strengths: string[];
  summary: string;
};

export type InterviewQuestion = {
  question: string;
  category: "verify" | "probe_gap" | "depth" | "behavioral";
  target_requirement: string;
  evidence?: Evidence | null;
};

export type InterviewKit = {
  candidate_id: string;
  candidate_name: string;
  questions: InterviewQuestion[];
};

export type EvaluationArea = {
  requirement_id: string;
  requirement_text: string;
  status: "covered" | "partial" | "unanswered";
  notes: string;
};

export type EvaluationReport = {
  candidate_id: string;
  candidate_name: string;
  overall_recommendation: "strong_yes" | "yes" | "maybe" | "no";
  areas: EvaluationArea[];
  unanswered_areas: string[];
  summary: string;
};

export type QuerySource = {
  candidate_id: string;
  candidate_name: string;
  snippet: string;
  source: string;
};

export type QueryResponse = {
  answer: string;
  sources: QuerySource[];
  matched_candidate_ids: string[];
};