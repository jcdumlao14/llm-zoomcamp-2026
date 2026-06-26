from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import README_PATH


def build_homework_report(summary: dict[str, Any]) -> str:
    """Create a markdown report for the homework from the computed summary data."""
    question_rows = [
        [question, str(answer)] for question, answer in summary["questions"].items()
    ]
    question_table = "\n".join(
        [
            "| Question | Answer |",
            "| --- | --- |",
            *[f"| {q} | {a} |" for q, a in question_rows],
        ]
    )

    return f"""# Module 02 Homework

## Overview
- Homework purpose: implement the official Module 02 vector search workflow.
- Learning objectives: embeddings, cosine similarity, chunking, vector search, keyword search, hybrid search, and RRF.
- Technologies used: ONNX Runtime, Hugging Face, MinSearch, NumPy, Tokenizers, gitsource.
- Development environment: Python 3.12+, uv, Jupyter, VS Code.

## Repository Structure
- Homework/homework.py: main executable workflow.
- Homework/helper.py: reusable retrieval and search helpers.
- Homework/embedder.py: ONNX embedder wrapper.
- Homework/download.py: model download helper.
- Homework/visualizations.py: optional plots.
- Homework/outputs/: generated JSON, markdown, and figures.

## Workflow
1. Environment Setup
2. Download Helper Files
3. Download ONNX Model
4. Load Documents
5. Generate Embeddings
6. Compute Cosine Similarity
7. Chunk Documents
8. Run Manual Vector Search
9. Run MinSearch Vector Search
10. Run Keyword Search
11. Run Hybrid Search with RRF
12. Write the final report and summary files

## Methodology
The workflow uses an ONNX-based embedder to transform lesson text into normalized vectors, computes cosine similarity for retrieval, creates overlapping chunks for more focused search, and combines vector and keyword search results through Reciprocal Rank Fusion.

## Homework Questions
### Question 1
- Objective: embed the query and inspect the first value.
- Final Computed Answer: {summary['questions']['Q1']}

### Question 2
- Objective: compute the cosine similarity between the query and a target lesson page.
- Final Computed Answer: {summary['questions']['Q2']}

### Question 3
- Objective: identify the highest-scoring chunk after batch embedding.
- Final Computed Answer: {summary['questions']['Q3']}

### Question 4
- Objective: run MinSearch vector search for the evaluation query.
- Final Computed Answer: {summary['questions']['Q4']}

### Question 5
- Objective: compare vector and keyword search results.
- Final Computed Answer: {summary['questions']['Q5']}

### Question 6
- Objective: fuse vector and keyword results with RRF.
- Final Computed Answer: {summary['questions']['Q6']}

## Results Summary
{question_table}

## Key Learnings
- Embeddings provide semantic representations of text.
- Vector search retrieves semantically similar content.
- Cosine similarity is an effective similarity measure for normalized embeddings.
- Chunking improves retrieval granularity for long documents.
- Hybrid search combines complementary strengths from vector and keyword search.
- RRF produces a robust merged ranking from multiple retrieval strategies.

## Challenges
- Handling large ONNX model downloads.
- Matching the official homework workflow closely while keeping the code modular.
- Making the notebook execute end to end without manual intervention.

## Future Improvements
- Optional: add richer visualizations for search comparisons.
- Optional: support alternative embedding models.
- Optional: save intermediate embeddings for later reuse.

## References
- LLM Zoomcamp
- ONNX Runtime
- Hugging Face
- MinSearch
- NumPy
- Tokenizers

## Conclusion
The module 02 homework has been implemented as a reproducible Python project with a polished notebook, modular code, and automatically generated results.
"""
