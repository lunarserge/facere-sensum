# facere-sensum: make sense of the turmoil

Too often in life we deal with many things and also often with more than we can realistically accomplish. `facere-sensum` helps its users to be in control by:
* Having the user assign relative priorities for things in scope and define their corresponding success metrics.
* Calculating a meaningful single score across all specified metrics that can be used as a pivot indicator of overall performance.
* Adjusting priorities between measurements to make sure that even low-priority things gets attention over time.

You can pick any scope like addressing various job deliverables or personal life matters, or even everything together to have a complete picture of everything that goes on in your life. For example, you can decide that there are 3 things you want to track: `Self-Development`, `Family Time` and `Job Deliverables`.

You will need to assign priorities. `facere-sensum` uses numbers between 0 and 1 to indicate relative priorities. E.g., you can assign priority of 0.4 to `Self-Development` and priority of 0.3 to each of `Family Time` and `Job Deliverables` which would mean that you care about your regular `Self-Development` a little more than about other two metrics.

You will also need to decide how to measure your performance for each of the metrics. Similar to priorities, `facere-sensum` expects the scores for metrics to be a number between 0 and 1. The scoring is really what you decide and you will need to provide scores for individual metrics. This can be very informal, e.g., score `Self-Development` between 0 and 1 depending how you generally feel about this metric. Or more formal, e.g., you can take a target of spending 100 minutes with your family daily and by dividing actual time spent in minutes by 100 you will arrive to a score between 0 and 1.

Metrics are specified and scores are stored in a `.csv` file:
* The first column is `ID`. This is where dates of the measurements will be stored.
* After `ID` any number of metrics can be specified. This comes as a pair of columns in a form of `P(Metric)` and `S(Metric)` for priorities and scores, and `Metric` being any descriptive string, e.g. `Self-Development`.
* Finally, the last column is overall `Score` for the day.

First data row in the `.csv` file need to be provided as well with the starting priorities (values in `P(Metric)` columns). As indicated above, priorities should be given in a form of a number in the range of 0..1. All priorities together should sum up to 1. This makes it easy to specify relative priorities for metrics by defining how big of a slice it gets within a pie of a fixed size.

See [log.csv](log.csv) for an example.

When `facere-sensum` is run it prompts the user to enter scores for individual metrics. Individual scores need to be provided in a form of a number in the range of 0..1, with bigger number corresponding to a better metric result.

`facere-sensum` will update the log `.csv` file by:
* Recording the date the scores were given.
* Recording the individual metric scores that the user has provided.
* Calculaing and recording overall day performance in the last (`Score`) column which is really a dot product of metric priorities and scores. Given the definitions above this will be a number in the range of 0..1 as well with bigger value reflecting better performance.
* Finally, `facere-sensum` will create a new row for the future scoring with adjusted priorities. This is where the interesting part is, as priorities will be modified to give a better chance for metrics that don't get enough attention:
  * for top performing metrics (the score is 1) the priority doesn't raise;
  * for comletely failed metrics (the score is 0) the priority grows 2x;
  * other metrics receive an increase in priority somewhere in the middle depending on their score.
* In the end, priorities for all the metrics are adjusted down proportionally to make all the priorities sum up to 1 again.

This process ensures that metrics of the lowest priority eventually get attention as they grow in priority over time if not addressed. The recommended process is to enter new data daily, but this can also be done more or less often.

Technically `facere-sensum` only needs latest priorities and doesn't use other data rows of the `.csv` file. However with each measurement a new row is created, so that all the historical data is preserved.

# Installation

    pip install facere-sensum

# Usage

    facere_sensum [-h] [--version] [log]

Options:
*  **-h**, **--help**: show help message and exit
*  **--version**:      show the version number and exit
*  **log**:            log file in CSV format (default: log.csv)
