# SPDX-License-Identifier: MIT

"""
Metric source for GitHub forks.
"""

from . import _github as gh

# Default success target for GutHub forks.
_TARGET = 100


def get_raw(
    metric,
):  # pragma: no cover - can't test REST API response changing over time.
    """
    Get raw metric score for GitHub forks: their number.
    'metric' is the metric definition.
    """
    return gh.g.get_repo(metric["repo"]).forks_count


def get_normalized(metric, raw):
    """
    Get normalized metric score for GitHub forks.
    'metric' is the metric definition.
    'raw' is the raw metric score.
    """
    return gh.get_normalized(metric, raw, _TARGET)
