# SPDX-License-Identifier: MIT

'''
Data connector for upleveling collective metric behavior to a higher-level.
'''

import sys
import csv

def get_raw(metric):
    '''
    Get metric score as the latest combined facere-sensum layer score.
    'metric' is the metric JSON description.
    '''
    log = metric['log']
    try:
        with open(log, encoding='utf-8') as log_file:
            # The latest score will be in the pre-last row, last column.
            return float(list(csv.reader(log_file))[-2][-1])
    except FileNotFoundError:
        print('Error (upleveling collective metric behavior connector): '
              f"layer data CSV file '{log}' not found. Exiting.",
              file=sys.stderr)
        sys.exit(1)

def get_normalized(metric, raw): # pylint: disable=unused-argument
    '''
    Get standard (i.e., normalized) metric score for upleveling. It is the same as raw.
    'metric' is the metric JSON description.
    'raw' is the raw metric score.
    '''
    return raw
