"""
Module 04 - Generate Ground Truth Questions

Generates synthetic Ground Truth questions using Google Gemini.

Homework 4
LLM Zoomcamp 2026
"""

import json
import os

import pandas as pd
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

from evaluation_utils import llm_structured
from load_documents import load_documents


# ==========================================================
# Load Environment
# ==========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# ==========================================================
# Structured Output Model
# ==========================================================

class Questions(BaseModel):
    questions: list[str]


# ==========================================================
# Prompt
# ==========================================================

DATA_GEN_INSTRUCTIONS = """
You emulate a student taking the LLM Zoomcamp course.

You are given ONE lesson page.

Generate exactly FIVE different questions.

Rules:

- Every question must be answerable from this lesson.
- Don't copy sentences.
- Rewrite naturally.
- Questions should sound like real users.
- Don't ask about filenames.
- Don't ask about formatting.
- Return ONLY valid JSON.
""".strip()


# ==========================================================
# Safe token extraction
# ==========================================================

def token_counts(usage):
    """
    Works with different Gemini SDK versions.
    """

    prompt = getattr(usage, "prompt_token_count", None)
    completion = getattr(usage, "candidates_token_count", None)
    total = getattr(usage, "total_token_count", None)

    if prompt is None:
        prompt = getattr(usage, "input_tokens", 0)

    if completion is None:
        completion = getattr(usage, "output_tokens", 0)

    if total is None:
        total = prompt + completion

    return prompt, completion, total


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("Loading lesson pages...")
    print("=" * 60)

    documents = load_documents()

    pages = documents[:3]

    print(f"\nGenerating questions for {len(pages)} lesson pages...\n")

    records = []

    prompt_tokens = []
    completion_tokens = []
    total_tokens = []

    for i, page in enumerate(pages, start=1):

        print("=" * 60)
        print(f"Page {i}")
        print(page["filename"])
        print("=" * 60)

        user_prompt = json.dumps(
            {
                "filename": page["filename"],
                "content": page["content"],
            },
            indent=2,
        )

        result, usage = llm_structured(
            client=client,
            instructions=DATA_GEN_INSTRUCTIONS,
            user_prompt=user_prompt,
            output_type=Questions,
            model="gemini-2.5-flash",
        )

        p, c, t = token_counts(usage)

        prompt_tokens.append(p)
        completion_tokens.append(c)
        total_tokens.append(t)

        for q in result.questions:

            print("•", q)

            records.append(
                {
                    "question": q,
                    "filename": page["filename"],
                }
            )

        print("\nToken Usage")
        print(f"Prompt Tokens     : {p}")
        print(f"Completion Tokens : {c}")
        print(f"Total Tokens      : {t}")

        print()

    os.makedirs("data", exist_ok=True)

    df = pd.DataFrame(records)

    output_file = "data/generated_ground_truth.csv"

    df.to_csv(output_file, index=False)

    print("=" * 60)
    print("Generation Complete")
    print("=" * 60)

    print(f"Questions Generated : {len(df)}")
    print(f"CSV Saved           : {output_file}")

    print()

    print(f"Average Prompt Tokens     : {sum(prompt_tokens)/len(prompt_tokens):.2f}")
    print(f"Average Completion Tokens : {sum(completion_tokens)/len(completion_tokens):.2f}")
    print(f"Average Total Tokens      : {sum(total_tokens)/len(total_tokens):.2f}")

    print("=" * 60)


if __name__ == "__main__":
    main()