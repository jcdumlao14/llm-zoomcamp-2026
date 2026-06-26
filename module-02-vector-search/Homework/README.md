# Module 02 Homework

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
- Final Computed Answer: -0.02058203437252893

### Question 2
- Objective: compute the cosine similarity between the query and a target lesson page.
- Final Computed Answer: 0.36107027225589694

### Question 3
- Objective: identify the highest-scoring chunk after batch embedding.
- Final Computed Answer: 02-vector-search/lessons/07-sqlitesearch-vector.md

### Question 4
- Objective: run MinSearch vector search for the evaluation query.
- Final Computed Answer: 04-evaluation/lessons/05-search-metrics.md

### Question 5
- Objective: compare vector and keyword search results.
- Final Computed Answer: 02-vector-search/lessons/08-pgvector.md

### Question 6
- Objective: fuse vector and keyword results with RRF.
- Final Computed Answer: 01-agentic-rag/lessons/13-function-calling.md

## Results Summary
| Question | Answer |
| --- | --- |
| Q1 | -0.02058203437252893 |
| Q2 | 0.36107027225589694 |
| Q3 | 02-vector-search/lessons/07-sqlitesearch-vector.md |
| Q4 | 04-evaluation/lessons/05-search-metrics.md |
| Q5 | 02-vector-search/lessons/08-pgvector.md |
| Q6 | 01-agentic-rag/lessons/13-function-calling.md |

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
