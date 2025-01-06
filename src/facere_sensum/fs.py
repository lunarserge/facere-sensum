# SPDX-License-Identifier: MIT

"""
facere-sensum: make sense of the turmoil.
"""

import sys
import importlib
import json
import csv
from argparse import ArgumentParser
import datetime
import numpy as np
import pandas as pd
import prettytable
import matplotlib.pyplot as plt

VERSION = "0.0.5"


def get_3rd_party_auth(party, entry):
    """
    Get 3rd parthy entry from the authentication config.
    'party' is the 3rd party name.
    'entry' is the entry name.
    Return the requested entry if it is specified via the authentication config, None otherwise.
    """
    if not "auth" in globals():
        return None  # No authentication config at all.
    config = globals()["auth"]
    if not party in config:
        return None  # No authentication info for the specified 3rd party.
    party = config[party]
    return party[entry] if entry in party else None


def command_create(config):
    """
    Create the layer data file using provided config.
    'config' is layer config in JSON form.
    """
    layer_data = config["layer data"]
    with open(layer_data, "w", encoding="utf-8", newline="") as data:
        writer = csv.writer(data)

        # Write header row.
        row = ["ID"]
        for metric in config["metrics"]:
            qualifier = "(" + metric["id"] + ")"
            row.append("W" + qualifier)
            row.append("RS" + qualifier)
            row.append("NS" + qualifier)
        row.append("Score")
        writer.writerow(row)

        # Write first row with initial weights.
        row = [""]
        for metric in config["metrics"]:
            row.append(metric["weight"])
            row.append("")
            row.append("")
        row.append("")
        writer.writerow(row)

    print(layer_data, "is created")


def _load_layer_data(config):
    """
    Load the layer data and return its contents as a dataframe.
    'config' is layer config in JSON form.
    """
    layer_data = config["layer data"]
    try:
        data = pd.read_csv(layer_data)
    except FileNotFoundError:
        print("Layer data '" + layer_data + "' not found. Exiting.")
        sys.exit(1)
    return data.astype({"ID": "string"})


# Map of pairs: metric source name / implementation.
_sources = {}


def _score(metric):
    """
    Get raw and normalized metric scores.
    'metric' is the metric definition.
    """
    source = metric["source"]

    if source == "const":
        res = metric["value"]
        return res, res

    if not source in _sources:
        _sources[source] = importlib.import_module("facere_sensum.sources." + source)

    source = _sources[source]
    raw = source.get_raw(metric)
    return raw, source.get_normalized(metric, raw)


def _print_report(metrics, scores):
    """
    Print report with the computed metric scores.
    'metrics' is a list with layer metrics.
    'scores' is a list of tuples with corresponding raw and normalized scores.
    """
    table = prettytable.PrettyTable(["Metric", "Raw", "Normalized"])
    for metric, score in zip(metrics, scores):
        table.add_row([metric["id"], score[0], score[1]])
    print()
    print(table)


def _compute_new_weights(weights, scores):
    """
    Compute new metric weights so that lagging metrics get a bump,
    but all the weights still sum up to 1. Return a list with the new weights.
    'weights' is a list with previous weights.
    'scores' is a matching list with the normilized scores.
    """
    # For top performing metrics (the score is 1) the weight doesn't raise.
    # For comletely failed metrics (the score is 0) the weight grows 2x.
    # Or anything else in the middle depending on the normalized metric score.
    weights = list(
        map(lambda weight, score: weight + (1 - score) * weight, weights, scores)
    )

    # Normalize so that weights sup up to 1.
    coeff = sum(weights)
    return list(map(lambda weight: weight / coeff, weights))


