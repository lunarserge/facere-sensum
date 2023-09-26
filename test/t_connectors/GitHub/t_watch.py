# SPDX-License-Identifier: MIT

'''
Data connector for GitHub watchers - testing support.
'''

from os import path
import json
from facere_sensum.connectors.GitHub import watch

def test():
    '''
    Test GitHub watchers data connector.
    Return True if the test was successful, False otherwise.
    '''
    # Metric from examples.
    with open(path.join('examples', 'config_github.json'), encoding='utf-8') as config_file:
        metric0 = json.load(config_file)['metrics'][2]

    metric1 = {
        'id': 'test case for watchers with default target',
        'source': 'GitHub.watch',
        'repo': 'lunarserge/facere-sensum'
    }
    metric2 = {
        'id': 'test case for watchers with specified target',
        'source': 'GitHub.watch',
        'repo': 'lunarserge/facere-sensum',
        'target': 10
    }

    return watch.get_normalized(metric0, 20) == 1 and \
        watch.get_normalized(metric1, 10) == .1 and \
        watch.get_normalized(metric2, 1) == .05
