############
Introduction
############

``facere-sensum`` is a general-purpose metrics framework designed to quantify anything in a meaningful numerical format. It permits the aggregation of individual metrics to create higher-level metrics that reflect collective behavior with a single indicator.

In practical terms, ``facere-sensum`` offers a structured approach for product management to establish development priorities and objectives. For development teams, it serves as a tool to pinpoint the specific areas where their efforts should be concentrated to achieve the desired goal.

For a more comprehensive understanding of this methodology, please refer to the general methodology description below and explore the sample use cases provided in the :doc:`examples <examples>` section.

.. _the-approach:

************
The Approach
************

The core concept of ``facere-sensum`` revolves around the idea that metrics can be organized into a hierarchical structure resembling a tree. In this structure, the individual metrics are represented as leaf nodes, while collective metrics for groups of metrics are represented as nodes that connect to their respective subgroups. To illustrate, let's consider a scenario where you are monitoring the efficiency of your company's SEO (Search Engine Optimization) efforts. The company manages multiple projects, and each of these projects has its own dedicated landing page. The goal is to ensure that these landing pages are discoverable in web searches conducted using specific keywords or search terms. Each project is associated with multiple search terms to optimize its online visibility.

In this example, there are several levels of metrics:

* At the lowest level, you have individual metrics that assess how effectively each project's landing page is discovered using specific search terms.
* Moving up to the next level, these search terms for a particular project are combined to produce a single numerical metric that gauges how well the project's landing page performs across *all* the associated search terms.
* Finally, at the top level, which is the highest point in the metric hierarchy, you arrive at a single numerical metric that reflects the overall SEO performance of the entire company across *all* its projects.

This hierarchical structure allows for a comprehensive assessment of SEO performance, from specific details at the bottom level to the overall company performance at the top level.

In this example, we're working with metrics that are relatively uniform, but in practice, metrics can become diverse. For instance, you can envision a higher-level metric that combines SEO efficiency with something entirely different, such as the uptime metric for landing pages. To address such variations, ``facere-sensum`` distinguishes between raw and normalized metric scores.

* **Raw Metric Score**: This is the original, user-friendly score for a metric. For instance, it could represent the ranking of a project's landing page in web search results for a particular search term.
* **Normalized Metric Score**: This score is a floating-point number between ``0`` and ``1``. A score of ``0`` indicates poor performance, ``1`` signifies perfect performance, and other values represent varying levels of performance in between. In the context of the SEO example, the lowest-level normalized metric score (for a project and search term combination) might be defined as ``1`` if the landing page appears first in search results, ``0.9`` if it's second, and so on. The metric score becomes ``0`` if the landing page doesn't appear in the top ten search results. This normalization process allows for consistent and comparable evaluation of metrics, even when they originate from different domains.

Here's how the system operates at different levels:

* At the lowest level, metrics should be defined to directly support both raw and normalized scores. ``facere-sensum`` offers an expanding collection of predefined lowest level metrics, and you can also create your own custom ones by referring to the :ref:`instructions for bringing your own metric <bringing-your-own-metric>`.
* At higher metric levels, raw and normalized scores maintain the same value. These scores are automatically calculated by ``facere-sensum`` as a weighted average of the corresponding lower-level normalized metric scores with weights adding up to a total of ``1``. This calculation occurs at all levels above the lowest. Given that lower-level metric normalized scores fall within the range of ``0`` to ``1``, and the weights sum to ``1``, this process results in higher-level metric scores also falling within the range of ``0`` to ``1``:

.. math::

   high\_level\_metric = \sum_{i=0}^{N}low\_level\_metric_i*weight_i

   \sum_{i=0}^{N}weight_i = 1

Although it's not an absolute requirement, it is advantageous to define lowest-level metrics in a manner where a 'successful' normalized metric score hovers around ``0.5``. Higher normalized scores should indicate that performance exceeds the business goal, while lower normalized scores should suggest that performance falls short of the business goal. When lowest-level metrics are defined in this way, metrics at all levels can serve not only as numerical data with relative scores over time but also as indicators of success or failure at the appropriate level.

For illustration, we've used the SEO efficiency metric, but in practice, this approach can be applied to various types of metrics.

*******************************
Use by Product Management Teams
*******************************

Product management teams harness ``facere-sensum`` for several key purposes:

* **Hierarchy of Metrics**: They use the framework to establish a structured hierarchy of metrics, defining the relationships between different metrics at various levels.
* **Lowest-Level Metrics**: Product management teams define both raw and normalized scoring for lowest-level metrics.
* **Weight Allocation**: They specify the weights used in calculating higher-level metrics. While lower-level metric weights on a particular level should sum to ``1``, specifying different relative weights would indicate that some metrics are more important than others to the overall success (more important metrics receive bigger weights).
* **Metric Goals**: Setting specific metric goals is another important aspect. While these goals can be set at any metric level, it becomes particularly interesting when established at higher levels. For instance, in the context of an SEO example, product management can define goals for each combination of project and search term. However, this approach may lead to micromanagement. A more effective strategy is to set goals for higher-level metrics, such as SEO efficiency for a product across search terms or even a single goal for overall SEO performance across all products. This approach empowers development teams to determine the most efficient strategies to achieve these goals.

************************
Use by Development Teams
************************

Development teams utilize ``facere-sensum`` for three primary purposes:

* **Assess Goal Feasibility**: They employ the framework to evaluate whether the established goals are realistically attainable. This evaluation may involve breaking down the tree of higher-level metrics all the way into a sum of weighted lowest-level metrics. The development team examines the potential for practical improvements in each lowest-level metric. By applying weights and the full equation, they can determine if the higher-level goal can be reached, assuming these improvements in the lowest-level metrics.
* **Focus Area Definition**: Following negotiations with the product management to establish achievable goals, the development team identifies specific focus areas. While striving to maximize improvement in every metric would be ideal under unlimited resources, it's generally unnecessary in practice when goals are reasonably set. In such scenarios, the development team has the flexibility to decide which lower-level metrics should be enhanced and to what extent, ensuring that the overall goal is met. They make these decisions using ROI (return on investment) analysis. Typically, it is advisable to prioritize the lowest-level metrics that are both easier to improve and carry a greater weight in the overall equation.
* **Execution Tracking and Communication**: Once the development team has formulated a plan based on these principles, they can use ``facere-sensum`` to automatically update higher-level metrics. This functionality facilitates tracking and monitoring progress, enabling the team to communicate their progress back to the product management.
