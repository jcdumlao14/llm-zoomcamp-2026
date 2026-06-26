# Module-01-Agentic Rag Homework

This project explores an Agentic RAG workflow for the LLM Zoomcamp homework. The goal is to load lesson content, search for relevant passages, compare standard RAG with chunked retrieval, and summarize how an agentic loop differs from plain retrieval-augmented generation.

## Project Overview

The repository includes a notebook-based workflow that:
- loads lesson pages from the course materials,
- indexes them for retrieval,
- runs a basic RAG flow,
- compares chunked retrieval performance, and
- examines agentic search behavior.

## Installation and Setup

1. Install dependencies with the project setup instructions.
2. Create a local environment file from the sample environment file and add your API key.
3. Open the homework notebook and run it from the project environment.

## Methodology

The workflow follows these stages:

- **Data Loading**: lesson markdown files are collected from the course repository.
- **Indexing and Search**: the content is indexed so relevant lesson pages can be retrieved for a question.
- **Basic RAG**: a retrieval step is paired with a prompt to generate an answer.
- **Document Chunking**: long lesson pages are split into overlapping chunks.
- **Chunked RAG**: the same query is run against the chunked index to compare retrieval efficiency.
- **Agentic RAG**: the system uses repeated search/tool steps to answer a broader question about the agentic loop.

## Homework Results

The results below are based on the executed notebook output.

| Question | Summary | Final Answer | Notes |
|---|---|---:|---|
| Q1 | Count the total lesson pages | 72 | The notebook reported 72 lesson documents loaded. |
| Q2 | Find the best matching lesson for the agentic loop question | `01-agentic-rag/lessons/14-agentic-loop.md` | This was the top retrieved lesson page. |
| Q3 | Capture the token usage for the original RAG query | 14,860 input tokens | The notebook recorded the input token count for the first retrieval run. |
| Q4 | Count the number of chunks created from the lesson content | 295 | Chunking produced 295 chunks for the dataset. |
| Q5 | Compare original vs. chunked retrieval efficiency | Approximately 3x fewer tokens | The notebook summary reported this as the practical comparison outcome. |
| Q6 | Count how many search/tool calls the agent made | 4 | The agentic run used four search calls. |

## Key Findings

- The most relevant lesson for the agentic loop question is [notebooks/homework.executed.ipynb](notebooks/homework.executed.ipynb).
- Chunking substantially reduces the amount of context sent for retrieval-related prompting.
- The agentic workflow performs multiple searches before answering, which helps with broader conceptual questions.
- The final notebook run confirms the expected homework answers and provides a clear summary of the retrieval pipeline behavior.

