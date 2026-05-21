from __future__ import annotations

import os

import chromadb
from dotenv import load_dotenv

from glossary.loader import load_glossary
from vector_store.embeddings import LocalEmbeddingFunction

load_dotenv()

_CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
_COLLECTION_NAME = "glossary_terms"
_SKIP_THRESHOLD = float(os.getenv("GLOSSARY_SKIP_THRESHOLD", "0.55"))

_client: chromadb.PersistentClient | None = None
_collection = None
_seeded_path: str | None = None


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=_CHROMA_PATH)
    return _client


def seed_from_csv(path: str) -> None:
    global _seeded_path, _collection

    if _seeded_path == path:
        return

    client = _get_client()

    try:
        client.delete_collection(_COLLECTION_NAME)
    except Exception:
        pass

    _collection = client.create_collection(
        name=_COLLECTION_NAME,
        embedding_function=LocalEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )

    terms = load_glossary(path)
    if not terms:
        _seeded_path = path
        return

    ids = [f"term_{i}" for i in range(len(terms))]
    documents = [f"{t.get('term', '')}: {t.get('definition', '')}" for t in terms]
    metadatas = [
        {
            "term": t.get("term", ""),
            "definition": t.get("definition", ""),
            "domain": t.get("domain", ""),
            "examples": t.get("examples", ""),
        }
        for t in terms
    ]

    _collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    _seeded_path = path


def _get_collection():
    global _collection
    if _collection is None:
        client = _get_client()
        _collection = client.get_or_create_collection(
            name=_COLLECTION_NAME,
            embedding_function=LocalEmbeddingFunction(),
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def search(query: str, top_k: int = 5) -> list[dict]:
    col = _get_collection()
    results = col.query(
        query_texts=[query],
        n_results=top_k,
        include=["metadatas", "documents", "distances"],
    )

    output = []
    for meta, doc, dist in zip(
        results["metadatas"][0],
        results["documents"][0],
        results["distances"][0],
    ):
        output.append(
            {
                "term": meta["term"],
                "definition": meta["definition"],
                "domain": meta["domain"],
                "examples": meta["examples"],
                "document": doc,
                "distance": dist,
            }
        )
    return output


def is_relevant(glossary_terms: list[dict]) -> bool:
    if not glossary_terms:
        return False
    return min(t["distance"] for t in glossary_terms) <= _SKIP_THRESHOLD
