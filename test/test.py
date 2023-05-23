# SPDX-License-Identifier: MIT

'''
facere-sensum unit tests.
'''

import os
import sys
import subprocess # nosec B404
import shutil
import unittest
import facere_sensum.facere_sensum as fs

# Generate paths for test output and reference.
_LOG = os.path.join('test', 'log.csv')
_REF = os.path.join('test', 'ref.csv')

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
        # Minimal extreme: all metrics are zero.
        _setup_test_input([0,0,0])
        fs.score_combined(_LOG, 'A')

        # Maximal extreme: all metrics are one.
        _setup_test_input([1,1,1])
        fs.score_combined(_LOG, 'B')

        # Various values for metrics.
        _setup_test_input([.25,.5,.75])
        fs.score_combined(_LOG, 'C')

        # Compare with a reference.
        with open(_LOG, encoding='ascii') as log:
            with open(_REF, encoding='ascii') as ref:
                self.assertEqual(log.readlines(), ref.readlines())

if __name__ == '__main__':
    print('Integration tests: ', end='')

    # Log file not found test.
    fs_py = ['python', os.path.join('src', 'facere_sensum', 'facere_sensum.py'), 'llog.csv']
    res = subprocess.run(fs_py, check=False, capture_output=True, text=True).stdout # nosec B603
    if res == 'Log file \'llog.csv\' not found. Exiting.\n':
        print('OK')
    else:
        print('FAILED')
        sys.exit(1)

    # Unit tests
    shutil.copy('log.csv', 'test')
    unittest.main()
