# Retrieval-Augmented Generation (RAG): A Practical Guide

## Table of Contents

1. [Overview](#overview)
2. [How RAG Works](#how-rag-works)
3. [Key Components](#key-components)
4. [Implementation Steps](#implementation-steps)
5. [RAG vs Non-RAG Comparison](#rag-vs-non-rag-comparison)
6. [Advanced RAG Techniques](#advanced-rag-techniques)
7. [Best Practices](#best-practices)

---

## Overview

**Retrieval-Augmented Generation (RAG)** is a technique that enhances Large Language Model (LLM) outputs by grounding them in retrieved external knowledge.

### The Problem RAG Solves

Standard LLMs have limitations:
- **Knowledge cutoff**: Training data is fixed at a point in time
- **Hallucinations**: Generate confident but false information
- **Domain specificity**: Struggle with specialized knowledge
- **Outdated information**: Cannot access real-time data

### The RAG Solution

RAG augments LLM responses with relevant external documents:
1. **Retrieve** relevant documents from a knowledge base
2. **Augment** the prompt with retrieved context
3. **Generate** a response grounded in real information

**Result**: More accurate, up-to-date, and verifiable responses

---

## How RAG Works

### High-Level Flow

```
User Query
    ↓
[Retrieve] → Search knowledge base for relevant documents
    ↓
Retrieved Context + User Query
    ↓
[Augment] → Combine query with context in prompt
    ↓
Augmented Prompt
    ↓
[Generate] → LLM produces response using context
    ↓
Grounded Response
```

### Example Workflow

**Query**: "What are the best practices for AI orchestration?"

**Without RAG**:
- LLM uses training knowledge (may be outdated)
- Could hallucinate details
- No guarantee of accuracy

**With RAG**:
1. Search knowledge base for "AI orchestration best practices"
2. Retrieve: "Best practices include monitoring, error handling, security..."
3. Augment prompt: "Based on these documents: [retrieved context], answer the question..."
4. Generate: LLM responds grounded in actual documentation

---

## Key Components

### 1. Document Collection

**Purpose**: Your domain knowledge in text form

**Formats**:
- PDFs
- Text files
- Markdown documents
- Web pages
- Database records
- Real-time APIs

**Characteristics**:
- Relevant to your domain
- Properly formatted
- Recently updated
- Accessible and queryable

### 2. Embedding Model

**Purpose**: Convert text to numerical vectors for similarity search

**How it works**:
- Takes text as input
- Generates a vector (list of numbers)
- Semantically similar texts → similar vectors

**Popular Models**:
- `all-MiniLM-L6-v2` (lightweight, fast)
- `sentence-transformers` (accurate)
- `OpenAI embeddings` (high quality)

**Example**:
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

query_embedding = model.encode("What is Kestra?")
# Output: [0.123, -0.456, 0.789, ...]  (384-dimensional vector)
```

### 3. Vector Store

**Purpose**: Store and retrieve embeddings efficiently

**Technologies**:
- **In-memory**: FAISS, Annoy (fast, no infrastructure)
- **Cloud**: Pinecone, Weaviate (scalable)
- **Self-hosted**: Milvus, Qdrant (flexible)
- **Database**: PostgreSQL with pgvector extension

**Features**:
- Fast similarity search (milliseconds)
- Scalable to millions of documents
- Supports filtering and metadata

### 4. Retrieval Mechanism

**Purpose**: Find relevant documents given a query

**Methods**:

- **Dense Retrieval**: Embedding similarity search
- **Sparse Retrieval**: TF-IDF, BM25 keyword search
- **Hybrid**: Combine dense and sparse

**Best Practices**:
- Retrieve top-k most similar documents (k=3-5)
- Filter by metadata/date if needed
- Score and rank results
- Handle edge cases (no results found)

### 5. Prompt Augmentation

**Purpose**: Incorporate context into the LLM prompt

**Structure**:
```
[System Message]
You are a helpful assistant. Answer questions based on the provided context.

[Context]
Retrieved Documents:
- Document 1: [relevant excerpt]
- Document 2: [relevant excerpt]
- Document 3: [relevant excerpt]

[User Query]
Question: [original user question]

[Response Instructions]
Cite sources when using retrieved information.
If information is not in the context, say so.
```

### 6. LLM Generation

**Purpose**: Generate response using context

**Configuration**:
- Temperature: Lower (0.3-0.5) for factual responses
- Max tokens: Sufficient for detailed answers
- Top-p sampling: Control diversity

---

## Implementation Steps

### Step 1: Prepare Documents

```
Input documents in your domain
       ↓
Clean and normalize text
       ↓
Split into chunks (300-512 tokens each)
       ↓
Add metadata (source, date, category)
       ↓
Store in accessible format
```

### Step 2: Generate Embeddings

```python
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example documents
documents = [
    "Kestra is a workflow orchestration platform",
    "RAG improves LLM accuracy by adding context",
    "Embeddings map text to numerical vectors"
]

# Generate embeddings
embeddings = model.encode(documents)
# Output shape: (3, 384) - 3 documents, 384-dim vectors
```

### Step 3: Store Embeddings

```python
import faiss
import numpy as np

# Create FAISS index
dimension = 384
index = faiss.IndexFlatL2(dimension)

# Add embeddings
embeddings_array = np.array(embeddings).astype('float32')
index.add(embeddings_array)

# Save index
faiss.write_index(index, "documents.index")
```

### Step 4: Retrieve Relevant Documents

```python
# Load index
index = faiss.read_index("documents.index")

# Encode query
query = "How do I use Kestra?"
query_embedding = model.encode([query])

# Search (k=3: retrieve top 3)
distances, indices = index.search(query_embedding, k=3)

# Get retrieved documents
retrieved_docs = [documents[i] for i in indices[0]]
```

### Step 5: Create Augmented Prompt

```python
context = "\n".join(retrieved_docs)

augmented_prompt = f"""
You are an expert assistant. Answer based on the context provided.

Context:
{context}

Question: {query}

Answer:
"""
```

### Step 6: Generate Response

```python
# Call LLM with augmented prompt
response = gemini_model.generate_content(augmented_prompt)
```

---

## RAG vs Non-RAG Comparison

### Homework Question 2: Hands-On Comparison

**Run both flows and compare**:

| Metric | Flow 1 (No RAG) | Flow 2 (With RAG) |
|--------|-----------------|------------------|
| **Response Length** | [Record] | [Record] |
| **Accuracy** | [Record] | [Record] |
| **Token Usage** | [Record] | [Record] |
| **Execution Time** | [Record] | [Record] |
| **Grounding** | General knowledge | Retrieved sources |
| **Confidence** | [Record] | [Record] |

**Analysis**:
- Which response was more accurate?
- Which used more tokens?
- Was the RAG overhead worth it?
- When would you use each approach?

---

## Advanced RAG Techniques

### 1. Hybrid Search

**Combine dense and sparse retrieval**:

```python
# Dense retrieval (semantic)
dense_results = semantic_search(query_embedding)

# Sparse retrieval (keyword-based)
sparse_results = keyword_search(query)

# Combine and rank
combined = merge_and_rerank(dense_results, sparse_results)
```

**Benefits**:
- Catches both semantic and keyword matches
- More robust retrieval
- Better coverage

### 2. Multi-Query Retrieval

**Generate multiple queries to retrieve more context**:

```python
# Original query
query = "How to deploy Kestra to production?"

# Generate related queries
related_queries = [
    "Kestra deployment best practices",
    "Production Kestra configuration",
    "Kestra scalability"
]

# Retrieve for all queries
all_results = []
for q in [query] + related_queries:
    results = retrieve(q, k=2)
    all_results.extend(results)

# Deduplicate and rank
final_results = deduplicate_and_rank(all_results)
```

### 3. Iterative Refinement

**Improve results by refining retrieval**:

```
Initial retrieval
     ↓
Generate response
     ↓
Check if answer satisfies query
     ↓
If not, refine query and retry
     ↓
Final response
```

### 4. Metadata Filtering

**Filter documents by metadata**:

```python
# Retrieve with filtering
results = retrieve(
    query_embedding,
    filters={
        'category': 'best-practices',
        'date': {'$gte': '2024-01-01'},
        'source': 'official-docs'
    },
    k=5
)
```

### 5. Re-ranking

**Rank retrieved documents by relevance**:

```python
from sentence_transformers.cross_encoders import CrossEncoder

# Cross-encoder for re-ranking
model = CrossEncoder('cross-encoder/qnli-distilroberta-base')

# Re-rank results
scores = model.predict([[query, doc] for doc in retrieved_docs])
ranked = sorted(zip(retrieved_docs, scores), key=lambda x: x[1], reverse=True)
```

---

## Best Practices

### 1. Document Preparation

✅ **Do**:
- Clean and normalize text
- Use consistent formatting
- Add metadata (source, date, category)
- Split documents into appropriate chunks

❌ **Don't**:
- Include raw PDFs without processing
- Mix different document formats
- Use outdated information
- Create extremely long chunks (>512 tokens)

### 2. Embedding Selection

✅ **Do**:
- Use embeddings matched to your domain
- Test different models
- Monitor embedding quality
- Update embeddings when documents change

❌ **Don't**:
- Use generic embeddings for specialized domains
- Assume larger dimension = better quality
- Ignore computational cost
- Mix embeddings from different models

### 3. Retrieval Configuration

✅ **Do**:
- Start with k=3-5 documents
- Monitor retrieval latency
- Implement caching
- Handle no-results gracefully

❌ **Don't**:
- Retrieve too many documents (increases cost)
- Ignore retrieval performance
- Use stale embeddings
- Fail silently on errors

### 4. Prompt Augmentation

✅ **Do**:
- Include clear source attribution
- Use structured context formatting
- Add instructions for handling missing information
- Keep augmentation concise

❌ **Don't**:
- Include too much irrelevant context
- Make prompts unnecessarily complex
- Forget to instruct model to cite sources
- Ignore token limits

### 5. Monitoring and Evaluation

✅ **Do**:
- Track retrieval quality
- Monitor response accuracy
- Measure token usage
- Collect user feedback

❌ **Don't**:
- Deploy without baseline metrics
- Ignore user feedback
- Skip quality evaluations
- Assume improvements without measurement

---

## Resources

- [RAG Papers](https://arxiv.org/abs/2312.10997)
- [Embedding Models](https://www.sbert.net/)
- [Vector Databases](https://www.pinecone.io/)
- [LangChain RAG Guide](https://python.langchain.com/)

---

**Last Updated**: July 3, 2026
