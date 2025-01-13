# SPDX-License-Identifier: MIT

"""
Metric source for tracking assets to be up-to-date - testing support.
"""

import os
import json
from datetime import date
from facere_sensum.sources import uptodate


def test():
    """
    Test the metric source for tracking assets to be up-to-date.
    Return True if the test was successful, False otherwise.
    """
    # Test the metrics from examples.
    with open(
        os.path.join("examples", "config_uptodate.json"), encoding="utf-8"
    ) as layer_config:
        metrics = json.load(layer_config)["metrics"]

    # Override today's date with a static date so that we get predictable test result.
    save = uptodate.today
    uptodate.today = lambda: date(2024, 2, 2)

    # Use first (not last) commit for testing 'github.com' method to get predictable test result.
    uptodate.commit_index = -1

    res = True
    for m, r, n in zip(metrics, [73, 1, 1095, 211], [0.9, 0.995, 0, 0.710]):
        raw = uptodate.get_raw(m)
        if raw != r or abs(n - uptodate.get_normalized(m, r)) >= 0.001:
            res = False
            break

    uptodate.commit_index = (
        0  # This is not necessary but it is a good practice to reset back.
    )
    uptodate.today = save
    return res
