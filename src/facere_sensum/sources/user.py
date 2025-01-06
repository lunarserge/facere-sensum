# SPDX-License-Identifier: MIT

"""
Metric source for direct user input.
"""


def get_raw(metric):  # pragma: no cover - can't automatically test direct user input
    """
    Get raw metric score for direct user input.
    'metric' is the metric definition.
    """
    metric = metric["id"]
    while True:
        score = float(input(f"Enter score for '{metric}': "))
        if 0 <= score <= 1:
            return score
        print("Entered score is outside 0..1 range, enter again")


def get_normalized(
    metric,  # pylint: disable=unused-argument
    raw,
):
    """
    Get normalized metric score for direct user input. It is the same as raw.
    'metric' is the metric definition.
    'raw' is the raw metric score.
    """
    return raw
