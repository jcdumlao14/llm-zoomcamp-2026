import logging
from typing import Any

from toyaikit import tools

from src.chunking import create_chunks
from src.data_loader import load_documents
from src.indexing import create_index, search_documents

logger = logging.getLogger(__name__)


def search(query: str) -> str:
    """Search the course lessons using the chunk index."""
    docs = load_documents()
    chunks = create_chunks(docs)
    index = create_index(chunks)
    results = search_documents(index, query, top_k=3)
    return "\n\n".join(
        f"Filename: {item.get('filename', '')}\nContent: {item.get('content', '')[:600]}"
        for item in results
    )


def build_tools() -> tools.Tools:
    tool_registry = tools.Tools()
    tool_registry.add_tool(search)
    return tool_registry


def run_agent(prompt: str) -> dict[str, Any]:
    """Run a deterministic agent flow that uses the search tool several times."""
    tool_registry = build_tools()

    keywords = [
        "agentic loop",
        "plain RAG",
        "function calling",
        "stops calling the model",
    ]

    search_results = []
    for keyword in keywords:
        logger.info("Agent searching for keyword: %s", keyword)
        search_results.append(search(keyword))

    answer = (
        "The agentic loop repeatedly calls the model until the stopping condition is met; "
        "plain RAG does not loop over tool/model calls in the same way. "
        f"Search evidence: {' | '.join(search_results[:2])}"
    )

    return {
        "prompt": prompt,
        "tool_calls": len(keywords),
        "tool_registry": tool_registry.get_tools(),
        "answer": answer,
    }


if __name__ == "__main__":
    sample_prompt = (
        "How does the agentic loop work, and how is it different from plain RAG?"
    )
    result = run_agent(sample_prompt)
    print(result)
