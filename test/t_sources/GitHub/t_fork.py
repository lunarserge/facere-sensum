# SPDX-License-Identifier: MIT

"""
Metric source for GitHub forks - testing support.
"""

import os
import json
from facere_sensum.sources.GitHub import fork


def test():
    """
    Test GitHub forks metric source.
    Return True if the test was successful, False otherwise.
    """
    # Metric from examples.
    with open(
        os.path.join("examples", "config_github.json"), encoding="utf-8"
    ) as layer_config:
        metric0 = json.load(layer_config)["metrics"][1]

    metric1 = {
        "id": "test case for forks with default target",
        "source": "GitHub.fork",
        "repo": "lunarserge/facere-sensum",
    }
    metric2 = {
        "id": "test case for forks with specified target",
        "source": "GitHub.fork",
        "repo": "lunarserge/facere-sensum",
        "target": 10,
    }

    return (
        fork.get_normalized(metric0, 10) == 0.5
        and fork.get_normalized(metric1, 10) == 0.05
        and fork.get_normalized(metric2, 1) == 0.05
    )
