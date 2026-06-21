import logging
from typing import Any

from minsearch import Index

logger = logging.getLogger(__name__)


def create_index(documents: list[dict[str, Any]]) -> Index:
    """Create a MinSearch index for lesson content."""
    index = Index(
        text_fields=["content"],
        keyword_fields=["filename"],
    )
    index.fit(documents)
    logger.info("Built index with %s documents", len(documents))
    return index


def search_documents(index: Index, query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Search indexed documents for the given query."""
    return index.search(query=query, num_results=top_k)
