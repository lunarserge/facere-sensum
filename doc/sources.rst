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

Monitors assets for their up to date status by calculating the number of days since the asset was last reviewed or updated. This metric is useful for tracking products or their collateral that require regular updates.

The raw metric score reflects the number of days since the asset was last reviewed or updated.

The normalized score is calculated as follows:

* ``1 - n / 2*t`` where ``n`` is the raw score and ``t`` is the expiration target. This is less than ``0.5`` if the raw score exceeds the expiration target, ``0.5`` if it matches the target, and greater than ``0.5`` if it falls below the target.
* ``0`` if the raw score is more than double the expiration target.

Layer config fields for metrics using source ``uptodate``:

* ``"source"``: ``"uptodate"``
* ``"method"`` (optional, defaults to ``"manual"``): Specifies how to obtain the date of the last review or update of an asset. Possible values are ``"manual"`` and ``"github.com"``. The ``"manual"`` method uses a date provided in the ``"updated"`` field (see below). The ``"github.com"`` method indicates that the asset is hosted on GitHub, and the update date can be automatically determined from the last commit date of that file.
* ``"updated"`` (required for ``"manual"`` method, optional otherwise): The date in ISO 8601 format representing the last update of the asset. For the ``"manual"`` method, this date is used as is. For the ``"github.com"`` method, if this field is provided, the later date between this and the automatically determined last commit date is used.
* ``"path"`` (required for ``"github.com"`` method): The path to the file hosted on GitHub. This path should include the GitHub username and project repository as the first two elements, followed by the path to the file within the project's file structure.
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

The ``facere-sensum`` framework allows you to easily add your own metric sources by defining Python modules in the ``src/facere_sensum/connectors`` directory. This feature enables users to tailor the framework to their specific needs by integrating custom metrics directly into the system. These custom metrics can be defined and managed within their respective Python modules, allowing for a seamless integration and extension of ``facere-sensum``'s capabilities.

Let's assume you want to define your own metric source named ``byom``. Follow these steps:

* Create a module named ``byom.py`` and place it in the ``src/facere_sensum/connectors`` folder.
* In your layer configs, reference your metric using the ``byom`` source. Include necessary fields such as ``id``, ``weight``, and any other fields that are required for your metric.

In your ``byom.py`` module, define the following two functions to handle metric calculations:

* ``get_raw(metric)``: This function should calculate and return a raw score for your metric. For example, if you are tracking a search engine optimization (SEO) metric, this function might return the ranking of a search term in Google search results. The ``metric`` argument passed to this function will contain the part of the layer config that pertains to your metric, including mandatory fields such as ``id``, ``source``, and ``weight``. You can also include additional fields specific to your metric's needs. For instance, an SEO metric would likely require at least a target URL.
* ``get_normalized(metric, raw)``: This function should convert the raw score obtained from ``get_raw(metric)`` into a normalized score, which should be a floating-point value ranging from ``0`` to ``1``. The ``metric`` argument has the same structure and meaning as in ``get_raw(metric)``. The ``raw`` argument is the raw score output from the corresponding call to ``get_raw(metric)``. For guidance on how to best normalize metrics, refer :ref:`here <the-approach>`.

Metrics that are related can be organized into subfolders. For example, all GitHub-related metrics are located in a subfolder named ``GitHub`` within ``src/facere_sensum/connectors``. A specific metric like the number of GitHub stars would be defined in a file called ``star.py`` inside the ``GitHub`` folder. In the layer config, this metric would be referenced as ``GitHub.star``. It's important to note the dot notation used here (``GitHub.star``) - it follows Python's module import syntax.

That's it! ``facere-sensum`` doesn't require any additional registration for your metric - it just searches for a module with the corresponding name within the ``src/facere_sensum/connectors`` directory.

All metrics included with ``facere-sensum`` follow the same implementation protocol, so numerous examples are available. You can find included metric definitions at `this GitHub repository <https://github.com/lunarserge/facere-sensum/tree/main/src/facere_sensum/connectors>`_ and corresponding layer configs at `this link <https://github.com/lunarserge/facere-sensum/tree/main/examples>`_.
