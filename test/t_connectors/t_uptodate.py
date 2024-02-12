# SPDX-License-Identifier: MIT

'''
Data connector for tracking assets to be up-to-date - testing support.
'''

from os import path
import json
from datetime import date
from facere_sensum.connectors import uptodate

def test():
    '''
    Test the data connector for tracking assets to be up-to-date.
    Return True if the test was successful, False otherwise.
    '''
    # Test the metrics from examples.
    with open(path.join('examples', 'config_uptodate.json'), encoding='utf-8') as config_file:
        metrics = json.load(config_file)['metrics']

    # Override today's date with a static date so that we get predictable test result.
    save = uptodate.today
    uptodate.today = lambda: date(2024,2,2)

    res = True
    for m,r,n in zip(metrics,[73,1,1095],[0.9,0.995,0]):
        raw = uptodate.get_raw(m)
        if raw != r or uptodate.get_normalized(m, r) != n:
            res = False
            break

    uptodate.today = save
    return res
