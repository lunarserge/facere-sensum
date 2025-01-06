# SPDX-License-Identifier: MIT

'''
Data connector for GitHub stars - testing support.
'''

from os import path
import json
from facere_sensum.sources.GitHub import star

def test():
    '''
    Test GitHub stars data connector.
    Return True if the test was successful, False otherwise.
    '''
    # Metric from examples.
    with open(path.join('examples', 'config_github.json'), encoding='utf-8') as config_file:
        metric0 = json.load(config_file)['metrics'][0]

    metric1 = {
        'id': 'test case for stars with default target',
        'source': 'GitHub.star',
        'repo': 'lunarserge/facere-sensum'
    }
    metric2 = {
        'id': 'test case for stars with specified target',
        'source': 'GitHub.star',
        'repo': 'lunarserge/facere-sensum',
        'target': 10
    }

    return star.get_normalized(metric0, 100) == .05 and \
        star.get_normalized(metric1, 10) == .005 and \
        star.get_normalized(metric2, 1) == .05
