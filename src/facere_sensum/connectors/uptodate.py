# SPDX-License-Identifier: MIT

'''
Data connector for tracking assets to be up-to-date.
'''

import sys
from datetime import date
from .GitHub import _github as gh

# Default success target for an up-to-date asset: no older than one year.
_TARGET = 365

# Index for the last commit is 0 (default, for regular execution).
# Index for the first commit is -1 (for test execution).
# The testing framework replaces the default value with -1 to get predictable test result
# since the first commit date is fixed.
commit_index = -1 # pylint: disable=invalid-name

def today(): # pragma: no cover
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
    updated = date.fromisoformat(metric['updated']) if 'updated' in metric else None

    method = metric['method'] if 'method' in metric else 'manual'
    match method:
        case 'manual':
            if updated is None:
                print("Error ('uptodate' connector): "
                      "no 'updated' field provided with 'manual' method. Exiting.", file=sys.stderr)
                sys.exit(1)

        case 'github.com':
            if 'path' not in metric:
                print("Error ('uptodate' connector): "
                      "no 'path' field provided with 'github.com' method. Exiting.",
                      file=sys.stderr)
                sys.exit(1)
            path = metric['path']

            # First two elements in the path point to a repo, the rest - to a particular file.
            # Finding the index that separates the repo from the file path.
            i = path.index('/', path.index('/',1)+1)

            # Get the last commit for regular execution, the first commit for testing.
            commit = list(gh.g.get_repo(path[:i]).get_commits(path=path[i+1:]))[commit_index].commit

            committed = commit.committer.date.date()
            updated = max(updated, committed) if updated else committed

        case _:
            print(f"Error ('uptodate' connector): unknown method '{method}'. Exiting.",
                  file=sys.stderr)
            sys.exit(1)

    return (today()-updated).days

def get_normalized(metric, raw):
    '''
    Get standard (i.e., normalized) metric score for tracking assets to be up-to-date.
    'metric' is the metric JSON description.
    'raw' is the raw metric score.
    '''
    target = metric['target'] if 'target' in metric else _TARGET
    outdated = target * 2
    return 0 if raw >= outdated else (outdated-raw)/outdated
