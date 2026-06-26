from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any
from urllib.request import urlretrieve

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from Homework.config import QUERY_Q1, QUERY_Q4, QUERY_Q5, QUERY_Q6, OUTPUTS_DIR, README_PATH
    from Homework.download import download
    from Homework.helper import (
        build_embedder,
        build_text_index,
        build_vector_index,
        compute_rrf,
        create_chunks,
        embed_texts,
        load_documents,
        search_text,
        search_vector,
    )
    from Homework.report_template import build_homework_report
    from Homework.utils import configure_logging, ensure_dir, to_serializable
    from Homework.visualizations import save_histogram
else:
    from .config import QUERY_Q1, QUERY_Q4, QUERY_Q5, QUERY_Q6, OUTPUTS_DIR, README_PATH
    from .download import download
    from .helper import (
        build_embedder,
        build_text_index,
        build_vector_index,
        compute_rrf,
        create_chunks,
        embed_texts,
        load_documents,
        search_text,
        search_vector,
    )
    from .report_template import build_homework_report
    from .utils import configure_logging, ensure_dir, to_serializable
    from .visualizations import save_histogram
    from .download import download
    from .helper import (
        build_embedder,
        build_text_index,
        build_vector_index,
        compute_rrf,
        create_chunks,
        embed_texts,
        load_documents,
        search_text,
        search_vector,
    )
    from .report_template import build_homework_report
    from .utils import configure_logging, ensure_dir, to_serializable
    from .visualizations import save_histogram

configure_logging()
logger = logging.getLogger(__name__)


def ensure_helper_files() -> None:
    """Download the official helper scripts if the workspace copy is missing."""
    base_dir = Path(__file__).resolve().parent
    files = {
        "download.py": "https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/02-vector-search/embed/download.py",
        "embedder.py": "https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/02-vector-search/embed/embedder.py",
    }
    for filename, url in files.items():
        target = base_dir / filename
        if not target.exists():
            logger.info("Downloading helper file %s", filename)
            urlretrieve(url, target)


def run_questions_1_to_3() -> dict[str, Any]:
    """Run the first three homework questions and print the intermediate outputs."""
    ensure_helper_files()

    model_path = download("Xenova/all-MiniLM-L6-v2", dest="Homework/models")
    embedder = build_embedder(str(model_path))

    documents = load_documents()
    logger.info("Loaded %s lesson documents", len(documents))

    query_vector = embedder.encode(QUERY_Q1)
    q1_first_value = float(query_vector[0])
    logger.info("Q1 first embedding value: %s", q1_first_value)

    target_filename = "02-vector-search/lessons/07-sqlitesearch-vector.md"
    target_document = next(doc for doc in documents if doc["filename"] == target_filename)
    target_vector = embedder.encode(target_document["content"])
    cosine_similarity = float(query_vector @ target_vector)
    logger.info("Q2 cosine similarity with %s: %s", target_filename, cosine_similarity)

    chunks = create_chunks(documents)
    logger.info("Created %s chunks", len(chunks))

    chunk_texts = [chunk.get("content", "") for chunk in chunks]
    chunk_vectors = embed_texts(embedder, chunk_texts)
    chunk_scores = chunk_vectors @ query_vector
    best_chunk_index = int(chunk_scores.argmax())
    best_chunk = chunks[best_chunk_index]
    logger.info("Q3 best chunk filename: %s", best_chunk.get("filename"))
    logger.info("Q3 best chunk score: %s", float(chunk_scores[best_chunk_index]))

    results = {
        "Q1": {
            "question": QUERY_Q1,
            "first_value": q1_first_value,
            "embedding_preview": query_vector[:5].round(6).tolist(),
        },
        "Q2": {
            "target_filename": target_filename,
            "cosine_similarity": cosine_similarity,
        },
        "Q3": {
            "chunk_count": len(chunks),
            "best_chunk_filename": best_chunk.get("filename"),
            "best_chunk_score": float(chunk_scores[best_chunk_index]),
            "top_chunk_scores": [
                {
                    "filename": chunk.get("filename"),
                    "score": float(score),
                }
                for chunk, score in sorted(
                    zip(chunks, chunk_scores),
                    key=lambda item: item[1],
                    reverse=True,
                )[:5]
            ],
        },
    }

    output_dir = ensure_dir(OUTPUTS_DIR)
    output_path = output_dir / "questions_1_to_3.json"
    output_path.write_text(json.dumps(to_serializable(results), indent=2), encoding="utf-8")
    return results


def render_markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [f"| {' | '.join(headers)} |", f"| {' | '.join(['---'] * len(headers))} |"]
    for row in rows:
        lines.append(f"| {' | '.join(str(cell) for cell in row)} |")
    return "\n".join(lines)


