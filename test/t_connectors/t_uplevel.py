# SPDX-License-Identifier: MIT

'''
Data connector for upleveling collective metric behavior to a higher-level - testing support.
'''

from os import path
import json
from facere_sensum.connectors import uplevel

def test():
    '''
    Test the data connector for upleveling collective metric behavior to a higher-level.
    Return True if the test was successful, False otherwise.
    '''
    # Test the metric from examples.
    with open(path.join('examples', 'config_uplevel.json'), encoding='utf-8') as config_file:
        metric = json.load(config_file)['metrics'][0]

    raw = uplevel.get_raw(metric)
    return raw == 0.475 and uplevel.get_normalized(metric, raw) == 0.475
