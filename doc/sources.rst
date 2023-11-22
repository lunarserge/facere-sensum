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

``uplevel``
===========

Uplevels collective metric behavior to a higher-level via computing the weighted sum of the corresponding lower-level metric values. This data source supports key ``facere-sensum`` idea of combining metrics into tree-like structures. See :ref:`here <the-approach>` for details.

JSON config fields for metrics using source ``uplevel``:

* ``"source": "uplevel"``
* ``"log"`` (required): CSV file storing the data for ``facere-sensum`` layer that is being upleveled.

See `uplevel JSON config <https://github.com/lunarserge/facere-sensum/tree/main/examples/config_uplevel.json>`_ for an example of using the ``uplevel`` data source.

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

``facere-sensum`` provides a simple API for bringing your own metric data sources. Data sources are defined by Python modules under ``src/facere_sensum/connectors`` folder.

Let's assume you want to define your own data source named ``byom``. Here is what needs to happen:

* Create ``byom.py`` module under ``src/facere_sensum/connectors`` folder.
* Refer to your metric from JSON configs using ``byom`` source along with ``id``, ``priority`` and any other additional fields of your choice that your metric might need.

``byom.py`` should define 2 functions:

* ``get_raw(metric)``. This function should produce a raw value for your metric. For example, search engine optimization (SEO) tracking metric might return search term ranking in Google search. ``facere-sensum`` will call this function with ``metric`` argument containing a portion of JSON config corresponding to your metric. The ``metric`` argument will have required fields (``id``, ``source`` and ``priority``) and you can add any additional more specific fields that are required for your metric. E.g., SEO metric will need a target URL at least. Raw metric values are used for providing measurements to a user in a friendly format.
* ``get_normalized(metric, raw)``. This function should produce a normalized value for your metric in a form of a floating-point value between ``0`` and ``1``. See :ref:`here <the-approach>` for recommendations on how to best normalize metrics. ``metric`` function argument has the same meaning as with ``get_raw(metric)``. ``raw`` argument will be a raw metric value produced by the earlier matching call to ``get_raw(metric)``. Normalized metric values are used for calculating collective metric behavior and thus fundamental for ``facere-sensum`` methodology.

Related metrics can be combined into subfolders. E.g., GitHub metrics are combined in ``GitHub`` subfolder under ``src/facere_sensum/connectors``. Something like GitHub stars metric definition would sit in ``GitHub/star.py`` and would be referred to as ``GitHub.star`` source in JSON configs. Notice the use of dot in JSON configs - it is a part of Python module import syntax.

That's it! ``facere-sensum`` doesn't require any additional registration for your metric - it will just look for a module with a matching name under ``src/facere_sensum/connectors``.

All metrics coming with ``facere-sensum`` are implemented using the same protocol, so plenty of examples are available for `metric definitions <https://github.com/lunarserge/facere-sensum/tree/main/src/facere_sensum/connectors>`_ and corresponding `JSON configs <https://github.com/lunarserge/facere-sensum/tree/main/examples>`_.
