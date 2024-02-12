############
Data Sources
############

This chapter describes details of metric data sources.

************************
Pre-Defined Data Sources
************************

``const``
=========

Specifies a constant to be used as a metric value. This source is useful for metrics that need to be entered manually, but also rarely change.

JSON config fields for metrics using source ``const``:

* ``"source": "const"``
* ``"value"`` (required): floating-point value between 0 and 1 to be used as the metric value.

``customsearch``
================

Captures search engine optimization efficiency with Google search. It looks at the top ``N`` results with certain search phrase and calculates the metric value as following:

* ``0`` if the target web page is not found in the top ``N`` results.
* ``(N+1-n) / N`` if the target web page is found as n\ :sup:`th` result. It is easy to see that this equals to ``1`` if the target page is the first search result and then linearly decreases until it becomes ``0``.

JSON config fields for metrics using source ``customsearch``:

* ``"source": "customsearch"``
* ``"URL"`` (required): target web page.
* ``"num"`` (optional, defaults to ``50``): number of search results to consider.

Since this source accesses Google services, authentication details need to be provided using ``--auth`` command line option. Authentication JSON file needs to have the following entry::

    "Google": {
        "custom search API key": "API key goes here",
        "search engine ID": "search engine ID goes here"
    }

See `Custom Search JSON API <https://developers.google.com/custom-search/v1/overview>`_ for information about Google API key and search engine ID.

See `customsearch JSON config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_customsearch.json>`_ for an example of using the ``customsearch`` data source.

``GitHub``
==========

Captures metrics for GitHub projects. See subsections for specific metrics.

GitHub does not require authenticated access, but rate limits are higher if a personal access token is provided. The personal access token can be provided using ``--auth`` command line option. Authentication JSON file needs to have the following entry::

    "GitHub": {
        "personal access token": "token goes here"
    }

See `GitHub JSON config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_github.json>`_ for an example of using GitHub data sources.

``GitHub.star``
---------------

Captures number of GitHub stars against the target.

JSON config fields for metrics using source ``GitHub.star``:

* ``"source": "GitHub.star"``
* ``"repo"`` (required): GitHub repository.
* ``"target"`` (optional, defaults to ``1000``): target success number of GitHub stars for the metric value to hit ``0.5``.

``GitHub.fork``
---------------

Captures number of GitHub forks against the target.

JSON config fields for metrics using source ``GitHub.fork``:

* ``"source": "GitHub.fork"``
* ``"repo"`` (required): GitHub repository.
* ``"target"`` (optional, defaults to ``100``): target success number of GitHub forks for the metric value to hit ``0.5``.

``GitHub.watch``
----------------

Captures number of GitHub watchers against the target.

JSON config fields for metrics using source ``GitHub.watch``:

* ``"source": "GitHub.watch"``
* ``"repo"`` (required): GitHub repository.
* ``"target"`` (optional, defaults to ``50``): target success number of GitHub watchers for the metric value to hit ``0.5``.

``uplevel``
===========

Uplevels collective metric behavior to a higher-level via computing the weighted sum of the corresponding lower-level metric values. This data source supports key ``facere-sensum`` idea of combining metrics into tree-like structures. See :ref:`here <the-approach>` for details.

JSON config fields for metrics using source ``uplevel``:

* ``"source": "uplevel"``
* ``"log"`` (required): CSV file storing the data for ``facere-sensum`` layer that is being upleveled.

See `uplevel JSON config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_uplevel.json>`_ for an example of using the ``uplevel`` data source.

``uptodate``
============

Tracks assets to be up to date by calculating number of days passed since an asset was updated last time. The date of the asset's last update should be manually corrected in the config file if the asset receives an update. This metric is useful, e.g., for tracking products that need their collateral regularly updated.

JSON config fields for metrics using source ``uptodate``:

* ``"source": "uptodate"``
* ``"updated"`` (required): string in ISO 8601 format representing the date when the asset was updated last time.
* ``"target"`` (optional, defaults to ``365``): number of days passed for the metric normalized score to hit ``0.5``. The normalized score will be above ``0.5`` for newer assets and below ``0.5`` for older assets.

See `uptodate JSON config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_uptodate.json>`_ for an example of using the ``uptodate`` data source.

``user``
========

Prompts a user to enter the value manually. This source is useful for metrics that can not be automatically computed.

JSON config fields for metrics using source ``user``:

* ``"source": "user"``

Source ``user`` does not use any additional fields.

.. _bringing-your-own-metric:

************************
Bringing Your Own Metric
************************

``facere-sensum`` provides a simple API for bringing your own metric data sources.

TO BE ADDED
