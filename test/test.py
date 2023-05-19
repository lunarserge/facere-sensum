# SPDX-License-Identifier: MIT

'''
facere-sensum unit tests.
'''

import os
import shutil
import unittest
import facere_sensum.facere_sensum as fs

def _setup_test_input(user_input):
    '''
    Mocks direct user input by replacing prompting with a generating from a pre-defined list.
    'user_input' is a list of values to be used instead of the actual user input.
    '''
    user_input = (item for item in user_input)
    fs.score_manual = lambda metric: next(user_input)

class Test(unittest.TestCase):
    '''
    Test cases.
    '''

    def test_score_combined(self):
        '''
        Test facere_sensum.score_combined function.
        '''
        log = os.path.join('test', 'log.csv')

        # Minimal extreme: all metrics are zero.
        _setup_test_input([0,0,0])
        fs.score_combined(log, 'A')

        # Maximal extreme: all metrics are one.
        _setup_test_input([1,1,1])
        fs.score_combined(log, 'B')

        # Various values for metrics.
        _setup_test_input([.25,.5,.75])
        fs.score_combined(log, 'C')

        # Compare with a reference.
        with open(log, encoding='ascii') as log:
            with open(os.path.join('test', 'ref.csv'), encoding='ascii') as ref:
                self.assertEqual(log.readlines(), ref.readlines())

if __name__ == '__main__':
    shutil.copy('log.csv', 'test')
    unittest.main()
