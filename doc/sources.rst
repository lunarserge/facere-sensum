##############
Metric Sources
##############

This chapter provides detailed information about various metric data sources.

**************************
Pre-Defined Metric Sources
**************************

``const``
=========

Specifies a constant value to be used as a metric score, both in its raw form and normalized. This source is suitable for metrics that require manual input and remain relatively constant.

Layer config fields for metrics using source ``const``:

* ``"source"``: ``"const"``
* ``"value"`` (required): floating-point value between ``0`` and ``1`` to serve as the metric score.

``customsearch``
================

Measures web search efficiency via the `Google Programmable Search Engine <https://developers.google.com/custom-search/v1/overview>`_. While not identical to Google search, it may be rather close. E.g., refer to `this article <https://www.oncrawl.com/technical-seo/custom-search-analyzing-search-intent-googles-programmable-search-engine-json-api>`_ for considerations.

The ``customsearch`` metric source analyzes the top ``N`` search results for a specific search phrase and calculates the raw metric score as follows:

* ``0`` if the target web page is not among the top ``N`` results.
* ``n`` if the target web page ranks as the n\ :sup:`th` result.

The normalized score is calculated as follows:

* ``0`` if the target web page is not among the top ``N`` results.
* ``(N+1-n) / N`` if the target web page ranks as the n\ :sup:`th` result. This equals to ``1`` if the target page is the first search result and then linearly decreases to ``0``.

Layer config fields for metrics using source ``customsearch``:

* ``"source"``: ``"customsearch"``
* ``"URL"`` (required): Target web page.
* ``"num"`` (optional, defaults to ``50``): Number of search results to consider.

Since this source accesses Google services, authentication details must be provided using the ``--auth`` command line option. Authentication config needs to have the following entry::

    "Google": {
        "custom search API key": "API key goes here",
        "search engine ID": "search engine ID goes here"
    }

See `Custom Search JSON API <https://developers.google.com/custom-search/v1/overview>`_ for information about Google API key and search engine ID.

See `customsearch layer config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_customsearch.json>`_ for an example of using the ``customsearch`` metric source.

``GitHub``
==========

Captures metrics for stars, forks, and watchers in GitHub projects.

The raw metric score represents the absolute number of stars, forks, or watchers.

The normalized score is calculated as follows:

* ``n / (2*t)`` where ``n`` is the raw score and ``t`` is a success target. This equals ``0.5`` if the raw score matches the target, less than ``0.5`` if below the target, and more than ``0.5`` if above the target.
* ``1`` if the raw score is more than double the target.

Layer config fields for metrics using source ``GitHub``:

* ``"source"``: ``"GitHub.star"``, ``GitHub.fork``, or ``GitHub.watch``
* ``"repo"`` (required): GitHub repository.
* ``"target"`` (optional, defaults to ``1000`` for stars / ``100`` for forks / ``50`` for watchers): Success target.

GitHub does not require authenticated access, but providing a personal access token can increase rate limits. The personal access token can be provided using ``--auth`` command line option. Authentication config needs to have the following entry::

    "GitHub": {
        "personal access token": "token goes here"
    }

See `GitHub layer config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_github.json>`_ for an example of using GitHub metric sources.

``uplevel``
===========

Elevates collective metric behavior to a higher level by computing the weighted sum of corresponding lower-level normalized metric scores. This source supports the key ``facere-sensum`` idea of combining metrics into tree-like structures. See :ref:`here <the-approach>` for details. The same weighted sum is used as both raw and normalized metric score.

Layer config fields for metrics using source ``uplevel``:

* ``"source"``: ``"uplevel"``
* ``"log"`` (required): Layer data for ``facere-sensum`` layer being elevated.

See `uplevel layer config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_uplevel.json>`_ for an example of using the ``uplevel`` metric source.

``uptodate``
============

Monitors assets for their update status by calculating the number of days since the asset was last updated. This metric is useful for tracking products or their collateral that require regular updates.

The raw metric score reflects the number of days since the asset was last updated.

The normalized score is calculated as follows:

* ``1 - n / 2*t`` where ``n`` is the raw score and ``t`` is the expiration target. This is less than ``0.5`` if the raw score exceeds the expiration target, ``0.5`` if it matches the target, and greater than ``0.5`` if it falls below the target.
* ``0`` if the raw score is more than double the expiration target.

Layer config fields for metrics using source ``uptodate``:

* ``"source"``: ``"uptodate"``
* ``"updated"`` (required): Date in ISO 8601 format representing the last update of the asset. This date should be manually corrected if the asset receives an update.
* ``"target"`` (optional, defaults to ``365``): Expiration target, indicating the number of days for the metric's normalized score to decrease to ``0.5``.

See `uptodate layer config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_uptodate.json>`_ for an example of using the ``uptodate`` metric source.

``user``
========

Prompts a user to manually enter the metric score. The entered value serves as both the raw and normalized metric score. This source is suitable for metrics that cannot be automatically computed.

Layer config fields for metrics using source ``user``:

* ``"source"``: ``"user"``

The ``user`` metric source does not utilize any additional fields.

.. _bringing-your-own-metric:

************************
Bringing Your Own Metric
************************

``facere-sensum`` provides a simple API for bringing your own metric data sources.

TO BE ADDED