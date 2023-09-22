# SPDX-License-Identifier: MIT

'''
facere-sensum: make sense of the turmoil.
'''

import sys
import importlib
import json
import csv
from argparse import ArgumentParser
import datetime
import numpy as np
import pandas as pd
import prettytable

VERSION = '0.0.5'

def _compute_new_priorities(priorities, scores):
    '''
    Compute new priorities so that lagging metrics get a bump,
    but all the priorities still sum up to 1. Return a list with new priorities.
    'priorities' is a list with previous priorities.
    'scores' is a matching list with the scoring.
    '''
    # For top performing metrics (the score is 1) the priority doesn't raise.
    # For comletely failed metrics (the score is 0) the priority grows 2x.
    # Or anything else in the middle depending on the metric value.
    priorities = list(map(lambda priority,score: priority+(1-score)*priority, priorities, scores))

    # Normalize so that priorities sup up to 1
    coeff = sum(priorities)
    return list(map(lambda priority: priority/coeff, priorities))

def command_create(config, log_file):
    '''
    Create the CSV log file using provided config.
    'config' is project config in JSON form.
    'log_file' is the name for the log.
    '''
    with open(log_file, 'w', encoding='utf-8', newline='') as log:
        writer = csv.writer(log)

        # Write header row.
        row = ['ID']
        for metric in config['metrics']:
            qualifier = '(' + metric['id'] + ')'
            row.append('P' + qualifier)
            row.append('S' + qualifier)
        row.append('Score')
        writer.writerow(row)

        # Write first row with initial priorities.
        row = ['']
        for metric in config['metrics']:
            row.append(metric['priority'])
            row.append('')
        row.append('')
        writer.writerow(row)

    print(log_file, 'is created')

# Map of pairs: data connector name / connector module.
_connectors = {}

def _score(metric):
    '''
    Get raw and normalized metric scores.
    'metric' is the metric JSON description.
    '''
    source = metric['source']

    if source == 'const':
        res = metric['value']
        return res, res

    if not source in _connectors:
        _connectors[source] = importlib.import_module('facere_sensum.connectors.'+source)

    source = _connectors[source]
    raw = source.get_raw(metric)
    return raw, source.get_normalized(metric, raw)

def _print_report(metrics, scores):
    '''
    Print report with the computed metric scores.
    'metrics' is a list with layer metrics.
    'scores' is a list of tuples with corresponding raw and normalized scores.
    '''
    table = prettytable.PrettyTable(['Metric', 'Raw', 'Normalized'])
    for metric,score in zip(metrics,scores):
        table.add_row([metric['id'], score[0], score[1]])
    print()
    print(table)

def command_update(config, log_file, marker):
    '''
    Process the log file by scoring all the metrics and updating priorities for the future.
    Return combined score.
    'config' is project config in JSON form.
    'log_file' is the name for the log.
    'marker' is the identificator to be used with the scoring (e.g., the date of data collection).
    '''
    try:
        data = pd.read_csv(log_file)
    except FileNotFoundError:
        print('Log file \''+log_file+'\' not found. Exiting.')
        sys.exit(1)
    data = data.astype({'ID': 'string'})

    priorities = data.iloc[-1,1:-1:2] # pick priorities from the last row
    priorities_combined = sum(priorities)
    if abs(priorities_combined-1) > 0.001:
        print("Warning: last row priorities don't sum up to 1 " \
              f"(sum is ~{priorities_combined:.2f})\n")

    print(f'\nScoring for {marker}:')
    metrics = config['metrics']
    scores = []
    for metric in metrics:
        scores.append(_score(metric))

    _print_report(metrics, scores)

    norm_scores = [score[1] for score in scores]
    score_comb = np.dot(priorities, norm_scores)
    print(f'\nYour combined score for {marker} is ~{score_comb:.2f}')

    # Populate date and scores in the last row in preparation for the log file update.
    data.iloc[-1,0] = str(marker)
    data.iloc[-1,2:-1:2] = norm_scores
    data.iloc[-1,-1] = score_comb

    if 'weights' in config and config['weights'] == 'dynamic':
        priorities = _compute_new_priorities(priorities, norm_scores)
        print('\nYour new priorities are:')
        pairs = list(zip([metric['id'] for metric in metrics], priorities))
        pairs.sort(key=lambda pair: pair[1], reverse=True)
        for (metric,priority) in pairs:
            print(f'  - {metric}: {priority:.2f}')

    # Create a new row and store new priorities in it.
    new_row = [''] # date is empty
    for priority in priorities:
        new_row.append(priority)
        new_row.append(0) # individual scores are zero until measured
    new_row.append(0) # combined score is zero until measured
    data.loc[len(data)] = new_row

    data.to_csv(log_file, index=False)
    print(log_file, 'is updated')
    return score_comb

def get_3rd_party_entry(party, entry):
    '''
    Get 3rd parthy entry from the authentication config.
    'party' is the 3rd party name.
    'entry' is the entry name.
    Return the requested entry if it is specified via the authentication config, None otherwise.
    '''
    if not 'auth' in globals():
        return None # No authentication config at all.
    config = globals()['auth']
    if not party in config:
        return None # No authentication info for the specified 3rd party.
    party = config[party]
    return party[entry] if entry in party else None

def main():
    '''
    CLI entry.
    '''
    parser = ArgumentParser(description='Make sense of the turmoil')
    parser.add_argument('command', choices=['create', 'update'],
                        help='high-level action to perform')
    parser.add_argument('--version', action='version', version='%(prog)s '+VERSION)
    parser.add_argument('--auth', nargs='?', help='authentication config')
    parser.add_argument('--config', nargs='?', default='config.json',
                        help='project config (default: config.json)')
    args = parser.parse_args()

    if args.auth:
        try :
            with open(args.auth, encoding='utf-8') as auth_file:
                # Put authentication config in global scope
                # for all other modules to access as necessary.
                globals()['auth'] = json.load(auth_file)
        except FileNotFoundError:
            print('Authentication config file \''+args.auth+'\' not found. Exiting.',
                  file=sys.stderr)
            sys.exit(1)

    try:
        with open(args.config, encoding='utf-8') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print('Project config file \''+args.config+'\' not found. Exiting.', file=sys.stderr)
        sys.exit(1)

    log = config['log']
    if args.command == 'create':
        command_create(config, log)
    elif args.command == 'update':
        command_update(config, log, datetime.date.today())
        print('\nSee you next time!')
    else: # pragma: no cover
        # Should never get here given that all the actions are processed above.
        print('Something weird happened.',
              'Please submit an issue at https://github.com/lunarserge/facere-sensum/issues/new',
              'with the command that led here.')
        sys.exit(1)
