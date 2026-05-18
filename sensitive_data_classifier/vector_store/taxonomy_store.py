from __future__ import annotations

import os

import chromadb

from taxonomy.definitions import SENSITIVE_TAGS
from vector_store.embeddings import LocalEmbeddingFunction

_COLLECTION_NAME = "sensitive_tags"

_client: chromadb.PersistentClient | None = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is not None:
        return _collection

    db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    _client = chromadb.PersistentClient(path=db_path)
    _collection = _client.get_or_create_collection(
        name=_COLLECTION_NAME,
        embedding_function=LocalEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )
    seed_if_empty(_collection)
    return _collection


def seed_if_empty(collection=None) -> None:
    """Upsert all taxonomy tags into ChromaDB. Idempotent — uses label as document ID."""
    col = collection or _get_collection()
    if col.count() >= len(SENSITIVE_TAGS):
        return

    documents, ids, metadatas = [], [], []
    for tag in SENSITIVE_TAGS:
        doc_text = f"{tag['label']}: {tag['description']}"
        documents.append(doc_text)
        ids.append(tag["label"])
        metadatas.append(
            {
                "label": tag["label"],
                "handling_policy": tag["handling_policy"],
                "frameworks": ", ".join(tag["frameworks"]),
            }
        )

    col.upsert(documents=documents, ids=ids, metadatas=metadatas)


def search(query: str, top_k: int = 5) -> list[dict]:
    """Return top-K sensitive tags most similar to the query string."""
    col = _get_collection()
    results = col.query(query_texts=[query], n_results=min(top_k, col.count()))
    tags = []
    for i, doc_id in enumerate(results["ids"][0]):
        meta = results["metadatas"][0][i]
        tags.append(
            {
                "label": meta["label"],
                "handling_policy": meta["handling_policy"],
                "frameworks": meta["frameworks"],
                "document": results["documents"][0][i],
                "distance": results["distances"][0][i],
            }
        )
    return tags


def add_tag(tag: dict) -> None:
    """Add or update a single sensitive tag in the collection."""
    col = _get_collection()
    doc_text = f"{tag['label']}: {tag['description']}"
    col.upsert(
        documents=[doc_text],
        ids=[tag["label"]],
        metadatas=[
            {
                "label": tag["label"],
                "handling_policy": tag["handling_policy"],
                "frameworks": ", ".join(tag.get("frameworks", [])),
            }
        ],
    )
