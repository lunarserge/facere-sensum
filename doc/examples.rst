########
Examples
########

*************************************************
Product Management and Development Teams Workflow
*************************************************

Let's use the same SEO example from the :doc:`introduction <intro>` but with specific actions and numbers. Imagine we have a company in the automobile industry with two product lines: cars and trucks. Trucks are more important to the company's business. The key selling points for the company's products are safety for all products and fuel efficiency for trucks.

Here’s how the workflow between product management and development teams might look. Since the problem at hand is SEO, the development team likely comes from the marketing department.

.. _metrics-hierarchy:

Step 1. Define Hierarchy of Metrics
===================================

The organization has two product lines, so let’s assume it has two separate landing pages targeting different customer bases. The product management team decides which search terms are important to resonate with targeted customers. For this example, it might look like this:

* For the 'car' landing page: 'best car', 'safe car'
* For the 'trucks' landing page: 'best truck', 'safe truck', 'fuel-efficient truck'

This results is the following hierarchy of metrics:

.. image:: _static/SEO-hierarchy.png

Step 2. Define Normalized Lowest-Level Metrics
==============================================

Assume the current results for search terms are:

* 'best car': not found in the top ten search results.
* 'safe car': 8\ :sup:`th` on the list of search results.
* 'best truck': 8\ :sup:`th` result.
* 'safe truck': 5\ :sup:`th` result.
* 'fuel-efficient truck': not found in the top ten search results.

According to ``facere-sensum`` rules, these need to be normalized so that metric receives a score between ``0`` and ``1``. Product management decides that the lowest-level normalized metric score is defined as ``1`` if the landing page shows up first in search results, ``0.9`` if it shows up second, and so forth. The normalized metric score becomes ``0`` if the landing page is not found in the top ten search results. This yields the following current normalized metric scores for the lowest level of the picture above:

.. math::

   SEO_{bestcar} = 0; SEO_{safecar} = 0.3

   SEO_{besttruck} = 0.3; SEO_{safetruck} = 0.6; SEO_{fuelefficienttruck} = 0

Let’s assume all these metrics are equally important from the SEO success perspective, and the company believes that being 6\ :sup:`th` in the search results for each term individually is good enough. Being 6\ :sup:`th` translates to a normalized metric score of ``0.5``. We see that SEO\ :sub:`safetruck` is doing well, but the other metrics are not.

In reality, you might set a higher bar for key selling point metrics like SEO\ :sub:`safecar` or SEO\ :sub:`safetruck`, making being 2\ :sup:`nd` or 3\ :sup:`rd` in search results correspond to a normilized metric score of ``0.5``. However, to keep things simple, we won’t do that in this example. Notice that lowest-level metrics do not need to use the same scheme and can be defined individually. What matters is that they have a normalized metric score between ``0`` and ``1``, with the midpoint being 'successful' performance from a business perspective.

Step 3. Define Weights for Calculating Higher-Level Metrics
===========================================================

The product management decides that:

* For SEO\ :sub:`overall`: since the trucks business is more important than cars SEO\ :sub:`trucks` gets a weight of ``0.7`` and SEO\ :sub:`cars` gets the remaining weight of ``0.3``.
* For SEO\ :sub:`cars`: safety is a key selling point, so SEO\ :sub:`safecar` gets a weight of ``0.8`` and SEO\ :sub:`bestcar` get the remaining weight of ``0.2``.
* Similarly, for SEO\ :sub:`trucks`: SEO\ :sub:`safetruck` gets a weight of ``0.5``, SEO\ :sub:`fuelefficienttruck` gets ``0.3`` and SEO\ :sub:`besttruck` gets the remaining ``0.2``.

Given these weights and current lowest-level normalized metric scores, we get the following current scores for higher-level metrics, automatically computed by ``facere-sensum``:

.. math::

   SEO_{cars} &= SEO_{bestcar}*0.2 + SEO_{safecar}*0.8 \\
              &= 0*0.2 + 0.3*0.8 = 0.24

.. math::
   SEO_{trucks} &= SEO_{besttruck}*0.2 + SEO_{safetruck}*0.5 + SEO_{fuelefficienttruck}*0.3 \\
                &= 0.3*0.2 + 0.6*0.5 + 0*0.3 \\
                &= 0.06 + 0.3 = 0.36

.. math::
   SEO_{overall} &= SEO_{cars}*0.3 + SEO_{trucks}*0.7 \\
                 &= 0.24*0.3 + 0.36*0.7 \\
                 &= 0.072 + 0.252 = 0.324

Step 4. Set Goals for Normalized Metric Scores at the Appropriate Level
=======================================================================

Most of the lowest-level normalized metric scores (SEO\ :sub:`bestcar`, SEO\ :sub:`safecar`, SEO\ :sub:`besttruck` and SEO\ :sub:`fuelefficienttruck`) are below the ``0.5`` success point, so goals might be set for each individually to reach success. But that would be micromanagement. It’s better to set higher-level goals.

All three higher-level normalized metric scores (SEO\ :sub:`cars`, SEO\ :sub:`trucks` and SEO\ :sub:`overall`) are below ``0.5`` as well. In this example, product management decides to set just one goal at the top level for SEO\ :sub:`overall`. Currently it has a score of ``0.324``. The target is set for SEO\ :sub:`overall` to reach ``0.5`` or higher, indicating that the company has generally improved SEO to a successful level across all its products.

Step 5. Understand If the Goal is Achievable
============================================

The marketing department concludes that there is some SEO webpage metadata/dark magic that can be applied to improve the search rankings for 'safe car' and 'fuel-efficient truck' terms. Assuming both can be optimized to become the 5\ :sup:`th` search result and SEO does not worsen for other terms, this is what we are looking at after potential improvement:

.. math::

   SEO_{bestcar} = 0; SEO_{safecar} = 0.6

   SEO_{besttruck} = 0.3; SEO_{safetruck} = 0.6; SEO_{fuelefficienttruck} = 0.6

.. math::

   SEO_{cars} &= SEO_{bestcar}*0.2 + SEO_{safecar}*0.8 \\
              &= 0*0.2 + 0.6*0.8 = 0.48

.. math::
   SEO_{trucks} &= SEO_{besttruck}*0.2 + SEO_{safetruck}*0.5 + SEO_{fuelefficienttruck}*0.3 \\
                &= 0.3*0.2 + 0.6*0.5 + 0.6*0.3 \\
                &= 0.06 + 0.3 + 0.18 = 0.54

.. math::
   SEO_{overall} &= SEO_{cars}*0.3 + SEO_{trucks}*0.7 \\
                 &= 0.48*0.3 + 0.54*0.7 \\
                 &= 0.144 + 0.378 = 0.522

This analysis shows that the goal is achievable. 

Step 6. Define Focus Areas and Track Execution
==============================================

We can see that the goal of ``0.5`` is achievable by focusing SEO efforts on improving search rankings for two out of five search terms. This provides the marketing department with a clear goal, a way to track progress, and a focus on which aspects of the SEO strategy to prioritize.
