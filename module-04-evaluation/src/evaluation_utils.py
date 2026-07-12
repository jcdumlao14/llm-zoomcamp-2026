"""
Module 04 - Evaluation Utilities
Supports Google Gemini (google-genai SDK)
"""

import time

from google.genai import types
from tqdm.auto import tqdm

from rag_helper import RAGBase


# ==========================================================
# Pricing Utilities (Approximate Gemini Pricing)
# ==========================================================

def calc_price(usage):
    """
    Approximate Gemini API pricing.
    Adjust prices if Google changes them.
    """

    input_price_per_million = 0.075
    output_price_per_million = 0.30

    input_tokens = getattr(usage, "prompt_token_count", 0)
    output_tokens = getattr(usage, "candidates_token_count", 0)

    input_cost = input_tokens / 1_000_000 * input_price_per_million
    output_cost = output_tokens / 1_000_000 * output_price_per_million

    total_cost = input_cost + output_cost

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def calc_total_price(usages):
    """
    Sum total API cost.
    """

    total = 0.0

    for usage in usages:
        total += calc_price(usage)["total_cost"]

    return total


# ==========================================================
# Structured Output (Gemini)
# ==========================================================

def llm_structured(
    client,
    instructions,
    user_prompt,
    output_type,
    model="gemini-2.5-flash",
):
    """
    Generate structured JSON output using Gemini.
    """

    response = client.models.generate_content(
        model=model,
        contents=[
            instructions,
            user_prompt,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=output_type,
        ),
    )

    return response.parsed, response.usage_metadata


def llm_structured_retry(
    client,
    instructions,
    user_prompt,
    output_type,
    model="gemini-2.5-flash",
    max_retries=3,
):
    """
    Retry Gemini requests automatically.
    """

    for attempt in range(max_retries):

        try:

            return llm_structured(
                client=client,
                instructions=instructions,
                user_prompt=user_prompt,
                output_type=output_type,
                model=model,
            )

        except Exception as e:

            print(f"Retry {attempt + 1}/{max_retries}: {e}")

            if attempt == max_retries - 1:
                raise

            time.sleep(2 ** attempt)


# ==========================================================
# RAG Wrapper with Usage Tracking
# ==========================================================

class RAGWithUsage(RAGBase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.usages = []

        self.last_usage = None

    def reset_usage(self):

        self.usages = []

        self.last_usage = None

    def search(self, query, num_results=5):

        boost_dict = {
            "question": 1.0,
            "answer": 2.0,
            "section": 0.1,
        }

        filter_dict = {
            "course": self.course
        }

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict,
        )

    def llm(self, prompt):
        """
        Send prompt to Gemini.
        """

        response = self.llm_client.models.generate_content(
            model=self.model,
            contents=[
                self.instructions,
                prompt,
            ],
        )

        self.last_usage = response.usage_metadata

        self.usages.append(response.usage_metadata)

        return response.text

    def total_cost(self):

        return calc_total_price(self.usages)

    def total_tokens(self):
        """
        Total prompt, output and overall token counts.
        """

        prompt_tokens = sum(
            getattr(u, "prompt_token_count", 0)
            for u in self.usages
        )

        output_tokens = sum(
            getattr(u, "candidates_token_count", 0)
            for u in self.usages
        )

        total_tokens = sum(
            getattr(u, "total_token_count", 0)
            for u in self.usages
        )

        return {
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }


# ==========================================================
# Progress Helper
# ==========================================================

def map_progress(pool, seq, func):
    """
    Execute tasks in parallel with a progress bar.
    """

    results = []

    with tqdm(total=len(seq)) as progress:

        futures = []

        for item in seq:

            future = pool.submit(func, item)

            future.add_done_callback(lambda _: progress.update())

            futures.append(future)

        for future in futures:

            results.append(future.result())

    return results


# ==========================================================
# Token Utility Functions
# ==========================================================

def average_prompt_tokens(usages):
    if not usages:
        return 0

    return sum(
        getattr(u, "prompt_token_count", 0)
        for u in usages
    ) / len(usages)


def average_output_tokens(usages):
    if not usages:
        return 0

    return sum(
        getattr(u, "candidates_token_count", 0)
        for u in usages
    ) / len(usages)


def average_total_tokens(usages):
    if not usages:
        return 0

    return sum(
        getattr(u, "total_token_count", 0)
        for u in usages
    ) / len(usages)