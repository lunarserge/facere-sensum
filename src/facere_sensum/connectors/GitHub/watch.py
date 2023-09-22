# SPDX-License-Identifier: MIT

'''
Data connector for number of GitHub watchers.
'''

from . import _github as gh

# Default success target for GutHub watchers.
_TARGET = 50

def get_raw(metric): # pragma: no cover - can't test REST API response changing over time.
    '''
    Get raw metric score for GitHub watchers: their number.
    'metric' is the metric JSON description.
    '''
    return gh.g.get_repo(metric['repo']).subscribers_count

def get_normalized(metric, raw):
    '''
    Get standard (i.e., normalized) metric score for GitHub watchers.
    'metric' is the metric JSON description.
    'raw' is the raw metric score.
    '''
    return gh.get_normalized(metric,raw,_TARGET)
