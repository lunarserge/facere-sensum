########
Features
########

Key ``facere-sensum`` features are:

* Growing collection of pre-defined lowest level metrics.
* API for bringing your own metrics.
* Automatic calculation of higher-level metrics to reflect collective metric behavior.

******************
Formal Definitions
******************

In ``facere-sensum``, *layer* is one level of combining individual metrics into a higher-level metric that represents their collective behavior as a single indicator. For example, :ref:`this metrics hierarchy <metrics-hierarchy>` has three layers. Two of them are parallel (SEO\ :sub:`cars` and SEO\ :sub:`trucks`) and combine lowest layer metrics into a corresponding single indicator. And one more (SEO\ :sub:`overall`) combines an ultimate single indicator for the whole thing from SEO\ :sub:`cars` and SEO\ :sub:`trucks`.

A layer is defined by a JSON file with the following informally described scheme::

    {
        "log": "CSV file for storing layer data",
        "metrics": [
            {
                "id": "string: metric id",
                "source": "string: data source",
                "weight": floating-point value between 0 and 1,
                <other source-specific fields>
            },
            ...
        ]
    }

* ``log`` is the name of CSV file for storing layer data. For the most part users do not need to work with the log file directly, but in the current version of ``facere-sensum`` the result (higher level metric values reflecting collective behavior of layer metrics) is obtained directly from there.
* ``metrics`` is the array of individual metrics that collectively form a layer:

  * ``id`` is a string with a short text description of the metric.
  * ``source`` is a string specifying the data source for the metric. For the list of pre-defined sources see :doc:`here <sources>`. For instructions on how to define your own data source see :ref:`here <bringing-your-own-metric>`.
  * ``weight`` is a floating-point value reflecting metric's weight in the weighted sum of the layer. See :ref:`here <the-approach>` for how to best define the weights.
  * ``<other source-specific fields>`` are additional source-dependent details for the metric. E.g., search engine optimization tracking metric would need to know which URL is the search target. These details are documented along with the corresponding :doc:`sources <sources>`.

See `here <https://github.com/lunarserge/facere-sensum/tree/main/examples>`_ for examples of ``facere-sensum`` layer configuration.

********************************************************
Authentication for Sourcing Metrics from Third Parties
********************************************************

Sometimes an authentication is necessary for a data source. E.g., search engine optimization tracking with Google requires an API key and search engine ID to be used for accessing necessary Google services. These keys are application-wide and not specific to a particular ``facere-sensum`` layer, hence provided by a separate JSON file. :doc:`Data sources <sources>` section explains authentication format, if required by a particular source type.

In general, authentication config JSON file would look like this::

    {
        "Third-Party Name (e.g., Google)": {
            <relevant authentication info, e.g., the following 2 lines for Google search>
            "custom search API key": "API key goes here",
            "search engine ID": "search engine ID goes here"
        }
        "Another Third-Party Name: {
            ...
        }
        ...
    }

**********************
Command Line Interface
**********************

::

    facere-sensum [-h] [--version] [--auth [AUTH]] [--config [CONFIG]] {create,update}

Command line options:

* ``-h, --help``: show the help message and exit.
* ``--version``: show ``facere-sensum`` version number and exit.
* ``--auth [AUTH]``: path to JSON file with authentication config for sourcing metrics from third parties. This option is only necessary if using metric sources that require such authentication.
* ``--config [CONFIG]``: path to JSON file defining ``facere-sensum`` layer to compute. Specifying the layer config is required, but the use of this option is not required since ``config.json`` will be used by default if it is missing.

``facere-sensum`` has two main commands:

* ``create``: create a CSV file for storing the layer data as per JSON layer config.
* ``update``: capture metrics per JSON config and update the CSV file with a new row of corresponding values and their collective score (weighted sum).

Typically, a user would use ``create`` command once per layer and then run ``update`` commands either manually or by automation to update metric values. In the current version the result is supposed to be taken by the user directly from the CSV file, rightmost (``Score``) column.
