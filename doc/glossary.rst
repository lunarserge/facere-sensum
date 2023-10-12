########
Glossary
########

.. glossary::

    Authentication Config
        JSON file specifying 3rd party authentication details for use in metric sources. E.g., Google API keys.

    Layer
        One level of combining individual metrics into a higher-level metric that represents their collective behavior as a single indicator.

    Layer Config
        JSON file specifying a layer.

    Layer Data
        CSV file containing a time series for individual layer metric scores as well as overall layer scores.

    Layer Score
        Weighted average of normalized metric scores of a layer.

    Metric
        A system or standard of measurement: a way to express performance of something as a number.

    Metric Score
        A number obtained as a result of taking a metric measurement.

    Metric Source
        Implementation of functions producing raw and normalized scores for a metric.

    Metric Weight
        Weight of a metric in a layer in a form of a floating-point value between ``0`` and ``1``. Sum of weights of all metrics in the layer should equal to ``1``.

    Normalized Metric Score
        Raw metric score converted into a floating-point value between ``0`` and ``1``. Often set in the context of a goal. E.g., if a project has a goal of reaching 1000 GitHub stars the normalized metric may be defined as ``max(raw_metric_score/2000, 1)``. This way it receives scores below ``0.5`` if the goal is not yet met and scores of ``0.5`` or higher for meeting / exceeding the goal.

    Raw Metric Score
        User-friendly metric score. E.g., number of stars of a GitHub project.
