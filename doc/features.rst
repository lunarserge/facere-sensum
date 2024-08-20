########
Features
########

Key features of ``facere-sensum`` include:

* An expanding set of pre-defined, lowest-level metrics.
* An API for bringing your own metrics.
* Automatic computation of higher-level metrics to capture the overall behavior of metrics collectively.
* Creation of charts to visualize the behavior of metrics over time.

.. _layers:

******
Layers
******

In ``facere-sensum``, *layer* serves as a grouping mechanism that consolidates individual metrics to form a higher-level metric, offering a unified representation of the collective behavior of these metrics. For instance, :ref:`this metrics hierarchy <metrics-hierarchy>` consists of three layers. Among them, two layers run in parallel (SEO\ :sub:`cars` and SEO\ :sub:`trucks`), combining the lowest-level metrics into corresponding single indicators. Additionally, a third layer (SEO\ :sub:`overall`) consolidates an ultimate single indicator for the entire set, derived from SEO\ :sub:`cars` and SEO\ :sub:`trucks`.

A layer is characterized by a JSON file that adheres to the informally described scheme outlined below::

    {
        "id": "string: layer id",
        "log": "CSV file for storing layer data",
        "weights": ["static", "dynamic"],
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

* ``id`` (optional): A string providing a brief text description of the layer. Currently, the layer ``id`` is utilized as the output file name in the ``chart`` command (refer to :ref:`here <facere-sensum-commands>`).
* ``log`` (required): The name of the CSV file used for storing layer data. In most cases, users won't need to directly interact with the log file. However, in the current version of ``facere-sensum``, the result (higher-level metric values reflecting the collective behavior of layer metrics) is obtained directly from this log.
* ``weights`` (optional, defaults to ``static``): Specifies the approach for calculating metric weights. ``static`` always employs the weights specified in this JSON file as they are. On the other hand, ``dynamic`` adjusts metric weights over time based on their scores, giving more weight to metrics that don't perform well. Refer to :ref:`dynamic-vs-static-weights` for detailed information.
* ``metrics`` (required): An array of individual metrics that collectively constitute a layer:

  * ``id``: A string providing a short text description of the metric.
  * ``source``: A string specifying the data source for the metric. For a list of pre-defined sources, see :doc:`here <sources>`. Instructions on defining your own data source can be found :ref:`here <bringing-your-own-metric>`.
  * ``weight``: A floating-point value representing the metric's weight in the weighted sum of the layer. See :ref:`here <the-approach>` for the best way to define weights.
  * ``<other source-specific fields>``: Additional source-dependent details for the metric. For example, a search engine optimization tracking metric would need to know the target URL. These details are documented along with the corresponding :doc:`sources <sources>`.

For examples of ``facere-sensum`` layer configuration, you can check `here <https://github.com/lunarserge/facere-sensum/tree/main/examples>`_.

.. _dynamic-vs-static-weights:

*************************
Dynamic vs Static Weights
*************************

In most cases metric weights are meant to be the same over time. E.g., in the SEO efficiency metric from :doc:`examples <examples>` section the weights are what the product management team decides. This is called *static weights* in ``facere-sensum``.

However, there are scenarios where dynamic adjustments to weights are necessary, i.e., *dynamic weights*. Consider a situation where you're managing various personal tasks like sport exercise and helping children with homework, but time constraints mean not all tasks can be completed daily. To optimize your daily activities, you assign weights to each task and use ``facere-sensum`` to maximize the overall daily metric score. Prioritizing higher-weighted tasks first seems logical, but it risks neglecting lower-priority tasks indefinitely.

Dynamic weights address this challenge. When a layer specifies ``dynamic`` weights, the following algorithm adjusts the weights after each measurement:

#. Metric weights increase based on normalized scores, giving more weight to underperforming metrics. Metrics with a normalized score of ``0`` have their weights doubled, while those with a score of ``1`` retain their weights. Weights for metrics with scores in between are adjusted up proportionally.
#. Due to the adjustments above, if at least one metric receives a normalized score below ``1`` then the sum of metric weights will exceed ``1``. Consequently, all weights are multiplied by a factor to ensure their sum equals ``1``. This preserves the fundamental assumption in ``facere-sensum`` that the sum of metric weights in a layer is ``1``.

Applying this algorithm ensures that even low-priority items eventually get attention as their weight grows. The drawback of this algorithm is that it completely ignores static weights and hence the original relative importance of metrics is lost over time. Future versions of ``facere-sensum`` aim to provide additional weighting algorithms that would combine static and dynamic weights.

This algorithm ensures that lower-priority tasks eventually gain attention as their weights increase. However, it disregards static weights, leading to a loss of the initial relative importance of metrics over time. Future versions of ``facere-sensum`` aim to introduce additional weighting algorithms that blend static and dynamic weights for more nuanced evaluation.

******************************************************
Authentication for Sourcing Metrics from Third Parties
******************************************************

Sometimes, accessing a data source requires authentication. For instance, tracking search engine optimization with Google necessitates an API key and a search engine ID to access the required Google services. These keys are application-wide and not specific to a particular ``facere-sensum`` layer, so they are provided by a separate JSON file. :doc:`The data sources <sources>` section provides details on the authentication format, if required by a specific source type.

In essence, an authentication configuration JSON file typically resembles the following format::

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

    facere-sensum [-h] [--version] [--auth [AUTH]] [--config [CONFIG]] {create,update,chart}

Command line options:

* ``-h, --help``: Display the help message and exit.
* ``--version``: Show the version number of ``facere-sensum`` and exit.
* ``--auth [AUTH]``: Path to the JSON file containing authentication configuration for accessing metrics from third-party sources. This option is necessary only if using metric sources that require authentication.
* ``--config [CONFIG]``: Path to the JSON file defining the ``facere-sensum`` layer to compute. Specifying the layer configuration is required, but this option is not mandatory since ``config.json`` will be used by default if it is missing.

.. _facere-sensum-commands:

Commands:

* ``create``: Generate a CSV file to store layer data based on the JSON layer configuration.
* ``update``: Collect metrics according to the JSON configuration and append a new row of corresponding values to the CSV file, along with their collective score (weighted sum).
* ``chart``: Produce a PNG file containing a chart depicting the collective score of the layer over time.

Typically, users would employ the ``create`` command once per layer and then use the ``update`` command either manually or through automation to refresh metric values. In the current version, users are expected to retrieve results directly from the CSV file, particularly from the rightmost (``Score``) column. Users can also opt to create a graphical representation of the layer behavior over time using the ``chart`` command.