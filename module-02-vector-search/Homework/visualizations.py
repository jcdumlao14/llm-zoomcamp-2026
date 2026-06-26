from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError as exc:  # pragma: no cover - dependency is installed by uv sync
    raise RuntimeError("matplotlib is required for visualization outputs. Run `uv sync`.") from exc

from .config import FIGURES_DIR
from .utils import ensure_dir


def save_histogram(values: list[float] | np.ndarray, title: str, filename: str) -> Path:
    """Save a simple histogram plot for an array of numeric values."""
    ensure_dir(FIGURES_DIR)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(values, bins=20, color="steelblue", edgecolor="black")
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    output_path = FIGURES_DIR / filename
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
