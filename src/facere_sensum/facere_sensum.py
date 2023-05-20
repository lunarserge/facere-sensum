# SPDX-License-Identifier: MIT

'''
facere-sensum: make sense of the turmoil.
'''

from argparse import ArgumentParser
import datetime
import numpy as np
import pandas as pd

VERSION = '0.0.2'

def score_manual(metric):
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

def score_combined(log_file, marker):
    '''
    Process the log file by scoring all the metrics and updating priorities for the future.
    Return combined score.
    'marker' is the identificator to be used with the scoring (e.g., the date of data collection).
    '''
    data = pd.read_csv(log_file)

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
    parser.add_argument('--version', action='version', version='%(prog)s '+VERSION)
    parser.add_argument('log', nargs='?', default='log.csv',
                        help='log file in CSV format (default: log.csv)')

    score_combined(parser.parse_args().log, datetime.date.today())
    print('\nSee you next time!')
