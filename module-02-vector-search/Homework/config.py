from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"
OUTPUTS_DIR = ROOT_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
DOCS_DIR = ROOT_DIR / "docs"
README_PATH = ROOT_DIR / "README.md"

REPO_OWNER = "DataTalksClub"
REPO_NAME = "llm-zoomcamp"
COMMIT_ID = "8c1834d"
MODEL_REPO = "Xenova/all-MiniLM-L6-v2"
MODEL_DIR = MODELS_DIR / MODEL_REPO

QUERY_Q1 = "How does approximate nearest neighbor search work?"
QUERY_Q4 = "What metric do we use to evaluate a search engine?"
QUERY_Q5 = "How do I store vectors in PostgreSQL?"
QUERY_Q6 = "How do I give the model access to tools?"

EMBEDDING_MODEL_PATH = MODEL_DIR

CHUNK_SIZE = 2000
CHUNK_STEP = 1000
