"""
Module 04 - Generate Ground Truth Questions
"""

import json
import os

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from evaluation_utils import llm_structured
from load_documents import load_documents


# Load API key
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Questions(BaseModel):
    questions: list[str]


DATA_GEN_INSTRUCTIONS = """
You emulate a student who is taking our LLM course.

You are given one lesson page from the course.

Formulate 5 questions this student might ask that are answered by this page.

Rules:

- The page should contain the answer to each question.
- Make the questions complete and not too short.
- Use as few words as possible from the page; don't copy its phrasing.
- The questions should resemble how people actually ask things online:
  not too formal, not too short, not too long.
- Ask about the content of the lesson, not about its formatting or filename.
""".strip()


def main():

    documents = load_documents()

    pages = documents[:3]

    records = []
    usages = []

    for page in pages:

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
        )

        usages.append(usage)

        for q in result.questions:
            records.append(
                {
                    "question": q,
                    "filename": page["filename"],
                }
            )

        print(f"Finished: {page['filename']}")
        print(f"Input tokens : {usage.input_tokens}")
        print(f"Output tokens: {usage.output_tokens}")
        print("-" * 60)

    df = pd.DataFrame(records)

    df.to_csv("data/generated_ground_truth.csv", index=False)

    avg_input = sum(u.input_tokens for u in usages) / len(usages)

    print("=" * 60)
    print(f"Generated {len(df)} questions")
    print(f"Average Input Tokens: {avg_input:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()