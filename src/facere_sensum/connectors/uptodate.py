# SPDX-License-Identifier: MIT

'''
Data connector for tracking assets to be up-to-date.
'''

from datetime import date

# Default success target for an up-to-date asset: no older than one year.
_TARGET = 365

def today():
    '''
    Get today's date.
    This function is to support testing by overriding it with a static date.
    Can't override date.today directly since datetime.date is immutable.
    '''
    return date.today()

def get_raw(metric):
    '''
    Get metric score as number of days passed since the specified date.
    'metric' is the metric JSON description.
    '''
    return (today()-date.fromisoformat(metric['updated'])).days

def get_normalized(metric, raw):
    '''
    Get standard (i.e., normalized) metric score for tracking assets to be up-to-date.
    'metric' is the metric JSON description.
    'raw' is the raw metric score.
    '''
    target = metric['target'] if 'target' in metric else _TARGET
    outdated = target * 2
    return 0 if raw >= outdated else (outdated-raw)/outdated
