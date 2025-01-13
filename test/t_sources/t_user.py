# SPDX-License-Identifier: MIT

"""
Metric source for direct user input - testing support.
"""

from facere_sensum.sources import user


def test():
    """
    Test direct user input metric source.
    Return True if the test was successful, False otherwise.
    """
    return user.get_normalized(None, 0.5) == 0.5
