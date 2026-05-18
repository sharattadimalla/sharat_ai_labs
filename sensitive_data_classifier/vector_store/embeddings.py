from __future__ import annotations

from chromadb import EmbeddingFunction, Documents, Embeddings
from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


class LocalEmbeddingFunction(EmbeddingFunction):
    """ChromaDB-compatible embedding function backed by sentence-transformers."""

    def __call__(self, input: Documents) -> Embeddings:
        model = _get_model()
        vectors = model.encode(list(input), convert_to_numpy=True)
        return vectors.tolist()
