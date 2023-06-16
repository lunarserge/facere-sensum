# SPDX-License-Identifier: MIT

'''
facere-sensum unit tests.
'''

import os
import sys
import subprocess # nosec B404
import json
import shutil
import unittest
from connectors import t_user
import facere_sensum.facere_sensum as fs

def _gen_path(file_name):
    '''
    Generate a path inside the testing folder.
    'file_name' is a name to put into testing.
    '''
    return os.path.join('test', file_name)

# Generate paths for test output and references.
_LOG         = _gen_path('log.csv')
_REF_BASE    = _gen_path('ref_base.csv')
_REF_UPDATED = _gen_path('ref_updated.csv')

with open('config.json', encoding='utf-8') as config:
    _CONFIG = json.load(config)

def _logs_equal(log1, log2):
    '''
    Compare two logs.
    Return True if logs are equal, Flase otherwise.
    '''
    # Need to compare line by line to ignore end-of-line differences between Linux and Windows.
    with open(log1, encoding='utf8') as file1:
        with open(log2, encoding='utf8') as file2:
            return file1.readlines() == file2.readlines()

class Test(unittest.TestCase):
    '''
    Test cases.
    '''

    def test_command_create(self):
        '''
        Test facere_sensum.command_create function.
        '''
        fs.command_create(_CONFIG, _LOG)
        self.assertTrue(_logs_equal(_LOG, _REF_BASE))

    def test_score_combined(self):
        '''
        Test facere_sensum.score_combined function.
        '''
        shutil.copy(_REF_BASE, _LOG)

        # Minimal extreme: all metrics are zero.
        t_user.mock_up_data([0,0,0])
        fs.command_update(_CONFIG, _LOG, 'A')

        # Maximal extreme: all metrics are one.
        t_user.mock_up_data([1,1,1])
        fs.command_update(_CONFIG, _LOG, 'B')

        # Various values for metrics.
        t_user.mock_up_data([.25,.5,.75])
        fs.command_update(_CONFIG, _LOG, 'C')

        # Compare with a reference.
        self.assertTrue(_logs_equal(_LOG, _REF_UPDATED))

if __name__ == '__main__':
    print('Integration tests: ', end='')

    # Log file not found test.
    fs_py = ['python', os.path.join('src', 'facere_sensum', 'facere_sensum.py'),
             '--log', 'llog.csv', 'update']
    res = subprocess.run(fs_py, check=False, capture_output=True, text=True).stdout # nosec B603
    if res == 'Log file \'llog.csv\' not found. Exiting.\n':
        print('OK')
    else:
        print('FAILED. Output:', res)
        sys.exit(1)

    # Unit tests
    unittest.main()
