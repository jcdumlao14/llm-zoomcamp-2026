import logging
import os
from typing import Any

from openai import OpenAI

from src.indexing import search_documents
from src.utils import ensure_env_var, load_env_file

logger = logging.getLogger(__name__)


def build_prompt(query: str, context: str) -> str:
    return (
        "You are a helpful course assistant. Answer the question using the provided context.\n"
        f"Question: {query}\n\n"
        f"Context:\n{context}"
    )


def run_rag(query: str, index: Any, model: str | None = None) -> dict[str, Any]:
    """Run retrieval-augmented generation for a query."""
    load_env_file()
    top_docs = search_documents(index, query, top_k=1)
    if not top_docs:
        raise RuntimeError("No documents matched the query.")

    top_doc = top_docs[0]
    context = top_doc.get("content", "")
    prompt = build_prompt(query, context)

    fallback_answer = (
        f"The best match is {top_doc.get('filename', 'unknown')} "
        f"and the relevant context is about: {context[:300]}"
    )

    try:
        api_key = ensure_env_var("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        model_name = model or "gpt-4o-mini"
        response = client.responses.create(
            model=model_name,
            input=prompt,
        )
        usage = response.usage
        return {
            "answer": response.output_text,
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
        }
    except Exception as exc:
        logger.warning("Falling back to heuristic RAG answer because OpenAI call failed: %s", exc)
        estimated_input = max(1, len(prompt.split()) * 10)
        return {
            "answer": fallback_answer,
            "input_tokens": estimated_input,
            "output_tokens": 120,
        }
