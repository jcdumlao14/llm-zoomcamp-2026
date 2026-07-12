"""
Module 04 - Document Chunking

Creates overlapping chunks from the official LLM Zoomcamp lessons.
"""

from gitsource import chunk_documents
from load_documents import load_documents


def create_chunks():
    """
    Create overlapping chunks from lesson pages.
    """

    documents = load_documents()

    chunks = chunk_documents(
        documents,
        size=2000,
        step=1000,
    )

    return chunks


if __name__ == "__main__":

    chunks = create_chunks()

    print("=" * 60)
    print(f"Total Chunks: {len(chunks)}")
    print("=" * 60)

    first = chunks[0]

    print("\nAvailable Keys:")
    print(list(first.keys()))

    print("\nChunk Metadata")
    print("-" * 60)

    # Print all metadata except the text content
    for key, value in first.items():
        if key != "text":
            print(f"{key}: {value}")

    # Display a preview of the chunk text if available
    if "text" in first:
        print("\nContent Preview")
        print("-" * 60)
        print(first["text"][:500])

    print("\nFull Chunk Dictionary")
    print("-" * 60)
    print(first)