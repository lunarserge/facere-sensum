# SPDX-License-Identifier: MIT

'''
Data connector for ValidLink - testing support.
'''

from facere_sensum.connectors import validlink

def test():
    '''
    Test ValidLink data connector.
    Return True if the test was successful, False otherwise.
    '''
    metric1 = {
        'id': 'test case for valid URL',
        'source': 'validlink',
        'URL': 'https://www.example.com/'
    }
    metric2 = {
        'id': 'test case for 404 URL',
        'source': 'validlink',
        'URL': 'https://www.example.com/404'
    }

    return validlink.get_raw(metric1) == 1 and \
        validlink.get_raw(metric2) == 0 and \
        validlink.get_normalized(metric1, 1) == 1 and \
        validlink.get_normalized(metric2, 0) == 0
