# SPDX-License-Identifier: MIT

'''
facere-sensum: make sense of the turmoil.
'''

import sys
import json
import csv
from argparse import ArgumentParser
import datetime
import numpy as np
import pandas as pd

VERSION = '0.0.5'

def score_manual(metric): # pragma: no cover - function is replaced by automated data in tests
    '''
    Get metric score as a direct user input.
    'metric' is the metric text description.
    '''
    while True:
        score = float(input(f'  - {metric}: '))
        if 0 <= score <= 1:
            return score
        print('Entered score is outside 0..1 range, enter again')

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
    'config' is config in JSON form.
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

def command_update(log_file, marker):
    '''
    Process the log file by scoring all the metrics and updating priorities for the future.
    Return combined score.
    'log_file' is the name for the log.
    'marker' is the identificator to be used with the scoring (e.g., the date of data collection).
    '''
    try:
        data = pd.read_csv(log_file)
    except FileNotFoundError:
        print('Log file \''+log_file+'\' not found. Exiting.')
        sys.exit(1)

    # Infer metrics from priority column names.
    metrics = [s[2:-1] for s in data.columns[1:-1:2]]

    priorities = data.iloc[-1,1:-1:2] # pick priorities from the last row
    priorities_combined = sum(priorities)
    if abs(priorities_combined-1) > 0.001:
        print("Warning: last row priorities don't sum up to 1 " \
              f"(sum is ~{priorities_combined:.2f})\n")

    print(f'\nEnter scoring for {marker} (each score must be within 0..1 range):')
    scores = [score_manual(metric) for metric in metrics]
    score_comb = np.dot(priorities, scores)
    print(f'\nYour combined score for {marker} is ~{score_comb:.2f}')

    # Populate date and scores in the last row in preparation for the log file update.
    data.iloc[-1,0] = marker
    data.iloc[-1,2:-1:2] = scores
    data.iloc[-1,-1] = score_comb

    priorities = _compute_new_priorities(priorities, scores)
    print('\nYour new priorities are:')
    pairs = list(zip(metrics, priorities))
    pairs.sort(key=lambda pair: pair[1], reverse=True)
    for (metric,priority) in pairs:
        print(f'  - {metric}: {priority:.2f}')

    # Create a new row and store new priorities in it.
    new_row = [None] # date is empty
    for priority in priorities:
        new_row.append(priority)
        new_row.append(None) # individual scores are empty
    new_row.append(None) # combined score is empty
    data.loc[len(data)] = new_row

    data.to_csv(log_file, index=False)
    print(log_file, 'is updated')
    return score_comb

def main():
    '''
    CLI entry.
    '''
    parser = ArgumentParser(description='Make sense of the turmoil')
    parser.add_argument('command', choices=['create', 'update'],
                        help='high-level action to perform')
    parser.add_argument('--version', action='version', version='%(prog)s '+VERSION)
    parser.add_argument('--config', nargs='?', default='config.json',
                        help='metrics config (see README for details, default: config.json)')
    parser.add_argument('--log', nargs='?', default='log.csv',
                        help='CSV log file name (default: log.csv)')
    args = parser.parse_args()

    try:
        with open(args.config, encoding='utf-8') as config:
            config = json.load(config)
    except FileNotFoundError:
        print('Config file \''+args.config+'\' not found. Exiting.')
        sys.exit(1)

    if args.command == 'create':
        command_create(config, args.log)
    elif args.command == 'update':
        command_update(args.log, datetime.date.today())
        print('\nSee you next time!')
    else:
        # Should never get here given that all the actions are processed above.
        print('Something weird happened.',
              'Please submit an issue at https://github.com/lunarserge/facere-sensum/issues/new',
              'with the command that led here.')
        sys.exit(1)

if __name__ == '__main__':
    main()
