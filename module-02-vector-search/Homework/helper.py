from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index, VectorSearch
import numpy as np
from tqdm import tqdm

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from Homework.config import CHUNK_SIZE, CHUNK_STEP, COMMIT_ID, REPO_NAME, REPO_OWNER
    from Homework.embedder import Embedder
else:
    from .config import CHUNK_SIZE, CHUNK_STEP, COMMIT_ID, REPO_NAME, REPO_OWNER
    from .embedder import Embedder


def load_documents() -> list[dict[str, Any]]:
    reader = GithubRepositoryDataReader(
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        commit_id=COMMIT_ID,
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )
    documents: list[dict[str, Any]] = []
    for item in reader.read():
        filename = getattr(item, "filename", "") or ""
        content = getattr(item, "content", "") or ""
        if not filename.endswith(".md"):
            continue
        documents.append({"filename": filename, "content": content})
    return documents


def create_chunks(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return chunk_documents(documents, size=CHUNK_SIZE, step=CHUNK_STEP)


def build_embedder(model_path: str | None = None) -> Embedder:
    path = model_path or "Homework/models/Xenova/all-MiniLM-L6-v2"
    return Embedder(path=path)


def embed_texts(embedder: Embedder, texts: list[str], batch_size: int = 16) -> np.ndarray:
    """Embed a list of texts in batches with a progress bar."""
    if not texts:
        return np.zeros((0, 384), dtype=np.float32)

    vectors: list[np.ndarray] = []
    for start in tqdm(range(0, len(texts), batch_size), desc="Embedding batches"):
        batch = texts[start : start + batch_size]
        vectors.append(embedder.encode_batch(batch, normalize=True))
    return np.vstack(vectors)


def build_vector_index(vectors: np.ndarray, documents: list[dict[str, Any]]) -> VectorSearch:
    index = VectorSearch(keyword_fields=["filename"])
    index.fit(vectors, documents)
    return index


def build_text_index(documents: list[dict[str, Any]]) -> Index:
    index = Index(text_fields=["content"], keyword_fields=["filename"])
    index.fit(documents)
    return index


def search_text(index: Index, query: str, top_k: int = 5) -> list[dict[str, Any]]:
    return index.search(query=query, num_results=top_k)


def search_vector(index: VectorSearch, query_vector: np.ndarray, top_k: int = 5) -> list[dict[str, Any]]:
    return index.search(query_vector=query_vector, num_results=top_k)


def compute_rrf(result_lists: list[list[dict[str, Any]]], k: int = 60, num_results: int = 5) -> list[dict[str, Any]]:
    scores: dict[tuple[str, int], float] = {}
    docs: dict[tuple[str, int], dict[str, Any]] = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc.get("start", 0))
            scores[key] = scores.get(key, 0.0) + 1 / (k + rank)
            docs[key] = doc

    ranked_keys = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked_keys[:num_results]]
