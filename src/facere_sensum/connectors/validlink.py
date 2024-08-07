# SPDX-License-Identifier: MIT

'''
Data connector for ValidLink.
'''

import requests

def get_raw(metric):
    '''
    Get raw metric score for ValidLink:
    0 if URL produces a 404 error, 1 otherwise.
    'metric' is the metric JSON description.
    '''
    url = metric['URL']
    try:
        response = requests.head(url)
        return 0 if response.status_code == 404 else 1
    except requests.RequestException:
        return 0

def get_normalized(metric, raw):
    '''
    Get standard (i.e., normalized) metric score for ValidLink.
    'metric' is the metric JSON description.
    'raw' is the raw metric score.
    '''
    return raw
