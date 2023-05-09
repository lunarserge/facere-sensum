# SPDX-License-Identifier: MIT

'''
facere-sensum unit tests.
'''

import unittest

class Test(unittest.TestCase):
    '''
    Test cases.
    '''

    def test(self):
        '''
        Just make this pass for now to test the infrastructure itself.
        '''
        self.assertTrue(self) # Pylint flags redundancy if simple True is used

if __name__ == '__main__':
    unittest.main()
