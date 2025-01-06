# SPDX-License-Identifier: MIT

'''
Data connector for direct user input - testing support.
'''

from facere_sensum.sources import user

def test():
    '''
    Test direct user input data connector.
    Return True if the test was successful, False otherwise.
    '''
    return user.get_normalized(None, .5) == .5
