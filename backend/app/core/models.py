from typing import Literal, Optional
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    text: str
    source: str
    page: Optional[int] = None
    line: Optional[int] = None


class SkillItem(BaseModel):
    skill: str
    evidence: Evidence
    confidence: Literal["high", "medium", "low"] = "medium"


class ExperienceItem(BaseModel):
    title: str
    company: str
    duration: str
    description: str
    evidence: Evidence


class ProjectItem(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)
    evidence: Evidence


class EducationItem(BaseModel):
    degree: str
    institution: str
    year: str = ""
    evidence: Evidence


class CandidateProfile(BaseModel):
    candidate_id: str
    name: str
    email: str = ""
    phone: str = ""
    location: str = ""
    total_experience_years: float = 0.0
    summary: str = ""
    skills: list[SkillItem] = Field(default_factory=list)
    experiences: list[ExperienceItem] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    raw_text: str = ""
    resume_filename: str = ""


class JDRequirement(BaseModel):
    requirement_id: str
    text: str
    category: Literal["must_have", "nice_to_have"] = "must_have"
    skill: str = ""
    min_years: Optional[float] = None


class JobDescription(BaseModel):
    title: str
    company: str = ""
    summary: str = ""
    requirements: list[JDRequirement] = Field(default_factory=list)
    raw_text: str = ""


class RequirementMatch(BaseModel):
    requirement_id: str
    requirement_text: str
    category: str
    status: Literal["met", "partial", "missing"]
    score: float
    reasoning: str
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"] = "medium"


class CandidateMatch(BaseModel):
    candidate_id: str
    candidate_name: str
    overall_score: float
    rank: int = 0
    matched_requirements: list[RequirementMatch] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    gaps_to_validate: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    summary: str = ""


class InterviewQuestion(BaseModel):
    question: str
    category: Literal["verify", "probe_gap", "depth", "behavioral"] = "verify"
    target_requirement: str = ""
    evidence: Optional[Evidence] = None


class InterviewKit(BaseModel):
    candidate_id: str
    candidate_name: str
    questions: list[InterviewQuestion] = Field(default_factory=list)


class QuerySource(BaseModel):
    candidate_id: str
    candidate_name: str
    snippet: str
    source: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[QuerySource] = Field(default_factory=list)
    matched_candidate_ids: list[str] = Field(default_factory=list)


class EvaluationArea(BaseModel):
    requirement_id: str
    requirement_text: str
    status: Literal["covered", "partial", "unanswered"]
    notes: str = ""


class EvaluationReport(BaseModel):
    candidate_id: str
    candidate_name: str
    overall_recommendation: Literal["strong_yes", "yes", "maybe", "no"] = "maybe"
    areas: list[EvaluationArea] = Field(default_factory=list)
    unanswered_areas: list[str] = Field(default_factory=list)
    summary: str = ""