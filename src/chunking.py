import logging
from typing import Any

from gitsource import chunk_documents

logger = logging.getLogger(__name__)


def create_chunks(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Chunk lesson documents using the repository helper."""
    chunks = chunk_documents(documents, size=2000, step=1000)
    logger.info("Created %s chunks", len(chunks))
    return chunks
