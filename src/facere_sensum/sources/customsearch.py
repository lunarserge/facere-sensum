# SPDX-License-Identifier: MIT

"""
Metric source for Google Custom Search API.
"""

from googleapiclient.discovery import build
from facere_sensum import fs

# Default number of search results to consider.
_NUM = 20

_cse = build(  # pylint: disable=E1101
    "customsearch",
    "v1",
    developerKey=fs.get_3rd_party_auth("Google", "custom search API key"),
).cse()


def invoke_cse(
    query,
    start,
):  # pragma: no cover
    """
    Invoke Custom Search API with specified query and index of the first result to return.
    Keep this function separate so that testing scripts can substitute with a mockup.
    """
    return _cse.list(
        q=query, cx=fs.get_3rd_party_auth("Google", "search engine ID"), start=start
    ).execute()


def get_raw(metric):
    """
    Get raw metric score for Google Custom Search API:
    rank of the query or zero, if it didn't appear in search results.
    'metric' is the metric definition.
    """
    query = metric["q"] if "q" in metric else metric["id"]
    num = metric["num"] if "num" in metric else _NUM
    url = metric["URL"]

    start = 1
    while num > 0:
        res = invoke_cse(query, start)

        for index, item in enumerate(res["items"][:num]):
            if item["link"] == url:
                return start + index

        if "nextPage" not in res["queries"]:
            print(
                "Warning ('customsearch' metric source): "
                f"query '{query}' produced small number of search results"
            )
            return 0

        start += 10
        num -= 10
    return 0


def get_normalized(metric, raw):
    """
    Get normalized metric score for Google Custom Search API.
    'metric' is the metric definition.
    'raw' is the raw metric score.
    """
    if raw:
        num = metric["num"] if "num" in metric else _NUM
        return (num + 1 - raw) / num

    return 0