def command_update(config, marker):
    """
    Process the layer data by scoring all the metrics and updating weights for the future.
    Return the layer score.
    'config' is layer config in JSON form.
    'marker' is the identificator to be used with the scoring (e.g., the date of data collection).
    """
    data = _load_layer_data(config)

    weights = data.iloc[-1, 1:-1:3]  # Pick weights from the last row.
    weights_combined = sum(weights)
    if abs(weights_combined - 1) > 0.001:
        print(
            "Warning: last row weights don't sum up to 1 "
            f"(sum is ~{weights_combined:.2f})\n"
        )

    print(f"\nScoring for {marker}:")
    metrics = config["metrics"]
    scores = []
    for metric in metrics:
        scores.append(_score(metric))

    _print_report(metrics, scores)

    norm_scores = [score[1] for score in scores]
    layer_score = np.dot(weights, norm_scores)
    print(f"\nThe layer score for {marker} is ~{layer_score:.2f}")

    # Populate date and scores in the last row in preparation for the layer data update.
    data.iloc[-1, 0] = str(marker)
    data.iloc[-1, 2:-1:3] = [score[0] for score in scores]
    data.iloc[-1, 3:-1:3] = norm_scores
    data.iloc[-1, -1] = layer_score

    if "weights" in config and config["weights"] == "dynamic":
        weights = _compute_new_weights(weights, norm_scores)
        print("\nYour new metric weights are:")
        pairs = list(zip([metric["id"] for metric in metrics], weights))
        pairs.sort(key=lambda pair: pair[1], reverse=True)
        for metric, weight in pairs:
            print(f"  - {metric}: {weight:.2f}")

    # Create a new row and store new weights in it.
    new_row = [""]  # ID is empty.
    for weight in weights:
        new_row.append(weight)
        # Individual scores are zero until measured: raw and normalized.
        new_row.append(0)
        new_row.append(0)
    new_row.append(0)  # Layer score is zero until measured.
    data.loc[len(data)] = new_row

    layer_data = config["layer data"]
    data.to_csv(layer_data, index=False)
    print(layer_data, "is updated")
    return layer_score


def command_chart(config):
    """
    Draw a chart for layer scores over time.
    'config' is layer config in JSON form.
    """
    title = config["id"]
    data = _load_layer_data(config)[:-1]
    fig, axes = plt.subplots()
    axes.set_title(title)
    scores = data["Score"]

    # Set the Y axis limits so that users have a better chance to notice that only part
    # of Y axis scale is shown while at the same time seeing the change in the scores as well.
    min_score, max_score = min(scores), max(scores)
    diff = max_score - min_score
    min_limit, max_limit = max(min_score - diff, 0), min(max_score + diff, 1)
    if min_limit < max_limit:
        axes.set_ylim(min_limit, max_limit)
    else:
        axes.set_ylim(
            auto=True
        )  # Avoids matplotlib warning in case of unchanging layer scores.

    axes.plot([datetime.date.fromisoformat(date) for date in data["ID"]], scores)
    fig.autofmt_xdate()
    fig.savefig(title)
    print(title, ".png is created", sep="")


def main():
    """
    CLI entry.
    """
    parser = ArgumentParser(description="Make sense of the turmoil")
    parser.add_argument(
        "command",
        choices=["create", "update", "chart"],
        help="high-level action to perform",
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    parser.add_argument("--auth", nargs="?", help="authentication config")
    parser.add_argument(
        "--config",
        nargs="?",
        default="config.json",
        help="layer config (default: config.json)",
    )
    args = parser.parse_args()

    if args.auth:
        try:
            with open(args.auth, encoding="utf-8") as auth_config:
                # Put authentication config in global scope
                # for all other modules to access as necessary.
                globals()["auth"] = json.load(auth_config)
        except FileNotFoundError:
            print(
                "Authentication config '" + args.auth + "' not found. Exiting.",
                file=sys.stderr,
            )
            sys.exit(1)

    try:
        with open(args.config, encoding="utf-8") as layer_config:
            config = json.load(layer_config)
    except FileNotFoundError:
        print("Layer config '" + args.config + "' not found. Exiting.", file=sys.stderr)
        sys.exit(1)

    match args.command:
        case "create":
            command_create(config)
        case "update":
            command_update(config, datetime.date.today())
            print("\nSee you next time!")
        case "chart":
            command_chart(config)
        case _:  # pragma: no cover
            # Should never get here given that all the actions are processed above.
            print(
                "Something weird happened.",
                "Please submit an issue at",
                "https://github.com/lunarserge/facere-sensum/issues/new",
                "with the command that led here.",
            )
            sys.exit(1)
