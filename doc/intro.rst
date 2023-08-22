############
Introduction
############

``facere-sensum`` is a general-purpose metrics framework that helps put a meaningful number on anything. It allows to combine individual metrics into a higher-level metric that represents collective behavior as a single indicator.

By doing that, ``facere-sensum`` provides a formal way for product management to define priorities and goals for development work. On the receiving end, ``facere-sensum`` enables development teams to determine where exactly their effort needs to focus to hit the goal.

See below for the overall methodology description and :doc:`examples <examples>` section for a sample of its practical application.

************
The Approach
************

The key idea behind ``facere-sensum`` is that metrics can be combined into tree-like structures where leaf nodes represent individual metrics and joints represent collective metrics for subtrees growing from them. E.g., imagine you are tracking SEO (Search Engine Optimization) efficiency metric for your company. The company has several projects. Each project has a landing page that you want to be found by web searches using certain phrases (search terms). There are multiple search terms per project.

Here we have several levels of metrics:

* On the lowest level there are individual metrics for how well specific project landing page is found using specific search term.
* Next level combines search terms for a particular project and yields a single-number metric for how well project landing page is found across *all* the search terms.
* Finally, the top level - top of the tree - is just one single number reflecting how well the company does SEO across *all* its projects.

This example is using homogeneous metrics, but in practice metrics can get heterogeneous. E.g., you can imagine even higher level which combines SEO efficiency with something different like uptime metric for landing pages. To abstract away such differences, ``facere-sensum`` is using normalized metric values at all levels. The values must be a number between ``0`` and ``1``, with ``0`` indicating inferior performance, ``1`` indicating perfect performance and other values indicating varying level of performance in between. This is how it works at various levels:

* Lowest level metrics should be defined to support this directly. E.g., in the SEO example, lowest level metric (for project / search term pair) can be defined as ``1`` if the landing page shows up first in search results, 0.9 if it shows up second and so forth. The metric becomes ``0`` if the landing page is not found in the top ten search results.
* Higher level metrics are calculated automatically by ``facere-sensum`` as a weighted sum of the corresponding lower-level metric values, with weights totaling to ``1``. This happens on all levels above the lowest. Since lower-level metric values are between ``0`` and ``1`` and weights are totaling to ``1`` this yields higher level metric values between ``0`` and ``1`` as well:

.. math::

   high\_level\_metric = \sum_{i=0}^{N}low\_level\_metric_i*weight_i

   \sum_{i=0}^{N}weight_i = 1

While not a strict requirement, it is helpful to define lowest-level metrics such that 'successful' metric value is around ``0.5`` with higher values indicating performing above the business goal and lower values indicating performing below the business goal. If lowest-level metrics defined in this way then metrics on all levels can be used not only as a number that has relative value over time, but also as an indicator of being successful or not on an appropriate level.

SEO efficiency metric is used here for illustrative purpose. In general, any kind of metrics can fit with this approach.

*******************************
Use by Product Management Teams
*******************************

Product management teams would use ``facere-sensum`` to:

* Specify hierarchy of metrics.
* Define normalized lowest-level metrics.
* Define weights for calculating higher-level metrics.
* Set goals for metrics at the appropriate level.

While metric weights on a particular level should total to ``1``, specifying different relative weights would indicate that some metrics are more important than others to the overall success (more important metrics receive bigger weights).

The goals can be set on any metric level, but it gets more interesting on higher levels since this gives development teams flexibility in deciding how to achieve it. E.g., in SEO example product management can specify goals for each combination of project / search term. But that would be micromanagement. It is better to set goals for higher-level metrics like SEO efficiency for a product across search terms or even one goal for overall SEO across products - and leave it to development to decide how to hit the goal.

************************
Use by Development Teams
************************

Development teams would use ``facere-sensum`` to:
* Understand if the goal is achievable.
* Define focus areas and track execution.

After the full parenthesis expansion, higher-level metric calculation on any level comes down to a sum of the lowest-level metrics with weights. For each of the lowest-level metrics the development team can assess how much it can be realistically improved. And then using weights and the full equation they can see if the higher-level goal will be achieved assuming such improvements in the lowest-level metrics.

After negotiating the achievable goal with the product management, development team can determine specific focus areas. While improving each metric to the limit is the best if your team has infinite resources, in practice it is typically not needed if the overall goal was set reasonably. In this case the development team has the flexibility to decide which of the lower-level metrics should be improved and how much so that the overall goal is achieved. They will make this determination using ROI (return on investment) analysis. Typically, it is a good idea to look at lowest-level metrics that are easiest to improve while having bigger weight in the overall equation.

Once the development team has a plan like this, they can use ``facere-sensum`` to automatically update higher-level metrics to track the progress.
