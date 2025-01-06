# SPDX-License-Identifier: MIT

"""
Common functionality for GitHub metric sources.
"""

import github
from facere_sensum import fs

_token = fs.get_3rd_party_auth("GitHub", "personal access token")
g = github.Github(auth=github.Auth.Token(_token) if _token else None)


def get_normalized(metric, raw, target):
    """
    Get normalized metric score for a GitHub metric.
    'metric' is the metric definition.
    'raw' is the raw metric score.
    'target' is the success target for the normalized metric to hit 0.5 mark.
    """
    if "target" in metric:
        target = metric["target"]
    perfect = target * 2
    return 1 if raw >= perfect else raw / perfect
