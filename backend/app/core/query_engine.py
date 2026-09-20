import json
from app.core.models import (
    CandidateProfile,
    QueryResponse,
    QuerySource,
)
from app.services.llm import llm
from app.services.vector_store import vector_store


SYSTEM_PROMPT = """You are HireLens, a recruiter's research assistant.
Answer the recruiter's question about the candidate pool STRICTLY using the provided evidence snippets.
Rules:
- Only use the given snippets.
- If the answer is not present, say so clearly.
- Reference the candidate names explicitly.
- Cite evidence inline by quoting the snippet.
- Return JSON only."""


class QueryEngine:
    def _schema(self) -> str:
        return """{
  "answer": "string (2-5 sentences)",
  "matched_candidate_ids": ["string"]
}"""

    def query(
        self,
        question: str,
        profiles: list[CandidateProfile],
        top_k: int = 8,
    ) -> QueryResponse:
        hits = vector_store.query(question, top_k=top_k)

        sources: list[QuerySource] = []
        context_blocks: list[str] = []
        matched_ids: set[str] = set()

        for hit in hits:
            meta = hit.get("metadata") or {}
            cid = str(meta.get("candidate_id", ""))
            cname = str(meta.get("candidate_name", ""))
            snippet = str(hit.get("text", ""))
            src = str(meta.get("source", ""))
            if cid:
                matched_ids.add(cid)
            sources.append(
                QuerySource(
                    candidate_id=cid,
                    candidate_name=cname,
                    snippet=snippet[:400],
                    source=src,
                )
            )
            context_blocks.append(f"[{cname} | {src}] {snippet}")

        if not context_blocks:
            return QueryResponse(
                answer="No candidate data indexed yet. Please upload resumes first.",
                sources=[],
                matched_candidate_ids=[],
            )

        user_prompt = (
            f"Recruiter question: {question}\n\n"
            f"Evidence snippets:\n" + "\n".join(f"- {b}" for b in context_blocks) + "\n\n"
            f"Return JSON matching:\n{self._schema()}"
        )
        data = llm.chat_json(system=SYSTEM_PROMPT, user=user_prompt, temperature=0.2)

        valid_ids = {p.candidate_id for p in profiles}
        final_ids = [cid for cid in (data.get("matched_candidate_ids") or []) if cid in valid_ids]
        if not final_ids:
            final_ids = [cid for cid in matched_ids if cid in valid_ids]

        return QueryResponse(
            answer=str(data.get("answer", "")).strip() or "No answer produced.",
            sources=sources,
            matched_candidate_ids=final_ids,
        )


query_engine = QueryEngine()