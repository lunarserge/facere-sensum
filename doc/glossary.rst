########
Glossary
########

.. glossary::

    Authentication Config
        A JSON file that contains details for third-party authentication, such as Google API keys, which are used in metric sources.

    Layer
        A grouping mechanism that combines individual metrics to create a higher-level metric, representing the collective behavior of these metrics as a single indicator.

    Layer Config
        A JSON file used to specify the configuration of a layer.

    Layer Data
        A CSV file that stores time series data for individual and overall scores of metrics forming a layer.

    Layer Score
        A weighted average of normalized metric scores within a layer.

    Metric
        A system or standard of measurement used to express the performance of something as a numerical value.

    Metric Score
        A numeric result obtained by taking a metric measurement.

    Metric Source
        An implementation of functions that generate raw and normalized scores for a specific metric.

    Metric Weight
        The weight assigned to a metric within a layer represented as a floating-point value between ``0`` and ``1``. The sum of weights for all metrics in a layer should equal ``1``.

    Normalized Metric Score
        A floating-point value between ``0`` and ``1``, representing a normalized version of a raw metric score. This normalization is often defined in the context of a goal. For example, if a project has a goal of reaching 1000 GitHub stars, it may be calculated as ``max(raw_metric_score/2000, 1)`` to assign scores below ``0.5`` if the goal hasn't been met and scores of ``0.5`` or higher if the goal has been achieved or exceeded.

    Raw Metric Score
        The user-friendly, unaltered score for a metric. For instance, it could be the number of stars for a GitHub project.
