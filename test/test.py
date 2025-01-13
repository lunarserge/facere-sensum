# SPDX-License-Identifier: MIT

"""
facere-sensum testing support.
"""

import os
import sys
import subprocess  # nosec B404
import importlib
import json
import shutil
import unittest
from facere_sensum import fs
from facere_sensum.sources import user as user_source


# Generate paths for test files.
with open(
    os.path.join("examples", "config_personal.json"), encoding="utf-8"
) as layer_config:
    _CONFIG = json.load(layer_config)
_LAYER_DATA = _CONFIG["layer data"]
_REF_BASE = os.path.join("test", "output", "ref_base.csv")
_REF_UPDATED = os.path.join("test", "output", "ref_updated.csv")


def _logs_equal(log1, log2):
    """
    Compare two logs.
    Return True if logs are equal, Flase otherwise.
    """
    # Need to compare line by line to ignore end-of-line differences between Linux and Windows.
    with open(log1, encoding="utf8") as file1:
        with open(log2, encoding="utf8") as file2:
            return file1.readlines() == file2.readlines()


def _mock_up_direct_user_input(data):
    """
    Mock up direct user input.
    'data' is a list of values to be used instead of the actual user input.
    """
    data = (item for item in data)
    user_source.get_raw = lambda metric: next(data)


class Test(unittest.TestCase):
    """
    Unit test cases.
    """

    def test_command_create(self):
        """
        Test facere_sensum.command_create function.
        """
        fs.command_create(_CONFIG)
        self.assertTrue(_logs_equal(_LAYER_DATA, _REF_BASE))

    def test_command_update(self):
        """
        Test facere_sensum.command_update function.
        """
        shutil.copy(_REF_BASE, _LAYER_DATA)

        # Minimal extreme: all normalized scores are zero.
        _mock_up_direct_user_input([0, 0, 0])
        fs.command_update(_CONFIG, "A")

        # Maximal extreme: all normalized scores are one.
        _mock_up_direct_user_input([1, 1, 1])
        fs.command_update(_CONFIG, "B")

        # Various normalized scores.
        _mock_up_direct_user_input([0.25, 0.5, 0.75])
        fs.command_update(_CONFIG, "C")

        # Compare with a reference.
        self.assertTrue(_logs_equal(_LAYER_DATA, _REF_UPDATED))

    def test_metric_sources(self):
        """
        Test metric sources.
        """
        # Load sample authentication config file so that all the metric sources can load.
        # Metric source loading only needs JSON scheme, not actual credentials.
        with open("auth.json", encoding="utf-8") as auth_config:
            fs.auth = json.load(auth_config)

        # pylint: disable-next=unused-variable
        for dir_path, dir_names, file_names in os.walk(
            os.path.join("test", "t_sources")
        ):
            if dir_path.endswith("__pycache__"):
                continue

            # Remove leading 'test' folder and convert to package syntax.
            dir_path = dir_path[5:].replace(os.sep, ".")

            for file_name in file_names:
                if file_name.startswith("t_") and file_name.endswith(".py"):
                    self.assertTrue(
                        importlib.import_module(dir_path + "." + file_name[:-3]).test()
                    )


def _test_integration(descr, args, ref_out, ref_err=""):
    """
    Run an integration test.
    'descr' is test user description.
    'args' command line arguments to use.
    'ref_out' expected output in stdout or None if the test doesn't use it.
    'ref_err' expected output in stderr.
    """
    print(descr, end=": ")
    res = subprocess.run(
        [sys.executable, "fsy.py"] + args, check=False, capture_output=True, text=True
    )  # nosec B603

    if ref_out and res.stdout != ref_out:
        print(
            "FAILED on stdout",
            "Output:",
            "---",
            res.stdout,
            "---",
            "Expected:",
            "---",
            ref_out,
            "---",
            sep="\n",
        )
        sys.exit(1)
    if res.stderr != ref_err:
        print(
            "FAILED on stderr",
            "Output:",
            "---",
            res.stderr,
            "---",
            "Expected:",
            "---",
            ref_err,
            "---",
            sep="\n",
        )
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    print("Integration tests:")

    layer_config = os.path.join("examples", "config_uplevel.json")
    _test_integration(
        "'create' command", ["--config", layer_config, "create"], "log.csv is created\n"
    )
    _test_integration("'update' command", ["--config", layer_config, "update"], None)
    _test_integration(
        "'chart' command",
        ["--config", layer_config, "chart"],
        "family.png is created\n",
    )
    if not os.path.exists("family.png"):
        print("Output PNG is not generated by 'chart' command")
        sys.exit(1)

    _test_integration(
        "Authentication config not found",
        ["--auth", "notfound.json", "update"],
        None,
        "Authentication config 'notfound.json' not found. Exiting.\n",
    )
    _test_integration(
        "Layer config not found",
        ["--config", "notfound.json", "update"],
        None,
        "Layer config 'notfound.json' not found. Exiting.\n",
    )
    _test_integration(
        "Layer data not found for 'uplevel' metric source",
        [
            "--config",
            os.path.join("test", "input", "config_uplevel_notfound.json"),
            "update",
        ],
        None,
        "Error ('uplevel' metric source): "
        "layer data CSV file 'notfound.csv' not found. Exiting.\n",
    )

    # Unit tests
    unittest.main()
