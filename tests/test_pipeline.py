from src.chunking import create_chunks
from src.data_loader import load_documents
from src.indexing import create_index, search_documents
from src.rag import run_rag
from src.agent import search


def test_load_documents():
    docs = load_documents()
    assert isinstance(docs, list)
    assert len(docs) > 0


def test_index_builds():
    docs = load_documents()
    index = create_index(docs)
    assert index is not None


def test_chunking_works():
    docs = load_documents()
    chunks = create_chunks(docs)
    assert len(chunks) > 0


def test_search_returns_results():
    docs = load_documents()
    index = create_index(docs)
    results = search_documents(index, "agentic loop", top_k=3)
    assert len(results) > 0


def test_rag_returns_response():
    docs = load_documents()
    index = create_index(docs)
    response = run_rag("How does the agentic loop work?", index)
    assert "answer" in response
    assert "input_tokens" in response


def test_agent_search_tool_executes():
    result = search("agentic loop")
    assert isinstance(result, str)
    assert len(result) > 0
