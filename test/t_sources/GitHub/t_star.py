# SPDX-License-Identifier: MIT

"""
Metric source for GitHub stars - testing support.
"""

import os
import json
from facere_sensum.sources.GitHub import star


def test():
    """
    Test GitHub stars metric source.
    Return True if the test was successful, False otherwise.
    """
    # Metric from examples.
    with open(
        os.path.join("examples", "config_github.json"), encoding="utf-8"
    ) as layer_config:
        metric0 = json.load(layer_config)["metrics"][0]

    metric1 = {
        "id": "test case for stars with default target",
        "source": "GitHub.star",
        "repo": "lunarserge/facere-sensum",
    }
    metric2 = {
        "id": "test case for stars with specified target",
        "source": "GitHub.star",
        "repo": "lunarserge/facere-sensum",
        "target": 10,
    }

    return (
        star.get_normalized(metric0, 100) == 0.05
        and star.get_normalized(metric1, 10) == 0.005
        and star.get_normalized(metric2, 1) == 0.05
    )
