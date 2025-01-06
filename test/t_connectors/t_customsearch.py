# SPDX-License-Identifier: MIT

'''
Data connector for Google Custom Search API - testing support.
'''

from os import path
import json
from facere_sensum.sources import customsearch

# Load mock response from the Custom Search API.
with open(path.join('test', 'input', 'customsearch.json'), encoding='utf-8') as cs_file:
    _cse_result = json.load(cs_file)

def _mock_up_data():
    '''
    Mock Google Custom Search API response.
    '''
    customsearch.invoke_cse = lambda term, start: _cse_result

def _test(metric, expected_raw, expected_value):
    '''
    Test Google Custom Search API data connector with one of the test metrics
    against its expected outcomes.
    Return True if the test was successful, False otherwise.
    '''
    _mock_up_data()
    if customsearch.get_raw(metric) != expected_raw:
        return False

    _mock_up_data()
    return customsearch.get_normalized(metric, expected_raw) == expected_value

def test():
    '''
    Test Google Custom Search API data connector.
    Return True if the test was successful, False otherwise.
    '''
    # Metric from examples.
    with open(path.join('examples', 'config_customsearch.json'), encoding='utf-8') as config_file:
        metric1 = json.load(config_file)['metrics'][1]

    # Metric to test for target URL that doesn't appear in search results.
    metric2 = {
        'id': 'obstacle course racing',
        'source': 'customsearch',
        'num': 10,
        'URL': 'https://www.notfound.com/'
    }

    return _test(metric1, 4, 0.85) & _test(metric2, 0, 0)
