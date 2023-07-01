# SPDX-License-Identifier: MIT

'''
Data connector for direct user input - testing support.
'''

import facere_sensum.connectors.user as user_connector

def mock_up_data(data):
    '''
    Mocks direct user input.
    'data' is a list of values to be used instead of the actual user input.
    '''
    data = (item for item in data)
    user_connector.get_value = lambda metric: next(data)
