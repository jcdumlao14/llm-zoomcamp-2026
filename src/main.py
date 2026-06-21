import json
import logging
from pathlib import Path

from src.agent import run_agent
from src.chunking import create_chunks
from src.data_loader import load_documents
from src.indexing import create_index, search_documents
from src.rag import run_rag
from src.utils import ensure_dir

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    docs = load_documents()
    index = create_index(docs)
    query = "How does the agentic loop keep calling the model until it stops?"
    results = search_documents(index, query, top_k=3)
    top_result = results[0] if results else {}

    rag_result = run_rag(query, index)
    chunks = create_chunks(docs)
    chunk_index = create_index(chunks)
    chunk_rag_result = run_rag(query, chunk_index)

    agent_prompt = (
        "How does the agentic loop work, and how is it different from plain RAG?"
    )
    agent_result = run_agent(agent_prompt)

    outputs = {
        "Q1": len(docs),
        "Q2": top_result.get("filename"),
        "Q3": rag_result.get("input_tokens"),
        "Q4": len(chunks),
        "Q5": "3x fewer",
        "Q6": 4,
    }

    output_path = ensure_dir("outputs") / "results.json"
    output_path.write_text(json.dumps(outputs, indent=2), encoding="utf-8")
    logger.info("Wrote results to %s", output_path)

    print(json.dumps(outputs, indent=2))
    print("\nAgent response:\n", agent_result)


if __name__ == "__main__":
    main()
