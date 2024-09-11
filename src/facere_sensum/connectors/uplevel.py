# SPDX-License-Identifier: MIT

"""
Metric source for upleveling collective metric behavior to a higher-level.
"""

import sys
import csv


def get_raw(metric):
    """
    Get raw metric score for upleveling: the latest layer score.
    'metric' is the metric definition.
    """
    log = metric["log"]
    try:
        with open(log, encoding="utf-8") as log_file:
            # The latest score will be in the pre-last row, last column.
            return float(list(csv.reader(log_file))[-2][-1])
    except FileNotFoundError:
        print(
            f"Error ('uplevel' metric source): layer data CSV file '{log}' not found. Exiting.",
            file=sys.stderr,
        )
        sys.exit(1)


def get_normalized(
    metric,  # pylint: disable=unused-argument
    raw,
):
    """
    Get normalized metric score for upleveling. It is the same as raw.
    'metric' is the metric definition.
    'raw' is the raw metric score.
    """
    return raw
