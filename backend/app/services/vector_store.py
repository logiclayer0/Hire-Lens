from typing import Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings


class VectorStore:
    def __init__(self) -> None:
        self.persist_dir = str(settings.resolve_path(settings.CHROMA_DIR))
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.candidates = self.client.get_or_create_collection(
            name="candidates",
            metadata={"hnsw:space": "cosine"},
        )

    def add_candidate_chunks(
        self,
        candidate_id: str,
        candidate_name: str,
        chunks: list[dict[str, Any]],
    ) -> None:
        if not chunks:
            return
        ids = [f"{candidate_id}::{i}" for i in range(len(chunks))]
        documents = [c["text"] for c in chunks]
        metadatas = [
            {
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "source": c.get("source", ""),
                "page": int(c.get("page") or 0),
                "line": int(c.get("line") or 0),
            }
            for c in chunks
        ]
        self.candidates.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

    def query(self, text: str, top_k: int = 8) -> list[dict[str, Any]]:
        if not text.strip():
            return []
        try:
            result = self.candidates.query(query_texts=[text], n_results=top_k)
        except Exception:
            return []
        out: list[dict[str, Any]] = []
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]
        dists = (result.get("distances") or [[]])[0]
        for doc, meta, dist in zip(docs, metas, dists):
            out.append(
                {
                    "text": doc,
                    "metadata": meta or {},
                    "distance": dist,
                }
            )
        return out

    def reset(self) -> None:
        try:
            self.client.delete_collection("candidates")
        except Exception:
            pass
        self.candidates = self.client.get_or_create_collection(
            name="candidates",
            metadata={"hnsw:space": "cosine"},
        )


vector_store = VectorStore()