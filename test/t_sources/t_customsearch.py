# SPDX-License-Identifier: MIT

"""
Metric source for Google Custom Search API - testing support.
"""

from os import path
import json
from facere_sensum.sources import customsearch

# Load mock response from the Custom Search API.
with open(path.join("test", "input", "customsearch.json"), encoding="utf-8") as cs_file:
    _cse_result = json.load(cs_file)
customsearch.invoke_cse = lambda term, start: _cse_result


def _test(metric, expected_raw, expected_norm):
    """
    Test Google Custom Search API metric source with one of the test metrics
    against its expected outcomes.
    Return True if the test was successful, False otherwise.
    """
    if customsearch.get_raw(metric) != expected_raw:
        return False

    return customsearch.get_normalized(metric, expected_raw) == expected_norm


def test():
    """
    Test Google Custom Search API metric source.
    Return True if the test was successful, False otherwise.
    """
    # Metric from examples.
    with open(
        path.join("examples", "config_customsearch.json"), encoding="utf-8"
    ) as layer_config:
        metric1 = json.load(layer_config)["metrics"][1]

    # Metric to test for target URL that doesn't appear in search results.
    metric2 = {
        "id": "obstacle course racing",
        "source": "customsearch",
        "num": 10,
        "URL": "https://www.notfound.com/",
    }

    return _test(metric1, 4, 0.85) and _test(metric2, 0, 0)
