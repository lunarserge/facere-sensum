# SPDX-License-Identifier: MIT

"""
Metric source for upleveling collective metric behavior to a higher-level - testing support.
"""

import os
import json
from facere_sensum.sources import uplevel


def test():
    """
    Test the metric source for upleveling collective metric behavior to a higher-level.
    Return True if the test was successful, False otherwise.
    """
    # Test the metric from examples.
    with open(
        os.path.join("examples", "config_uplevel.json"), encoding="utf-8"
    ) as layer_config:
        metric = json.load(layer_config)["metrics"][0]

    raw = uplevel.get_raw(metric)
    return raw == 0.475 and uplevel.get_normalized(metric, raw) == 0.475