def run_homework() -> dict[str, Any]:
    """Run the full homework workflow, including Questions 1–6."""
    questions_1_to_3 = run_questions_1_to_3()

    embedder = build_embedder("Homework/models/Xenova/all-MiniLM-L6-v2")
    documents = load_documents()
    chunks = create_chunks(documents)
    chunk_texts = [chunk.get("content", "") for chunk in chunks]
    chunk_vectors = embed_texts(embedder, chunk_texts)
    vector_index = build_vector_index(chunk_vectors, chunks)
    text_index = build_text_index(chunks)

    query_vector_q1 = embedder.encode(QUERY_Q1)
    chunk_scores = chunk_vectors @ query_vector_q1
    query_vector_q4 = embedder.encode(QUERY_Q4)
    query_vector_q5 = embedder.encode(QUERY_Q5)
    query_vector_q6 = embedder.encode(QUERY_Q6)

    vector_results_q4 = search_vector(vector_index, query_vector_q4, top_k=5)
    text_results_q4 = search_text(text_index, QUERY_Q4, top_k=5)
    vector_results_q5 = search_vector(vector_index, query_vector_q5, top_k=5)
    text_results_q5 = search_text(text_index, QUERY_Q5, top_k=5)
    vector_results_q6 = search_vector(vector_index, query_vector_q6, top_k=5)
    text_results_q6 = search_text(text_index, QUERY_Q6, top_k=5)
    combined_results_q6 = compute_rrf([vector_results_q6, text_results_q6], num_results=5)

    q4_filename = vector_results_q4[0].get("filename") if vector_results_q4 else None
    q5_filename = next(
        (
            doc.get("filename")
            for doc in vector_results_q5
            if doc.get("filename") not in {result.get("filename") for result in text_results_q5}
        ),
        None,
    )
    q6_filename = combined_results_q6[0].get("filename") if combined_results_q6 else None

    comparison_rows = [
        [
            QUERY_Q5,
            "; ".join(doc.get("filename") for doc in vector_results_q5),
            "; ".join(doc.get("filename") for doc in text_results_q5),
            q5_filename or "",
        ]
    ]
    comparison_table_markdown = render_markdown_table(
        ["Query", "Vector Search", "Keyword Search", "Unique to Vector"],
        comparison_rows,
    )

    ranking_rows = [
        ["Q4 vector", "; ".join(doc.get("filename") for doc in vector_results_q4)],
        ["Q4 keyword", "; ".join(doc.get("filename") for doc in text_results_q4)],
        ["Q6 RRF", "; ".join(doc.get("filename") for doc in combined_results_q6)],
    ]
    ranking_markdown = render_markdown_table(["Method", "Top results"], ranking_rows)

    summary_rows = [
        ["Q1", str(questions_1_to_3["Q1"]["first_value"])],
        ["Q2", str(questions_1_to_3["Q2"]["cosine_similarity"])],
        ["Q3", str(questions_1_to_3["Q3"]["best_chunk_filename"])],
        ["Q4", q4_filename or ""],
        ["Q5", q5_filename or ""],
        ["Q6", q6_filename or ""],
    ]
    summary_markdown = render_markdown_table(["Question", "Answer"], summary_rows)

    answers = {
        "Q1": questions_1_to_3["Q1"]["first_value"],
        "Q2": questions_1_to_3["Q2"]["cosine_similarity"],
        "Q3": questions_1_to_3["Q3"]["best_chunk_filename"],
        "Q4": q4_filename,
        "Q5": q5_filename,
        "Q6": q6_filename,
    }

    summary = {
        "questions": answers,
        "comparison_table": comparison_rows,
        "comparison_table_markdown": comparison_table_markdown,
        "ranking_outputs": ranking_rows,
        "ranking_table_markdown": ranking_markdown,
        "summary_table_markdown": summary_markdown,
        "evaluation_metrics": {
            "vector_result_count": len(vector_results_q5),
            "keyword_result_count": len(text_results_q5),
            "rrf_result_count": len(combined_results_q6),
        },
    }

    output_dir = ensure_dir(OUTPUTS_DIR)
    output_path = output_dir / "results.json"
    output_path.write_text(json.dumps(to_serializable(summary), indent=2), encoding="utf-8")

    readme_path = README_PATH
    readme_path.write_text(build_homework_report(summary), encoding="utf-8")

    markdown_path = output_dir / "summary.md"
    markdown_path.write_text(
        "# Module 02 Homework Summary\n\n"
        f"{summary_markdown}\n\n"
        f"## Comparison\n\n{comparison_table_markdown}\n\n"
        f"## Ranking\n\n{ranking_markdown}\n",
        encoding="utf-8",
    )
    try:
        save_histogram(
            [float(score) for score in chunk_scores],
            "Chunk embedding scores",
            "chunk_scores.png",
        )
    except Exception as exc:  # pragma: no cover - optional visualization
        logger.warning("Skipping histogram visualization: %s", exc)

    logger.info("Q4 vector result: %s", q4_filename)
    logger.info("Q5 unique to vector: %s", q5_filename)
    logger.info("Q6 RRF winner: %s", q6_filename)
    logger.info("Summary markdown written to %s", markdown_path)
    return summary


if __name__ == "__main__":
    results = run_homework()
    print("\nComputed homework summary:")
    print(json.dumps(to_serializable(results), indent=2))
