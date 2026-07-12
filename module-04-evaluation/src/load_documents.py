from gitsource import GithubRepositoryDataReader


def load_documents():
    """
    Load the official LLM Zoomcamp lesson pages.
    """

    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )

    documents = [file.parse() for file in reader.read()]

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print("=" * 60)
    print(f"Loaded {len(documents)} lesson pages")
    print("=" * 60)

    print("\nFirst five lesson pages:\n")

    for doc in documents[:5]:
        print(doc["filename"])