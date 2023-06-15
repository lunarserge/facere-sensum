'''
Data connector for direct user input.
'''

def get_value(metric): # pragma: no cover - can't automatically test direct user input
    '''
    Get metric score as a direct user input.
    'metric' is the metric JSON description.
    '''
    metric = metric['id']
    while True:
        score = float(input(f'  - {metric}: '))
        if 0 <= score <= 1:
            return score
        print('Entered score is outside 0..1 range, enter again')
