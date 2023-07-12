# SPDX-License-Identifier: MIT

'''
facere-sensum unit tests.
'''

import os
import sys
import subprocess # nosec B404
import importlib
import json
import shutil
import unittest
from facere_sensum import fs
from facere_sensum.connectors import user as user_connector

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

def _mock_up_direct_user_input(data):
    '''
    Mock direct user input.
    'data' is a list of values to be used instead of the actual user input.
    '''
    data = (item for item in data)
    user_connector.get_value = lambda metric: next(data)

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
        _mock_up_direct_user_input([0,0,0])
        fs.command_update(_CONFIG, _LOG_PATH, 'A')

        # Maximal extreme: all metrics are one.
        _mock_up_direct_user_input([1,1,1])
        fs.command_update(_CONFIG, _LOG_PATH, 'B')

        # Various values for metrics.
        _mock_up_direct_user_input([.25,.5,.75])
        fs.command_update(_CONFIG, _LOG_PATH, 'C')

        # Compare with a reference.
        self.assertTrue(_logs_equal(_LOG_PATH, _REF_UPDATED_PATH))

    def test_connectors(self):
        '''
        Test data connectors.
        '''
        # Load sample authentication config file so that all the connectors can load.
        # Connector loading only needs JSON scheme, not actual credentials.
        with open('auth.json', encoding='utf-8') as auth_file:
            fs.auth = json.load(auth_file)

        for file_name in os.listdir(os.path.join('test', 't_connectors')):
            if file_name.startswith('t_') and file_name.endswith('.py'):
                self.assertTrue(importlib.import_module('t_connectors.t_'+file_name[2:-3]).test())

def _test_integration(descr, args, ref):
    '''
    Run an integration test.
    'descr' is test user description.
    'args' command line arguments to use.
    'ref' expected output.
    '''
    print(descr, end=': ')
    res = subprocess.run(['python', 'fsy.py'] + args,
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
