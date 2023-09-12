# SPDX-License-Identifier: MIT

'''
Data connector for direct user input.
'''

def get_raw(metric): # pragma: no cover - can't automatically test direct user input
    '''
    Get metric score as a direct user input.
    'metric' is the metric JSON description.
    '''
    metric = metric['id']
    while True:
        score = float(input(f"Enter score for '{metric}': "))
        if 0 <= score <= 1:
            return score
        print('Entered score is outside 0..1 range, enter again')

def get_normalized(metric, raw): # pylint: disable=unused-argument
    '''
    Get standard (i.e., normalized) metric score for a direct user input. It is the same as raw.
    'metric' is the metric JSON description.
    'raw' is the raw metric score.
    '''
    return raw
