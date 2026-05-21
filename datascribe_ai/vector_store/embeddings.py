from __future__ import annotations

from chromadb import EmbeddingFunction, Documents, Embeddings

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


class LocalEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        return _get_model().encode(list(input)).tolist()
