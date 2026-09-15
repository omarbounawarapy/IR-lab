"""The seed convention IR Lab commits to before it needs one.

Nothing in the framework is stochastic yet -- boolean retrieval, the
current indexers, and the analysis pipeline are all fully deterministic.
That is exactly why this exists now rather than later: the first
stochastic component (a sampled train/dev/test split, an approximate
index, anything reaching for `random`/`numpy.random`) must seed through
this single entry point, or reproducibility breaks silently on day one
for that component instead of never.
"""
import random

DEFAULT_SEED = 1337


def set_global_seed(seed: int = DEFAULT_SEED) -> None:
    """Seed every source of randomness IR Lab uses. Call this once, at
    the start of an experiment run, before any stochastic component."""
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
