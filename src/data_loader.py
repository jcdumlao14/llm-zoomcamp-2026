import logging
from typing import Any

from gitsource import GithubRepositoryDataReader

logger = logging.getLogger(__name__)

REPO_OWNER = "DataTalksClub"
REPO_NAME = "llm-zoomcamp"
COMMIT_ID = "8c1834d"


def load_documents() -> list[dict[str, Any]]:
    """Load markdown lesson pages from the target repository."""
    reader = GithubRepositoryDataReader(
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        commit_id=COMMIT_ID,
    )

    docs: list[dict[str, Any]] = []
    for item in reader.read():
        filename = getattr(item, "filename", "") or ""
        content = getattr(item, "content", "") or ""
        if not filename.endswith(".md") or "/lessons/" not in filename:
            continue
        docs.append(
            {
                "filename": filename,
                "content": content,
            }
        )

    logger.info("Loaded %s lesson documents", len(docs))
    return docs
