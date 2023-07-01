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
from t_connectors import t_user
from facere_sensum import fs

# Generate paths for test files.
_CONFIG_PATH      = os.path.join('examples', 'config_personal.json')
_LOG_PATH         = 'log.csv'
_REF_BASE_PATH    = os.path.join('test', 'output', 'ref_base.csv')
_REF_UPDATED_PATH = os.path.join('test', 'output', 'ref_updated.csv')

with open(_CONFIG_PATH, encoding='utf-8') as config:
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
        fs.command_create(_CONFIG, _LOG_PATH)
        self.assertTrue(_logs_equal(_LOG_PATH, _REF_BASE_PATH))

    def test_score_combined(self):
        '''
        Test facere_sensum.score_combined function.
        '''
        shutil.copy(_REF_BASE_PATH, _LOG_PATH)

        # Minimal extreme: all metrics are zero.
        t_user.mock_up_data([0,0,0])
        fs.command_update(_CONFIG, _LOG_PATH, 'A')

        # Maximal extreme: all metrics are one.
        t_user.mock_up_data([1,1,1])
        fs.command_update(_CONFIG, _LOG_PATH, 'B')

        # Various values for metrics.
        t_user.mock_up_data([.25,.5,.75])
        fs.command_update(_CONFIG, _LOG_PATH, 'C')

        # Compare with a reference.
        self.assertTrue(_logs_equal(_LOG_PATH, _REF_UPDATED_PATH))

def _test_integration(descr, args, ref):
    '''
    Run an integration test.
    'descr' is test user description.
    'args' command line arguments to use.
    'ref' expected output.
    '''
    print(descr, end=': ')
    res = subprocess.run(['python',
                         os.path.join('src', 'facere_sensum', 'fs.py')] + args,
                         check=False, capture_output=True, text=True).stdout # nosec B603
    if res == ref:
        print('OK')
    else:
        print('FAILED', 'Output:', '---', res, '---', 'Expected:', '---', ref, '---', sep='\n')
        sys.exit(1)

if __name__ == '__main__':
    print('Integration tests:')
    _test_integration('Authentication config not found',
                      ['--auth', 'notfound.json', 'update'],
                      'Authentication config file \'notfound.json\' not found. Exiting.\n')
    _test_integration('Project config not found',
                      ['--config', 'notfound.json', 'update'],
                      'Project config file \'notfound.json\' not found. Exiting.\n')
    _test_integration('Create command', ['--config', _CONFIG_PATH, 'create'],
                      'log.csv is created\n')

    # Unit tests
    unittest.main()
