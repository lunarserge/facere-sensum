# SPDX-License-Identifier: MIT

'''
Data connector for GitHub forks - testing support.
'''

from os import path
import json
from facere_sensum.connectors.GitHub import fork

def test():
    '''
    Test GitHub forks data connector.
    Return True if the test was successful, False otherwise.
    '''
    # Metric from examples.
    with open(path.join('examples', 'config_github.json'), encoding='utf-8') as config_file:
        metric0 = json.load(config_file)['metrics'][1]

    metric1 = {
        'id': 'test case for forks with default target',
        'source': 'GitHub.fork',
        'repo': 'lunarserge/facere-sensum'
    }
    metric2 = {
        'id': 'test case for forks with specified target',
        'source': 'GitHub.fork',
        'repo': 'lunarserge/facere-sensum',
        'target': 10
    }

    return fork.get_normalized(metric0, 10) == .5 and \
        fork.get_normalized(metric1, 10) == .05 and \
        fork.get_normalized(metric2, 1) == .05
